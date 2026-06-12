"""
teacher.py — Teacher model for the School Management System.

Inherits from Person and adds subject specialization and classroom assignments.
"""

from models.person import Person


class Teacher(Person):
    """
    Represents a teacher employed at the school.

    Extends Person with:
        - subject specialization
        - assigned classrooms list
        - employee number
    """

    def __init__(
        self,
        name: str,
        age: int,
        subject: str = "",
        email: str = "",
        phone: str = "",
        teacher_id: int = None,
    ):
        """
        Initialize a Teacher.

        Args:
            name: Full name.
            age: Age (positive integer).
            subject: Main subject taught (e.g., "Mathematics").
            email: Optional email.
            phone: Optional phone number.
            teacher_id: If provided, use this ID (for loading from storage).
        """
        super().__init__(name=name, age=age, email=email, phone=phone, person_id=teacher_id)

        self._subject = subject
        self._classroom_ids: list[int] = []  # IDs of assigned Classroom records

    # ── Properties ──────────────────────────────────────────────────────────

    @property
    def subject(self) -> str:
        """Return the teacher's primary subject."""
        return self._subject

    @subject.setter
    def subject(self, value: str):
        """Set the subject, stripping leading/trailing whitespace."""
        self._subject = value.strip() if value else ""

    @property
    def classroom_ids(self) -> list[int]:
        """Return the list of classroom IDs this teacher is assigned to."""
        return self._classroom_ids

    # ── Classroom helpers ────────────────────────────────────────────────────

    def assign_classroom(self, classroom_id: int):
        """
        Assign a classroom to this teacher if not already assigned.

        Args:
            classroom_id: The ID of the classroom to assign.
        """
        if classroom_id not in self._classroom_ids:
            self._classroom_ids.append(classroom_id)

    def remove_classroom(self, classroom_id: int):
        """
        Remove a classroom assignment from this teacher.

        Args:
            classroom_id: The ID of the classroom to remove.
        """
        if classroom_id in self._classroom_ids:
            self._classroom_ids.remove(classroom_id)

    # ── Serialization ───────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Return a dictionary representation suitable for JSON storage."""
        data = super().to_dict()
        data.update({
            "subject": self._subject,
            "classroom_ids": self._classroom_ids,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Teacher":
        """
        Reconstruct a Teacher from a stored dictionary.

        Args:
            data: Dictionary loaded from JSON storage.

        Returns:
            A fully populated Teacher instance.
        """
        teacher = cls(
            name=data["name"],
            age=data["age"],
            subject=data.get("subject", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            teacher_id=data["id"],
        )
        teacher._created_at = data.get("created_at", teacher._created_at)
        teacher._classroom_ids = data.get("classroom_ids", [])
        return teacher

    # ── String representations ───────────────────────────────────────────────

    def __str__(self) -> str:
        return (
            f"Teacher(id={self._id}, name='{self._name}', "
            f"age={self._age}, subject='{self._subject}')"
        )

    def __repr__(self) -> str:
        return (
            f"Teacher(id={self._id!r}, name={self._name!r}, "
            f"age={self._age!r}, subject={self._subject!r})"
        )
