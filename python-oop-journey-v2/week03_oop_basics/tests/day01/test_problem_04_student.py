"""Tests for Problem 04: Student."""

from __future__ import annotations

from week03_oop_basics.solutions.day01.problem_04_student import Student


def test_student_creation() -> None:
    """Test creating a student."""
    student = Student("Alice", "S001")
    assert student.name == "Alice"
    assert student.student_id == "S001"


def test_add_single_course() -> None:
    """Test adding a single course."""
    student = Student("Alice", "S001")
    student.add_course("Math", 90)
    assert student.get_grade("Math") == 90


def test_add_multiple_courses() -> None:
    """Test adding multiple courses."""
    student = Student("Alice", "S001")
    student.add_course("Math", 90)
    student.add_course("Science", 85)
    
    courses = student.get_courses()
    assert "Math" in courses
    assert "Science" in courses
    assert len(courses) == 2


def test_get_courses_returns_list() -> None:
    """Test that get_courses returns a list."""
    student = Student("Alice", "S001")
    student.add_course("Math", 90)
    courses = student.get_courses()
    assert isinstance(courses, list)


def test_get_grade_nonexistent() -> None:
    """Test getting grade for non-existent course."""
    student = Student("Alice", "S001")
    result = student.get_grade("History")
    assert result is None


def test_update_course_grade() -> None:
    """Test updating an existing course grade."""
    student = Student("Alice", "S001")
    student.add_course("Math", 90)
    student.add_course("Math", 95)
    assert student.get_grade("Math") == 95


def test_average_grade() -> None:
    """Test calculating average grade."""
    student = Student("Alice", "S001")
    student.add_course("Math", 90)
    student.add_course("Science", 80)
    assert student.average_grade() == 85.0


def test_average_grade_single_course() -> None:
    """Test average with single course."""
    student = Student("Alice", "S001")
    student.add_course("Math", 90)
    assert student.average_grade() == 90.0


def test_average_grade_no_courses() -> None:
    """Test average with no courses."""
    student = Student("Alice", "S001")
    assert student.average_grade() is None


def test_average_grade_with_decimal() -> None:
    """Test average calculation results in decimal."""
    student = Student("Alice", "S001")
    student.add_course("Math", 90)
    student.add_course("Science", 85)
    assert student.average_grade() == 87.5


def test_str_representation() -> None:
    """Test the __str__ method."""
    student = Student("Alice", "S001")
    student.add_course("Math", 90)
    result = str(student)
    assert "Alice" in result


def test_repr_representation() -> None:
    """Test the __repr__ method."""
    student = Student("Alice", "S001")
    result = repr(student)
    assert "Student" in result
    assert "Alice" in result
