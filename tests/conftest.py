"""
conftest.py — Shared pytest fixtures for the School Management System test suite.
"""

import pytest

from models.person import Person
from models.student import Student
from models.teacher import Teacher
from models.parent import Parent
from models.classroom import Classroom
from models.grade import Grade
from models.attendance import Attendance
from services.school_manager import SchoolManager
from services.storage import StorageService


class InMemoryStorage:
    """
    A non-persistent StorageService replacement for tests.

    Keeps all data in memory so tests don't touch the filesystem.
    """

    def load(self) -> dict:
        return {
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

    def save(self, data: dict) -> None:
        """No-op — in-memory tests don't persist to disk."""
        pass


@pytest.fixture(autouse=True)
def reset_id_counters():
    """
    Reset all class-level ID counters before each test.

    Without this, tests would share global state and IDs would
    accumulate across the test session.
    """
    Person._id_counter = 1
    Teacher._id_counter = 1
    Parent._id_counter = 1
    Classroom._id_counter = 1
    Grade._id_counter = 1
    Attendance._id_counter = 1
    yield


@pytest.fixture
def manager():
    """Return a fresh SchoolManager backed by in-memory (non-persistent) storage."""
    return SchoolManager(storage=InMemoryStorage())


@pytest.fixture
def sample_student(manager):
    """Add and return a single sample student."""
    return manager.add_student(name="Alice Mwangi", age=17, classroom="Form 3")


@pytest.fixture
def sample_teacher(manager):
    """Add and return a single sample teacher."""
    return manager.add_teacher(name="Mr. Ochieng", age=35, subject="Mathematics")


@pytest.fixture
def sample_parent(manager):
    """Add and return a single sample parent."""
    return manager.add_parent(name="Grace Mwangi", age=42, relationship="Mother")
