"""Tests for Problem 02: Fibonacci Memoized."""

from __future__ import annotations

import pytest

from week01_fundamentals.solutions.day06.problem_02_fibonacci_memoized import fibonacci_memoized


def test_fibonacci_memoized_base_cases() -> None:
    """Test the base cases F(0) and F(1)."""
    assert fibonacci_memoized(0) == 0
    assert fibonacci_memoized(1) == 1


def test_fibonacci_memoized_small_values() -> None:
    """Test small Fibonacci values."""
    assert fibonacci_memoized(2) == 1
    assert fibonacci_memoized(3) == 2
    assert fibonacci_memoized(6) == 8
    assert fibonacci_memoized(10) == 55


def test_fibonacci_memoized_large_value() -> None:
    """Test that memoization handles large values efficiently."""
    assert fibonacci_memoized(50) == 12586269025
    assert fibonacci_memoized(100) == 354224848179261915075


def test_fibonacci_memoized_negative_raises() -> None:
    """Test that negative input raises ValueError."""
    with pytest.raises(ValueError, match="non-negative"):
        fibonacci_memoized(-1)


def test_fibonacci_memoized_with_external_memo() -> None:
    """Test that passing an external memo dict works."""
    memo: dict[int, int] = {}
    result = fibonacci_memoized(10, memo)
    assert result == 55
    # The memo should be populated
    assert 10 in memo
    assert memo[10] == 55
