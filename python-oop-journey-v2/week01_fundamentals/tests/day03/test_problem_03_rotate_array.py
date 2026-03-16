"""Tests for Problem 03: Rotate Array."""

from __future__ import annotations

from week01_fundamentals.solutions.day03.problem_03_rotate_array import rotate


def test_example_1() -> None:
    """Test first example from problem."""
    nums = [1, 2, 3, 4, 5, 6, 7]
    rotate(nums, 3)
    assert nums == [5, 6, 7, 1, 2, 3, 4]


def test_example_2() -> None:
    """Test second example from problem."""
    nums = [-1, -100, 3, 99]
    rotate(nums, 2)
    assert nums == [3, 99, -1, -100]


def test_k_zero() -> None:
    """Test with k=0 (no rotation)."""
    nums = [1, 2, 3, 4, 5]
    rotate(nums, 0)
    assert nums == [1, 2, 3, 4, 5]


def test_k_equals_length() -> None:
    """Test with k equal to array length (full cycle)."""
    nums = [1, 2, 3, 4, 5]
    rotate(nums, 5)
    assert nums == [1, 2, 3, 4, 5]


def test_k_greater_than_length() -> None:
    """Test with k > array length."""
    nums = [1, 2, 3]
    rotate(nums, 4)  # Same as rotating by 1
    assert nums == [3, 1, 2]


def test_single_element() -> None:
    """Test with single element."""
    nums = [42]
    rotate(nums, 100)
    assert nums == [42]


def test_k_multiple_of_length() -> None:
    """Test with k being multiple of length."""
    nums = [1, 2, 3, 4]
    rotate(nums, 8)  # 2 full cycles
    assert nums == [1, 2, 3, 4]


def test_two_elements() -> None:
    """Test with two elements."""
    nums = [1, 2]
    rotate(nums, 1)
    assert nums == [2, 1]


def test_large_k() -> None:
    """Test with very large k."""
    nums = [1, 2, 3]
    rotate(nums, 1000000000)
    # 1000000000 % 3 = 1
    assert nums == [3, 1, 2]
