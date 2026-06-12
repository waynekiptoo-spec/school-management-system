"""
test_teacher.py — Unit tests for Teacher creation and management.
"""

import pytest

from models.teacher import Teacher


class TestTeacherCreation:
    """Tests for creating Teacher instances."""

    def test_teacher_basic_creation(self, manager):
        """A teacher created via SchoolManager should have correct attributes."""
        teacher = manager.add_teacher(
            name="Mr. Ochieng",
            age=35,
            subject="Mathematics",
            email="ochieng@school.ac.ke",
        )
        assert teacher.name == "Mr. Ochieng"
        assert teacher.age == 35
        assert teacher.subject == "Mathematics"
        assert teacher.email == "ochieng@school.ac.ke"
        assert teacher.id == 1

    def test_teacher_id_auto_increments(self, manager):
        """Each new teacher should receive a unique, incrementing ID."""
        t1 = manager.add_teacher(name="Teacher One", age=30, subject="English")
        t2 = manager.add_teacher(name="Teacher Two", age=32, subject="Science")
        assert t1.id < t2.id

    def test_teacher_invalid_name_raises(self, manager):
        """A teacher registered with an empty name should raise ValueError."""
        with pytest.raises(ValueError):
            manager.add_teacher(name="", age=30, subject="History")

    def test_teacher_invalid_age_raises(self, manager):
        """A teacher registered with a negative age should raise ValueError."""
        with pytest.raises(ValueError):
            manager.add_teacher(name="Valid Name", age=0, subject="Art")

    def test_teacher_str_representation(self, manager):
        """__str__ should contain teacher name and subject."""
        teacher = manager.add_teacher(name="Ms. Amara", age=28, subject="Biology")
        result = str(teacher)
        assert "Ms. Amara" in result
        assert "Biology" in result

    def test_teacher_repr(self, manager):
        """__repr__ should include the class name."""
        teacher = manager.add_teacher(name="Ms. Amara", age=28, subject="Biology")
        assert "Teacher" in repr(teacher)

    def test_teacher_list(self, manager):
        """list_teachers should return all registered teachers."""
        manager.add_teacher(name="Alpha", age=40, subject="Maths")
        manager.add_teacher(name="Beta",  age=45, subject="English")
        teachers = manager.list_teachers()
        assert len(teachers) == 2

    def test_teacher_classroom_assignment(self, manager):
        """A teacher should be able to be assigned to a classroom."""
        teacher = manager.add_teacher(name="Mr. K", age=33, subject="Physics")
        teacher.assign_classroom(101)
        assert 101 in teacher.classroom_ids

    def test_teacher_classroom_not_duplicated(self, manager):
        """Assigning the same classroom twice should not create a duplicate."""
        teacher = manager.add_teacher(name="Mr. K", age=33, subject="Physics")
        teacher.assign_classroom(101)
        teacher.assign_classroom(101)
        assert teacher.classroom_ids.count(101) == 1

    def test_get_teacher_by_id(self, manager, sample_teacher):
        """get_teacher should return the correct teacher by ID."""
        result = manager.get_teacher(sample_teacher.id)
        assert result is sample_teacher
