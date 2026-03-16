"""Tests for Problem 04."""

from __future__ import annotations

from week00_getting_started.solutions.day04.problem_04_variable_naming_conventions import variable_naming_conventions


def test_naming_conventions() -> None:
    """Test case 1."""
    assert variable_naming_conventions(10, 20) == {'student_count': 10, 'max_score': 20}


def test_naming_zero() -> None:
    """Test case 2."""
    assert variable_naming_conventions(0, 0) == {'student_count': 0, 'max_score': 0}


def test_naming_large() -> None:
    """Test case 3."""
    assert variable_naming_conventions(1000, 5000) == {'student_count': 1000, 'max_score': 5000}
