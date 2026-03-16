"""Tests for Problem 02: Remove Duplicates from Sorted Array."""

from __future__ import annotations

from week01_fundamentals.solutions.day03.problem_02_remove_duplicates_sorted import (
    remove_duplicates,
)


def test_basic_case() -> None:
    """Test basic case with duplicates."""
    nums = [1, 1, 2]
    k = remove_duplicates(nums)
    assert k == 2
    assert nums[:k] == [1, 2]


def test_multiple_duplicates() -> None:
    """Test with multiple duplicates of same value."""
    nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    k = remove_duplicates(nums)
    assert k == 5
    assert nums[:k] == [0, 1, 2, 3, 4]


def test_empty_array() -> None:
    """Test with empty array."""
    nums: list[int] = []
    k = remove_duplicates(nums)
    assert k == 0


def test_single_element() -> None:
    """Test with single element."""
    nums = [1]
    k = remove_duplicates(nums)
    assert k == 1
    assert nums[:k] == [1]


def test_no_duplicates() -> None:
    """Test with no duplicates."""
    nums = [1, 2, 3, 4, 5]
    k = remove_duplicates(nums)
    assert k == 5
    assert nums[:k] == [1, 2, 3, 4, 5]


def test_all_duplicates() -> None:
    """Test with all same elements."""
    nums = [1, 1, 1, 1, 1]
    k = remove_duplicates(nums)
    assert k == 1
    assert nums[:k] == [1]


def test_negative_numbers() -> None:
    """Test with negative numbers."""
    nums = [-3, -3, -2, -1, -1, 0, 0, 1]
    k = remove_duplicates(nums)
    assert k == 5
    assert nums[:k] == [-3, -2, -1, 0, 1]


def test_two_elements_same() -> None:
    """Test with two identical elements."""
    nums = [5, 5]
    k = remove_duplicates(nums)
    assert k == 1
    assert nums[:k] == [5]


def test_two_elements_different() -> None:
    """Test with two different elements."""
    nums = [1, 2]
    k = remove_duplicates(nums)
    assert k == 2
    assert nums[:k] == [1, 2]
