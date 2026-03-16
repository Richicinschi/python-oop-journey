"""Tests for Problem 01: Fibonacci Recursive."""

from __future__ import annotations

import pytest

from week01_fundamentals.solutions.day06.problem_01_fibonacci_recursive import fibonacci


def test_fibonacci_base_cases() -> None:
    """Test the base cases F(0) and F(1)."""
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1


def test_fibonacci_small_values() -> None:
    """Test small Fibonacci values."""
    assert fibonacci(2) == 1
    assert fibonacci(3) == 2
    assert fibonacci(4) == 3
    assert fibonacci(5) == 5
    assert fibonacci(6) == 8


def test_fibonacci_larger_value() -> None:
    """Test a larger Fibonacci value."""
    assert fibonacci(10) == 55
    assert fibonacci(15) == 610


def test_fibonacci_negative_raises() -> None:
    """Test that negative input raises ValueError."""
    with pytest.raises(ValueError, match="non-negative"):
        fibonacci(-1)
    with pytest.raises(ValueError, match="non-negative"):
        fibonacci(-10)
