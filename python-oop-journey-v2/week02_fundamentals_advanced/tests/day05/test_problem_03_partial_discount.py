"""Tests for Problem 03: Partial Discount."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day05.problem_03_partial_discount import (
    calculate_price,
    create_fixed_discount_calculator,
    create_standard_pricer,
    create_bulk_pricer,
)


class TestCalculatePrice:
    """Tests for calculate_price function."""

    def test_no_discount_no_tax(self) -> None:
        """Test with no discount and no tax."""
        result = calculate_price(100.0, 0.0, 0.0, 1)
        assert result == 100.0

    def test_with_discount(self) -> None:
        """Test with discount applied."""
        result = calculate_price(100.0, 0.1, 0.0, 1)
        assert result == 90.0

    def test_with_tax(self) -> None:
        """Test with tax applied."""
        result = calculate_price(100.0, 0.0, 0.08, 1)
        assert result == 108.0

    def test_with_discount_and_tax(self) -> None:
        """Test with both discount and tax."""
        result = calculate_price(100.0, 0.1, 0.08, 1)
        # 100 * 0.9 = 90, 90 * 1.08 = 97.2
        assert result == 97.2

    def test_with_quantity(self) -> None:
        """Test with multiple quantity."""
        result = calculate_price(50.0, 0.0, 0.08, 3)
        # 50 * 3 = 150, 150 * 1.08 = 162
        assert result == 162.0

    def test_complete_example(self) -> None:
        """Test complete example from docstring."""
        result = calculate_price(100.0, 0.1, 0.08, 2)
        # (100 * 0.9 * 2) * 1.08 = 194.4
        assert result == 194.4


class TestCreateFixedDiscountCalculator:
    """Tests for create_fixed_discount_calculator function."""

    def test_ten_percent_discount(self) -> None:
        """Test 10% discount calculator."""
        ten_percent_off = create_fixed_discount_calculator(0.10)
        result = ten_percent_off(100.0, 0.08, 1)
        # calculate_price(100.0, 0.10, 0.08, 1) = 97.2
        assert result == 97.2

    def test_twenty_percent_discount(self) -> None:
        """Test 20% discount calculator."""
        twenty_percent_off = create_fixed_discount_calculator(0.20)
        result = twenty_percent_off(100.0, 0.08, 1)
        # 100 * 0.8 * 1.08 = 86.4
        assert result == 86.4

    def test_no_discount(self) -> None:
        """Test 0% discount calculator."""
        no_discount = create_fixed_discount_calculator(0.0)
        result = no_discount(100.0, 0.08, 2)
        # 100 * 2 * 1.08 = 216
        assert result == 216.0

    def test_reusability(self) -> None:
        """Test that calculator can be reused."""
        fifteen_percent_off = create_fixed_discount_calculator(0.15)

        result1 = fifteen_percent_off(100.0, 0.08, 1)
        result2 = fifteen_percent_off(200.0, 0.08, 1)
        result3 = fifteen_percent_off(100.0, 0.0, 2)

        assert result1 == 91.8  # 100 * 0.85 * 1.08
        assert result2 == 183.6  # 200 * 0.85 * 1.08
        assert result3 == 170.0  # 100 * 0.85 * 2


class TestCreateStandardPricer:
    """Tests for create_standard_pricer function."""

    def test_california_tax(self) -> None:
        """Test with California-like tax rate (8%)."""
        california_price = create_standard_pricer(0.08)
        result = california_price(100.0, 0.0, 1)
        assert result == 108.0

    def test_oregon_no_tax(self) -> None:
        """Test with Oregon-like no tax."""
        oregon_price = create_standard_pricer(0.0)
        result = oregon_price(100.0, 0.10, 1)
        assert result == 90.0

    def test_high_tax_region(self) -> None:
        """Test with high tax region."""
        high_tax_price = create_standard_pricer(0.20)
        result = high_tax_price(100.0, 0.0, 1)
        assert result == 120.0

    def test_with_discount(self) -> None:
        """Test that discount parameter still works."""
        price_with_tax = create_standard_pricer(0.10)
        result = price_with_tax(100.0, 0.25, 2)
        # 100 * 0.75 * 2 * 1.10 = 165
        assert result == 165.0


class TestCreateBulkPricer:
    """Tests for create_bulk_pricer function."""

    def test_below_minimum_quantity(self) -> None:
        """Test that None is returned below minimum quantity."""
        bulk_pricer = create_bulk_pricer(10, 0.10)
        result = bulk_pricer(100.0, 0.0, 0.08, 5)
        assert result is None

    def test_at_minimum_quantity(self) -> None:
        """Test at exactly minimum quantity."""
        bulk_pricer = create_bulk_pricer(10, 0.10)
        result = bulk_pricer(100.0, 0.0, 0.0, 10)
        # 100 * (1 - 0.10) * 10 = 900
        assert result == 900.0

    def test_above_minimum_quantity(self) -> None:
        """Test above minimum quantity."""
        bulk_pricer = create_bulk_pricer(5, 0.15)
        result = bulk_pricer(100.0, 0.0, 0.0, 10)
        # 100 * (1 - 0.15) * 10 = 850
        assert result == 850.0

    def test_bulk_with_regular_discount(self) -> None:
        """Test bulk discount combined with regular discount."""
        bulk_pricer = create_bulk_pricer(5, 0.10)
        result = bulk_pricer(100.0, 0.10, 0.0, 10)
        # Total discount = 0.10 + 0.10 = 0.20
        # 100 * (1 - 0.20) * 10 = 800
        assert result == 800.0

    def test_bulk_discount_capped(self) -> None:
        """Test that total discount doesn't exceed 100%."""
        bulk_pricer = create_bulk_pricer(5, 0.60)
        result = bulk_pricer(100.0, 0.50, 0.0, 10)
        # Total discount would be 1.10, capped at 1.0
        # 100 * (1 - 1.0) * 10 = 0
        assert result == 0.0

    def test_bulk_with_tax(self) -> None:
        """Test bulk discount with tax applied."""
        bulk_pricer = create_bulk_pricer(5, 0.10)
        result = bulk_pricer(100.0, 0.0, 0.08, 10)
        # 100 * 0.90 * 10 * 1.08 = 972
        assert result == 972.0
