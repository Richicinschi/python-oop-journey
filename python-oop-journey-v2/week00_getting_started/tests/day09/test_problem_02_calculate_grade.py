"""Tests for Problem 02: Calculate Grade."""

from __future__ import annotations

from week00_getting_started.solutions.day09.problem_02_calculate_grade import calculate_grade


def test_calculate_grade_a() -> None:
    """Test grade A."""
    assert calculate_grade(90) == "A"
    assert calculate_grade(95) == "A"
    assert calculate_grade(100) == "A"


def test_calculate_grade_b() -> None:
    """Test grade B."""
    assert calculate_grade(80) == "B"
    assert calculate_grade(85) == "B"
    assert calculate_grade(89) == "B"


def test_calculate_grade_c() -> None:
    """Test grade C."""
    assert calculate_grade(70) == "C"
    assert calculate_grade(75) == "C"
    assert calculate_grade(79) == "C"


def test_calculate_grade_d() -> None:
    """Test grade D."""
    assert calculate_grade(60) == "D"
    assert calculate_grade(65) == "D"
    assert calculate_grade(69) == "D"


def test_calculate_grade_f() -> None:
    """Test grade F."""
    assert calculate_grade(0) == "F"
    assert calculate_grade(50) == "F"
    assert calculate_grade(59) == "F"
