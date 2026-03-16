"""Tests for Problem 01: Sum Range."""

from __future__ import annotations

from week00_getting_started.solutions.day11.problem_01_sum_range import sum_range


def test_sum_range_normal() -> None:
    """Test normal range summation."""
    assert sum_range(1, 5) == 15  # 1+2+3+4+5
    assert sum_range(1, 10) == 55  # 1+2+...+10
    assert sum_range(3, 7) == 25  # 3+4+5+6+7


def test_sum_range_single() -> None:
    """Test with single number range."""
    assert sum_range(5, 5) == 5
    assert sum_range(1, 1) == 1
    assert sum_range(100, 100) == 100


def test_sum_range_reverse() -> None:
    """Test when start > end."""
    assert sum_range(5, 1) == 0
    assert sum_range(10, 5) == 0


def test_sum_range_negative() -> None:
    """Test with negative numbers."""
    assert sum_range(-3, 3) == 0  # -3-2-1+0+1+2+3 = 0
    assert sum_range(-2, 2) == 0  # -2-1+0+1+2 = 0
    assert sum_range(-5, -1) == -15  # -5-4-3-2-1


def test_sum_range_zero() -> None:
    """Test ranges including zero."""
    assert sum_range(0, 0) == 0
    assert sum_range(0, 5) == 15  # 0+1+2+3+4+5
