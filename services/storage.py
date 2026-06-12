"""
storage.py — JSON file persistence service for the School Management System.

Handles all reading and writing of application data to data/database.json.
"""

import json
import os
from pathlib import Path

# Default path for the database file
DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "database.json"

# Empty schema used when creating a fresh database
EMPTY_DB: dict = {
    "students": [],
    "teachers": [],
    "parents": [],
    "classrooms": [],
    "meta": {
        "student_id_counter": 1,
        "teacher_id_counter": 1,
        "parent_id_counter": 1,
        "classroom_id_counter": 1,
        "grade_id_counter": 1,
        "attendance_id_counter": 1,
    },
}


class StorageService:
    """
    Provides JSON-based file persistence for all school data.

    Usage:
        storage = StorageService()
        data = storage.load()
        storage.save(data)
    """

    def __init__(self, db_path: Path = DEFAULT_DB_PATH):
        """
        Initialize the storage service.

        Args:
            db_path: Path to the JSON database file.
        """
        self._db_path = db_path
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Create the data directory if it doesn't already exist."""
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict:
        """
        Load and return the database from disk.

        Handles missing files and corrupt JSON gracefully by returning
        a fresh empty database schema in either case.

        Returns:
            Dictionary containing all school data collections.
        """
        if not self._db_path.exists():
            # First run — return empty schema; it will be saved on first write
            return dict(EMPTY_DB)

        try:
            with open(self._db_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return dict(EMPTY_DB)
                data = json.loads(content)
                # Ensure all required top-level keys exist (forward compat)
                for key, default in EMPTY_DB.items():
                    if key not in data:
                        data[key] = default
                return data

        except json.JSONDecodeError:
            # Corrupt file — back it up and start fresh
            backup_path = self._db_path.with_suffix(".json.bak")
            try:
                os.replace(self._db_path, backup_path)
            except OSError:
                pass
            return dict(EMPTY_DB)

        except OSError as exc:
            raise RuntimeError(
                f"Could not read database file at {self._db_path}: {exc}"
            ) from exc

    def save(self, data: dict) -> None:
        """
        Persist the provided data dictionary to the JSON file.

        Writes atomically by first writing to a temp file then replacing,
        to prevent data loss on unexpected crashes.

        Args:
            data: The full database dictionary to persist.

        Raises:
            RuntimeError: If the file cannot be written.
        """
        tmp_path = self._db_path.with_suffix(".json.tmp")
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.replace(tmp_path, self._db_path)
        except OSError as exc:
            raise RuntimeError(
                f"Could not write database file at {self._db_path}: {exc}"
            ) from exc
        finally:
            # Clean up temp file if replace failed
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except OSError:
                    pass
