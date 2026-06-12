"""
test_student.py — Unit tests for Student creation, properties, and management.
"""

import pytest

from models.student import Student
from models.person import Person


class TestStudentCreation:
    """Tests for creating Student instances."""

    def test_student_basic_creation(self, manager):
        """A student created via SchoolManager should have the correct attributes."""
        student = manager.add_student(name="Wayne Kiptoo", age=20, classroom="Form 4")
        assert student.name == "Wayne Kiptoo"
        assert student.age == 20
        assert student.classroom == "Form 4"
        assert student.id == 1

    def test_student_id_auto_increments(self, manager):
        """Each new student should receive a unique, incrementing ID."""
        s1 = manager.add_student(name="Alice", age=15)
        s2 = manager.add_student(name="Bob", age=16)
        s3 = manager.add_student(name="Carol", age=17)
        assert s1.id < s2.id < s3.id

    def test_student_optional_fields_default_empty(self, manager):
        """Email and phone should default to empty strings."""
        student = manager.add_student(name="TestStudent", age=14)
        assert student.email == ""
        assert student.phone == ""

    def test_student_invalid_name_raises(self, manager):
        """Registering a student with an empty name should raise ValueError."""
        with pytest.raises(ValueError):
            manager.add_student(name="", age=15)

    def test_student_invalid_age_raises(self, manager):
        """Registering a student with a non-positive age should raise ValueError."""
        with pytest.raises(ValueError):
            manager.add_student(name="Test", age=-5)

    def test_student_str_representation(self, manager):
        """__str__ should include id, name, age, and classroom."""
        student = manager.add_student(name="Jane Doe", age=18, classroom="Form 5")
        result = str(student)
        assert "Jane Doe" in result
        assert "Form 5" in result

    def test_student_repr(self, manager):
        """__repr__ should be a complete developer-facing representation."""
        student = manager.add_student(name="Jane Doe", age=18, classroom="Form 5")
        result = repr(student)
        assert "Student" in result
        assert "Jane Doe" in result


class TestStudentSearch:
    """Tests for searching student records."""

    def test_search_by_partial_name(self, manager):
        """Partial-name search should return all matching students."""
        manager.add_student(name="Wayne Kiptoo", age=20)
        manager.add_student(name="Wayne Otieno", age=19)
        manager.add_student(name="Alice Njeri",  age=18)

        results = manager.search_students("Wayne")
        assert len(results) == 2

    def test_search_case_insensitive(self, manager):
        """Search should be case-insensitive."""
        manager.add_student(name="Alice Njeri", age=16)
        results = manager.search_students("alice")
        assert len(results) == 1
        assert results[0].name == "Alice Njeri"

    def test_search_no_match_returns_empty(self, manager):
        """Searching for a non-existent name should return an empty list."""
        manager.add_student(name="Bob Kamau", age=15)
        results = manager.search_students("Zephyr")
        assert results == []


class TestStudentUpdate:
    """Tests for updating student records."""

    def test_update_student_name(self, manager, sample_student):
        """Updating a student's name should persist the change."""
        updated = manager.update_student(sample_student.id, name="Alice Wanjiku")
        assert updated.name == "Alice Wanjiku"

    def test_update_student_classroom(self, manager, sample_student):
        """Updating a student's classroom should persist the change."""
        updated = manager.update_student(sample_student.id, classroom="Form 4")
        assert updated.classroom == "Form 4"

    def test_update_nonexistent_student_raises(self, manager):
        """Updating a student that doesn't exist should raise ValueError."""
        with pytest.raises(ValueError):
            manager.update_student(9999, name="Ghost")


class TestStudentDeletion:
    """Tests for deleting student records."""

    def test_delete_student_success(self, manager, sample_student):
        """Deleting an existing student should return True."""
        result = manager.delete_student(sample_student.id)
        assert result is True
        assert manager.get_student(sample_student.id) is None

    def test_delete_nonexistent_student_returns_false(self, manager):
        """Deleting a student that doesn't exist should return False."""
        result = manager.delete_student(9999)
        assert result is False
