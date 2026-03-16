"""Tests for Problem 04: Longest Consecutive Sequence."""

from __future__ import annotations

from week01_fundamentals.solutions.day04.problem_04_longest_consecutive_sequence import (
    longest_consecutive_sequence,
)


def test_basic_case() -> None:
    """Test basic sequence detection."""
    result = longest_consecutive_sequence([100, 4, 200, 1, 3, 2])
    assert result == 4  # [1, 2, 3, 4]


def test_longer_sequence() -> None:
    """Test with longer consecutive sequence."""
    result = longest_consecutive_sequence([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])
    assert result == 9  # [0, 1, 2, 3, 4, 5, 6, 7, 8]


def test_empty_list() -> None:
    """Test with empty list."""
    result = longest_consecutive_sequence([])
    assert result == 0


def test_single_element() -> None:
    """Test with single element."""
    result = longest_consecutive_sequence([1])
    assert result == 1


def test_no_consecutive() -> None:
    """Test when no consecutive elements."""
    result = longest_consecutive_sequence([1, 3, 5, 7, 9])
    assert result == 1


def test_all_same() -> None:
    """Test with all same elements."""
    result = longest_consecutive_sequence([5, 5, 5, 5])
    assert result == 1


def test_negative_numbers() -> None:
    """Test with negative numbers."""
    result = longest_consecutive_sequence([-1, -2, -3, 0, 1, 2])
    assert result == 6  # [-3, -2, -1, 0, 1, 2]


def test_unsorted_with_gaps() -> None:
    """Test unsorted array with gaps."""
    result = longest_consecutive_sequence([9, 1, 4, 7, 3, 2, 8, 5, 6])
    assert result == 9  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
