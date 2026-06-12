"""
student.py — Student model for the School Management System.

Inherits from Person and adds classroom assignment, grades, and attendance.
"""

from models.person import Person


class Student(Person):
    """
    Represents a student enrolled in the school.

    Extends Person with:
        - classroom assignment
        - list of grade records
        - list of attendance records
        - parent linkage
    """

    _id_counter: int = 1  # Separate counter so student IDs start from S-1

    def __init__(
        self,
        name: str,
        age: int,
        classroom: str = "",
        email: str = "",
        phone: str = "",
        parent_id: int = None,
        student_id: int = None,
    ):
        """
        Initialize a Student.

        Args:
            name: Full name.
            age: Age (positive integer).
            classroom: Name of the classroom (e.g., "Form 4").
            email: Optional email.
            phone: Optional phone.
            parent_id: ID of the linked Parent record.
            student_id: If provided, use this ID (for loading from storage).
        """
        super().__init__(name=name, age=age, email=email, phone=phone, person_id=student_id)

        self._classroom = classroom
        self._parent_id = parent_id
        self._grades: list[dict] = []      # [{subject, score, date, grade_id}]
        self._attendance: list[dict] = []  # [{date, status, attendance_id}]

    # ── Properties ──────────────────────────────────────────────────────────

    @property
    def classroom(self) -> str:
        """Return the student's assigned classroom."""
        return self._classroom

    @classroom.setter
    def classroom(self, value: str):
        """Assign the student to a classroom."""
        self._classroom = value.strip() if value else ""

    @property
    def parent_id(self) -> int | None:
        """Return the linked parent's ID."""
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value: int | None):
        """Link a parent to this student."""
        self._parent_id = value

    @property
    def grades(self) -> list[dict]:
        """Return the list of grade records (read-only list reference)."""
        return self._grades

    @property
    def attendance(self) -> list[dict]:
        """Return the list of attendance records (read-only list reference)."""
        return self._attendance

    # ── Grade helpers ────────────────────────────────────────────────────────

    def add_grade(self, grade_record: dict):
        """Append a grade record dict to this student's grade list."""
        self._grades.append(grade_record)

    def get_average_score(self) -> float:
        """Calculate and return the average score across all grades."""
        if not self._grades:
            return 0.0
        return round(sum(g["score"] for g in self._grades) / len(self._grades), 2)

    # ── Attendance helpers ───────────────────────────────────────────────────

    def add_attendance(self, attendance_record: dict):
        """Append an attendance record dict to this student's attendance list."""
        self._attendance.append(attendance_record)

    def get_attendance_summary(self) -> dict:
        """
        Return a summary of attendance counts.

        Returns:
            dict with keys 'Present', 'Absent', 'Late', 'total'.
        """
        summary = {"Present": 0, "Absent": 0, "Late": 0, "total": len(self._attendance)}
        for record in self._attendance:
            status = record.get("status", "")
            if status in summary:
                summary[status] += 1
        return summary

    # ── Serialization ───────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Return a dictionary representation suitable for JSON storage."""
        data = super().to_dict()
        data.update({
            "classroom": self._classroom,
            "parent_id": self._parent_id,
            "grades": self._grades,
            "attendance": self._attendance,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        """
        Reconstruct a Student from a stored dictionary.

        Args:
            data: Dictionary loaded from JSON storage.

        Returns:
            A fully populated Student instance.
        """
        student = cls(
            name=data["name"],
            age=data["age"],
            classroom=data.get("classroom", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            parent_id=data.get("parent_id"),
            student_id=data["id"],
        )
        student._created_at = data.get("created_at", student._created_at)
        student._grades = data.get("grades", [])
        student._attendance = data.get("attendance", [])
        return student

    # ── String representations ───────────────────────────────────────────────

    def __str__(self) -> str:
        return (
            f"Student(id={self._id}, name='{self._name}', "
            f"age={self._age}, classroom='{self._classroom}')"
        )

    def __repr__(self) -> str:
        return (
            f"Student(id={self._id!r}, name={self._name!r}, "
            f"age={self._age!r}, classroom={self._classroom!r})"
        )
