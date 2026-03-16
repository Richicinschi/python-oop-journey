"""Tests for Problem 05: Reverse Integer."""

from __future__ import annotations

from week01_fundamentals.solutions.day01.problem_05_reverse_integer import reverse_integer


def test_positive_number() -> None:
    """Test reversing positive numbers."""
    assert reverse_integer(123) == 321
    assert reverse_integer(456) == 654


def test_negative_number() -> None:
    """Test reversing negative numbers."""
    assert reverse_integer(-456) == -654
    assert reverse_integer(-123) == -321


def test_trailing_zeros() -> None:
    """Test that trailing zeros are handled correctly."""
    assert reverse_integer(120) == 21
    assert reverse_integer(100) == 1
    assert reverse_integer(1000) == 1


def test_single_digit() -> None:
    """Test single digit numbers."""
    assert reverse_integer(5) == 5
    assert reverse_integer(0) == 0
    assert reverse_integer(-7) == -7


def test_overflow_positive() -> None:
    """Test overflow for positive numbers."""
    # 1534236469 reversed is 9646324351 > INT32_MAX
    assert reverse_integer(1534236469) == 0


def test_overflow_negative() -> None:
    """Test overflow for negative numbers."""
    # -1563847412 reversed is -2147483651 < INT32_MIN
    assert reverse_integer(-1563847412) == 0


def test_boundary_values() -> None:
    """Test values at 32-bit boundaries."""
    assert reverse_integer(1463847412) == 2147483641  # Within range
    assert reverse_integer(-1463847412) == -2147483641  # Within range


def test_ten() -> None:
    """Test the number 10."""
    assert reverse_integer(10) == 1
    assert reverse_integer(-10) == -1
