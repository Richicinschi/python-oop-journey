"""Problem 07: Mini TDD Refactor

Topic: Practicing Test-Driven Development workflow
Difficulty: Medium

Practice the Red-Green-Refactor cycle by implementing a shopping cart
following TDD principles.

Your task:
    1. Look at the test requirements below
    2. Write a failing test (Red)
    3. Write minimal code to make it pass (Green)
    4. Refactor while keeping tests passing (Refactor)
    5. Repeat for each feature

Features to implement:
    - Add items to cart
    - Remove items from cart
    - Calculate total price
    - Apply discount codes
    - Get item count

Example TDD cycle:
    RED: Write test_add_item_increases_count() -> fails (ShoppingCart doesn't exist)
    GREEN: Create ShoppingCart with add_item() that just increments count
    REFACTOR: Clean up implementation
    
    RED: Write test_total_price_calculated_correctly() -> fails
    GREEN: Implement price tracking
    REFACTOR: Extract helper methods if needed

Hints:
    * Hint 1: TDD is about behavior, not implementation. Write tests that
      describe WHAT the code should do, not HOW. Start with the simplest
      case - an empty cart should have 0 items and $0 total.
    
    * Hint 2: Keep the Red-Green-Refactor cycle tight:
      - Red: Write ONE test, watch it fail for the right reason
      - Green: Write MINIMAL code to pass (even hardcoded values okay!)
      - Refactor: Clean up only when tests are green
      - Then move to the next test
    
    * Hint 3: For the shopping cart data structure:
      - Dict mapping item_id -> {name, price, quantity} works well
      - add_item: update quantity if exists, else add new entry
      - remove_item: decrease quantity or remove if reaches 0
      - get_total: sum(item['price'] * item['quantity'] for all items)

Debugging Tips:
    - "Test passes immediately": Your test isn't specific enough or
      you're testing after implementation (not TDD!)
    - "Refactor broke tests": You changed behavior instead of just
      structure. Only refactor when all tests are green.
    - "Can't test private methods": Don't! Test public behavior.
      If you can't test it through public API, reconsider the design.
    - "Stuck on what to test next": Look at the method signatures
      in the class - each public method needs tests for normal case,
      edge cases, and error conditions
"""

from __future__ import annotations

from typing import Dict, Optional


class ShoppingCart:
    """A shopping cart for an e-commerce system.
    
    Implements standard cart operations:
    - Adding/removing items
    - Price calculation
    - Discount application
    """

    def __init__(self) -> None:
        """Initialize an empty shopping cart."""
        # TODO: Initialize cart state
        raise NotImplementedError("Implement __init__")

    def add_item(self, item_id: str, name: str, price: float, quantity: int = 1) -> None:
        """Add an item to the cart.

        If the item already exists, increase its quantity.

        Args:
            item_id: Unique identifier for the item.
            name: Human-readable item name.
            price: Price per unit (must be non-negative).
            quantity: Number of units to add (default 1).

        Raises:
            ValueError: If price is negative or quantity is not positive.
        """
        # TODO: Implement add_item
        raise NotImplementedError("Implement add_item")

    def remove_item(self, item_id: str, quantity: Optional[int] = None) -> None:
        """Remove an item or reduce its quantity.

        Args:
            item_id: The item to remove.
            quantity: Amount to remove (None = remove all).

        Raises:
            KeyError: If item_id is not in cart.
        """
        # TODO: Implement remove_item
        raise NotImplementedError("Implement remove_item")

    def get_item_count(self) -> int:
        """Return total number of items in cart (sum of quantities)."""
        # TODO: Implement item counting
        raise NotImplementedError("Implement get_item_count")

    def get_unique_item_count(self) -> int:
        """Return number of unique items in cart."""
        # TODO: Implement unique item counting
        raise NotImplementedError("Implement get_unique_item_count")

    def get_total(self) -> float:
        """Calculate total price of all items (before discounts)."""
        # TODO: Implement total calculation
        raise NotImplementedError("Implement get_total")

    def apply_discount(self, discount_percent: float) -> float:
        """Calculate total with discount applied.

        Args:
            discount_percent: Discount percentage (0-100).

        Returns:
            Discounted total price.

        Raises:
            ValueError: If discount_percent is not in valid range.
        """
        # TODO: Implement discount calculation
        raise NotImplementedError("Implement apply_discount")

    def is_empty(self) -> bool:
        """Return True if cart has no items."""
        # TODO: Implement empty check
        raise NotImplementedError("Implement is_empty")

    def clear(self) -> None:
        """Remove all items from cart."""
        # TODO: Implement clear
        raise NotImplementedError("Implement clear")


# TODO: Follow the TDD workflow:
#
# 1. Write a test for the simplest feature (e.g., cart starts empty)
# 2. Run the test - it should fail (Red)
# 3. Write minimal code to make it pass (Green)
# 4. Refactor if needed (Refactor)
# 5. Move to the next feature
#
# Feature order suggestion:
# - Cart starts empty
# - Can add items
# - Item count increases
# - Can get total price
# - Can add multiple of same item
# - Can remove items
# - Can apply discounts
# - Edge cases (negative prices, etc.)
