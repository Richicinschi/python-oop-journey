"""Tests for Problem 02: Find The Bug."""

from __future__ import annotations

from week00_getting_started.solutions.day27.problem_02_find_the_bug import find_max


def test_find_max_normal() -> None:
    """Test finding max in normal list."""
    assert find_max([1, 5, 3, 9, 2]) == 9


def test_find_max_with_negatives() -> None:
    """Test finding max with all negatives."""
    assert find_max([-5, -2, -10]) == -2


def test_find_max_single_element() -> None:
    """Test finding max in single element list."""
    assert find_max([5]) == 5


def test_find_max_empty() -> None:
    """Test empty list returns None."""
    assert find_max([]) is None


def test_find_max_all_same() -> None:
    """Test list with all same values."""
    assert find_max([7, 7, 7]) == 7


def test_find_max_negative_single() -> None:
    """Test single negative element."""
    assert find_max([-5]) == -5
