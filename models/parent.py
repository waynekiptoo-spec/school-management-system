"""
parent.py — Parent/Guardian model for the School Management System.

Inherits from Person and tracks linked student children.
"""

from models.person import Person


class Parent(Person):
    """
    Represents a parent or guardian linked to one or more students.

    Extends Person with:
        - list of linked student IDs
        - relationship type (e.g., Mother, Father, Guardian)
    """

    def __init__(
        self,
        name: str,
        age: int,
        relationship: str = "Guardian",
        email: str = "",
        phone: str = "",
        parent_id: int = None,
    ):
        """
        Initialize a Parent.

        Args:
            name: Full name.
            age: Age (positive integer).
            relationship: Relationship to child (e.g., 'Mother', 'Father', 'Guardian').
            email: Optional email address.
            phone: Optional phone number.
            parent_id: If provided, use this ID (for loading from storage).
        """
        super().__init__(name=name, age=age, email=email, phone=phone, person_id=parent_id)

        self._relationship = relationship
        self._student_ids: list[int] = []  # IDs of linked Student records

    # ── Properties ──────────────────────────────────────────────────────────

    @property
    def relationship(self) -> str:
        """Return the relationship type to the child."""
        return self._relationship

    @relationship.setter
    def relationship(self, value: str):
        """Set the relationship type."""
        self._relationship = value.strip() if value else "Guardian"

    @property
    def student_ids(self) -> list[int]:
        """Return the list of linked student IDs."""
        return self._student_ids

    # ── Student-link helpers ─────────────────────────────────────────────────

    def link_student(self, student_id: int):
        """
        Link a student to this parent if not already linked.

        Args:
            student_id: The ID of the student to link.
        """
        if student_id not in self._student_ids:
            self._student_ids.append(student_id)

    def unlink_student(self, student_id: int):
        """
        Remove a student link from this parent.

        Args:
            student_id: The ID of the student to unlink.
        """
        if student_id in self._student_ids:
            self._student_ids.remove(student_id)

    # ── Serialization ───────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Return a dictionary representation suitable for JSON storage."""
        data = super().to_dict()
        data.update({
            "relationship": self._relationship,
            "student_ids": self._student_ids,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Parent":
        """
        Reconstruct a Parent from a stored dictionary.

        Args:
            data: Dictionary loaded from JSON storage.

        Returns:
            A fully populated Parent instance.
        """
        parent = cls(
            name=data["name"],
            age=data["age"],
            relationship=data.get("relationship", "Guardian"),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            parent_id=data["id"],
        )
        parent._created_at = data.get("created_at", parent._created_at)
        parent._student_ids = data.get("student_ids", [])
        return parent

    # ── String representations ───────────────────────────────────────────────

    def __str__(self) -> str:
        return (
            f"Parent(id={self._id}, name='{self._name}', "
            f"relationship='{self._relationship}')"
        )

    def __repr__(self) -> str:
        return (
            f"Parent(id={self._id!r}, name={self._name!r}, "
            f"relationship={self._relationship!r})"
        )
