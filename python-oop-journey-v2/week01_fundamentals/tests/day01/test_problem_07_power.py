"""Tests for Problem 07: Power."""

from __future__ import annotations

from week01_fundamentals.solutions.day01.problem_07_power import power


def test_positive_exponent() -> None:
    """Test with positive exponents."""
    assert power(2, 3) == 8
    assert power(5, 2) == 25
    assert power(3, 4) == 81


def test_zero_exponent() -> None:
    """Test with zero exponent (anything^0 = 1)."""
    assert power(5, 0) == 1
    assert power(0, 0) == 1  # Convention
    assert power(-3, 0) == 1


def test_negative_exponent() -> None:
    """Test with negative exponents."""
    assert power(2, -2) == 0.25
    assert power(5, -1) == 0.2
    assert abs(power(10, -3) - 0.001) < 1e-15


def test_base_zero() -> None:
    """Test with base zero."""
    assert power(0, 5) == 0
    assert power(0, 1) == 0
    assert power(0, 100) == 0


def test_base_one() -> None:
    """Test with base one."""
    assert power(1, 100) == 1
    assert power(1, -5) == 1


def test_negative_base() -> None:
    """Test with negative base."""
    assert power(-2, 3) == -8
    assert power(-2, 2) == 4
    assert power(-2, 4) == 16


def test_large_exponent() -> None:
    """Test with large exponents."""
    assert power(2, 10) == 1024
    assert power(2, 20) == 1048576


def test_fractional_base() -> None:
    """Test with fractional base."""
    assert power(0.5, 2) == 0.25
    assert power(0.5, 3) == 0.125
