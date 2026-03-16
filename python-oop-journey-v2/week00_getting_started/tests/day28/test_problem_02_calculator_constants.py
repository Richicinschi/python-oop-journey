"""Tests for Problem 02: Calculator Module with Constants."""

from __future__ import annotations

from week00_getting_started.solutions.day28.problem_02_calculator_constants import (
    E,
    GOLDEN_RATIO,
    PI,
    add,
    circle_area,
    divide,
    multiply,
    subtract,
)


def test_pi_constant() -> None:
    """Test PI constant value."""
    assert PI == 3.14159


def test_e_constant() -> None:
    """Test E constant value."""
    assert E == 2.71828


def test_golden_ratio_constant() -> None:
    """Test GOLDEN_RATIO constant value."""
    assert GOLDEN_RATIO == 1.61803


def test_add_positive_numbers() -> None:
    """Test add with positive numbers."""
    assert add(5, 3) == 8
    assert add(10, 20) == 30


def test_add_negative_numbers() -> None:
    """Test add with negative numbers."""
    assert add(-5, 3) == -2
    assert add(-5, -3) == -8


def test_add_floats() -> None:
    """Test add with floats."""
    assert add(2.5, 3.5) == 6.0


def test_subtract() -> None:
    """Test subtract function."""
    assert subtract(10, 3) == 7
    assert subtract(5, 10) == -5
    assert subtract(2.5, 1.5) == 1.0


def test_multiply() -> None:
    """Test multiply function."""
    assert multiply(4, 5) == 20
    assert multiply(-3, 4) == -12
    assert multiply(2.5, 2) == 5.0


def test_divide_normal() -> None:
    """Test divide with valid divisor."""
    assert divide(10, 2) == 5.0
    assert divide(7, 2) == 3.5


def test_divide_by_zero() -> None:
    """Test divide returns None for division by zero."""
    assert divide(10, 0) is None


def test_circle_area() -> None:
    """Test circle_area function."""
    # Area = PI * r^2
    assert round(circle_area(1), 5) == round(PI, 5)
    assert round(circle_area(2), 5) == 12.56636
    assert round(circle_area(0), 5) == 0.0
