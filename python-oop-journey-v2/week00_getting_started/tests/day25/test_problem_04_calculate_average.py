"""Tests for Problem 04: Calculate Average."""

from __future__ import annotations

from week00_getting_started.solutions.day25.problem_04_calculate_average import (
    calculate_average,
)


def test_normal_list() -> None:
    """Test average of normal list."""
    assert calculate_average([1, 2, 3, 4]) == 2.5


def test_empty_list() -> None:
    """Test empty list returns 0."""
    assert calculate_average([]) == 0.0


def test_with_invalid_items() -> None:
    """Test skipping invalid items."""
    assert calculate_average([1, "two", 3]) == 2.0
    assert calculate_average([10, None, 20, "abc"]) == 15.0


def test_all_invalid() -> None:
    """Test list with all invalid items."""
    assert calculate_average(["a", "b", None]) == 0.0


def test_float_numbers() -> None:
    """Test with float numbers."""
    assert calculate_average([1.5, 2.5, 3.0]) == 2.3333333333333335


def test_mixed_types() -> None:
    """Test with mixed numeric types."""
    assert calculate_average([1, 2.0, 3]) == 2.0
