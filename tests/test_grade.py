"""
test_grade.py — Unit tests for grade recording and letter grade computation.
"""

import pytest

from models.grade import Grade, score_to_letter


class TestScoreToLetter:
    """Tests for the score-to-letter-grade conversion function."""

    def test_a_plus(self):
        assert score_to_letter(95) == "A+"

    def test_a(self):
        assert score_to_letter(85) == "A"

    def test_b_plus(self):
        assert score_to_letter(75) == "B+"

    def test_b(self):
        assert score_to_letter(65) == "B"

    def test_c(self):
        assert score_to_letter(55) == "C"

    def test_d(self):
        assert score_to_letter(45) == "D"

    def test_f(self):
        assert score_to_letter(30) == "F"

    def test_boundary_90_is_a_plus(self):
        assert score_to_letter(90) == "A+"

    def test_boundary_80_is_a(self):
        assert score_to_letter(80) == "A"


class TestGradeRecording:
    """Tests for recording grades through SchoolManager."""

    def test_record_grade_basic(self, manager, sample_student):
        """A grade should be recorded and retrievable for the student."""
        grade = manager.record_grade(
            student_id=sample_student.id,
            subject="Mathematics",
            score=87,
        )
        assert grade.score == 87.0
        assert grade.subject == "Mathematics"
        assert grade.letter == "A"

    def test_recorded_grade_appears_in_student(self, manager, sample_student):
        """The grade should appear in the student's grade list."""
        manager.record_grade(
            student_id=sample_student.id,
            subject="Science",
            score=72,
        )
        grades = manager.get_student_grades(sample_student.id)
        assert len(grades) == 1
        assert grades[0]["subject"] == "Science"

    def test_multiple_grades_tracked(self, manager, sample_student):
        """Multiple grades across different subjects should all be stored."""
        manager.record_grade(sample_student.id, "Maths",    score=90)
        manager.record_grade(sample_student.id, "English",  score=75)
        manager.record_grade(sample_student.id, "Kiswahili", score=82)

        grades = manager.get_student_grades(sample_student.id)
        assert len(grades) == 3

    def test_average_score_calculated(self, manager, sample_student):
        """Average score should be the mean of all recorded scores."""
        manager.record_grade(sample_student.id, "Maths",   score=80)
        manager.record_grade(sample_student.id, "English", score=60)
        # Average = 70.0
        avg = sample_student.get_average_score()
        assert avg == 70.0

    def test_invalid_score_raises(self, manager, sample_student):
        """Recording a score above 100 should raise ValueError."""
        with pytest.raises(ValueError):
            manager.record_grade(sample_student.id, "Maths", score=105)

    def test_negative_score_raises(self, manager, sample_student):
        """Recording a negative score should raise ValueError."""
        with pytest.raises(ValueError):
            manager.record_grade(sample_student.id, "Maths", score=-10)

    def test_grade_for_nonexistent_student_raises(self, manager):
        """Recording a grade for a non-existent student ID should raise ValueError."""
        with pytest.raises(ValueError):
            manager.record_grade(student_id=9999, subject="Maths", score=50)

    def test_empty_subject_raises(self, manager, sample_student):
        """Recording a grade with an empty subject should raise ValueError."""
        with pytest.raises(ValueError):
            manager.record_grade(sample_student.id, subject="", score=70)

    def test_grade_str(self):
        """Grade __str__ should include student_id, subject, and score."""
        g = Grade(student_id=1, subject="Physics", score=88.5)
        result = str(g)
        assert "Physics" in result
        assert "88.5" in result

    def test_grade_serialization_roundtrip(self):
        """A grade converted to dict and back should be identical."""
        g = Grade(student_id=2, subject="Chemistry", score=76, grade_id=10)
        d = g.to_dict()
        restored = Grade.from_dict(d)
        assert restored.score == g.score
        assert restored.subject == g.subject
        assert restored.letter == g.letter
