"""
person.py — Base Person class for the School Management System.

All people in the system (Students, Teachers, Parents) inherit from this class.
"""

from datetime import datetime


class Person:
    """
    Base class representing a person in the school system.

    Attributes:
        _id (int): Unique identifier auto-assigned at creation.
        _name (str): Full name of the person.
        _age (int): Age of the person.
        _email (str): Contact email address.
        _phone (str): Contact phone number.
        _created_at (str): ISO timestamp of when the record was created.
    """

    _id_counter: int = 1  # Class-level counter for unique IDs

    def __init__(
        self,
        name: str,
        age: int,
        email: str = "",
        phone: str = "",
        person_id: int = None,
    ):
        """
        Initialize a Person instance.

        Args:
            name: Full name of the person.
            age: Age (must be a positive integer).
            email: Optional email address.
            phone: Optional phone number.
            person_id: If provided, use this ID (used when loading from storage).
        """
        if person_id is not None:
            self._id = person_id
        else:
            self._id = Person._id_counter
            Person._id_counter += 1

        self.name = name    # Goes through property setter for validation
        self.age = age
        self._email = email
        self._phone = phone
        self._created_at = datetime.now().isoformat()

    # ── Properties ──────────────────────────────────────────────────────────

    @property
    def id(self) -> int:
        """Return the unique ID (read-only)."""
        return self._id

    @property
    def name(self) -> str:
        """Return the person's name."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Set name after stripping whitespace; must be non-empty."""
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def age(self) -> int:
        """Return the person's age."""
        return self._age

    @age.setter
    def age(self, value: int):
        """Set age; must be a positive integer."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Age must be a positive integer.")
        self._age = value

    @property
    def email(self) -> str:
        """Return the email address."""
        return self._email

    @email.setter
    def email(self, value: str):
        """Set email address."""
        self._email = value.strip() if value else ""

    @property
    def phone(self) -> str:
        """Return the phone number."""
        return self._phone

    @phone.setter
    def phone(self, value: str):
        """Set phone number."""
        self._phone = value.strip() if value else ""

    @property
    def created_at(self) -> str:
        """Return the creation timestamp (read-only)."""
        return self._created_at

    # ── Serialization ───────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Return a dictionary representation for JSON serialization."""
        return {
            "id": self._id,
            "name": self._name,
            "age": self._age,
            "email": self._email,
            "phone": self._phone,
            "created_at": self._created_at,
        }

    # ── String representations ───────────────────────────────────────────────

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id}, name='{self._name}', age={self._age})"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self._id!r}, name={self._name!r}, age={self._age!r})"
        )
