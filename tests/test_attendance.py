"""
test_attendance.py — Unit tests for attendance marking and summaries.
"""

import pytest

from models.attendance import Attendance, VALID_STATUSES


class TestAttendanceModel:
    """Tests for the Attendance model class directly."""

    def test_valid_present_status(self):
        """Creating an Attendance record with 'Present' should succeed."""
        a = Attendance(student_id=1, status="Present")
        assert a.status == "Present"

    def test_valid_absent_status(self):
        """Creating an Attendance record with 'Absent' should succeed."""
        a = Attendance(student_id=1, status="Absent")
        assert a.status == "Absent"

    def test_valid_late_status(self):
        """Creating an Attendance record with 'Late' should succeed."""
        a = Attendance(student_id=1, status="Late")
        assert a.status == "Late"

    def test_invalid_status_raises(self):
        """An invalid status string should raise ValueError."""
        with pytest.raises(ValueError):
            Attendance(student_id=1, status="Sick")

    def test_attendance_str(self):
        """__str__ should include status and student ID."""
        a = Attendance(student_id=3, status="Present", date="2025-06-01")
        result = str(a)
        assert "Present" in result
        assert "2025-06-01" in result

    def test_attendance_serialization_roundtrip(self):
        """An Attendance record should survive a to_dict → from_dict round-trip."""
        a = Attendance(
            student_id=5,
            status="Absent",
            date="2025-05-15",
            notes="Sick leave",
            attendance_id=42,
        )
        d = a.to_dict()
        restored = Attendance.from_dict(d)
        assert restored.status == a.status
        assert restored.date == a.date
        assert restored.notes == a.notes


class TestAttendanceRecording:
    """Tests for marking attendance via SchoolManager."""

    def test_mark_attendance_present(self, manager, sample_student):
        """Marking a student as Present should create a valid record."""
        record = manager.mark_attendance(
            student_id=sample_student.id,
            status="Present",
        )
        assert record.status == "Present"
        assert record.student_id == sample_student.id

    def test_mark_attendance_absent(self, manager, sample_student):
        """Marking a student as Absent should create a valid record."""
        record = manager.mark_attendance(
            student_id=sample_student.id,
            status="Absent",
            notes="Sick day",
        )
        assert record.status == "Absent"
        assert record.notes == "Sick day"

    def test_attendance_appears_in_student_records(self, manager, sample_student):
        """A marked attendance record should appear in the student's attendance list."""
        manager.mark_attendance(sample_student.id, status="Present")
        records = manager.get_student_attendance(sample_student.id)
        assert len(records) == 1

    def test_attendance_summary_counts(self, manager, sample_student):
        """Attendance summary should correctly count each status."""
        manager.mark_attendance(sample_student.id, status="Present")
        manager.mark_attendance(sample_student.id, status="Present")
        manager.mark_attendance(sample_student.id, status="Absent")
        manager.mark_attendance(sample_student.id, status="Late")

        summary = sample_student.get_attendance_summary()
        assert summary["Present"] == 2
        assert summary["Absent"] == 1
        assert summary["Late"] == 1
        assert summary["total"] == 4

    def test_attendance_for_nonexistent_student_raises(self, manager):
        """Marking attendance for a non-existent student ID should raise ValueError."""
        with pytest.raises(ValueError):
            manager.mark_attendance(student_id=9999, status="Present")

    def test_attendance_invalid_status_raises(self, manager, sample_student):
        """An invalid status should raise ValueError."""
        with pytest.raises(ValueError):
            manager.mark_attendance(student_id=sample_student.id, status="Unknown")

    def test_attendance_with_custom_date(self, manager, sample_student):
        """Marking attendance with a specific date should store that date."""
        record = manager.mark_attendance(
            student_id=sample_student.id,
            status="Late",
            date="2025-03-10",
        )
        assert record.date == "2025-03-10"

    def test_multiple_attendance_records(self, manager, sample_student):
        """Multiple attendance records should all be stored per student."""
        for status in ["Present", "Present", "Absent", "Late", "Present"]:
            manager.mark_attendance(sample_student.id, status=status)

        records = manager.get_student_attendance(sample_student.id)
        assert len(records) == 5
