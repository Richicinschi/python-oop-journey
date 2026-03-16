"""Tests for Problem 04: First and Last."""

from __future__ import annotations

from week00_getting_started.solutions.day13.problem_04_first_last import first_last


def test_first_last_multiple() -> None:
    """Test getting first and last with multiple elements."""
    assert first_last(("a", "b", "c", "d")) == ("a", "d")
    assert first_last(("apple", "banana", "cherry")) == ("apple", "cherry")


def test_first_last_single() -> None:
    """Test with single element - first and last should be same."""
    assert first_last(("solo",)) == ("solo", "solo")


def test_first_last_empty() -> None:
    """Test with empty tuple returns None."""
    assert first_last(()) is None


def test_first_last_two_elements() -> None:
    """Test with exactly two elements."""
    assert first_last(("start", "end")) == ("start", "end")
