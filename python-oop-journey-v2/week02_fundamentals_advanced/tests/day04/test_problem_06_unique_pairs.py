"""Tests for Problem 06: Unique Pairs."""

from __future__ import annotations

from week02_fundamentals_advanced.solutions.day04.problem_06_unique_pairs import (
    unique_pairs,
)


def test_three_items() -> None:
    """Test with three items."""
    items = ["a", "b", "c"]
    result = unique_pairs(items)
    assert result == {("a", "b"), ("a", "c"), ("b", "c")}


def test_two_items() -> None:
    """Test with two items."""
    items = ["x", "y"]
    assert unique_pairs(items) == {("x", "y")}


def test_single_item() -> None:
    """Test with single item - no pairs possible."""
    items = ["a"]
    assert unique_pairs(items) == set()


def test_empty_list() -> None:
    """Test with empty list."""
    assert unique_pairs([]) == set()


def test_four_items() -> None:
    """Test with four items - should have 6 pairs."""
    items = ["a", "b", "c", "d"]
    result = unique_pairs(items)
    expected = {
        ("a", "b"),
        ("a", "c"),
        ("a", "d"),
        ("b", "c"),
        ("b", "d"),
        ("c", "d"),
    }
    assert result == expected


def test_unsorted_input() -> None:
    """Test that unsorted input produces ordered pairs."""
    items = ["c", "a", "b"]
    result = unique_pairs(items)
    # Pairs should be ordered with smaller item first
    assert result == {("a", "b"), ("a", "c"), ("b", "c")}


def test_duplicate_items() -> None:
    """Test with duplicate items in input."""
    items = ["a", "a", "b"]
    result = unique_pairs(items)
    # Duplicates create same pairs, so set deduplicates
    assert result == {("a", "a"), ("a", "b")}


def test_numeric_strings() -> None:
    """Test with numeric strings."""
    items = ["1", "2", "3"]
    result = unique_pairs(items)
    assert result == {("1", "2"), ("1", "3"), ("2", "3")}
