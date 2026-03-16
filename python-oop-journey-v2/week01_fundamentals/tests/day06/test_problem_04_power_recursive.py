"""Tests for Problem 04: Power Recursive."""

from __future__ import annotations

from week01_fundamentals.solutions.day06.problem_04_power_recursive import power


def test_power_zero_exponent() -> None:
    """Test x^0 = 1 for any x."""
    assert power(2, 0) == 1.0
    assert power(5, 0) == 1.0
    assert power(0, 0) == 1.0


def test_power_positive_exponent() -> None:
    """Test positive exponents."""
    assert power(2, 3) == 8.0
    assert power(3, 4) == 81.0
    assert power(5, 2) == 25.0
    assert power(10, 5) == 100000.0


def test_power_one_exponent() -> None:
    """Test x^1 = x."""
    assert power(7, 1) == 7.0
    assert power(42, 1) == 42.0


def test_power_negative_exponent() -> None:
    """Test negative exponents."""
    assert power(2, -1) == 0.5
    assert power(2, -2) == 0.25
    assert power(2, -3) == 0.125
    assert power(10, -2) == 0.01


def test_power_fractional_base() -> None:
    """Test with fractional base."""
    assert power(0.5, 2) == 0.25
    assert power(0.5, 3) == 0.125


def test_power_large_exponent() -> None:
    """Test with larger exponents (efficiency check)."""
    assert power(2, 10) == 1024.0
    assert power(2, 20) == 1048576.0
