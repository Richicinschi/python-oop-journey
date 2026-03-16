"""Tests for Problem 01: Safe Divide."""

from __future__ import annotations

from week00_getting_started.solutions.day25.problem_01_safe_divide import safe_divide


def test_normal_division() -> None:
    """Test normal division."""
    assert safe_divide(10, 2) == 5.0


def test_division_by_zero() -> None:
    """Test division by zero returns 0."""
    assert safe_divide(10, 0) == 0


def test_invalid_first_argument() -> None:
    """Test invalid first argument returns None."""
    assert safe_divide("hello", 2) is None


def test_invalid_second_argument() -> None:
    """Test invalid second argument returns None."""
    assert safe_divide(10, "world") is None


def test_float_division() -> None:
    """Test float division."""
    assert safe_divide(7.0, 2.0) == 3.5


def test_negative_numbers() -> None:
    """Test division with negative numbers."""
    assert safe_divide(-10, 2) == -5.0
    assert safe_divide(10, -2) == -5.0
