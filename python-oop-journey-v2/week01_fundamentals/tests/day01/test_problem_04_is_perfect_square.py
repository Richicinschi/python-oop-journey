"""Tests for Problem 04: Is Perfect Square."""

from __future__ import annotations

from week01_fundamentals.solutions.day01.problem_04_is_perfect_square import is_perfect_square


def test_perfect_squares() -> None:
    """Test various perfect squares."""
    perfect_squares = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    for n in perfect_squares:
        assert is_perfect_square(n) is True, f"{n} should be a perfect square"


def test_non_perfect_squares() -> None:
    """Test numbers that are not perfect squares."""
    non_squares = [2, 3, 5, 6, 7, 8, 10, 15, 26, 50, 99]
    for n in non_squares:
        assert is_perfect_square(n) is False, f"{n} should not be a perfect square"


def test_zero() -> None:
    """Test zero (0² = 0)."""
    assert is_perfect_square(0) is True


def test_one() -> None:
    """Test one (1² = 1)."""
    assert is_perfect_square(1) is True


def test_negative_numbers() -> None:
    """Test negative numbers (not perfect squares)."""
    negatives = [-1, -4, -9, -16, -100]
    for n in negatives:
        assert is_perfect_square(n) is False, f"{n} should not be a perfect square"


def test_large_perfect_square() -> None:
    """Test a large perfect square."""
    assert is_perfect_square(1_000_000) is True  # 1000²
    assert is_perfect_square(9_991_921) is True  # 3161²


def test_large_non_perfect_square() -> None:
    """Test a large non-perfect square."""
    assert is_perfect_square(1_000_001) is False
