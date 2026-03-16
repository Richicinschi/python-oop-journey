"""Tests for Problem 08: Find Minimum in Rotated Sorted Array."""

from __future__ import annotations

from week01_fundamentals.solutions.day03.problem_08_find_min_rotated import find_min


def test_example_1() -> None:
    """Test first example from problem."""
    nums = [3, 4, 5, 1, 2]
    assert find_min(nums) == 1


def test_example_2() -> None:
    """Test second example from problem."""
    nums = [4, 5, 6, 7, 0, 1, 2]
    assert find_min(nums) == 0


def test_example_3() -> None:
    """Test unrotated array."""
    nums = [11, 13, 15, 17]
    assert find_min(nums) == 11


def test_single_element() -> None:
    """Test with single element."""
    nums = [1]
    assert find_min(nums) == 1


def test_two_elements_rotated() -> None:
    """Test with two elements (rotated)."""
    nums = [2, 1]
    assert find_min(nums) == 1


def test_two_elements_not_rotated() -> None:
    """Test with two elements (not rotated)."""
    nums = [1, 2]
    assert find_min(nums) == 1


def test_minimum_at_beginning() -> None:
    """Test when minimum is at beginning (not rotated)."""
    nums = [1, 2, 3, 4, 5]
    assert find_min(nums) == 1


def test_minimum_at_end() -> None:
    """Test when minimum is at end."""
    nums = [2, 3, 4, 5, 1]
    assert find_min(nums) == 1


def test_large_rotation() -> None:
    """Test with large rotation."""
    nums = [5, 6, 7, 8, 9, 1, 2, 3, 4]
    assert find_min(nums) == 1


def test_negative_numbers() -> None:
    """Test with negative numbers."""
    nums = [-2, -1, 0, 1, 2, -5, -4, -3]
    assert find_min(nums) == -5


def test_all_negative() -> None:
    """Test with all negative numbers."""
    nums = [-3, -2, -1]
    assert find_min(nums) == -3


def test_rotated_all_negative() -> None:
    """Test rotated array with all negative numbers."""
    nums = [-2, -1, -5, -4, -3]
    assert find_min(nums) == -5
