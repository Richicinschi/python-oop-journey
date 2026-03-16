"""Tests for Problem 05: Maximum Subarray."""

from __future__ import annotations

from week01_fundamentals.solutions.day03.problem_05_maximum_subarray import (
    max_subarray_sum,
    max_subarray_with_indices,
)


def test_example_1() -> None:
    """Test first example from problem."""
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    assert max_subarray_sum(nums) == 6


def test_example_2() -> None:
    """Test with single element."""
    nums = [1]
    assert max_subarray_sum(nums) == 1


def test_example_3() -> None:
    """Test second example from problem."""
    nums = [5, 4, -1, 7, 8]
    assert max_subarray_sum(nums) == 23


def test_all_positive() -> None:
    """Test with all positive numbers."""
    nums = [1, 2, 3, 4, 5]
    assert max_subarray_sum(nums) == 15


def test_all_negative() -> None:
    """Test with all negative numbers."""
    nums = [-5, -2, -8, -1, -9]
    assert max_subarray_sum(nums) == -1


def test_mixed() -> None:
    """Test with mixed positive and negative."""
    nums = [-2, -3, 4, -1, -2, 1, 5, -3]
    assert max_subarray_sum(nums) == 7  # [4, -1, -2, 1, 5]


def test_alternating() -> None:
    """Test with alternating signs."""
    nums = [1, -1, 1, -1, 1]
    assert max_subarray_sum(nums) == 1


def test_large_positive_at_end() -> None:
    """Test with large positive at the end."""
    nums = [-1, -2, -3, 100]
    assert max_subarray_sum(nums) == 100


def test_two_elements() -> None:
    """Test with two elements."""
    assert max_subarray_sum([1, 2]) == 3
    assert max_subarray_sum([-1, 2]) == 2
    assert max_subarray_sum([-1, -2]) == -1


def test_with_indices() -> None:
    """Test the extended version with indices."""
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    max_sum, start, end = max_subarray_with_indices(nums)
    assert max_sum == 6
    assert nums[start:end + 1] == [4, -1, 2, 1]


def test_indices_single_element() -> None:
    """Test indices with single element."""
    nums = [5]
    max_sum, start, end = max_subarray_with_indices(nums)
    assert max_sum == 5
    assert start == 0
    assert end == 0
