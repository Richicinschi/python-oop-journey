"""Tests for Problem 01: Two Sum List."""

from __future__ import annotations

from week01_fundamentals.solutions.day03.problem_01_two_sum_list import two_sum


def test_basic_example() -> None:
    """Test the basic example from the problem."""
    result = two_sum([2, 7, 11, 15], 9)
    # Result can be [0, 1] or [1, 0]
    assert sorted(result) == [0, 1]


def test_different_positions() -> None:
    """Test with target numbers at different positions."""
    result = two_sum([3, 2, 4], 6)
    assert sorted(result) == [1, 2]


def test_same_value() -> None:
    """Test when same value appears twice."""
    result = two_sum([3, 3], 6)
    assert sorted(result) == [0, 1]


def test_negative_numbers() -> None:
    """Test with negative numbers."""
    result = two_sum([-1, -2, -3, -4, -5], -8)
    assert sorted(result) == [2, 4]  # -3 + -5 = -8


def test_mixed_positive_negative() -> None:
    """Test with mix of positive and negative numbers."""
    result = two_sum([-3, 4, 3, 90], 0)
    assert sorted(result) == [0, 2]  # -3 + 3 = 0


def test_large_numbers() -> None:
    """Test with large numbers."""
    result = two_sum([1000000000, 999999999, 1], 1000000000)
    assert sorted(result) == [1, 2]  # 999999999 + 1 = 1000000000


def test_result_at_end() -> None:
    """Test when solution is at the end of the list."""
    result = two_sum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 19)
    assert sorted(result) == [8, 9]  # 9 + 10 = 19
