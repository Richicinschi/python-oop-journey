"""Tests for Problem 06: Comparison Ready Money."""

from __future__ import annotations
from decimal import Decimal

import pytest

from week05_oop_advanced.solutions.day04.problem_06_comparison_ready_money import (
    Money, PriceRange
)


class TestMoneyCreation:
    """Tests for Money creation."""
    
    def test_money_creation_from_cents(self) -> None:
        """Test creating Money from cents directly."""
        money = Money(amount_cents=1000, currency="USD")
        
        assert money.amount_cents == 1000
        assert money.currency == "USD"
    
    def test_money_default_currency(self) -> None:
        """Test default currency is USD."""
        money = Money(amount_cents=100)
        
        assert money.currency == "USD"
    
    def test_money_from_decimal(self) -> None:
        """Test creating Money from Decimal."""
        money = Money.from_decimal(Decimal("10.50"))
        
        assert money.amount_cents == 1050
    
    def test_money_from_float(self) -> None:
        """Test creating Money from float."""
        money = Money.from_decimal(10.50)
        
        assert money.amount_cents == 1050
    
    def test_money_from_string(self) -> None:
        """Test creating Money from string."""
        money = Money.from_decimal("10.50")
        
        assert money.amount_cents == 1050
    
    def test_money_zero(self) -> None:
        """Test creating zero Money."""
        money = Money.zero("EUR")
        
        assert money.amount_cents == 0
        assert money.currency == "EUR"
    
    def test_money_parse_simple(self) -> None:
        """Test parsing simple amount string."""
        money = Money.parse("10.50")
        
        assert money.amount_cents == 1050
    
    def test_money_parse_with_symbol(self) -> None:
        """Test parsing amount with currency symbol."""
        money = Money.parse("$10.50")
        
        assert money.amount_cents == 1050
    
    def test_money_parse_with_whitespace(self) -> None:
        """Test parsing amount with whitespace."""
        money = Money.parse("  10.50  ")
        
        assert money.amount_cents == 1050


class TestMoneyConversion:
    """Tests for Money conversion methods."""
    
    def test_to_decimal(self) -> None:
        """Test converting to Decimal."""
        money = Money(amount_cents=1050)
        
        assert money.to_decimal() == Decimal("10.50")
    
    def test_to_decimal_zero(self) -> None:
        """Test converting zero to Decimal."""
        money = Money(amount_cents=0)
        
        assert money.to_decimal() == Decimal("0")
    
    def test_format_with_symbol(self) -> None:
        """Test formatting with currency symbol."""
        money = Money.from_decimal(10.50, "USD")
        
        assert money.format() == "$10.50"
    
    def test_format_without_symbol(self) -> None:
        """Test formatting without currency symbol."""
        money = Money.from_decimal(10.50, "USD")
        
        assert money.format(symbol=False) == "10.50 USD"
    
    def test_format_euro(self) -> None:
        """Test formatting Euro currency."""
        money = Money.from_decimal(10.50, "EUR")
        
        assert "€" in money.format()


class TestMoneyArithmetic:
    """Tests for Money arithmetic operations."""
    
    def test_add_same_currency(self) -> None:
        """Test adding Money with same currency."""
        m1 = Money.from_decimal(10.00, "USD")
        m2 = Money.from_decimal(5.00, "USD")
        result = m1.add(m2)
        
        assert result.amount_cents == 1500
        assert result.currency == "USD"
    
    def test_add_different_currency_raises(self) -> None:
        """Test adding Money with different currency raises error."""
        m1 = Money.from_decimal(10.00, "USD")
        m2 = Money.from_decimal(5.00, "EUR")
        
        with pytest.raises(ValueError):
            m1.add(m2)
    
    def test_subtract_same_currency(self) -> None:
        """Test subtracting Money with same currency."""
        m1 = Money.from_decimal(10.00, "USD")
        m2 = Money.from_decimal(3.50, "USD")
        result = m1.subtract(m2)
        
        assert result.amount_cents == 650
    
    def test_subtract_different_currency_raises(self) -> None:
        """Test subtracting Money with different currency raises error."""
        m1 = Money.from_decimal(10.00, "USD")
        m2 = Money.from_decimal(5.00, "EUR")
        
        with pytest.raises(ValueError):
            m1.subtract(m2)
    
    def test_multiply_by_float(self) -> None:
        """Test multiplying by float."""
        money = Money.from_decimal(10.00, "USD")
        result = money.multiply(1.5)
        
        assert result.amount_cents == 1500
    
    def test_multiply_by_decimal(self) -> None:
        """Test multiplying by Decimal."""
        money = Money.from_decimal(10.00, "USD")
        result = money.multiply(Decimal("1.5"))
        
        assert result.amount_cents == 1500


class TestMoneyAllocation:
    """Tests for Money allocation."""
    
    def test_allocate_equal(self) -> None:
        """Test equal allocation."""
        money = Money.from_decimal(100.00, "USD")
        parts = money.allocate([1, 1])
        
        assert len(parts) == 2
        assert parts[0].amount_cents == 5000
        assert parts[1].amount_cents == 5000
    
    def test_allocate_unequal(self) -> None:
        """Test unequal allocation."""
        money = Money.from_decimal(100.00, "USD")
        parts = money.allocate([2, 1])
        
        assert len(parts) == 2
        assert parts[0].amount_cents == 6667  # Rounded
        assert parts[1].amount_cents == 3333  # Remainder
    
    def test_allocate_three_ways(self) -> None:
        """Test three-way allocation."""
        money = Money.from_decimal(100.00, "USD")
        parts = money.allocate([1, 1, 1])
        
        assert len(parts) == 3
        # Sum should equal original
        total = sum(p.amount_cents for p in parts)
        assert total == 10000
    
    def test_allocate_empty_ratios(self) -> None:
        """Test allocation with empty ratios."""
        money = Money.from_decimal(100.00, "USD")
        parts = money.allocate([])
        
        assert parts == []
    
    def test_allocate_zero_ratio(self) -> None:
        """Test allocation with zero total ratio."""
        money = Money.from_decimal(100.00, "USD")
        parts = money.allocate([0, 0])
        
        assert all(p.amount_cents == 0 for p in parts)


class TestMoneyQueries:
    """Tests for Money query methods."""
    
    def test_is_zero_true(self) -> None:
        """Test is_zero returns True for zero."""
        money = Money.zero("USD")
        
        assert money.is_zero() is True
    
    def test_is_zero_false(self) -> None:
        """Test is_zero returns False for non-zero."""
        money = Money.from_decimal(0.01, "USD")
        
        assert money.is_zero() is False
    
    def test_is_positive_true(self) -> None:
        """Test is_positive returns True for positive."""
        money = Money.from_decimal(1.00, "USD")
        
        assert money.is_positive() is True
    
    def test_is_positive_false(self) -> None:
        """Test is_positive returns False for zero/negative."""
        zero = Money.zero("USD")
        negative = Money(amount_cents=-100, currency="USD")
        
        assert zero.is_positive() is False
        assert negative.is_positive() is False
    
    def test_is_negative_true(self) -> None:
        """Test is_negative returns True for negative."""
        money = Money(amount_cents=-100, currency="USD")
        
        assert money.is_negative() is True
    
    def test_abs_positive(self) -> None:
        """Test abs on positive amount."""
        money = Money.from_decimal(10.00, "USD")
        
        assert money.abs().amount_cents == 1000
    
    def test_abs_negative(self) -> None:
        """Test abs on negative amount."""
        money = Money(amount_cents=-1000, currency="USD")
        
        assert money.abs().amount_cents == 1000
    
    def test_with_currency(self) -> None:
        """Test currency conversion."""
        usd = Money.from_decimal(100.00, "USD")
        eur = usd.with_currency("EUR", 0.85)  # 1 USD = 0.85 EUR
        
        assert eur.currency == "EUR"
        assert eur.amount_cents == 8500


class TestMoneyComparison:
    """Tests for Money comparison operators."""
    
    def test_equal_same_amount(self) -> None:
        """Test equality for same amount."""
        m1 = Money.from_decimal(10.00, "USD")
        m2 = Money.from_decimal(10.00, "USD")
        
        assert m1 == m2
    
    def test_not_equal_different_amount(self) -> None:
        """Test inequality for different amount."""
        m1 = Money.from_decimal(10.00, "USD")
        m2 = Money.from_decimal(20.00, "USD")
        
        assert m1 != m2
    
    def test_less_than(self) -> None:
        """Test less than comparison."""
        m1 = Money.from_decimal(10.00, "USD")
        m2 = Money.from_decimal(20.00, "USD")
        
        assert m1 < m2
        assert m2 > m1
    
    def test_less_than_or_equal(self) -> None:
        """Test less than or equal comparison."""
        m1 = Money.from_decimal(10.00, "USD")
        m2 = Money.from_decimal(10.00, "USD")
        m3 = Money.from_decimal(20.00, "USD")
        
        assert m1 <= m2
        assert m1 <= m3
    
    def test_sorting(self) -> None:
        """Test that Money can be sorted."""
        amounts = [
            Money.from_decimal(30.00, "USD"),
            Money.from_decimal(10.00, "USD"),
            Money.from_decimal(20.00, "USD")
        ]
        sorted_amounts = sorted(amounts)
        
        assert sorted_amounts[0].amount_cents == 1000
        assert sorted_amounts[1].amount_cents == 2000
        assert sorted_amounts[2].amount_cents == 3000


class TestPriceRange:
    """Tests for PriceRange dataclass."""
    
    def test_price_range_creation(self) -> None:
        """Test creating a price range."""
        min_price = Money.from_decimal(10.00, "USD")
        max_price = Money.from_decimal(100.00, "USD")
        
        range_obj = PriceRange(min_price=min_price, max_price=max_price)
        
        assert range_obj.min_price == min_price
        assert range_obj.max_price == max_price
    
    def test_price_range_different_currency_raises(self) -> None:
        """Test that different currencies raise error."""
        min_price = Money.from_decimal(10.00, "USD")
        max_price = Money.from_decimal(100.00, "EUR")
        
        with pytest.raises(ValueError):
            PriceRange(min_price=min_price, max_price=max_price)
    
    def test_price_range_min_greater_than_max_raises(self) -> None:
        """Test that min > max raises error."""
        min_price = Money.from_decimal(100.00, "USD")
        max_price = Money.from_decimal(10.00, "USD")
        
        with pytest.raises(ValueError):
            PriceRange(min_price=min_price, max_price=max_price)
    
    def test_contains_true(self) -> None:
        """Test that price within range is contained."""
        range_obj = PriceRange(
            min_price=Money.from_decimal(10.00, "USD"),
            max_price=Money.from_decimal(100.00, "USD")
        )
        price = Money.from_decimal(50.00, "USD")
        
        assert range_obj.contains(price) is True
    
    def test_contains_false(self) -> None:
        """Test that price outside range is not contained."""
        range_obj = PriceRange(
            min_price=Money.from_decimal(10.00, "USD"),
            max_price=Money.from_decimal(100.00, "USD")
        )
        price = Money.from_decimal(150.00, "USD")
        
        assert range_obj.contains(price) is False
    
    def test_contains_different_currency(self) -> None:
        """Test that different currency is not contained."""
        range_obj = PriceRange(
            min_price=Money.from_decimal(10.00, "USD"),
            max_price=Money.from_decimal(100.00, "USD")
        )
        price = Money.from_decimal(50.00, "EUR")
        
        assert range_obj.contains(price) is False
    
    def test_contains_boundary(self) -> None:
        """Test that boundary prices are contained."""
        range_obj = PriceRange(
            min_price=Money.from_decimal(10.00, "USD"),
            max_price=Money.from_decimal(100.00, "USD")
        )
        
        assert range_obj.contains(Money.from_decimal(10.00, "USD")) is True
        assert range_obj.contains(Money.from_decimal(100.00, "USD")) is True
    
    def test_overlaps_true(self) -> None:
        """Test that overlapping ranges overlap."""
        range1 = PriceRange(
            min_price=Money.from_decimal(10.00, "USD"),
            max_price=Money.from_decimal(100.00, "USD")
        )
        range2 = PriceRange(
            min_price=Money.from_decimal(50.00, "USD"),
            max_price=Money.from_decimal(150.00, "USD")
        )
        
        assert range1.overlaps(range2) is True
        assert range2.overlaps(range1) is True
    
    def test_overlaps_false(self) -> None:
        """Test that non-overlapping ranges don't overlap."""
        range1 = PriceRange(
            min_price=Money.from_decimal(10.00, "USD"),
            max_price=Money.from_decimal(50.00, "USD")
        )
        range2 = PriceRange(
            min_price=Money.from_decimal(100.00, "USD"),
            max_price=Money.from_decimal(200.00, "USD")
        )
        
        assert range1.overlaps(range2) is False
    
    def test_overlaps_different_currency(self) -> None:
        """Test that different currencies don't overlap."""
        range1 = PriceRange(
            min_price=Money.from_decimal(10.00, "USD"),
            max_price=Money.from_decimal(100.00, "USD")
        )
        range2 = PriceRange(
            min_price=Money.from_decimal(10.00, "EUR"),
            max_price=Money.from_decimal(100.00, "EUR")
        )
        
        assert range1.overlaps(range2) is False
    
    def test_midpoint(self) -> None:
        """Test midpoint calculation."""
        range_obj = PriceRange(
            min_price=Money.from_decimal(10.00, "USD"),
            max_price=Money.from_decimal(20.00, "USD")
        )
        
        midpoint = range_obj.midpoint()
        
        assert midpoint.amount_cents == 1500  # $15.00
        assert midpoint.currency == "USD"
    
    def test_price_range_comparison(self) -> None:
        """Test that price ranges can be compared."""
        range1 = PriceRange(
            min_price=Money.from_decimal(10.00, "USD"),
            max_price=Money.from_decimal(100.00, "USD")
        )
        range2 = PriceRange(
            min_price=Money.from_decimal(20.00, "USD"),
            max_price=Money.from_decimal(200.00, "USD")
        )
        
        assert range1 < range2  # 1000 < 2000 cents
