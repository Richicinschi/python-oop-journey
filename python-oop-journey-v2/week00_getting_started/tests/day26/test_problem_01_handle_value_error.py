"""Tests for Problem 01: Handle ValueError."""

from __future__ import annotations

from week00_getting_started.solutions.day26.problem_01_handle_value_error import (
    convert_number,
)


def test_convert_valid_int() -> None:
    """Test converting valid integer string."""
    result = convert_number("42")
    assert result == 42
    assert isinstance(result, int)


def test_convert_valid_float() -> None:
    """Test converting valid float string."""
    result = convert_number("3.14")
    assert result == 3.14
    assert isinstance(result, float)


def test_convert_negative() -> None:
    """Test converting negative number."""
    assert convert_number("-10") == -10


def test_convert_invalid() -> None:
    """Test converting invalid string returns None."""
    assert convert_number("abc") is None
    assert convert_number("12.34.56") is None
    assert convert_number("") is None


def test_convert_whole_number_float() -> None:
    """Test that whole number floats are converted."""
    result = convert_number("5.0")
    assert result == 5.0
    assert isinstance(result, float)
