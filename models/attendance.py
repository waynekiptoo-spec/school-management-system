"""
attendance.py — Attendance model for the School Management System.

Represents a single attendance entry for a student on a given date.
"""

from datetime import datetime

VALID_STATUSES = {"Present", "Absent", "Late"}


class Attendance:
    """
    Represents a single attendance record for a student.

    Attributes:
        _id (int): Unique attendance record ID.
        _student_id (int): ID of the student.
        _date (str): ISO date string for the attendance day.
        _status (str): 'Present', 'Absent', or 'Late'.
        _notes (str): Optional additional notes.
    """

    _id_counter: int = 1

    def __init__(
        self,
        student_id: int,
        status: str,
        date: str = None,
        notes: str = "",
        attendance_id: int = None,
    ):
        """
        Initialize an Attendance record.

        Args:
            student_id: The ID of the student.
            status: Attendance status — 'Present', 'Absent', or 'Late'.
            date: ISO date string (defaults to today).
            notes: Optional notes about the absence or lateness.
            attendance_id: If provided, use this ID (for loading from storage).
        """
        if attendance_id is not None:
            self._id = attendance_id
        else:
            self._id = Attendance._id_counter
            Attendance._id_counter += 1

        self._student_id = student_id
        self.status = status    # Validated via setter
        self._date = date or datetime.now().date().isoformat()
        self._notes = notes.strip() if notes else ""

    # ── Properties ──────────────────────────────────────────────────────────

    @property
    def id(self) -> int:
        """Return the attendance record ID (read-only)."""
        return self._id

    @property
    def student_id(self) -> int:
        """Return the student ID."""
        return self._student_id

    @property
    def status(self) -> str:
        """Return the attendance status."""
        return self._status

    @status.setter
    def status(self, value: str):
        """
        Set the attendance status.

        Raises:
            ValueError: If the status is not one of the valid options.
        """
        if value not in VALID_STATUSES:
            raise ValueError(
                f"Status must be one of {sorted(VALID_STATUSES)}, got '{value}'."
            )
        self._status = value

    @property
    def date(self) -> str:
        """Return the attendance date."""
        return self._date

    @property
    def notes(self) -> str:
        """Return any additional notes."""
        return self._notes

    @notes.setter
    def notes(self, value: str):
        """Update attendance notes."""
        self._notes = value.strip() if value else ""

    # ── Serialization ───────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Return a dictionary representation for JSON storage."""
        return {
            "id": self._id,
            "student_id": self._student_id,
            "status": self._status,
            "date": self._date,
            "notes": self._notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Attendance":
        """
        Reconstruct an Attendance record from a stored dictionary.

        Args:
            data: Dictionary loaded from JSON storage.

        Returns:
            A fully populated Attendance instance.
        """
        return cls(
            student_id=data["student_id"],
            status=data["status"],
            date=data.get("date"),
            notes=data.get("notes", ""),
            attendance_id=data["id"],
        )

    # ── String representations ───────────────────────────────────────────────

    def __str__(self) -> str:
        return (
            f"Attendance(student={self._student_id}, "
            f"date='{self._date}', status='{self._status}')"
        )

    def __repr__(self) -> str:
        return (
            f"Attendance(id={self._id!r}, student_id={self._student_id!r}, "
            f"status={self._status!r}, date={self._date!r})"
        )
