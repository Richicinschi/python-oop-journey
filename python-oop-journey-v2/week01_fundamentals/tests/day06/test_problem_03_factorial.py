"""Tests for Problem 03: Factorial."""

from __future__ import annotations

import pytest

from week01_fundamentals.solutions.day06.problem_03_factorial import factorial


def test_factorial_base_case() -> None:
    """Test the base case 0! = 1."""
    assert factorial(0) == 1


def test_factorial_one() -> None:
    """Test 1! = 1."""
    assert factorial(1) == 1


def test_factorial_small_values() -> None:
    """Test small factorial values."""
    assert factorial(2) == 2
    assert factorial(3) == 6
    assert factorial(4) == 24
    assert factorial(5) == 120


def test_factorial_larger_values() -> None:
    """Test larger factorial values."""
    assert factorial(6) == 720
    assert factorial(10) == 3628800
    assert factorial(12) == 479001600


def test_factorial_negative_raises() -> None:
    """Test that negative input raises ValueError."""
    with pytest.raises(ValueError, match="non-negative"):
        factorial(-1)
    with pytest.raises(ValueError, match="non-negative"):
        factorial(-5)
