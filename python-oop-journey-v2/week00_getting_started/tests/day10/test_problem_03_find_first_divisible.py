"""Tests for Problem 03: Find First Divisible."""

from __future__ import annotations

from week00_getting_started.solutions.day10.problem_03_find_first_divisible import find_first_divisible


def test_find_first_divisible_start_is_divisible() -> None:
    """Test when start is already divisible."""
    assert find_first_divisible(10, 5) == 10
    assert find_first_divisible(15, 3) == 15
    assert find_first_divisible(100, 25) == 100


def test_find_first_divisible_need_to_search() -> None:
    """Test when need to search for next divisible."""
    assert find_first_divisible(11, 5) == 15
    assert find_first_divisible(14, 7) == 14
    assert find_first_divisible(16, 7) == 21


def test_first_divisible_small_numbers() -> None:
    """Test with small numbers."""
    assert find_first_divisible(1, 5) == 5
    assert find_first_divisible(1, 2) == 2
    assert find_first_divisible(3, 5) == 5


def test_find_first_divisible_prime_divisor() -> None:
    """Test with prime divisors."""
    assert find_first_divisible(10, 7) == 14
    assert find_first_divisible(20, 11) == 22
