"""Tests for Problem 07: First Missing Positive."""

from __future__ import annotations

from week01_fundamentals.solutions.day04.problem_07_first_missing_positive import (
    first_missing_positive,
)


def test_basic_case() -> None:
    """Test basic missing positive."""
    result = first_missing_positive([1, 2, 0])
    assert result == 3


def test_missing_in_middle() -> None:
    """Test missing positive in middle of range."""
    result = first_missing_positive([3, 4, -1, 1])
    assert result == 2


def test_large_missing() -> None:
    """Test when smallest missing is larger than array."""
    result = first_missing_positive([7, 8, 9, 11, 12])
    assert result == 1


def test_single_element_one() -> None:
    """Test with single element 1."""
    result = first_missing_positive([1])
    assert result == 2


def test_single_element_not_one() -> None:
    """Test with single element not 1."""
    result = first_missing_positive([2])
    assert result == 1


def test_empty_array() -> None:
    """Test with empty array."""
    result = first_missing_positive([])
    assert result == 1


def test_all_negative() -> None:
    """Test with all negative numbers."""
    result = first_missing_positive([-5, -4, -3])
    assert result == 1


def test_sequential_from_one() -> None:
    """Test with sequential numbers from 1."""
    result = first_missing_positive([1, 2, 3, 4, 5])
    assert result == 6


def test_duplicates() -> None:
    """Test with duplicate values."""
    result = first_missing_positive([1, 1, 2, 2])
    assert result == 3
