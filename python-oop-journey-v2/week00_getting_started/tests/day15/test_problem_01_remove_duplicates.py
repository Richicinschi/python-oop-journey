"""Tests for Problem 01: Remove Duplicates."""

from __future__ import annotations

from week00_getting_started.solutions.day15.problem_01_remove_duplicates import remove_duplicates


def test_remove_duplicates_multiple() -> None:
    """Test removing multiple duplicates."""
    items = ["a", "b", "a", "c", "b", "a"]
    result = remove_duplicates(items)
    assert result == {"a", "b", "c"}


def test_remove_duplicates_no_duplicates() -> None:
    """Test with list that has no duplicates."""
    items = ["x", "y", "z"]
    result = remove_duplicates(items)
    assert result == {"x", "y", "z"}


def test_remove_duplicates_empty() -> None:
    """Test with empty list."""
    assert remove_duplicates([]) == set()


def test_remove_duplicates_all_same() -> None:
    """Test when all elements are the same."""
    items = ["dup", "dup", "dup"]
    result = remove_duplicates(items)
    assert result == {"dup"}


def test_remove_duplicates_single() -> None:
    """Test with single element."""
    assert remove_duplicates(["only"]) == {"only"}
