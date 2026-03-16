"""Tests for Problem 05: Binary Search Recursive."""

from __future__ import annotations

from week01_fundamentals.solutions.day06.problem_05_binary_search_recursive import binary_search


def test_binary_search_found() -> None:
    """Test finding existing elements."""
    arr = [1, 2, 3, 4, 5]
    assert binary_search(arr, 1) == 0
    assert binary_search(arr, 3) == 2
    assert binary_search(arr, 5) == 4


def test_binary_search_not_found() -> None:
    """Test searching for non-existent elements."""
    arr = [1, 2, 3, 4, 5]
    assert binary_search(arr, 0) == -1
    assert binary_search(arr, 6) == -1
    assert binary_search(arr, 100) == -1


def test_binary_search_empty_array() -> None:
    """Test searching in empty array."""
    assert binary_search([], 5) == -1


def test_binary_search_single_element() -> None:
    """Test searching in single-element array."""
    assert binary_search([5], 5) == 0
    assert binary_search([5], 3) == -1


def test_binary_search_larger_array() -> None:
    """Test with a larger sorted array."""
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    assert binary_search(arr, 1) == 0
    assert binary_search(arr, 19) == 9
    assert binary_search(arr, 11) == 5
    assert binary_search(arr, 10) == -1


def test_binary_search_duplicates() -> None:
    """Test with duplicate values (should find one of them)."""
    arr = [1, 2, 2, 2, 3]
    result = binary_search(arr, 2)
    assert result in [1, 2, 3]  # Any valid index is acceptable
