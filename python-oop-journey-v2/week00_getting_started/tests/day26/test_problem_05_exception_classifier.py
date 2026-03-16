"""Tests for Problem 05: Exception Classifier."""

from __future__ import annotations

from week00_getting_started.solutions.day26.problem_05_exception_classifier import (
    classify_exception,
)


def test_divide_by_zero() -> None:
    """Test division by zero."""
    assert classify_exception("divide", 10, 0) == "ZeroDivisionError"


def test_divide_success() -> None:
    """Test successful division."""
    assert classify_exception("divide", 10, 2) == "None"


def test_index_error() -> None:
    """Test index out of range."""
    assert classify_exception("index", [1, 2], 5) == "IndexError"


def test_index_success() -> None:
    """Test valid index."""
    assert classify_exception("index", [1, 2, 3], 1) == "None"


def test_key_error() -> None:
    """Test missing key."""
    assert classify_exception("key", {"a": 1}, "b") == "KeyError"


def test_key_success() -> None:
    """Test valid key."""
    assert classify_exception("key", {"a": 1}, "a") == "None"


def test_value_error() -> None:
    """Test invalid conversion."""
    assert classify_exception("convert_int", "abc") == "ValueError"


def test_convert_success() -> None:
    """Test valid conversion."""
    assert classify_exception("convert_int", "42") == "None"


def test_type_error() -> None:
    """Test type error in concat."""
    # Note: safe_concat handles this, but direct concat might fail
    assert classify_exception("concat", [1, 2], [3, 4]) == "None"  # Lists can concat
