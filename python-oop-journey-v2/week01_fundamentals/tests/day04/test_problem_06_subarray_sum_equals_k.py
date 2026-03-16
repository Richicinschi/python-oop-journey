"""Tests for Problem 06: Subarray Sum Equals K."""

from __future__ import annotations

from week01_fundamentals.solutions.day04.problem_06_subarray_sum_equals_k import (
    subarray_sum_equals_k,
)


def test_basic_case() -> None:
    """Test basic subarray counting."""
    result = subarray_sum_equals_k([1, 1, 1], 2)
    assert result == 2  # [1,1] at indices (0,1) and (1,2)


def test_target_at_start() -> None:
    """Test when subarray starts at beginning."""
    result = subarray_sum_equals_k([1, 2, 3], 3)
    assert result == 2  # [1,2] and [3]


def test_single_element_match() -> None:
    """Test with single element matching target."""
    result = subarray_sum_equals_k([5], 5)
    assert result == 1


def test_single_element_no_match() -> None:
    """Test with single element not matching target."""
    result = subarray_sum_equals_k([5], 3)
    assert result == 0


def test_empty_array() -> None:
    """Test with empty array."""
    result = subarray_sum_equals_k([], 0)
    assert result == 0


def test_negative_numbers() -> None:
    """Test with negative numbers."""
    result = subarray_sum_equals_k([1, -1, 1, -1], 0)
    assert result == 4  # [1,-1] at (0,1), (2,3), [1,-1,1,-1], [1,-1]


def test_all_zeros() -> None:
    """Test with all zeros."""
    result = subarray_sum_equals_k([0, 0, 0], 0)
    assert result == 6  # All possible subarrays: n*(n+1)/2 = 6


def test_large_target() -> None:
    """Test with large target value."""
    result = subarray_sum_equals_k([1, 2, 3, 4, 5], 15)
    assert result == 1  # [1,2,3,4,5]
