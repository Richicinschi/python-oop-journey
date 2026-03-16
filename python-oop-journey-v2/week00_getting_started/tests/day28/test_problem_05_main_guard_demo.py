"""Tests for Problem 05: Main Guard Pattern Module."""

from __future__ import annotations

from week00_getting_started.solutions.day28.problem_05_main_guard_demo import (
    double,
    power,
    square,
    triple,
)


def test_double_positive() -> None:
    """Test double with positive numbers."""
    assert double(5) == 10
    assert double(3) == 6


def test_double_negative() -> None:
    """Test double with negative numbers."""
    assert double(-4) == -8
    assert double(-1) == -2


def test_double_zero() -> None:
    """Test double with zero."""
    assert double(0) == 0


def test_double_floats() -> None:
    """Test double with floats."""
    assert double(2.5) == 5.0


def test_triple_positive() -> None:
    """Test triple with positive numbers."""
    assert triple(3) == 9
    assert triple(4) == 12


def test_triple_negative() -> None:
    """Test triple with negative numbers."""
    assert triple(-3) == -9


def test_triple_zero() -> None:
    """Test triple with zero."""
    assert triple(0) == 0


def test_square_positive() -> None:
    """Test square with positive numbers."""
    assert square(4) == 16
    assert square(5) == 25


def test_square_negative() -> None:
    """Test square with negative numbers (result is positive)."""
    assert square(-4) == 16
    assert square(-5) == 25


def test_square_zero() -> None:
    """Test square with zero."""
    assert square(0) == 0


def test_power_positive_base_positive_exp() -> None:
    """Test power with positive base and exponent."""
    assert power(2, 3) == 8
    assert power(3, 2) == 9
    assert power(2, 8) == 256


def test_power_zero_exponent() -> None:
    """Test power with zero exponent (any number^0 = 1)."""
    assert power(5, 0) == 1
    assert power(100, 0) == 1


def test_power_one_exponent() -> None:
    """Test power with exponent of 1."""
    assert power(5, 1) == 5
    assert power(100, 1) == 100


def test_power_negative_base() -> None:
    """Test power with negative base."""
    assert power(-2, 3) == -8
    assert power(-2, 2) == 4
