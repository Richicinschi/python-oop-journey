"""Tests for Problem 05: Intersection of Two Arrays."""

from __future__ import annotations

from week01_fundamentals.solutions.day04.problem_05_intersection_of_two_arrays import (
    intersection_of_two_arrays,
)


def test_basic_case() -> None:
    """Test basic intersection."""
    result = intersection_of_two_arrays([1, 2, 2, 1], [2, 2])
    assert sorted(result) == [2]


def test_multiple_intersections() -> None:
    """Test with multiple common elements."""
    result = intersection_of_two_arrays([4, 9, 5], [9, 4, 9, 8, 4])
    assert sorted(result) == [4, 9]


def test_no_intersection() -> None:
    """Test when no intersection exists."""
    result = intersection_of_two_arrays([1, 2, 3], [4, 5, 6])
    assert result == []


def test_empty_first_array() -> None:
    """Test with empty first array."""
    result = intersection_of_two_arrays([], [1, 2, 3])
    assert result == []


def test_empty_second_array() -> None:
    """Test with empty second array."""
    result = intersection_of_two_arrays([1, 2, 3], [])
    assert result == []


def test_both_empty() -> None:
    """Test with both arrays empty."""
    result = intersection_of_two_arrays([], [])
    assert result == []


def test_identical_arrays() -> None:
    """Test with identical arrays."""
    result = intersection_of_two_arrays([1, 2, 3], [1, 2, 3])
    assert sorted(result) == [1, 2, 3]


def test_negative_numbers() -> None:
    """Test with negative numbers."""
    result = intersection_of_two_arrays([-1, -2, 3], [-2, 3, 4])
    assert sorted(result) == [-2, 3]
