"""Tests for Problem 03: Sum List Elements."""

from __future__ import annotations

from week00_getting_started.solutions.day12.problem_03_sum_elements import sum_elements


def test_sum_positive_numbers() -> None:
    """Test sum of positive numbers."""
    assert sum_elements([1, 2, 3, 4, 5]) == 15
    assert sum_elements([10, 20, 30]) == 60


def test_sum_empty_list() -> None:
    """Test sum of empty list returns 0."""
    assert sum_elements([]) == 0


def test_sum_single_element() -> None:
    """Test sum of single element list."""
    assert sum_elements([42]) == 42


def test_sum_with_negatives() -> None:
    """Test sum with negative numbers."""
    assert sum_elements([1, -2, 3, -4]) == -2
    assert sum_elements([-5, -5, -5]) == -15
