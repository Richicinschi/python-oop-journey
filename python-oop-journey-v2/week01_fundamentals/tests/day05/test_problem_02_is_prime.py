"""Tests for Problem 02: Is Prime."""

from __future__ import annotations

from week01_fundamentals.solutions.day05.problem_02_is_prime import is_prime


def test_is_prime_small_primes() -> None:
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(5) is True
    assert is_prime(7) is True


def test_is_prime_small_composites() -> None:
    assert is_prime(4) is False
    assert is_prime(6) is False
    assert is_prime(8) is False
    assert is_prime(9) is False


def test_is_prime_edge_cases() -> None:
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(-5) is False


def test_is_prime_larger_numbers() -> None:
    assert is_prime(97) is True
    assert is_prime(100) is False
    assert is_prime(101) is True
    assert is_prime(179) is True
    assert is_prime(200) is False


def test_is_prime_perfect_square() -> None:
    assert is_prime(49) is False  # 7 * 7
    assert is_prime(121) is False  # 11 * 11
