"""Tests for Problem 05: Is Power of Two."""

from __future__ import annotations

from week01_fundamentals.solutions.day05.problem_05_is_power_of_two import is_power_of_two


def test_is_power_of_two_positive_cases() -> None:
    assert is_power_of_two(1) is True   # 2^0
    assert is_power_of_two(2) is True   # 2^1
    assert is_power_of_two(4) is True   # 2^2
    assert is_power_of_two(8) is True   # 2^3
    assert is_power_of_two(16) is True  # 2^4
    assert is_power_of_two(1024) is True  # 2^10


def test_is_power_of_two_negative_cases() -> None:
    assert is_power_of_two(0) is False
    assert is_power_of_two(3) is False
    assert is_power_of_two(5) is False
    assert is_power_of_two(6) is False
    assert is_power_of_two(12) is False
    assert is_power_of_two(100) is False


def test_is_power_of_two_negative_numbers() -> None:
    assert is_power_of_two(-1) is False
    assert is_power_of_two(-2) is False
    assert is_power_of_two(-16) is False


def test_is_power_of_two_large() -> None:
    assert is_power_of_two(2**20) is True
    assert is_power_of_two(2**20 - 1) is False
