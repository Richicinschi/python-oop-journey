"""Tests for Problem 05: Count Occurrences."""

from __future__ import annotations

from week00_getting_started.solutions.day13.problem_05_count_occurrences import count_occurrences


def test_count_multiple_occurrences() -> None:
    """Test counting multiple occurrences."""
    data = (1, 2, 2, 3, 2, 4, 2)
    assert count_occurrences(data, 2) == 4


def test_count_single_occurrence() -> None:
    """Test counting single occurrence."""
    data = (1, 2, 3, 4, 5)
    assert count_occurrences(data, 3) == 1


def test_count_zero_occurrences() -> None:
    """Test counting value not in tuple."""
    data = (1, 2, 3, 4, 5)
    assert count_occurrences(data, 10) == 0


def test_count_empty_tuple() -> None:
    """Test counting in empty tuple."""
    assert count_occurrences((), 5) == 0


def test_count_all_same() -> None:
    """Test counting when all elements are the same."""
    data = (7, 7, 7, 7, 7)
    assert count_occurrences(data, 7) == 5
