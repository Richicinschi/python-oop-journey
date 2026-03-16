"""Tests for Problem 03: Tuple Statistics."""

from __future__ import annotations

from week00_getting_started.solutions.day13.problem_03_tuple_statistics import tuple_statistics


def test_statistics_multiple_elements() -> None:
    """Test statistics with multiple elements."""
    result = tuple_statistics((3, 1, 4, 1, 5, 9, 2, 6))
    assert result == (1, 9, 8)


def test_statistics_single_element() -> None:
    """Test statistics with single element."""
    result = tuple_statistics((42,))
    assert result == (42, 42, 1)


def test_statistics_empty_tuple() -> None:
    """Test statistics with empty tuple returns None."""
    result = tuple_statistics(())
    assert result is None


def test_statistics_with_negatives() -> None:
    """Test statistics with negative numbers."""
    result = tuple_statistics((-5, -2, -10, -1))
    assert result == (-10, -1, 4)
