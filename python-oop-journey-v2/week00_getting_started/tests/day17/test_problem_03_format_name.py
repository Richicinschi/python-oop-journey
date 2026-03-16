"""Tests for Problem 03: Format Name."""

from __future__ import annotations

from week00_getting_started.solutions.day17.problem_03_format_name import format_name


def test_format_name_with_middle() -> None:
    """Test formatting with middle name."""
    assert format_name("John", "Doe", "Quincy") == "John Quincy Doe"
    assert format_name("Mary", "Smith", "Jane") == "Mary Jane Smith"


def test_format_name_without_middle() -> None:
    """Test formatting without middle name."""
    assert format_name("John", "Doe") == "John Doe"
    assert format_name("Alice", "Johnson") == "Alice Johnson"


def test_format_name_with_none_middle() -> None:
    """Test formatting with None as middle name."""
    assert format_name("John", "Doe", None) == "John Doe"


def test_format_name_keyword_arguments() -> None:
    """Test formatting with keyword arguments."""
    assert format_name(first="Bob", last="Smith") == "Bob Smith"
    assert format_name(last="Jones", first="Alice", middle="Marie") == "Alice Marie Jones"
