"""Tests for Problem 06: Merge Sorted Arrays."""

from __future__ import annotations

from week01_fundamentals.solutions.day03.problem_06_merge_sorted_arrays import merge


def test_example_1() -> None:
    """Test first example from problem."""
    nums1 = [1, 2, 3, 0, 0, 0]
    merge(nums1, 3, [2, 5, 6], 3)
    assert nums1 == [1, 2, 2, 3, 5, 6]


def test_example_2() -> None:
    """Test second example from problem."""
    nums1 = [1]
    merge(nums1, 1, [], 0)
    assert nums1 == [1]


def test_example_3() -> None:
    """Test third example from problem."""
    nums1 = [0]
    merge(nums1, 0, [1], 1)
    assert nums1 == [1]


def test_nums1_all_smaller() -> None:
    """Test when all nums1 elements are smaller."""
    nums1 = [1, 2, 3, 0, 0, 0]
    merge(nums1, 3, [4, 5, 6], 3)
    assert nums1 == [1, 2, 3, 4, 5, 6]


def test_nums2_all_smaller() -> None:
    """Test when all nums2 elements are smaller."""
    nums1 = [4, 5, 6, 0, 0, 0]
    merge(nums1, 3, [1, 2, 3], 3)
    assert nums1 == [1, 2, 3, 4, 5, 6]


def test_interleaved() -> None:
    """Test with interleaved values."""
    nums1 = [1, 3, 5, 0, 0, 0]
    merge(nums1, 3, [2, 4, 6], 3)
    assert nums1 == [1, 2, 3, 4, 5, 6]


def test_duplicates() -> None:
    """Test with duplicate values."""
    nums1 = [1, 2, 3, 0, 0, 0, 0]
    merge(nums1, 3, [1, 2, 3, 4], 4)
    assert nums1 == [1, 1, 2, 2, 3, 3, 4]


def test_negative_numbers() -> None:
    """Test with negative numbers."""
    # nums1 has [-1] + padding zeros, nums2 = [-3, -2, 5]
    # Merged result: [-3, -2, -1, 5, 0]
    nums1 = [-1, 0, 0, 0, 0]
    merge(nums1, 1, [-3, -2, 5], 3)
    assert nums1 == [-3, -2, -1, 5, 0]


def test_negative_numbers_v2() -> None:
    """Test with negative numbers - variant."""
    nums1 = [-3, -2, -1, 0, 0]
    merge(nums1, 4, [5], 1)
    assert nums1 == [-3, -2, -1, 0, 5]


def test_only_nums2() -> None:
    """Test when nums1 is empty."""
    nums1 = [0, 0, 0]
    merge(nums1, 0, [1, 2, 3], 3)
    assert nums1 == [1, 2, 3]


def test_only_nums1() -> None:
    """Test when nums2 is empty."""
    nums1 = [1, 2, 3]
    merge(nums1, 3, [], 0)
    assert nums1 == [1, 2, 3]


def test_single_element_each() -> None:
    """Test with single element in each."""
    nums1 = [2, 0]
    merge(nums1, 1, [1], 1)
    assert nums1 == [1, 2]
