"""
validators.py — Input validation utilities for the School Management System.

Centralizes reusable validation functions used by CLI commands and services.
"""

import re
from dateutil import parser as dateutil_parser


def validate_name(name: str) -> str:
    """
    Validate and clean a person's name.

    Args:
        name: Raw name string.

    Returns:
        Cleaned name.

    Raises:
        ValueError: If the name is empty or contains invalid characters.
    """
    if not name or not name.strip():
        raise ValueError("Name cannot be empty.")
    cleaned = " ".join(name.strip().split())  # Normalize whitespace
    if len(cleaned) < 2:
        raise ValueError("Name must be at least 2 characters long.")
    if not re.match(r"^[a-zA-Z\s\-'.]+$", cleaned):
        raise ValueError(
            "Name can only contain letters, spaces, hyphens, apostrophes, and periods."
        )
    return cleaned


def validate_age(age_input) -> int:
    """
    Validate and convert an age value.

    Args:
        age_input: Age as int or string.

    Returns:
        Validated integer age.

    Raises:
        ValueError: If age is not a positive integer within a reasonable range.
    """
    try:
        age = int(age_input)
    except (TypeError, ValueError):
        raise ValueError(f"Age must be a whole number, got '{age_input}'.")

    if age <= 0:
        raise ValueError("Age must be a positive number.")
    if age > 120:
        raise ValueError("Age seems unrealistically high (>120).")
    return age


def validate_score(score_input) -> float:
    """
    Validate and convert a grade score.

    Args:
        score_input: Score as int, float, or string.

    Returns:
        Validated float score.

    Raises:
        ValueError: If score is not between 0 and 100.
    """
    try:
        score = float(score_input)
    except (TypeError, ValueError):
        raise ValueError(f"Score must be a number, got '{score_input}'.")

    if not (0.0 <= score <= 100.0):
        raise ValueError(f"Score must be between 0 and 100, got {score}.")
    return round(score, 2)


def validate_date(date_input: str) -> str:
    """
    Validate and normalize a date string using python-dateutil.

    Accepts many formats (e.g., "2025-06-01", "June 1, 2025", "01/06/2025").

    Args:
        date_input: Raw date string.

    Returns:
        ISO-format date string ("YYYY-MM-DD").

    Raises:
        ValueError: If the date string cannot be parsed.
    """
    if not date_input or not date_input.strip():
        raise ValueError("Date cannot be empty.")
    try:
        parsed = dateutil_parser.parse(date_input)
        return parsed.date().isoformat()
    except (ValueError, OverflowError):
        raise ValueError(
            f"Could not parse '{date_input}' as a date. "
            "Try formats like '2025-06-01' or 'June 1 2025'."
        )


def validate_status(status: str) -> str:
    """
    Validate an attendance status string.

    Args:
        status: Raw status string.

    Returns:
        Normalized status ('Present', 'Absent', or 'Late').

    Raises:
        ValueError: If the status is not valid.
    """
    valid = {"Present", "Absent", "Late"}
    normalized = status.strip().capitalize() if status else ""
    if normalized not in valid:
        raise ValueError(
            f"Status must be one of {sorted(valid)}, got '{status}'."
        )
    return normalized


def validate_capacity(capacity_input) -> int:
    """
    Validate a classroom capacity value.

    Args:
        capacity_input: Capacity as int or string.

    Returns:
        Validated integer capacity.

    Raises:
        ValueError: If capacity is not a positive integer.
    """
    try:
        cap = int(capacity_input)
    except (TypeError, ValueError):
        raise ValueError(f"Capacity must be a whole number, got '{capacity_input}'.")
    if cap <= 0:
        raise ValueError("Capacity must be a positive number.")
    if cap > 500:
        raise ValueError("Capacity seems unrealistically high (>500).")
    return cap
