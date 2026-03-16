"""Tests for Problem 01: Sum of Squares with Validation."""

from __future__ import annotations

import pytest

from week00_getting_started.solutions.day29.problem_01_sum_of_squares import (
    sum_of_squares,
    sum_of_squares_safe,
)


def test_sum_of_squares_basic() -> None:
    """Test sum_of_squares with basic integers."""
    assert sum_of_squares([1, 2, 3]) == 14  # 1 + 4 + 9
    assert sum_of_squares([1, 2, 3, 4]) == 30  # 1 + 4 + 9 + 16


def test_sum_of_squares_empty() -> None:
    """Test sum_of_squares with empty list."""
    assert sum_of_squares([]) == 0


def test_sum_of_squares_floats() -> None:
    """Test sum_of_squares with floats."""
    assert sum_of_squares([2.5, 3.0]) == 15.25  # 6.25 + 9.0


def test_sum_of_squares_mixed() -> None:
    """Test sum_of_squares with mixed int and float."""
    assert sum_of_squares([1, 2.5]) == 7.25  # 1 + 6.25


def test_sum_of_squares_with_string_raises() -> None:
    """Test sum_of_squares raises ValueError for string."""
    with pytest.raises(ValueError, match="numeric"):
        sum_of_squares([1, "two", 3])


def test_sum_of_squares_with_none_raises() -> None:
    """Test sum_of_squares raises ValueError for None."""
    with pytest.raises(ValueError, match="numeric"):
        sum_of_squares([1, None, 3])


def test_sum_of_squares_safe_valid() -> None:
    """Test sum_of_squares_safe returns correct value for valid input."""
    assert sum_of_squares_safe([1, 2, 3]) == 14


def test_sum_of_squares_safe_invalid() -> None:
    """Test sum_of_squares_safe returns None for invalid input."""
    assert sum_of_squares_safe([1, "two", 3]) is None


def test_sum_of_squares_safe_empty() -> None:
    """Test sum_of_squares_safe with empty list."""
    assert sum_of_squares_safe([]) == 0


def test_sum_of_squares_negative_numbers() -> None:
    """Test sum_of_squares with negative numbers."""
    assert sum_of_squares([-2, -3]) == 13  # 4 + 9
    assert sum_of_squares([-1, 1]) == 2  # 1 + 1
