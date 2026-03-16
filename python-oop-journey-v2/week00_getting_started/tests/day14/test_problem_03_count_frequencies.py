"""Tests for Problem 03: Count Frequencies."""

from __future__ import annotations

from week00_getting_started.solutions.day14.problem_03_count_frequencies import count_frequencies


def test_count_basic() -> None:
    """Test basic frequency counting."""
    items = ["a", "b", "a", "c", "b", "a"]
    result = count_frequencies(items)
    assert result == {"a": 3, "b": 2, "c": 1}


def test_count_empty_list() -> None:
    """Test with empty list."""
    assert count_frequencies([]) == {}


def test_count_single_item() -> None:
    """Test with single item."""
    assert count_frequencies(["only"]) == {"only": 1}


def test_count_all_same() -> None:
    """Test when all items are the same."""
    items = ["x", "x", "x", "x"]
    assert count_frequencies(items) == {"x": 4}


def test_count_all_unique() -> None:
    """Test when all items are unique."""
    items = ["a", "b", "c", "d"]
    assert count_frequencies(items) == {"a": 1, "b": 1, "c": 1, "d": 1}
