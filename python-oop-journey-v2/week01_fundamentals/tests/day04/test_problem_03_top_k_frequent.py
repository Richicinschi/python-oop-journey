"""Tests for Problem 03: Top K Frequent Elements."""

from __future__ import annotations

from week01_fundamentals.solutions.day04.problem_03_top_k_frequent import top_k_frequent


def test_basic_case() -> None:
    """Test basic frequency counting."""
    result = top_k_frequent([1, 1, 1, 2, 2, 3], 2)
    assert sorted(result) == [1, 2]


def test_single_element() -> None:
    """Test with single element."""
    result = top_k_frequent([1], 1)
    assert result == [1]


def test_k_equals_n() -> None:
    """Test when k equals number of unique elements."""
    result = top_k_frequent([1, 2, 3, 4], 4)
    assert sorted(result) == [1, 2, 3, 4]


def test_all_same() -> None:
    """Test when all elements are the same."""
    result = top_k_frequent([5, 5, 5, 5, 5], 1)
    assert result == [5]


def test_two_with_same_frequency() -> None:
    """Test when two elements have same frequency."""
    result = top_k_frequent([1, 1, 2, 2, 3], 2)
    # Should return 1 and 2 (both appear twice)
    assert sorted(result) == [1, 2]


def test_negative_numbers() -> None:
    """Test with negative numbers."""
    result = top_k_frequent([-1, -1, -1, 2, 2, 3], 2)
    assert sorted(result) == [-1, 2]


def test_k_equals_one() -> None:
    """Test when k=1."""
    result = top_k_frequent([1, 1, 2, 2, 2, 3], 1)
    assert result == [2]
