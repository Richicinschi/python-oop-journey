"""Tests for Problem 02: Calculate Total Price."""

from __future__ import annotations

from week00_getting_started.solutions.day17.problem_02_calculate_total_price import calculate_total_price


def test_basic_price_only() -> None:
    """Test with just price and quantity, no tax or discount."""
    assert calculate_total_price(10.0, 5) == 50.0
    assert calculate_total_price(25.0, 2) == 50.0


def test_with_tax_only() -> None:
    """Test with tax but no discount."""
    # $100 + 8% tax = $108
    assert calculate_total_price(100.0, 1, tax_rate=0.08) == 108.0
    # $50 + 10% tax = $55
    assert calculate_total_price(25.0, 2, tax_rate=0.10) == 55.0


def test_with_discount_only() -> None:
    """Test with discount but no tax."""
    # $100 - 10% discount = $90
    assert calculate_total_price(100.0, 1, discount=0.10) == 90.0
    # $200 - 25% discount = $150
    assert calculate_total_price(50.0, 4, discount=0.25) == 150.0


def test_with_tax_and_discount() -> None:
    """Test with both tax and discount."""
    # $100 - 10% = $90, then + 8% tax = $97.20
    result = calculate_total_price(100.0, 1, tax_rate=0.08, discount=0.10)
    assert result == 97.2


def test_zero_quantity() -> None:
    """Test with zero quantity."""
    assert calculate_total_price(100.0, 0, tax_rate=0.08, discount=0.10) == 0.0


def test_with_default_parameters() -> None:
    """Test using all default optional parameters."""
    assert calculate_total_price(10.0, 3) == 30.0
