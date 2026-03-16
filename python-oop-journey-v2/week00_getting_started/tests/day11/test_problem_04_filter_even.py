"""Tests for Problem 04: Filter Even."""

from __future__ import annotations

from week00_getting_started.solutions.day11.problem_04_filter_even import filter_even


def test_filter_even_mixed() -> None:
    """Test filtering mixed lists."""
    assert filter_even([1, 2, 3, 4, 5]) == [2, 4]
    assert filter_even([1, 3, 5, 7]) == []
    assert filter_even([2, 4, 6, 8]) == [2, 4, 6, 8]


def test_filter_even_empty() -> None:
    """Test with empty list."""
    assert filter_even([]) == []


def test_filter_even_all_odd() -> None:
    """Test with all odd numbers."""
    assert filter_even([1, 3, 5]) == []
    assert filter_even([11, 13, 15]) == []


def test_filter_even_all_even() -> None:
    """Test with all even numbers."""
    assert filter_even([2, 4, 6]) == [2, 4, 6]
    assert filter_even([10, 20, 30]) == [10, 20, 30]


def test_filter_even_with_zero() -> None:
    """Test with zero (which is even)."""
    assert filter_even([0, 1, 2]) == [0, 2]
    assert filter_even([0]) == [0]


def test_filter_even_negative() -> None:
    """Test with negative numbers."""
    assert filter_even([-4, -3, -2, -1]) == [-4, -2]
    assert filter_even([-5, -4, -3]) == [-4]
