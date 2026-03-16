"""Tests for Problem 03: Count Primes."""

from __future__ import annotations

from week01_fundamentals.solutions.day05.problem_03_count_primes import count_primes


def test_count_primes_example_cases() -> None:
    assert count_primes(10) == 4  # Primes: 2, 3, 5, 7
    assert count_primes(0) == 0
    assert count_primes(1) == 0


def test_count_primes_small_values() -> None:
    assert count_primes(2) == 0  # No primes less than 2
    assert count_primes(3) == 1  # Only 2
    assert count_primes(4) == 2  # 2, 3


def test_count_primes_negative() -> None:
    assert count_primes(-5) == 0


def test_count_primes_larger_values() -> None:
    assert count_primes(100) == 25  # 25 primes less than 100
    assert count_primes(1000) == 168


def test_count_primes_prime_input() -> None:
    assert count_primes(7) == 3  # 2, 3, 5 (7 is not counted)
    assert count_primes(13) == 5  # 2, 3, 5, 7, 11
