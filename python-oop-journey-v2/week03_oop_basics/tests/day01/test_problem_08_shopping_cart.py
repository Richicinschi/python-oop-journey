"""Tests for Problem 08: Shopping Cart."""

from __future__ import annotations

from week03_oop_basics.solutions.day01.problem_08_shopping_cart import ShoppingCart


def test_empty_cart_creation() -> None:
    """Test creating an empty cart."""
    cart = ShoppingCart()
    assert cart.is_empty() is True
    assert cart.get_total() == 0.0
    assert cart.get_item_count() == 0


def test_add_single_item() -> None:
    """Test adding a single item."""
    cart = ShoppingCart()
    cart.add_item("Apple", 1.50, 3)
    assert cart.is_empty() is False
    assert cart.get_item_count() == 3


def test_add_multiple_items() -> None:
    """Test adding multiple different items."""
    cart = ShoppingCart()
    cart.add_item("Apple", 1.50, 3)
    cart.add_item("Banana", 0.75, 2)
    assert cart.get_item_count() == 5


def test_get_total() -> None:
    """Test calculating total."""
    cart = ShoppingCart()
    cart.add_item("Apple", 1.50, 3)  # 4.50
    cart.add_item("Banana", 0.75, 2)  # 1.50
    assert cart.get_total() == 6.0


def test_remove_item_success() -> None:
    """Test removing an existing item."""
    cart = ShoppingCart()
    cart.add_item("Apple", 1.50, 3)
    result = cart.remove_item("Apple")
    assert result is True
    assert cart.is_empty() is True


def test_remove_item_failure() -> None:
    """Test removing a non-existent item."""
    cart = ShoppingCart()
    cart.add_item("Apple", 1.50, 3)
    result = cart.remove_item("Banana")
    assert result is False
    assert cart.get_item_count() == 3


def test_get_items() -> None:
    """Test getting list of items."""
    cart = ShoppingCart()
    cart.add_item("Apple", 1.50, 3)
    items = cart.get_items()
    assert len(items) == 1
    assert items[0] == ("Apple", 1.50, 3)


def test_clear_cart() -> None:
    """Test clearing the cart."""
    cart = ShoppingCart()
    cart.add_item("Apple", 1.50, 3)
    cart.add_item("Banana", 0.75, 2)
    cart.clear()
    assert cart.is_empty() is True
    assert cart.get_total() == 0.0


def test_negative_price_ignored() -> None:
    """Test that negative price items are ignored."""
    cart = ShoppingCart()
    cart.add_item("Apple", -1.50, 3)
    assert cart.is_empty() is True


def test_zero_quantity_ignored() -> None:
    """Test that zero quantity items are ignored."""
    cart = ShoppingCart()
    cart.add_item("Apple", 1.50, 0)
    assert cart.is_empty() is True


def test_negative_quantity_ignored() -> None:
    """Test that negative quantity items are ignored."""
    cart = ShoppingCart()
    cart.add_item("Apple", 1.50, -1)
    assert cart.is_empty() is True


def test_update_item() -> None:
    """Test that adding same item updates it."""
    cart = ShoppingCart()
    cart.add_item("Apple", 1.50, 3)
    cart.add_item("Apple", 2.00, 5)  # Update
    assert cart.get_item_count() == 5
    assert cart.get_total() == 10.0


def test_str_representation() -> None:
    """Test the __str__ method."""
    cart = ShoppingCart()
    cart.add_item("Apple", 1.50, 3)
    result = str(cart)
    assert "3" in result or "items" in result


def test_repr_representation() -> None:
    """Test the __repr__ method."""
    cart = ShoppingCart()
    cart.add_item("Apple", 1.50, 3)
    result = repr(cart)
    assert "ShoppingCart" in result
