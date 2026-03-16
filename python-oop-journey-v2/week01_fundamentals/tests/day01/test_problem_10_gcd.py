"""Tests for Problem 10: GCD."""

from __future__ import annotations

from week01_fundamentals.solutions.day01.problem_10_gcd import gcd


def test_basic_cases() -> None:
    """Test basic GCD calculations."""
    assert gcd(48, 18) == 6
    assert gcd(56, 98) == 14
    assert gcd(12, 8) == 4


def test_coprime() -> None:
    """Test coprime numbers (GCD = 1)."""
    assert gcd(17, 13) == 1
    assert gcd(100, 49) == 1


def test_one_is_multiple() -> None:
    """Test when one number is a multiple of the other."""
    assert gcd(10, 5) == 5
    assert gcd(25, 100) == 25


def test_equal_numbers() -> None:
    """Test when both numbers are equal."""
    assert gcd(42, 42) == 42
    assert gcd(7, 7) == 7


def test_zero_cases() -> None:
    """Test cases involving zero."""
    assert gcd(0, 5) == 5
    assert gcd(5, 0) == 5
    assert gcd(0, 0) == 0


def test_negative_numbers() -> None:
    """Test with negative numbers."""
    assert gcd(-48, 18) == 6
    assert gcd(48, -18) == 6
    assert gcd(-48, -18) == 6


def test_result_always_positive() -> None:
    """Ensure GCD result is always non-negative."""
    assert gcd(-48, -18) >= 0
    assert gcd(-100, -25) == 25


def test_large_numbers() -> None:
    """Test with larger numbers."""
    assert gcd(1071, 462) == 21
    assert gcd(1000000, 500000) == 500000


def test_prime_numbers() -> None:
    """Test with prime numbers."""
    assert gcd(13, 17) == 1  # Both prime, different
    assert gcd(13, 26) == 13  # One is prime factor of other
