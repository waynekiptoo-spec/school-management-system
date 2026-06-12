"""
grade.py — Grade model for the School Management System.

Represents a single graded assessment result for a student in a subject.
"""

from datetime import datetime


# Grade letter boundaries
GRADE_BOUNDARIES = [
    (90, "A+"),
    (80, "A"),
    (70, "B+"),
    (60, "B"),
    (50, "C"),
    (40, "D"),
    (0,  "F"),
]


def score_to_letter(score: float) -> str:
    """
    Convert a numeric score (0–100) to a letter grade.

    Args:
        score: Numeric score.

    Returns:
        Letter grade string (e.g., 'A', 'B+', 'F').
    """
    for threshold, letter in GRADE_BOUNDARIES:
        if score >= threshold:
            return letter
    return "F"


class Grade:
    """
    Represents a single grade entry for a student.

    Attributes:
        _id (int): Unique grade ID.
        _student_id (int): ID of the student this grade belongs to.
        _subject (str): Subject name.
        _score (float): Numeric score (0–100).
        _letter (str): Computed letter grade.
        _teacher_id (int|None): ID of the teacher who recorded the grade.
        _date (str): ISO date string when the grade was recorded.
    """

    _id_counter: int = 1

    def __init__(
        self,
        student_id: int,
        subject: str,
        score: float,
        teacher_id: int = None,
        grade_id: int = None,
        date: str = None,
    ):
        """
        Initialize a Grade entry.

        Args:
            student_id: The ID of the student being graded.
            subject: The subject name.
            score: Numeric score between 0 and 100.
            teacher_id: Optional ID of the recording teacher.
            grade_id: If provided, use this ID (for loading from storage).
            date: ISO date string; defaults to today.
        """
        if grade_id is not None:
            self._id = grade_id
        else:
            self._id = Grade._id_counter
            Grade._id_counter += 1

        self._student_id = student_id
        self.subject = subject      # Validated via setter
        self.score = score          # Validated via setter (also sets letter)
        self._teacher_id = teacher_id
        self._date = date or datetime.now().date().isoformat()

    # ── Properties ──────────────────────────────────────────────────────────

    @property
    def id(self) -> int:
        """Return the grade ID (read-only)."""
        return self._id

    @property
    def student_id(self) -> int:
        """Return the student ID this grade belongs to."""
        return self._student_id

    @property
    def subject(self) -> str:
        """Return the subject name."""
        return self._subject

    @subject.setter
    def subject(self, value: str):
        """Set subject name; must be non-empty."""
        if not value or not value.strip():
            raise ValueError("Subject cannot be empty.")
        self._subject = value.strip()

    @property
    def score(self) -> float:
        """Return the numeric score."""
        return self._score

    @score.setter
    def score(self, value: float):
        """Set the score (0–100) and update the letter grade."""
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("Score must be a number.")
        if not (0.0 <= value <= 100.0):
            raise ValueError("Score must be between 0 and 100.")
        self._score = round(value, 2)
        self._letter = score_to_letter(self._score)

    @property
    def letter(self) -> str:
        """Return the computed letter grade."""
        return self._letter

    @property
    def teacher_id(self) -> int | None:
        """Return the recording teacher's ID."""
        return self._teacher_id

    @property
    def date(self) -> str:
        """Return the date the grade was recorded."""
        return self._date

    # ── Serialization ───────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Return a dictionary representation for JSON storage."""
        return {
            "id": self._id,
            "student_id": self._student_id,
            "subject": self._subject,
            "score": self._score,
            "letter": self._letter,
            "teacher_id": self._teacher_id,
            "date": self._date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Grade":
        """
        Reconstruct a Grade from a stored dictionary.

        Args:
            data: Dictionary loaded from JSON storage.

        Returns:
            A fully populated Grade instance.
        """
        return cls(
            student_id=data["student_id"],
            subject=data["subject"],
            score=data["score"],
            teacher_id=data.get("teacher_id"),
            grade_id=data["id"],
            date=data.get("date"),
        )

    # ── String representations ───────────────────────────────────────────────

    def __str__(self) -> str:
        return (
            f"Grade(student={self._student_id}, subject='{self._subject}', "
            f"score={self._score}, letter='{self._letter}', date='{self._date}')"
        )

    def __repr__(self) -> str:
        return (
            f"Grade(id={self._id!r}, student_id={self._student_id!r}, "
            f"subject={self._subject!r}, score={self._score!r})"
        )
