"""Tests for Problem 05: Fraction Number."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day04.problem_05_fraction_number import FractionNumber


class TestFractionNumberInit:
    """Test FractionNumber initialization."""
    
    def test_init_basic(self) -> None:
        f = FractionNumber(1, 2)
        assert f.numerator == 1
        assert f.denominator == 2
    
    def test_init_simplifies(self) -> None:
        f = FractionNumber(2, 4)
        assert f.numerator == 1
        assert f.denominator == 2
    
    def test_init_ensures_positive_denominator(self) -> None:
        f = FractionNumber(1, -2)
        assert f.numerator == -1
        assert f.denominator == 2
    
    def test_init_negative_numerator_positive_denominator(self) -> None:
        f = FractionNumber(-3, 6)
        assert f.numerator == -1
        assert f.denominator == 2
    
    def test_init_zero_denominator_raises(self) -> None:
        with pytest.raises(ZeroDivisionError):
            FractionNumber(1, 0)


class TestFractionNumberAddition:
    """Test FractionNumber addition."""
    
    def test_add_same_denominator(self) -> None:
        f1 = FractionNumber(1, 4)
        f2 = FractionNumber(2, 4)
        result = f1 + f2
        assert result.numerator == 3
        assert result.denominator == 4
    
    def test_add_different_denominator(self) -> None:
        f1 = FractionNumber(1, 2)
        f2 = FractionNumber(1, 3)
        result = f1 + f2
        assert result.numerator == 5
        assert result.denominator == 6
    
    def test_add_simplifies_result(self) -> None:
        f1 = FractionNumber(1, 4)
        f2 = FractionNumber(1, 4)
        result = f1 + f2
        assert result.numerator == 1
        assert result.denominator == 2


class TestFractionNumberSubtraction:
    """Test FractionNumber subtraction."""
    
    def test_subtract(self) -> None:
        f1 = FractionNumber(3, 4)
        f2 = FractionNumber(1, 4)
        result = f1 - f2
        assert result.numerator == 1
        assert result.denominator == 2
    
    def test_subtract_negative_result(self) -> None:
        f1 = FractionNumber(1, 4)
        f2 = FractionNumber(3, 4)
        result = f1 - f2
        assert result.numerator == -1
        assert result.denominator == 2


class TestFractionNumberMultiplication:
    """Test FractionNumber multiplication."""
    
    def test_multiply(self) -> None:
        f1 = FractionNumber(2, 3)
        f2 = FractionNumber(3, 4)
        result = f1 * f2
        assert result.numerator == 1
        assert result.denominator == 2


class TestFractionNumberDivision:
    """Test FractionNumber division."""
    
    def test_divide(self) -> None:
        f1 = FractionNumber(1, 2)
        f2 = FractionNumber(1, 4)
        result = f1 / f2
        assert result.numerator == 2
        assert result.denominator == 1
    
    def test_divide_by_zero_raises(self) -> None:
        f1 = FractionNumber(1, 2)
        f2 = FractionNumber(0, 1)
        with pytest.raises(ZeroDivisionError):
            f1 / f2


class TestFractionNumberEquality:
    """Test FractionNumber equality."""
    
    def test_equal_same_value(self) -> None:
        f1 = FractionNumber(1, 2)
        f2 = FractionNumber(2, 4)
        assert f1 == f2
    
    def test_not_equal_different_value(self) -> None:
        f1 = FractionNumber(1, 2)
        f2 = FractionNumber(1, 3)
        assert f1 != f2
    
    def test_not_equal_non_fraction(self) -> None:
        f = FractionNumber(1, 2)
        assert f != 0.5
        assert f != "1/2"


class TestFractionNumberComparison:
    """Test FractionNumber comparison operators."""
    
    def test_less_than_true(self) -> None:
        f1 = FractionNumber(1, 3)
        f2 = FractionNumber(1, 2)
        assert f1 < f2
    
    def test_less_than_false(self) -> None:
        f1 = FractionNumber(1, 2)
        f2 = FractionNumber(1, 3)
        assert not (f1 < f2)
    
    def test_less_than_or_equal(self) -> None:
        f1 = FractionNumber(1, 2)
        f2 = FractionNumber(2, 4)
        f3 = FractionNumber(1, 3)
        assert f3 <= f1
        assert f1 <= f2
    
    def test_greater_than_true(self) -> None:
        f1 = FractionNumber(1, 2)
        f2 = FractionNumber(1, 3)
        assert f1 > f2
    
    def test_greater_than_or_equal(self) -> None:
        f1 = FractionNumber(1, 2)
        f2 = FractionNumber(2, 4)
        f3 = FractionNumber(2, 3)
        assert f3 >= f1
        assert f1 >= f2


class TestFractionNumberRepresentation:
    """Test FractionNumber string representation."""
    
    def test_repr(self) -> None:
        f = FractionNumber(1, 2)
        assert repr(f) == "FractionNumber(1, 2)"
    
    def test_str(self) -> None:
        f = FractionNumber(1, 2)
        assert str(f) == "1/2"


class TestFractionNumberToFloat:
    """Test FractionNumber conversion to float."""
    
    def test_to_float(self) -> None:
        f = FractionNumber(1, 2)
        assert f.to_float() == 0.5
    
    def test_to_float_repeating(self) -> None:
        f = FractionNumber(1, 3)
        assert abs(f.to_float() - 0.333333) < 0.0001
