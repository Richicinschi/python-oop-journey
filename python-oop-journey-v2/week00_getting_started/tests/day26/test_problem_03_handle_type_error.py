"""Tests for Problem 03: Handle TypeError."""

from __future__ import annotations

from week00_getting_started.solutions.day26.problem_03_handle_type_error import (
    safe_concat,
)


def test_string_concat() -> None:
    """Test concatenating strings."""
    assert safe_concat("Hello, ", "World") == "Hello, World"


def test_string_and_int() -> None:
    """Test concatenating string and int."""
    assert safe_concat("Age: ", 25) == "Age: 25"


def test_int_and_string() -> None:
    """Test concatenating int and string."""
    assert safe_concat(100, " items") == "100 items"


def test_two_ints() -> None:
    """Test concatenating two ints."""
    assert safe_concat(1, 2) == "12"


def test_none_value() -> None:
    """Test concatenating with None."""
    assert safe_concat("Value: ", None) == "Value: None"


def test_list_value() -> None:
    """Test concatenating with list."""
    assert safe_concat("Items: ", [1, 2, 3]) == "Items: [1, 2, 3]"
