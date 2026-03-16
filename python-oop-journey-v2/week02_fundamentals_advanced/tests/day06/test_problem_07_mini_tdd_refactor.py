"""Tests for Problem 07: Mini TDD Refactor.

These tests demonstrate a TDD-style approach to testing a shopping cart.
The tests are organized to reflect the Red-Green-Refactor workflow.
"""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day06.problem_07_mini_tdd_refactor import (
    ShoppingCart,
)


class TestCartInitialization:
    """Tests for cart creation - Step 1: Cart starts empty."""

    def test_new_cart_is_empty(self) -> None:
        """RED: Cart should start empty. GREEN: Implement empty check."""
        cart = ShoppingCart()
        assert cart.is_empty() is True

    def test_new_cart_has_zero_items(self) -> None:
        """RED: New cart has 0 items. GREEN: Implement count."""
        cart = ShoppingCart()
        assert cart.get_item_count() == 0

    def test_new_cart_has_zero_total(self) -> None:
        """RED: New cart has $0 total. GREEN: Implement total."""
        cart = ShoppingCart()
        assert cart.get_total() == 0.0


class TestAddItem:
    """Tests for adding items - Step 2: Can add items."""

    def test_add_item_increases_count(self) -> None:
        """RED: Adding item increases count. GREEN: Implement add_item."""
        cart = ShoppingCart()
        cart.add_item("item1", "Test Item", 10.00)
        assert cart.get_item_count() == 1

    def test_add_item_updates_total(self) -> None:
        """RED: Total updates when item added. GREEN: Calculate total."""
        cart = ShoppingCart()
        cart.add_item("item1", "Test Item", 10.00)
        assert cart.get_total() == 10.00

    def test_add_item_makes_cart_not_empty(self) -> None:
        """Cart is no longer empty after adding item."""
        cart = ShoppingCart()
        cart.add_item("item1", "Test Item", 10.00)
        assert cart.is_empty() is False

    def test_add_multiple_items_increases_count(self) -> None:
        """RED: Can add multiple items. GREEN: Support multiple items."""
        cart = ShoppingCart()
        cart.add_item("item1", "Item 1", 10.00)
        cart.add_item("item2", "Item 2", 20.00)
        assert cart.get_item_count() == 2

    def test_add_multiple_items_updates_total(self) -> None:
        """Total reflects sum of all items."""
        cart = ShoppingCart()
        cart.add_item("item1", "Item 1", 10.00)
        cart.add_item("item2", "Item 2", 20.00)
        assert cart.get_total() == 30.00

    def test_add_same_item_increases_quantity(self) -> None:
        """RED: Adding same item increases quantity. GREEN: Track quantities."""
        cart = ShoppingCart()
        cart.add_item("item1", "Test Item", 10.00, quantity=2)
        cart.add_item("item1", "Test Item", 10.00, quantity=3)
        assert cart.get_item_count() == 5

    def test_add_negative_price_raises(self) -> None:
        """RED: Handle invalid price. GREEN: Add validation."""
        cart = ShoppingCart()
        with pytest.raises(ValueError, match="cannot be negative"):
            cart.add_item("item1", "Test Item", -10.00)

    def test_add_zero_quantity_raises(self) -> None:
        """RED: Handle invalid quantity. GREEN: Add validation."""
        cart = ShoppingCart()
        with pytest.raises(ValueError, match="must be positive"):
            cart.add_item("item1", "Test Item", 10.00, quantity=0)


class TestRemoveItem:
    """Tests for removing items - Step 3: Can remove items."""

    @pytest.fixture
    def cart_with_items(self) -> ShoppingCart:
        """Fixture: Cart with some items."""
        cart = ShoppingCart()
        cart.add_item("item1", "Item 1", 10.00)
        cart.add_item("item2", "Item 2", 20.00)
        return cart

    def test_remove_item_decreases_count(self, cart_with_items: ShoppingCart) -> None:
        """RED: Removing item decreases count. GREEN: Implement remove."""
        cart_with_items.remove_item("item1")
        assert cart_with_items.get_item_count() == 1

    def test_remove_item_updates_total(self, cart_with_items: ShoppingCart) -> None:
        """Total updates when item removed."""
        cart_with_items.remove_item("item1")
        assert cart_with_items.get_total() == 20.00

    def test_remove_all_items_makes_empty(self, cart_with_items: ShoppingCart) -> None:
        """Cart is empty when all items removed."""
        cart_with_items.remove_item("item1")
        cart_with_items.remove_item("item2")
        assert cart_with_items.is_empty() is True

    def test_remove_nonexistent_item_raises(self) -> None:
        """RED: Handle removing nonexistent item. GREEN: Add validation."""
        cart = ShoppingCart()
        with pytest.raises(KeyError, match="not in cart"):
            cart.remove_item("nonexistent")

    def test_remove_partial_quantity(self) -> None:
        """RED: Can remove partial quantity. GREEN: Support partial removal."""
        cart = ShoppingCart()
        cart.add_item("item1", "Test Item", 10.00, quantity=5)
        cart.remove_item("item1", quantity=2)
        assert cart.get_item_count() == 3

    def test_remove_all_quantity_removes_item(self) -> None:
        """Removing all quantity removes the item entirely."""
        cart = ShoppingCart()
        cart.add_item("item1", "Test Item", 10.00, quantity=3)
        cart.remove_item("item1", quantity=3)
        assert cart.get_unique_item_count() == 0


class TestDiscount:
    """Tests for discounts - Step 4: Can apply discounts."""

    @pytest.fixture
    def cart_with_100_total(self) -> ShoppingCart:
        """Fixture: Cart with $100 total."""
        cart = ShoppingCart()
        cart.add_item("item1", "Expensive Item", 100.00)
        return cart

    def test_apply_discount_reduces_total(self, cart_with_100_total: ShoppingCart) -> None:
        """RED: Discount reduces total. GREEN: Implement discount."""
        discounted = cart_with_100_total.apply_discount(10)  # 10% off
        assert discounted == 90.00

    def test_apply_zero_discount(self, cart_with_100_total: ShoppingCart) -> None:
        """0% discount means no change."""
        discounted = cart_with_100_total.apply_discount(0)
        assert discounted == 100.00

    def test_apply_full_discount(self, cart_with_100_total: ShoppingCart) -> None:
        """100% discount means free."""
        discounted = cart_with_100_total.apply_discount(100)
        assert discounted == 0.00

    def test_invalid_discount_negative(self, cart_with_100_total: ShoppingCart) -> None:
        """RED: Handle invalid discount. GREEN: Add validation."""
        with pytest.raises(ValueError, match="between 0 and 100"):
            cart_with_100_total.apply_discount(-10)

    def test_invalid_discount_over_100(self, cart_with_100_total: ShoppingCart) -> None:
        """Discount over 100% is invalid."""
        with pytest.raises(ValueError, match="between 0 and 100"):
            cart_with_100_total.apply_discount(110)

    def test_discount_on_empty_cart(self) -> None:
        """Discount on empty cart is $0."""
        cart = ShoppingCart()
        assert cart.apply_discount(50) == 0.00


class TestClearCart:
    """Tests for clearing cart - Step 5: Can clear cart."""

    @pytest.fixture
    def full_cart(self) -> ShoppingCart:
        """Fixture: Cart with multiple items."""
        cart = ShoppingCart()
        cart.add_item("item1", "Item 1", 10.00, quantity=2)
        cart.add_item("item2", "Item 2", 20.00)
        return cart

    def test_clear_removes_all_items(self, full_cart: ShoppingCart) -> None:
        """RED: Can clear cart. GREEN: Implement clear."""
        full_cart.clear()
        assert full_cart.is_empty() is True

    def test_clear_resets_count(self, full_cart: ShoppingCart) -> None:
        """Clear resets item count to 0."""
        full_cart.clear()
        assert full_cart.get_item_count() == 0

    def test_clear_resets_total(self, full_cart: ShoppingCart) -> None:
        """Clear resets total to $0."""
        full_cart.clear()
        assert full_cart.get_total() == 0.00


class TestUniqueItemCount:
    """Tests for unique item counting - Step 6: Track unique items."""

    def test_empty_cart_has_zero_unique(self) -> None:
        """Empty cart has 0 unique items."""
        cart = ShoppingCart()
        assert cart.get_unique_item_count() == 0

    def test_single_item_is_one_unique(self) -> None:
        """One item type means 1 unique."""
        cart = ShoppingCart()
        cart.add_item("item1", "Item 1", 10.00)
        assert cart.get_unique_item_count() == 1

    def test_multiple_different_items(self) -> None:
        """Multiple different items count as unique."""
        cart = ShoppingCart()
        cart.add_item("item1", "Item 1", 10.00)
        cart.add_item("item2", "Item 2", 20.00)
        assert cart.get_unique_item_count() == 2

    def test_same_item_different_quantity(self) -> None:
        """Same item with different quantity is still 1 unique."""
        cart = ShoppingCart()
        cart.add_item("item1", "Item 1", 10.00, quantity=5)
        assert cart.get_unique_item_count() == 1


class TestCartEdgeCases:
    """Edge case tests - Step 7: Handle edge cases."""

    def test_float_prices(self) -> None:
        """Cart handles float prices correctly."""
        cart = ShoppingCart()
        cart.add_item("item1", "Item 1", 9.99)
        cart.add_item("item2", "Item 2", 19.99)
        total = cart.get_total()
        assert abs(total - 29.98) < 0.001

    def test_very_large_quantity(self) -> None:
        """Cart handles large quantities."""
        cart = ShoppingCart()
        cart.add_item("item1", "Item 1", 1.00, quantity=10000)
        assert cart.get_item_count() == 10000

    def test_price_zero_is_valid(self) -> None:
        """Price of 0 is valid (free item)."""
        cart = ShoppingCart()
        cart.add_item("free", "Free Item", 0.00)
        assert cart.get_total() == 0.00

    def test_rounding_in_discount(self) -> None:
        """Discount calculation handles rounding."""
        cart = ShoppingCart()
        cart.add_item("item1", "Item 1", 33.33)
        discounted = cart.apply_discount(33.333)
        # Should be approximately 22.22
        assert abs(discounted - 22.22) < 0.01


class TestTDDWorkflowDemonstration:
    """Tests demonstrating the TDD workflow explicitly."""

    def test_red_green_refactor_example(self) -> None:
        """
        Demonstrates the TDD cycle:
        
        RED: Write this test first (it will fail because feature doesn't exist)
        GREEN: Implement just enough code to make it pass
        REFACTOR: Clean up the implementation while keeping test passing
        """
        # This test represents what you'd write first in TDD
        cart = ShoppingCart()
        
        # Add some items
        cart.add_item("apple", "Apple", 0.50, quantity=3)
        cart.add_item("banana", "Banana", 0.30, quantity=2)
        
        # Verify state
        assert cart.get_unique_item_count() == 2
        assert cart.get_item_count() == 5
        assert cart.get_total() == 2.10  # 3*0.50 + 2*0.30
        
        # Apply discount
        final_price = cart.apply_discount(10)
        # 10% off of 2.10 = 1.89, use approximate comparison for floats
        assert abs(final_price - 1.89) < 0.001
