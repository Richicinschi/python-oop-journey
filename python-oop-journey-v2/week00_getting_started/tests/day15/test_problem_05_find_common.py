"""Tests for Problem 05: Find Common Elements."""

from __future__ import annotations

from week00_getting_started.solutions.day15.problem_05_find_common import find_common


def test_common_elements_exist() -> None:
    """Test finding common elements."""
    list1 = [1, 2, 3, 4, 5]
    list2 = [4, 5, 6, 7, 8]
    result = find_common(list1, list2)
    assert result == [4, 5]


def test_no_common_elements() -> None:
    """Test with no common elements."""
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    result = find_common(list1, list2)
    assert result == []


def test_identical_lists() -> None:
    """Test with identical lists."""
    list1 = [3, 1, 2]
    list2 = [2, 3, 1]
    result = find_common(list1, list2)
    assert result == [1, 2, 3]


def test_with_duplicates() -> None:
    """Test with duplicate elements in input lists."""
    list1 = [1, 1, 2, 2, 3, 3]
    list2 = [2, 2, 3, 3, 4, 4]
    result = find_common(list1, list2)
    assert result == [2, 3]


def test_one_empty_list() -> None:
    """Test with one empty list."""
    list1 = [1, 2, 3]
    list2 = []
    result = find_common(list1, list2)
    assert result == []
