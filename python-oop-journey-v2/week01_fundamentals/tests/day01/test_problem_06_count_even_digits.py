"""Tests for Problem 06: Count Even Digits."""

from __future__ import annotations

from week01_fundamentals.solutions.day01.problem_06_count_even_digits import count_even_digits


def test_mixed_digits() -> None:
    """Test numbers with mixed even and odd digits."""
    assert count_even_digits(12345) == 2  # 2, 4
    assert count_even_digits(13579) == 0  # None
    assert count_even_digits(24680) == 5  # All


def test_all_even_digits() -> None:
    """Test numbers with all even digits."""
    assert count_even_digits(2468) == 4
    assert count_even_digits(0) == 1
    assert count_even_digits(2222) == 4


def test_all_odd_digits() -> None:
    """Test numbers with all odd digits."""
    assert count_even_digits(13579) == 0
    assert count_even_digits(1111) == 0
    assert count_even_digits(3) == 0


def test_negative_numbers() -> None:
    """Test that negative numbers are handled correctly."""
    assert count_even_digits(-2468) == 4
    assert count_even_digits(-13579) == 0
    assert count_even_digits(-12345) == 2


def test_zero() -> None:
    """Test zero specifically."""
    assert count_even_digits(0) == 1  # 0 is even


def test_single_digit() -> None:
    """Test single digit numbers."""
    assert count_even_digits(2) == 1
    assert count_even_digits(4) == 1
    assert count_even_digits(1) == 0
    assert count_even_digits(3) == 0


def test_large_number() -> None:
    """Test with larger numbers."""
    assert count_even_digits(1234567890) == 5  # 2, 4, 6, 8, 0
    assert count_even_digits(1111111111) == 0
    assert count_even_digits(2222222222) == 10
