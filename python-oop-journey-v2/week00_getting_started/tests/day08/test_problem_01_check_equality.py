"""Tests for Problem 01: Check Equality."""

from __future__ import annotations

from week00_getting_started.solutions.day08.problem_01_check_equality import check_equality


def test_check_equality_integers_equal() -> None:
    """Test equality with identical integers."""
    assert check_equality(5, 5) is True
    assert check_equality(0, 0) is True
    assert check_equality(-10, -10) is True


def test_check_equality_integers_not_equal() -> None:
    """Test equality with different integers."""
    assert check_equality(5, 3) is False
    assert check_equality(0, 1) is False
    assert check_equality(-5, 5) is False


def test_check_equality_strings_equal() -> None:
    """Test equality with identical strings."""
    assert check_equality("hello", "hello") is True
    assert check_equality("", "") is True
    assert check_equality("Hello World", "Hello World") is True


def test_check_equality_strings_not_equal() -> None:
    """Test equality with different strings."""
    assert check_equality("hello", "world") is False
    assert check_equality("Hello", "hello") is False
    assert check_equality("", " ") is False


def test_check_equality_floats() -> None:
    """Test equality with floats."""
    assert check_equality(3.14, 3.14) is True
    assert check_equality(0.0, 0.0) is True
    assert check_equality(1.5, 2.5) is False


def test_check_equality_mixed_types() -> None:
    """Test equality with mixed types (should be False)."""
    assert check_equality(5, "5") is False
    assert check_equality(1, True) is True  # In Python, 1 == True
    assert check_equality(0, False) is True  # In Python, 0 == False
