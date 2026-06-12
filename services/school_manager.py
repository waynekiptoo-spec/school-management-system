"""
school_manager.py — Core business logic for the School Management System.

SchoolManager acts as the central service that coordinates all entities
(students, teachers, parents, classrooms) and delegates persistence to
StorageService.
"""

from models.attendance import Attendance
from models.classroom import Classroom
from models.grade import Grade
from models.parent import Parent
from models.student import Student
from models.teacher import Teacher
from services.storage import StorageService


class SchoolManager:
    """
    The central service class that manages all school entities.

    Responsibilities:
        - Load and persist data via StorageService.
        - CRUD operations for students, teachers, parents, classrooms.
        - Grade and attendance recording.
        - Reporting (student report, school summary).

    All mutation methods call _save() automatically.
    """

    def __init__(self, storage: StorageService = None):
        """
        Initialize SchoolManager and load existing data.

        Args:
            storage: Optional StorageService instance (useful for testing).
        """
        self._storage = storage or StorageService()
        self._students: dict[int, Student] = {}
        self._teachers: dict[int, Teacher] = {}
        self._parents: dict[int, Parent] = {}
        self._classrooms: dict[int, Classroom] = {}
        self._load()

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _load(self):
        """Load all entities from the JSON store and sync ID counters."""
        data = self._storage.load()
        meta = data.get("meta", {})

        for s in data.get("students", []):
            student = Student.from_dict(s)
            self._students[student.id] = student

        for t in data.get("teachers", []):
            teacher = Teacher.from_dict(t)
            self._teachers[teacher.id] = teacher

        for p in data.get("parents", []):
            parent = Parent.from_dict(p)
            self._parents[parent.id] = parent

        for c in data.get("classrooms", []):
            classroom = Classroom.from_dict(c)
            self._classrooms[classroom.id] = classroom

        # Restore ID counters so new records never collide with loaded ones
        from models.person import Person
        Person._id_counter = meta.get("student_id_counter", 1)
        Teacher._id_counter = meta.get("teacher_id_counter", 1)
        Parent._id_counter = meta.get("parent_id_counter", 1)
        Classroom._id_counter = meta.get("classroom_id_counter", 1)
        Grade._id_counter = meta.get("grade_id_counter", 1)
        Attendance._id_counter = meta.get("attendance_id_counter", 1)

    def _save(self):
        """Serialize all entities and persist them to the JSON store."""
        from models.person import Person
        data = {
            "students": [s.to_dict() for s in self._students.values()],
            "teachers": [t.to_dict() for t in self._teachers.values()],
            "parents": [p.to_dict() for p in self._parents.values()],
            "classrooms": [c.to_dict() for c in self._classrooms.values()],
            "meta": {
                "student_id_counter": Person._id_counter,
                "teacher_id_counter": Teacher._id_counter,
                "parent_id_counter": Parent._id_counter,
                "classroom_id_counter": Classroom._id_counter,
                "grade_id_counter": Grade._id_counter,
                "attendance_id_counter": Attendance._id_counter,
            },
        }
        self._storage.save(data)

    def _next_id(self, collection: dict) -> int:
        """Return max(existing ids) + 1; returns 1 for an empty collection."""
        return max(collection.keys(), default=0) + 1

    # ══════════════════════════════════════════════════════════════════════════
    # STUDENT OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def add_student(
        self,
        name: str,
        age: int,
        classroom: str = "",
        email: str = "",
        phone: str = "",
    ) -> Student:
        """
        Register a new student.

        Args:
            name: Full name.
            age: Age.
            classroom: Classroom name/label.
            email: Optional email.
            phone: Optional phone.

        Returns:
            The newly created Student.
        """
        student_id = self._next_id(self._students)
        student = Student(
            name=name,
            age=age,
            classroom=classroom,
            email=email,
            phone=phone,
            student_id=student_id,
        )
        self._students[student.id] = student
        self._save()
        return student

    def list_students(self) -> list[Student]:
        """Return all registered students sorted by ID."""
        return sorted(self._students.values(), key=lambda s: s.id)

    def get_student(self, student_id: int) -> Student | None:
        """
        Retrieve a student by ID.

        Args:
            student_id: The student's numeric ID.

        Returns:
            The Student, or None if not found.
        """
        return self._students.get(student_id)

    def search_students(self, query: str) -> list[Student]:
        """
        Search students by name (case-insensitive partial match).

        Args:
            query: Search string.

        Returns:
            List of matching students.
        """
        q = query.lower().strip()
        return [s for s in self._students.values() if q in s.name.lower()]

    def update_student(self, student_id: int, **kwargs) -> Student:
        """
        Update one or more fields on an existing student record.

        Args:
            student_id: ID of the student to update.
            **kwargs: Fields to update (name, age, classroom, email, phone).

        Returns:
            The updated Student.

        Raises:
            ValueError: If no student with the given ID exists.
        """
        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"No student found with ID {student_id}.")

        for field, value in kwargs.items():
            if hasattr(student, field) and value is not None:
                setattr(student, field, value)

        self._save()
        return student

    def delete_student(self, student_id: int) -> bool:
        """
        Remove a student from the system.

        Also removes the student from any enrolled classroom.

        Args:
            student_id: ID of the student to delete.

        Returns:
            True if deleted, False if not found.
        """
        if student_id not in self._students:
            return False

        # Remove from any classroom
        for classroom in self._classrooms.values():
            classroom.remove_student(student_id)

        del self._students[student_id]
        self._save()
        return True

    # ══════════════════════════════════════════════════════════════════════════
    # TEACHER OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def add_teacher(
        self,
        name: str,
        age: int,
        subject: str = "",
        email: str = "",
        phone: str = "",
    ) -> Teacher:
        """
        Register a new teacher.

        Args:
            name: Full name.
            age: Age.
            subject: Primary subject taught.
            email: Optional email.
            phone: Optional phone.

        Returns:
            The newly created Teacher.
        """
        teacher_id = self._next_id(self._teachers)
        teacher = Teacher(
            name=name,
            age=age,
            subject=subject,
            email=email,
            phone=phone,
            teacher_id=teacher_id,
        )
        self._teachers[teacher.id] = teacher
        self._save()
        return teacher

    def list_teachers(self) -> list[Teacher]:
        """Return all teachers sorted by ID."""
        return sorted(self._teachers.values(), key=lambda t: t.id)

    def get_teacher(self, teacher_id: int) -> Teacher | None:
        """Retrieve a teacher by ID."""
        return self._teachers.get(teacher_id)

    # ══════════════════════════════════════════════════════════════════════════
    # PARENT OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def add_parent(
        self,
        name: str,
        age: int,
        relationship: str = "Guardian",
        email: str = "",
        phone: str = "",
    ) -> Parent:
        """
        Register a new parent/guardian.

        Args:
            name: Full name.
            age: Age.
            relationship: Type (e.g., 'Mother', 'Father', 'Guardian').
            email: Optional email.
            phone: Optional phone.

        Returns:
            The newly created Parent.
        """
        parent_id = self._next_id(self._parents)
        parent = Parent(
            name=name,
            age=age,
            relationship=relationship,
            email=email,
            phone=phone,
            parent_id=parent_id,
        )
        self._parents[parent.id] = parent
        self._save()
        return parent

    def list_parents(self) -> list[Parent]:
        """Return all parents sorted by ID."""
        return sorted(self._parents.values(), key=lambda p: p.id)

    def get_parent(self, parent_id: int) -> Parent | None:
        """Retrieve a parent by ID."""
        return self._parents.get(parent_id)

    # ══════════════════════════════════════════════════════════════════════════
    # CLASSROOM OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def add_classroom(
        self,
        name: str,
        capacity: int = 40,
        teacher_id: int = None,
    ) -> Classroom:
        """
        Create a new classroom.

        Args:
            name: Classroom name (e.g., 'Form 4').
            capacity: Maximum students (default 40).
            teacher_id: Optional ID of the assigned teacher.

        Returns:
            The newly created Classroom.
        """
        classroom_id = self._next_id(self._classrooms)
        classroom = Classroom(
            name=name,
            capacity=capacity,
            teacher_id=teacher_id,
            classroom_id=classroom_id,
        )
        self._classrooms[classroom.id] = classroom
        self._save()
        return classroom

    def list_classrooms(self) -> list[Classroom]:
        """Return all classrooms sorted by ID."""
        return sorted(self._classrooms.values(), key=lambda c: c.id)

    def get_classroom(self, classroom_id: int) -> Classroom | None:
        """Retrieve a classroom by ID."""
        return self._classrooms.get(classroom_id)

    def get_classroom_by_name(self, name: str) -> Classroom | None:
        """Retrieve a classroom by name (case-insensitive)."""
        name_lower = name.lower()
        for classroom in self._classrooms.values():
            if classroom.name.lower() == name_lower:
                return classroom
        return None

    # ══════════════════════════════════════════════════════════════════════════
    # ASSIGNMENT OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def assign_student_to_classroom(
        self,
        student_id: int,
        classroom_id: int,
    ) -> bool:
        """
        Enroll a student in a classroom.

        Also updates the student's classroom field.

        Args:
            student_id: ID of the student.
            classroom_id: ID of the classroom.

        Returns:
            True on success, False if classroom is full or student not found.

        Raises:
            ValueError: If either the student or classroom doesn't exist.
        """
        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"No student found with ID {student_id}.")

        classroom = self._classrooms.get(classroom_id)
        if not classroom:
            raise ValueError(f"No classroom found with ID {classroom_id}.")

        if classroom.is_full:
            return False

        # Remove from previous classroom if any
        for c in self._classrooms.values():
            c.remove_student(student_id)

        classroom.enroll_student(student_id)
        student.classroom = classroom.name
        self._save()
        return True

    def link_parent_to_student(self, parent_id: int, student_id: int):
        """
        Link a parent to a student (bidirectional).

        Args:
            parent_id: ID of the parent.
            student_id: ID of the student.

        Raises:
            ValueError: If parent or student doesn't exist.
        """
        parent = self._parents.get(parent_id)
        if not parent:
            raise ValueError(f"No parent found with ID {parent_id}.")

        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"No student found with ID {student_id}.")

        parent.link_student(student_id)
        student.parent_id = parent_id
        self._save()

    # ══════════════════════════════════════════════════════════════════════════
    # GRADE OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def record_grade(
        self,
        student_id: int,
        subject: str,
        score: float,
        teacher_id: int = None,
    ) -> Grade:
        """
        Record a grade for a student.

        Args:
            student_id: ID of the student.
            subject: Subject name.
            score: Numeric score (0–100).
            teacher_id: Optional ID of the recording teacher.

        Returns:
            The created Grade record.

        Raises:
            ValueError: If the student doesn't exist or score is invalid.
        """
        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"No student found with ID {student_id}.")

        grade_id = Grade._id_counter
        Grade._id_counter += 1

        grade = Grade(
            student_id=student_id,
            subject=subject,
            score=score,
            teacher_id=teacher_id,
            grade_id=grade_id,
        )
        student.add_grade(grade.to_dict())
        self._save()
        return grade

    def get_student_grades(self, student_id: int) -> list[dict]:
        """
        Return all grades for a student.

        Args:
            student_id: ID of the student.

        Returns:
            List of grade dicts, or empty list.
        """
        student = self._students.get(student_id)
        return student.grades if student else []

    # ══════════════════════════════════════════════════════════════════════════
    # ATTENDANCE OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def mark_attendance(
        self,
        student_id: int,
        status: str,
        date: str = None,
        notes: str = "",
    ) -> Attendance:
        """
        Record an attendance entry for a student.

        Args:
            student_id: ID of the student.
            status: 'Present', 'Absent', or 'Late'.
            date: ISO date string (defaults to today).
            notes: Optional notes.

        Returns:
            The created Attendance record.

        Raises:
            ValueError: If the student doesn't exist or status is invalid.
        """
        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"No student found with ID {student_id}.")

        attendance_id = Attendance._id_counter
        Attendance._id_counter += 1

        record = Attendance(
            student_id=student_id,
            status=status,
            date=date,
            notes=notes,
            attendance_id=attendance_id,
        )
        student.add_attendance(record.to_dict())
        self._save()
        return record

    def get_student_attendance(self, student_id: int) -> list[dict]:
        """
        Return all attendance records for a student.

        Args:
            student_id: ID of the student.

        Returns:
            List of attendance dicts, or empty list.
        """
        student = self._students.get(student_id)
        return student.attendance if student else []

    # ══════════════════════════════════════════════════════════════════════════
    # REPORTING
    # ══════════════════════════════════════════════════════════════════════════

    def get_student_report(self, student_id: int) -> dict | None:
        """
        Build a comprehensive report for a single student.

        Args:
            student_id: ID of the student.

        Returns:
            Report dict, or None if the student doesn't exist.
        """
        student = self._students.get(student_id)
        if not student:
            return None

        parent = self._parents.get(student.parent_id) if student.parent_id else None
        attendance_summary = student.get_attendance_summary()

        return {
            "student": student.to_dict(),
            "parent": parent.to_dict() if parent else None,
            "grades": student.grades,
            "average_score": student.get_average_score(),
            "attendance_summary": attendance_summary,
        }

    def get_school_report(self) -> dict:
        """
        Build a high-level summary of the entire school.

        Returns:
            Dict containing counts and aggregate statistics.
        """
        total_students = len(self._students)
        total_teachers = len(self._teachers)
        total_parents = len(self._parents)
        total_classrooms = len(self._classrooms)

        # Compute school-wide average grade
        all_scores = [
            g["score"]
            for s in self._students.values()
            for g in s.grades
        ]
        school_avg = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0.0

        # Attendance stats across all students
        total_present = sum(
            s.get_attendance_summary()["Present"]
            for s in self._students.values()
        )
        total_absent = sum(
            s.get_attendance_summary()["Absent"]
            for s in self._students.values()
        )

        return {
            "total_students": total_students,
            "total_teachers": total_teachers,
            "total_parents": total_parents,
            "total_classrooms": total_classrooms,
            "school_average_score": school_avg,
            "total_present_records": total_present,
            "total_absent_records": total_absent,
        }
