"""Tests for Problem 04: Error Description."""

from __future__ import annotations

from week00_getting_started.solutions.day24.problem_04_error_description import (
    describe_error,
)


def test_describe_zero_division() -> None:
    """Test ZeroDivisionError description."""
    assert describe_error("ZeroDivisionError") == "Cannot divide a number by zero"


def test_describe_name_error() -> None:
    """Test NameError description."""
    assert describe_error("NameError") == "Variable name is not defined"


def test_describe_type_error() -> None:
    """Test TypeError description."""
    assert describe_error("TypeError") == "Operation applied to wrong type"


def test_describe_value_error() -> None:
    """Test ValueError description."""
    assert describe_error("ValueError") == "Right type but inappropriate value"


def test_describe_index_error() -> None:
    """Test IndexError description."""
    assert describe_error("IndexError") == "Sequence index out of range"


def test_describe_key_error() -> None:
    """Test KeyError description."""
    assert describe_error("KeyError") == "Dictionary key not found"


def test_describe_attribute_error() -> None:
    """Test AttributeError description."""
    assert describe_error("AttributeError") == "Object has no such attribute"


def test_describe_unknown_error() -> None:
    """Test unknown error type."""
    assert describe_error("SomeRandomError") == "Unknown error type"
