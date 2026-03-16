"""Tests for Problem 05: Sort Data."""

from __future__ import annotations

from week00_getting_started.solutions.day19.problem_05_sort_data import (
    sort_ascending,
    sort_descending,
    sort_by_length,
    sort_by_last_letter,
    sort_tuples_by_second_item,
)


def test_sort_ascending() -> None:
    """Test sorting numbers in ascending order."""
    assert sort_ascending([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]
    assert sort_ascending([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    assert sort_ascending([]) == []


def test_sort_descending() -> None:
    """Test sorting numbers in descending order."""
    assert sort_descending([1, 3, 2, 5, 4]) == [5, 4, 3, 2, 1]
    assert sort_descending([1, 1, 1]) == [1, 1, 1]


def test_sort_by_length() -> None:
    """Test sorting strings by length."""
    words = ["aaa", "bb", "c", "dddd"]
    assert sort_by_length(words) == ["c", "bb", "aaa", "dddd"]


def test_sort_by_length_empty() -> None:
    """Test sorting empty list."""
    assert sort_by_length([]) == []


def test_sort_by_last_letter() -> None:
    """Test sorting strings by last letter."""
    words = ["cat", "bed", "car"]  # last letters: t, d, r
    result = sort_by_last_letter(words)
    assert result == ["bed", "car", "cat"]  # d, r, t


def test_sort_tuples_by_second_item() -> None:
    """Test sorting tuples by second element."""
    data = [("b", 2), ("a", 3), ("c", 1)]
    result = sort_tuples_by_second_item(data)
    assert result == [("c", 1), ("b", 2), ("a", 3)]


def test_original_list_unchanged() -> None:
    """Test that sorted() doesn't modify the original list."""
    original = [3, 1, 2]
    sorted_list = sort_ascending(original)
    assert original == [3, 1, 2]  # Unchanged
    assert sorted_list == [1, 2, 3]  # New sorted list
