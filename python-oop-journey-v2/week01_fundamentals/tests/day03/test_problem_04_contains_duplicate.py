"""Tests for Problem 04: Contains Duplicate."""

from __future__ import annotations

from week01_fundamentals.solutions.day03.problem_04_contains_duplicate import (
    contains_duplicate,
)


def test_has_duplicate() -> None:
    """Test with duplicate present."""
    assert contains_duplicate([1, 2, 3, 1]) is True


def test_no_duplicate() -> None:
    """Test with all unique elements."""
    assert contains_duplicate([1, 2, 3, 4]) is False


def test_multiple_duplicates() -> None:
    """Test with multiple duplicates."""
    assert contains_duplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) is True


def test_single_element() -> None:
    """Test with single element."""
    assert contains_duplicate([42]) is False


def test_two_elements_same() -> None:
    """Test with two identical elements."""
    assert contains_duplicate([1, 1]) is True


def test_two_elements_different() -> None:
    """Test with two different elements."""
    assert contains_duplicate([1, 2]) is False


def test_negative_numbers() -> None:
    """Test with negative numbers."""
    assert contains_duplicate([-1, -2, -3, -1]) is True


def test_mixed_duplicates() -> None:
    """Test with mix of positive and negative."""
    assert contains_duplicate([-1, 1, -1, 1]) is True


def test_large_numbers() -> None:
    """Test with large numbers."""
    assert contains_duplicate([1000000000, -1000000000, 1000000000]) is True


def test_consecutive_duplicates() -> None:
    """Test with consecutive duplicates."""
    assert contains_duplicate([1, 1, 2, 2, 3, 3]) is True


def test_distant_duplicates() -> None:
    """Test with duplicates far apart."""
    assert contains_duplicate([1, 2, 3, 4, 5, 1]) is True
