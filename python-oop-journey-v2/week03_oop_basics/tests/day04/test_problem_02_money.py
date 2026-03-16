"""Tests for Problem 02: Money."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day04.problem_02_money import Money


class TestMoneyInit:
    """Test Money initialization."""
    
    def test_init_basic(self) -> None:
        m = Money(10, 50, "USD")
        assert m.dollars == 10
        assert m.cents == 50
        assert m.currency == "USD"
    
    def test_init_currency_uppercase(self) -> None:
        m = Money(10, 0, "usd")
        assert m.currency == "USD"
    
    def test_init_with_cents_overflow(self) -> None:
        m = Money(10, 150, "USD")
        assert m.dollars == 11
        assert m.cents == 50
    
    def test_init_with_negative_cents(self) -> None:
        m = Money(10, -50, "USD")
        # 10 dollars and -50 cents = 9.50 dollars
        assert m.dollars == 9
        assert m.cents == 50  # Cents are always positive, sign is in the total


class TestMoneyAddition:
    """Test Money addition."""
    
    def test_add_same_currency(self) -> None:
        m1 = Money(10, 50, "USD")
        m2 = Money(5, 25, "USD")
        result = m1 + m2
        assert result.dollars == 15
        assert result.cents == 75
        assert result.currency == "USD"
    
    def test_add_with_cents_carry(self) -> None:
        m1 = Money(10, 75, "USD")
        m2 = Money(5, 50, "USD")
        result = m1 + m2
        assert result.dollars == 16
        assert result.cents == 25
    
    def test_add_different_currencies_raises(self) -> None:
        m1 = Money(10, 0, "USD")
        m2 = Money(5, 0, "EUR")
        with pytest.raises(ValueError, match="different currencies"):
            m1 + m2
    
    def test_add_non_money_returns_not_implemented(self) -> None:
        m = Money(10, 0, "USD")
        result = m.__add__("not money")
        assert result is NotImplemented


class TestMoneySubtraction:
    """Test Money subtraction."""
    
    def test_subtract_same_currency(self) -> None:
        m1 = Money(10, 50, "USD")
        m2 = Money(3, 25, "USD")
        result = m1 - m2
        assert result.dollars == 7
        assert result.cents == 25
    
    def test_subtract_with_borrow(self) -> None:
        m1 = Money(10, 25, "USD")
        m2 = Money(3, 50, "USD")
        result = m1 - m2
        assert result.dollars == 6
        assert result.cents == 75
    
    def test_subtract_different_currencies_raises(self) -> None:
        m1 = Money(10, 0, "USD")
        m2 = Money(5, 0, "EUR")
        with pytest.raises(ValueError, match="different currencies"):
            m1 - m2


class TestMoneyEquality:
    """Test Money equality."""
    
    def test_equal_same_value(self) -> None:
        m1 = Money(10, 50, "USD")
        m2 = Money(10, 50, "USD")
        assert m1 == m2
    
    def test_not_equal_different_value(self) -> None:
        m1 = Money(10, 50, "USD")
        m2 = Money(10, 51, "USD")
        assert m1 != m2
    
    def test_not_equal_different_currency(self) -> None:
        m1 = Money(10, 50, "USD")
        m2 = Money(10, 50, "EUR")
        assert m1 != m2
    
    def test_not_equal_non_money(self) -> None:
        m = Money(10, 50, "USD")
        assert m != "10.50"
        assert m != 10.50


class TestMoneyComparison:
    """Test Money comparison operators."""
    
    def test_less_than_true(self) -> None:
        m1 = Money(5, 0, "USD")
        m2 = Money(10, 0, "USD")
        assert m1 < m2
    
    def test_less_than_false(self) -> None:
        m1 = Money(10, 0, "USD")
        m2 = Money(5, 0, "USD")
        assert not (m1 < m2)
    
    def test_less_than_or_equal(self) -> None:
        m1 = Money(10, 0, "USD")
        m2 = Money(10, 0, "USD")
        m3 = Money(5, 0, "USD")
        assert m3 <= m1
        assert m1 <= m2
    
    def test_greater_than_true(self) -> None:
        m1 = Money(10, 0, "USD")
        m2 = Money(5, 0, "USD")
        assert m1 > m2
    
    def test_greater_than_or_equal(self) -> None:
        m1 = Money(10, 0, "USD")
        m2 = Money(10, 0, "USD")
        m3 = Money(15, 0, "USD")
        assert m3 >= m1
        assert m1 >= m2
    
    def test_comparison_different_currencies_raises(self) -> None:
        m1 = Money(10, 0, "USD")
        m2 = Money(5, 0, "EUR")
        with pytest.raises(ValueError, match="different currencies"):
            m1 < m2


class TestMoneyRepresentation:
    """Test Money string representation."""
    
    def test_repr(self) -> None:
        m = Money(10, 50, "USD")
        assert repr(m) == "Money(10, 50, 'USD')"
    
    def test_str(self) -> None:
        m = Money(10, 5, "USD")
        assert str(m) == "USD 10.05"
    
    def test_str_with_leading_zero_cents(self) -> None:
        m = Money(10, 5, "USD")
        assert str(m) == "USD 10.05"
