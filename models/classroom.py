"""
classroom.py — Classroom model for the School Management System.

Tracks enrolled students, assigned teachers, and room metadata.
"""

from datetime import datetime


class Classroom:
    """
    Represents a classroom or class group within the school.

    Attributes:
        _id (int): Unique identifier.
        _name (str): Classroom name (e.g., "Form 4", "Grade 7A").
        _capacity (int): Maximum number of students.
        _student_ids (list): IDs of enrolled students.
        _teacher_id (int|None): ID of the assigned class teacher.
        _created_at (str): ISO timestamp of record creation.
    """

    _id_counter: int = 1

    def __init__(
        self,
        name: str,
        capacity: int = 40,
        teacher_id: int = None,
        classroom_id: int = None,
    ):
        """
        Initialize a Classroom.

        Args:
            name: The classroom name or label.
            capacity: Maximum student capacity (default 40).
            teacher_id: ID of the assigned class teacher.
            classroom_id: If provided, use this ID (for loading from storage).
        """
        if classroom_id is not None:
            self._id = classroom_id
        else:
            self._id = Classroom._id_counter
            Classroom._id_counter += 1

        self.name = name        # Validated through setter
        self.capacity = capacity
        self._teacher_id = teacher_id
        self._student_ids: list[int] = []
        self._created_at = datetime.now().isoformat()

    # ── Properties ──────────────────────────────────────────────────────────

    @property
    def id(self) -> int:
        """Return the classroom ID (read-only)."""
        return self._id

    @property
    def name(self) -> str:
        """Return the classroom name."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Set classroom name; must be non-empty."""
        if not value or not value.strip():
            raise ValueError("Classroom name cannot be empty.")
        self._name = value.strip()

    @property
    def capacity(self) -> int:
        """Return the student capacity."""
        return self._capacity

    @capacity.setter
    def capacity(self, value: int):
        """Set capacity; must be a positive integer."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self._capacity = value

    @property
    def teacher_id(self) -> int | None:
        """Return the assigned teacher's ID."""
        return self._teacher_id

    @teacher_id.setter
    def teacher_id(self, value: int | None):
        """Assign a teacher to this classroom."""
        self._teacher_id = value

    @property
    def student_ids(self) -> list[int]:
        """Return the list of enrolled student IDs."""
        return self._student_ids

    @property
    def current_enrollment(self) -> int:
        """Return the current number of enrolled students."""
        return len(self._student_ids)

    @property
    def is_full(self) -> bool:
        """Return True if the classroom has reached capacity."""
        return len(self._student_ids) >= self._capacity

    # ── Enrollment helpers ───────────────────────────────────────────────────

    def enroll_student(self, student_id: int) -> bool:
        """
        Enroll a student if capacity allows and not already enrolled.

        Args:
            student_id: ID of the student to enroll.

        Returns:
            True if enrolled successfully, False if already enrolled or full.
        """
        if self.is_full:
            return False
        if student_id not in self._student_ids:
            self._student_ids.append(student_id)
            return True
        return False

    def remove_student(self, student_id: int) -> bool:
        """
        Remove a student from this classroom.

        Args:
            student_id: ID of the student to remove.

        Returns:
            True if removed, False if not found.
        """
        if student_id in self._student_ids:
            self._student_ids.remove(student_id)
            return True
        return False

    # ── Serialization ───────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Return a dictionary representation for JSON storage."""
        return {
            "id": self._id,
            "name": self._name,
            "capacity": self._capacity,
            "teacher_id": self._teacher_id,
            "student_ids": self._student_ids,
            "created_at": self._created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Classroom":
        """
        Reconstruct a Classroom from a stored dictionary.

        Args:
            data: Dictionary loaded from JSON storage.

        Returns:
            A fully populated Classroom instance.
        """
        classroom = cls(
            name=data["name"],
            capacity=data.get("capacity", 40),
            teacher_id=data.get("teacher_id"),
            classroom_id=data["id"],
        )
        classroom._created_at = data.get("created_at", classroom._created_at)
        classroom._student_ids = data.get("student_ids", [])
        return classroom

    # ── String representations ───────────────────────────────────────────────

    def __str__(self) -> str:
        return (
            f"Classroom(id={self._id}, name='{self._name}', "
            f"enrollment={self.current_enrollment}/{self._capacity})"
        )

    def __repr__(self) -> str:
        return (
            f"Classroom(id={self._id!r}, name={self._name!r}, "
            f"capacity={self._capacity!r})"
        )
