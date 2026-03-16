"""Tests for Problem 04: Product Price Validation."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day03.problem_04_product_price_validation import (
    Product,
)


class TestProduct:
    """Test suite for Product class."""
    
    def test_initialization(self) -> None:
        """Test product initialization."""
        product = Product("P001", "Laptop", 1000.0)
        assert product.product_id == "P001"
        assert product.name == "Laptop"
        assert product.price == 1000.0
        assert product.discount_percent == 0.0
    
    def test_initialization_strips_strings(self) -> None:
        """Test that strings are stripped."""
        product = Product("  P001  ", "  Laptop  ", 1000.0)
        assert product.product_id == "P001"
        assert product.name == "Laptop"
    
    def test_product_id_read_only(self) -> None:
        """Test that product_id is read-only."""
        product = Product("P001", "Laptop", 1000.0)
        with pytest.raises(AttributeError):
            product.product_id = "P002"  # type: ignore
    
    def test_name_getter(self) -> None:
        """Test name getter."""
        product = Product("P001", "Laptop", 1000.0)
        assert product.name == "Laptop"
    
    def test_name_setter_valid(self) -> None:
        """Test name setter with valid value."""
        product = Product("P001", "Laptop", 1000.0)
        product.name = "Desktop"
        assert product.name == "Desktop"
    
    def test_name_setter_strips(self) -> None:
        """Test name setter strips whitespace."""
        product = Product("P001", "Laptop", 1000.0)
        product.name = "  Desktop  "
        assert product.name == "Desktop"
    
    def test_name_setter_empty_raises(self) -> None:
        """Test name setter with empty value raises ValueError."""
        product = Product("P001", "Laptop", 1000.0)
        with pytest.raises(ValueError, match="empty"):
            product.name = ""
    
    def test_name_setter_non_string_raises(self) -> None:
        """Test name setter with non-string raises TypeError."""
        product = Product("P001", "Laptop", 1000.0)
        with pytest.raises(TypeError, match="string"):
            product.name = 123  # type: ignore
    
    def test_price_getter(self) -> None:
        """Test price getter."""
        product = Product("P001", "Laptop", 1000.0)
        assert product.price == 1000.0
    
    def test_price_setter_valid(self) -> None:
        """Test price setter with valid value."""
        product = Product("P001", "Laptop", 1000.0)
        product.price = 800.0
        assert product.price == 800.0
    
    def test_price_setter_zero(self) -> None:
        """Test price setter with zero."""
        product = Product("P001", "Laptop", 1000.0)
        product.price = 0.0
        assert product.price == 0.0
    
    def test_price_setter_negative_raises(self) -> None:
        """Test price setter with negative value raises ValueError."""
        product = Product("P001", "Laptop", 1000.0)
        with pytest.raises(ValueError, match="cannot be negative"):
            product.price = -100.0
    
    def test_price_setter_non_number_raises(self) -> None:
        """Test price setter with non-number raises TypeError."""
        product = Product("P001", "Laptop", 1000.0)
        with pytest.raises(TypeError, match="number"):
            product.price = "free"  # type: ignore
    
    def test_discount_percent_default(self) -> None:
        """Test discount_percent defaults to 0."""
        product = Product("P001", "Laptop", 1000.0)
        assert product.discount_percent == 0.0
    
    def test_discount_percent_setter_valid(self) -> None:
        """Test discount_percent setter with valid value."""
        product = Product("P001", "Laptop", 1000.0)
        product.discount_percent = 10.0
        assert product.discount_percent == 10.0
    
    def test_discount_percent_setter_zero(self) -> None:
        """Test discount_percent setter with zero."""
        product = Product("P001", "Laptop", 1000.0)
        product.discount_percent = 0.0
        assert product.discount_percent == 0.0
    
    def test_discount_percent_setter_max(self) -> None:
        """Test discount_percent setter at maximum."""
        product = Product("P001", "Laptop", 1000.0)
        product.discount_percent = 50.0
        assert product.discount_percent == 50.0
    
    def test_discount_percent_setter_negative_raises(self) -> None:
        """Test discount_percent setter with negative raises ValueError."""
        product = Product("P001", "Laptop", 1000.0)
        with pytest.raises(ValueError, match="between 0"):
            product.discount_percent = -10.0
    
    def test_discount_percent_setter_over_max_raises(self) -> None:
        """Test discount_percent setter over max raises ValueError."""
        product = Product("P001", "Laptop", 1000.0)
        with pytest.raises(ValueError, match="between 0"):
            product.discount_percent = 51.0
    
    def test_final_price_no_discount(self) -> None:
        """Test final_price with no discount."""
        product = Product("P001", "Laptop", 1000.0)
        assert product.final_price == 1000.0
    
    def test_final_price_with_discount(self) -> None:
        """Test final_price with discount."""
        product = Product("P001", "Laptop", 1000.0)
        product.discount_percent = 10.0
        assert product.final_price == 900.0
    
    def test_final_price_read_only(self) -> None:
        """Test that final_price is read-only."""
        product = Product("P001", "Laptop", 1000.0)
        with pytest.raises(AttributeError):
            product.final_price = 500  # type: ignore
    
    def test_discount_amount_no_discount(self) -> None:
        """Test discount_amount with no discount."""
        product = Product("P001", "Laptop", 1000.0)
        assert product.discount_amount == 0.0
    
    def test_discount_amount_with_discount(self) -> None:
        """Test discount_amount with discount."""
        product = Product("P001", "Laptop", 1000.0)
        product.discount_percent = 25.0
        assert product.discount_amount == 250.0
    
    def test_apply_discount(self) -> None:
        """Test apply_discount method."""
        product = Product("P001", "Laptop", 1000.0)
        final = product.apply_discount(20.0)
        assert final == 800.0
        assert product.discount_percent == 20.0
        assert product.final_price == 800.0
