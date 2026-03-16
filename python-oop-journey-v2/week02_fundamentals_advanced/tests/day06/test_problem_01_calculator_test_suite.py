"""Tests for Problem 01: Calculator Test Suite."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day06.problem_01_calculator_test_suite import (
    Calculator,
)


class TestCalculatorAdd:
    """Tests for the add method."""

    def test_add_positive_numbers(self) -> None:
        """Test adding two positive numbers."""
        calc = Calculator()
        assert calc.add(2, 3) == 5
        assert calc.add(10, 20) == 30

    def test_add_negative_numbers(self) -> None:
        """Test adding negative numbers."""
        calc = Calculator()
        assert calc.add(-2, -3) == -5
        assert calc.add(-10, 5) == -5

    def test_add_with_zero(self) -> None:
        """Test adding with zero."""
        calc = Calculator()
        assert calc.add(0, 0) == 0
        assert calc.add(5, 0) == 5
        assert calc.add(0, 5) == 5

    def test_add_floats(self) -> None:
        """Test adding floating point numbers."""
        calc = Calculator()
        result = calc.add(0.1, 0.2)
        assert abs(result - 0.3) < 1e-10  # Floating point comparison

    def test_add_large_numbers(self) -> None:
        """Test adding large numbers."""
        calc = Calculator()
        assert calc.add(1_000_000, 2_000_000) == 3_000_000


class TestCalculatorSubtract:
    """Tests for the subtract method."""

    def test_subtract_positive_numbers(self) -> None:
        """Test subtracting positive numbers."""
        calc = Calculator()
        assert calc.subtract(5, 3) == 2
        assert calc.subtract(3, 5) == -2

    def test_subtract_with_zero(self) -> None:
        """Test subtracting with zero."""
        calc = Calculator()
        assert calc.subtract(5, 0) == 5
        assert calc.subtract(0, 5) == -5


class TestCalculatorMultiply:
    """Tests for the multiply method."""

    def test_multiply_positive_numbers(self) -> None:
        """Test multiplying positive numbers."""
        calc = Calculator()
        assert calc.multiply(3, 4) == 12

    def test_multiply_with_zero(self) -> None:
        """Test multiplying by zero."""
        calc = Calculator()
        assert calc.multiply(5, 0) == 0
        assert calc.multiply(0, 5) == 0

    def test_multiply_negative_numbers(self) -> None:
        """Test multiplying with negative numbers."""
        calc = Calculator()
        assert calc.multiply(-3, 4) == -12
        assert calc.multiply(-3, -4) == 12


class TestCalculatorDivide:
    """Tests for the divide method."""

    def test_divide_positive_numbers(self) -> None:
        """Test dividing positive numbers."""
        calc = Calculator()
        assert calc.divide(10, 2) == 5.0
        assert calc.divide(7, 2) == 3.5

    def test_divide_by_one(self) -> None:
        """Test dividing by one."""
        calc = Calculator()
        assert calc.divide(5, 1) == 5.0

    def test_divide_by_zero_raises(self) -> None:
        """Test that dividing by zero raises ZeroDivisionError."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            calc.divide(10, 0)

    def test_divide_negative_numbers(self) -> None:
        """Test dividing with negative numbers."""
        calc = Calculator()
        assert calc.divide(-10, 2) == -5.0
        assert calc.divide(-10, -2) == 5.0


class TestCalculatorPower:
    """Tests for the power method."""

    def test_power_positive_exponents(self) -> None:
        """Test power with positive exponents."""
        calc = Calculator()
        assert calc.power(2, 3) == 8
        assert calc.power(5, 2) == 25

    def test_power_zero_exponent(self) -> None:
        """Test power with zero exponent."""
        calc = Calculator()
        assert calc.power(5, 0) == 1

    def test_power_negative_exponent(self) -> None:
        """Test power with negative exponent."""
        calc = Calculator()
        assert calc.power(2, -1) == 0.5


class TestCalculatorAbsolute:
    """Tests for the absolute method."""

    def test_absolute_positive(self) -> None:
        """Test absolute value of positive number."""
        calc = Calculator()
        assert calc.absolute(5) == 5

    def test_absolute_negative(self) -> None:
        """Test absolute value of negative number."""
        calc = Calculator()
        assert calc.absolute(-5) == 5

    def test_absolute_zero(self) -> None:
        """Test absolute value of zero."""
        calc = Calculator()
        assert calc.absolute(0) == 0
