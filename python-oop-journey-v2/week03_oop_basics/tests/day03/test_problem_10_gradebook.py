"""Tests for Problem 10: Gradebook."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day03.problem_10_gradebook import (
    Student,
)


class TestStudent:
    """Test suite for Student class."""
    
    def test_initialization(self) -> None:
        """Test student initialization."""
        student = Student("S001", "Alice")
        assert student.student_id == "S001"
        assert student.name == "Alice"
        assert student.num_courses == 0
    
    def test_initialization_strips_strings(self) -> None:
        """Test that strings are stripped."""
        student = Student("  S001  ", "  Alice  ")
        assert student.student_id == "S001"
        assert student.name == "Alice"
    
    def test_student_id_read_only(self) -> None:
        """Test that student_id is read-only."""
        student = Student("S001", "Alice")
        with pytest.raises(AttributeError):
            student.student_id = "S002"  # type: ignore
    
    def test_name_setter_valid(self) -> None:
        """Test name setter with valid value."""
        student = Student("S001", "Alice")
        student.name = "Bob"
        assert student.name == "Bob"
    
    def test_name_setter_empty_raises(self) -> None:
        """Test name setter with empty value raises."""
        student = Student("S001", "Alice")
        with pytest.raises(ValueError, match="empty"):
            student.name = ""
    
    def test_name_setter_non_string_raises(self) -> None:
        """Test name setter with non-string raises TypeError."""
        student = Student("S001", "Alice")
        with pytest.raises(TypeError, match="string"):
            student.name = 123  # type: ignore
    
    def test_add_grade_valid(self) -> None:
        """Test add_grade with valid values."""
        student = Student("S001", "Alice")
        student.add_grade("Math", 90.0)
        assert student.num_courses == 1
        assert student.get_grade("Math") == 90.0
    
    def test_add_grade_multiple(self) -> None:
        """Test adding multiple grades."""
        student = Student("S001", "Alice")
        student.add_grade("Math", 90.0)
        student.add_grade("Science", 85.0)
        student.add_grade("English", 92.0)
        assert student.num_courses == 3
    
    def test_add_grade_update_existing(self) -> None:
        """Test updating existing grade."""
        student = Student("S001", "Alice")
        student.add_grade("Math", 80.0)
        student.add_grade("Math", 90.0)
        assert student.get_grade("Math") == 90.0
        assert student.num_courses == 1  # Still 1 course
    
    def test_add_grade_invalid_range_high(self) -> None:
        """Test add_grade with grade > 100 raises."""
        student = Student("S001", "Alice")
        with pytest.raises(ValueError, match="0 and 100"):
            student.add_grade("Math", 105.0)
    
    def test_add_grade_invalid_range_low(self) -> None:
        """Test add_grade with grade < 0 raises."""
        student = Student("S001", "Alice")
        with pytest.raises(ValueError, match="0 and 100"):
            student.add_grade("Math", -5.0)
    
    def test_add_grade_non_string_course(self) -> None:
        """Test add_grade with non-string course raises."""
        student = Student("S001", "Alice")
        with pytest.raises(TypeError, match="string"):
            student.add_grade(123, 90.0)  # type: ignore
    
    def test_add_grade_non_numeric_grade(self) -> None:
        """Test add_grade with non-numeric grade raises."""
        student = Student("S001", "Alice")
        with pytest.raises(TypeError, match="number"):
            student.add_grade("Math", "A")  # type: ignore
    
    def test_courses_property(self) -> None:
        """Test courses property."""
        student = Student("S001", "Alice")
        student.add_grade("Math", 90.0)
        student.add_grade("Science", 85.0)
        courses = student.courses
        assert "Math" in courses
        assert "Science" in courses
        assert len(courses) == 2
    
    def test_get_grade_not_found(self) -> None:
        """Test get_grade returns None for non-existent course."""
        student = Student("S001", "Alice")
        assert student.get_grade("NonExistent") is None
    
    def test_remove_grade_success(self) -> None:
        """Test remove_grade returns True on success."""
        student = Student("S001", "Alice")
        student.add_grade("Math", 90.0)
        result = student.remove_grade("Math")
        assert result is True
        assert student.num_courses == 0
    
    def test_remove_grade_failure(self) -> None:
        """Test remove_grade returns False when course doesn't exist."""
        student = Student("S001", "Alice")
        result = student.remove_grade("NonExistent")
        assert result is False
    
    def test_average_no_grades(self) -> None:
        """Test average returns None when no grades."""
        student = Student("S001", "Alice")
        assert student.average is None
    
    def test_average_single_grade(self) -> None:
        """Test average with single grade."""
        student = Student("S001", "Alice")
        student.add_grade("Math", 90.0)
        assert student.average == 90.0
    
    def test_average_multiple_grades(self) -> None:
        """Test average with multiple grades."""
        student = Student("S001", "Alice")
        student.add_grade("Math", 90.0)
        student.add_grade("Science", 80.0)
        assert student.average == 85.0
    
    def test_gpa_no_grades(self) -> None:
        """Test gpa returns None when no grades."""
        student = Student("S001", "Alice")
        assert student.gpa is None
    
    def test_gpa_all_a(self) -> None:
        """Test gpa with all A grades."""
        student = Student("S001", "Alice")
        student.add_grade("Math", 95.0)
        student.add_grade("Science", 93.0)
        assert student.gpa == 4.0
    
    def test_gpa_mixed(self) -> None:
        """Test gpa with mixed grades."""
        student = Student("S001", "Alice")
        student.add_grade("Math", 95.0)  # A = 4.0
        student.add_grade("Science", 85.0)  # B = 3.0
        assert student.gpa == 3.5
    
    def test_highest_grade_no_grades(self) -> None:
        """Test highest_grade returns None when no grades."""
        student = Student("S001", "Alice")
        assert student.highest_grade is None
    
    def test_highest_grade_single(self) -> None:
        """Test highest_grade with single grade."""
        student = Student("S001", "Alice")
        student.add_grade("Math", 90.0)
        assert student.highest_grade == ("Math", 90.0)
    
    def test_highest_grade_multiple(self) -> None:
        """Test highest_grade with multiple grades."""
        student = Student("S001", "Alice")
        student.add_grade("Math", 80.0)
        student.add_grade("Science", 95.0)
        student.add_grade("English", 85.0)
        assert student.highest_grade == ("Science", 95.0)
    
    def test_lowest_grade_no_grades(self) -> None:
        """Test lowest_grade returns None when no grades."""
        student = Student("S001", "Alice")
        assert student.lowest_grade is None
    
    def test_lowest_grade_multiple(self) -> None:
        """Test lowest_grade with multiple grades."""
        student = Student("S001", "Alice")
        student.add_grade("Math", 80.0)
        student.add_grade("Science", 95.0)
        student.add_grade("English", 70.0)
        assert student.lowest_grade == ("English", 70.0)
    
    def test_get_letter_grade_a(self) -> None:
        """Test get_letter_grade for A."""
        student = Student("S001", "Alice")
        student.add_grade("Math", 95.0)
        assert student.get_letter_grade("Math") == "A"
    
    def test_get_letter_grade_b(self) -> None:
        """Test get_letter_grade for B."""
        student = Student("S001", "Alice")
        student.add_grade("Math", 85.0)
        assert student.get_letter_grade("Math") == "B"
    
    def test_get_letter_grade_f(self) -> None:
        """Test get_letter_grade for F."""
        student = Student("S001", "Alice")
        student.add_grade("Math", 55.0)
        assert student.get_letter_grade("Math") == "F"
    
    def test_get_letter_grade_not_found(self) -> None:
        """Test get_letter_grade returns None for non-existent course."""
        student = Student("S001", "Alice")
        assert student.get_letter_grade("NonExistent") is None
