"""Tests for Problem 02: Swap Variables."""

from __future__ import annotations

from week00_getting_started.solutions.day13.problem_02_swap_variables import swap_variables


def test_swap_positive_numbers() -> None:
    """Test swapping positive numbers."""
    assert swap_variables(1, 2) == (2, 1)
    assert swap_variables(10, 20) == (20, 10)


def test_swap_with_zero() -> None:
    """Test swapping with zero."""
    assert swap_variables(0, 5) == (5, 0)
    assert swap_variables(0, 0) == (0, 0)


def test_swap_negative_numbers() -> None:
    """Test swapping negative numbers."""
    assert swap_variables(-1, -2) == (-2, -1)
    assert swap_variables(-5, 10) == (10, -5)
