"""Tests for Problem 01: Calculate Sum."""

from __future__ import annotations

from week01_fundamentals.solutions.day01.problem_01_calculate_sum import calculate_sum


def test_calculate_sum_positive_numbers() -> None:
    """Test sum of two positive numbers."""
    assert calculate_sum(2, 3) == 5
    assert calculate_sum(10, 20) == 30


def test_calculate_sum_with_zero() -> None:
    """Test sum involving zero."""
    assert calculate_sum(0, 0) == 0
    assert calculate_sum(5, 0) == 5
    assert calculate_sum(0, 5) == 5


def test_calculate_sum_negative_numbers() -> None:
    """Test sum with negative numbers."""
    assert calculate_sum(-2, 5) == 3
    assert calculate_sum(2, -5) == -3
    assert calculate_sum(-2, -5) == -7


def test_calculate_sum_large_numbers() -> None:
    """Test sum with large numbers."""
    assert calculate_sum(1_000_000, 2_000_000) == 3_000_000
    assert calculate_sum(-1_000_000, 500_000) == -500_000
