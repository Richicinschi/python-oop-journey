"""Tests for Problem 04: Find Maximum."""

from __future__ import annotations

from week00_getting_started.solutions.day12.problem_04_find_max import find_max


def test_find_max_positive_numbers() -> None:
    """Test finding max in positive numbers."""
    assert find_max([1, 2, 3, 4, 5]) == 5
    assert find_max([5, 4, 3, 2, 1]) == 5
    assert find_max([3, 1, 4, 1, 5, 9]) == 9


def test_find_max_empty_list() -> None:
    """Test finding max in empty list returns None."""
    assert find_max([]) is None


def test_find_max_single_element() -> None:
    """Test finding max in single element list."""
    assert find_max([42]) == 42


def test_find_max_with_negatives() -> None:
    """Test finding max with negative numbers."""
    assert find_max([-5, -2, -10]) == -2
    assert find_max([-1, 0, -5]) == 0
