"""Tests for Problem 04: Shopping Cart Refactor."""

from __future__ import annotations

import pytest

from week07_real_world.solutions.day03.problem_04_shopping_cart_refactor import (
    Product,
    LineItem,
    ShoppingCart,
    create_cart_procedural,
    add_to_cart_procedural,
    remove_from_cart_procedural,
    update_quantity_procedural,
    get_cart_summary_procedural,
    format_cart_procedural,
)


class TestProduct:
    """Tests for Product value object."""
    
    def test_creation(self) -> None:
        product = Product("SKU123", "Widget", 29.99)
        assert product.sku == "SKU123"
        assert product.name == "Widget"
        assert product.price == 29.99
    
    def test_negative_price_raises(self) -> None:
        with pytest.raises(ValueError, match="Price cannot be negative"):
            Product("SKU123", "Widget", -10.0)
    
    def test_zero_price_allowed(self) -> None:
        product = Product("FREE", "Free Item", 0.0)
        assert product.price == 0.0
    
    def test_immutable(self) -> None:
        product = Product("SKU123", "Widget", 29.99)
        with pytest.raises(AttributeError):
            product.price = 19.99


class TestLineItem:
    """Tests for LineItem."""
    
    def test_creation(self) -> None:
        product = Product("SKU123", "Widget", 29.99)
        item = LineItem(product, 2)
        
        assert item.product == product
        assert item.quantity == 2
    
    def test_zero_quantity_raises(self) -> None:
        product = Product("SKU123", "Widget", 29.99)
        with pytest.raises(ValueError, match="Quantity must be positive"):
            LineItem(product, 0)
    
    def test_negative_quantity_raises(self) -> None:
        product = Product("SKU123", "Widget", 29.99)
        with pytest.raises(ValueError, match="Quantity must be positive"):
            LineItem(product, -1)
    
    def test_line_total_calculation(self) -> None:
        product = Product("SKU123", "Widget", 29.99)
        item = LineItem(product, 3)
        
        assert item.line_total == pytest.approx(89.97)
    
    def test_update_quantity_returns_new_item(self) -> None:
        product = Product("SKU123", "Widget", 29.99)
        item = LineItem(product, 2)
        new_item = item.update_quantity(5)
        
        assert new_item.quantity == 5
        assert item.quantity == 2  # Original unchanged
    
    def test_str_formatting(self) -> None:
        product = Product("SKU123", "Widget", 29.99)
        item = LineItem(product, 2)
        
        result = str(item)
        assert "SKU123" in result
        assert "Widget" in result
        assert "2 x $29.99" in result
        assert "$59.98" in result


class TestShoppingCart:
    """Tests for ShoppingCart."""
    
    def test_init_empty(self) -> None:
        cart = ShoppingCart()
        assert cart.item_count == 0
        assert cart.total_quantity == 0
        assert cart.subtotal == 0.0
        assert cart.tax == 0.0
        assert cart.total == 0.0
        assert cart.items == ()
    
    def test_add_item_new(self) -> None:
        cart = ShoppingCart()
        result = cart.add_item("SKU123", "Widget", 29.99, 2)
        
        assert result is cart  # Returns self
        assert cart.item_count == 1
        assert cart.total_quantity == 2
        assert cart.subtotal == pytest.approx(59.98)
    
    def test_add_item_existing_increments_quantity(self) -> None:
        cart = ShoppingCart()
        cart.add_item("SKU123", "Widget", 29.99, 2)
        cart.add_item("SKU123", "Widget", 29.99, 3)
        
        assert cart.item_count == 1  # Still one unique SKU
        assert cart.total_quantity == 5
        assert cart.subtotal == pytest.approx(149.95)
    
    def test_add_item_chaining(self) -> None:
        cart = ShoppingCart()
        cart.add_item("A", "Item A", 10.0, 1).add_item("B", "Item B", 20.0, 2)
        
        assert cart.item_count == 2
        assert cart.subtotal == pytest.approx(50.0)
    
    def test_remove_item_success(self) -> None:
        cart = ShoppingCart()
        cart.add_item("SKU123", "Widget", 29.99, 2)
        result = cart.remove_item("SKU123")
        
        assert result is True
        assert cart.item_count == 0
    
    def test_remove_item_not_found(self) -> None:
        cart = ShoppingCart()
        result = cart.remove_item("NOTEXIST")
        
        assert result is False
    
    def test_update_quantity_success(self) -> None:
        cart = ShoppingCart()
        cart.add_item("SKU123", "Widget", 29.99, 2)
        result = cart.update_quantity("SKU123", 5)
        
        assert result is True
        item = cart.get_line_item("SKU123")
        assert item is not None
        assert item.quantity == 5
    
    def test_update_quantity_to_zero_removes(self) -> None:
        cart = ShoppingCart()
        cart.add_item("SKU123", "Widget", 29.99, 2)
        cart.update_quantity("SKU123", 0)
        
        assert cart.item_count == 0
        assert cart.has_item("SKU123") is False
    
    def test_update_quantity_negative_raises(self) -> None:
        cart = ShoppingCart()
        cart.add_item("SKU123", "Widget", 29.99, 2)
        
        with pytest.raises(ValueError, match="Quantity cannot be negative"):
            cart.update_quantity("SKU123", -1)
    
    def test_update_quantity_not_found(self) -> None:
        cart = ShoppingCart()
        result = cart.update_quantity("NOTEXIST", 5)
        
        assert result is False
    
    def test_clear(self) -> None:
        cart = ShoppingCart()
        cart.add_item("A", "Item A", 10.0, 1)
        cart.add_item("B", "Item B", 20.0, 2)
        result = cart.clear()
        
        assert result is cart  # Returns self
        assert cart.item_count == 0
        assert cart.subtotal == 0.0
    
    def test_has_item(self) -> None:
        cart = ShoppingCart()
        cart.add_item("SKU123", "Widget", 29.99, 2)
        
        assert cart.has_item("SKU123") is True
        assert cart.has_item("NOTEXIST") is False
    
    def test_get_line_item(self) -> None:
        cart = ShoppingCart()
        cart.add_item("SKU123", "Widget", 29.99, 2)
        
        item = cart.get_line_item("SKU123")
        assert item is not None
        assert item.product.sku == "SKU123"
        assert item.product.name == "Widget"
        
        assert cart.get_line_item("NOTEXIST") is None
    
    def test_items_immutable(self) -> None:
        cart = ShoppingCart()
        cart.add_item("SKU123", "Widget", 29.99, 2)
        
        items = cart.items
        assert isinstance(items, tuple)
        with pytest.raises(TypeError):
            items[0] = None  # type: ignore
    
    def test_tax_calculation(self) -> None:
        cart = ShoppingCart()
        cart.add_item("SKU123", "Widget", 100.0, 1)
        
        assert cart.subtotal == 100.0
        assert cart.tax == 8.0  # 8%
        assert cart.total == 108.0
    
    def test_get_summary(self) -> None:
        cart = ShoppingCart()
        cart.add_item("SKU123", "Widget", 100.0, 2)
        
        summary = cart.get_summary()
        
        assert summary["item_count"] == 1
        assert summary["total_quantity"] == 2
        assert summary["subtotal"] == 200.0
        assert summary["tax"] == 16.0
        assert summary["total"] == 216.0
    
    def test_format(self) -> None:
        cart = ShoppingCart()
        cart.add_item("SKU123", "Widget", 29.99, 2)
        
        formatted = cart.format()
        
        assert "Shopping Cart:" in formatted
        assert "SKU123" in formatted
        assert "Widget" in formatted
        assert "Subtotal:" in formatted
        assert "Tax (8%):" in formatted
        assert "Total:" in formatted
    
    def test_str_delegates_to_format(self) -> None:
        cart = ShoppingCart()
        assert str(cart) == cart.format()
    
    def test_len_returns_item_count(self) -> None:
        cart = ShoppingCart()
        assert len(cart) == 0
        
        cart.add_item("A", "Item", 10.0, 1)
        assert len(cart) == 1
    
    def test_bool_returns_true_with_items(self) -> None:
        cart = ShoppingCart()
        assert bool(cart) is False
        
        cart.add_item("A", "Item", 10.0, 1)
        assert bool(cart) is True


class TestProceduralCompatibility:
    """Tests comparing procedural and OOP results."""
    
    def test_add_item_behavior(self) -> None:
        # Procedural
        proc_cart = create_cart_procedural()
        add_to_cart_procedural(proc_cart, "SKU123", "Widget", 29.99, 2)
        
        # OOP
        oop_cart = ShoppingCart()
        oop_cart.add_item("SKU123", "Widget", 29.99, 2)
        
        assert proc_cart["subtotal"] == pytest.approx(oop_cart.subtotal)
    
    def test_multiple_items_behavior(self) -> None:
        # Procedural
        proc_cart = create_cart_procedural()
        add_to_cart_procedural(proc_cart, "A", "Item A", 10.0, 1)
        add_to_cart_procedural(proc_cart, "B", "Item B", 20.0, 2)
        
        # OOP
        oop_cart = ShoppingCart()
        oop_cart.add_item("A", "Item A", 10.0, 1)
        oop_cart.add_item("B", "Item B", 20.0, 2)
        
        assert proc_cart["total"] == pytest.approx(oop_cart.total)
    
    def test_add_existing_item_behavior(self) -> None:
        # Procedural
        proc_cart = create_cart_procedural()
        add_to_cart_procedural(proc_cart, "SKU123", "Widget", 29.99, 2)
        add_to_cart_procedural(proc_cart, "SKU123", "Widget", 29.99, 3)
        
        # OOP
        oop_cart = ShoppingCart()
        oop_cart.add_item("SKU123", "Widget", 29.99, 2)
        oop_cart.add_item("SKU123", "Widget", 29.99, 3)
        
        assert proc_cart["subtotal"] == pytest.approx(oop_cart.subtotal)
    
    def test_remove_item_behavior(self) -> None:
        # Procedural
        proc_cart = create_cart_procedural()
        add_to_cart_procedural(proc_cart, "SKU123", "Widget", 29.99, 2)
        remove_from_cart_procedural(proc_cart, "SKU123")
        
        # OOP
        oop_cart = ShoppingCart()
        oop_cart.add_item("SKU123", "Widget", 29.99, 2)
        oop_cart.remove_item("SKU123")
        
        assert len(proc_cart["items"]) == oop_cart.item_count
    
    def test_update_quantity_behavior(self) -> None:
        # Procedural
        proc_cart = create_cart_procedural()
        add_to_cart_procedural(proc_cart, "SKU123", "Widget", 29.99, 2)
        update_quantity_procedural(proc_cart, "SKU123", 5)
        
        # OOP
        oop_cart = ShoppingCart()
        oop_cart.add_item("SKU123", "Widget", 29.99, 2)
        oop_cart.update_quantity("SKU123", 5)
        
        assert proc_cart["subtotal"] == pytest.approx(oop_cart.subtotal)
    
    def test_summary_behavior(self) -> None:
        # Procedural
        proc_cart = create_cart_procedural()
        add_to_cart_procedural(proc_cart, "A", "Item A", 10.0, 1)
        add_to_cart_procedural(proc_cart, "B", "Item B", 20.0, 2)
        proc_summary = get_cart_summary_procedural(proc_cart)
        
        # OOP
        oop_cart = ShoppingCart()
        oop_cart.add_item("A", "Item A", 10.0, 1)
        oop_cart.add_item("B", "Item B", 20.0, 2)
        oop_summary = oop_cart.get_summary()
        
        assert proc_summary["item_count"] == oop_summary["item_count"]
        assert proc_summary["total_quantity"] == oop_summary["total_quantity"]
        assert proc_summary["subtotal"] == pytest.approx(oop_summary["subtotal"])
