"""Tests for Problem 02: Safe Convert."""

from __future__ import annotations

from week00_getting_started.solutions.day25.problem_02_safe_convert import safe_convert


def test_valid_integer() -> None:
    """Test converting valid integer string."""
    assert safe_convert("42") == 42


def test_valid_negative() -> None:
    """Test converting negative integer."""
    assert safe_convert("-10") == -10


def test_invalid_string() -> None:
    """Test invalid string returns default."""
    assert safe_convert("abc") == 0


def test_empty_string() -> None:
    """Test empty string returns default."""
    assert safe_convert("") == 0


def test_custom_default() -> None:
    """Test custom default value."""
    assert safe_convert("abc", default=-1) == -1
    assert safe_convert("xyz", default=100) == 100


def test_float_string() -> None:
    """Test float string (should fail and return default)."""
    assert safe_convert("3.14") == 0
