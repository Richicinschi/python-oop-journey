"""Tests for Problem 03: Find In List."""

from __future__ import annotations

from week00_getting_started.solutions.day11.problem_03_find_in_list import find_in_list


def test_find_in_list_found() -> None:
    """Test finding existing items."""
    assert find_in_list([1, 2, 3, 4, 5], 3) == 2
    assert find_in_list([10, 20, 30], 10) == 0
    assert find_in_list([10, 20, 30], 30) == 2


def test_find_in_list_not_found() -> None:
    """Test when item is not in list."""
    assert find_in_list([1, 2, 3], 5) == -1
    assert find_in_list([1, 2, 3], 0) == -1
    assert find_in_list([], 1) == -1


def test_find_in_list_duplicates() -> None:
    """Test with duplicate values - should return first index."""
    assert find_in_list([1, 2, 2, 3], 2) == 1
    assert find_in_list([5, 5, 5], 5) == 0


def test_find_in_list_single() -> None:
    """Test with single item list."""
    assert find_in_list([42], 42) == 0
    assert find_in_list([42], 0) == -1


def test_find_in_list_negative() -> None:
    """Test with negative numbers."""
    assert find_in_list([-5, -3, -1], -3) == 1
    assert find_in_list([-5, -3, -1], 0) == -1
