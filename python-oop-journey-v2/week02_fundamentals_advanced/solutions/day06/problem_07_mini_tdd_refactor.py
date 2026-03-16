"""Reference solution for Problem 07: Mini TDD Refactor."""

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
        self._items: Dict[str, Dict[str, any]] = {}

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
        if price < 0:
            raise ValueError(f"Price cannot be negative: {price}")
        if quantity <= 0:
            raise ValueError(f"Quantity must be positive: {quantity}")

        if item_id in self._items:
            self._items[item_id]["quantity"] += quantity
        else:
            self._items[item_id] = {
                "name": name,
                "price": price,
                "quantity": quantity,
            }

    def remove_item(self, item_id: str, quantity: Optional[int] = None) -> None:
        """Remove an item or reduce its quantity.

        Args:
            item_id: The item to remove.
            quantity: Amount to remove (None = remove all).

        Raises:
            KeyError: If item_id is not in cart.
        """
        if item_id not in self._items:
            raise KeyError(f"Item '{item_id}' not in cart")

        if quantity is None:
            del self._items[item_id]
        else:
            self._items[item_id]["quantity"] -= quantity
            if self._items[item_id]["quantity"] <= 0:
                del self._items[item_id]

    def get_item_count(self) -> int:
        """Return total number of items in cart (sum of quantities)."""
        return sum(item["quantity"] for item in self._items.values())

    def get_unique_item_count(self) -> int:
        """Return number of unique items in cart."""
        return len(self._items)

    def get_total(self) -> float:
        """Calculate total price of all items (before discounts)."""
        return sum(
            item["price"] * item["quantity"]
            for item in self._items.values()
        )

    def apply_discount(self, discount_percent: float) -> float:
        """Calculate total with discount applied.

        Args:
            discount_percent: Discount percentage (0-100).

        Returns:
            Discounted total price.

        Raises:
            ValueError: If discount_percent is not in valid range.
        """
        if not (0 <= discount_percent <= 100):
            raise ValueError(f"Discount must be between 0 and 100, got {discount_percent}")

        total = self.get_total()
        discount_multiplier = (100 - discount_percent) / 100
        return total * discount_multiplier

    def is_empty(self) -> bool:
        """Return True if cart has no items."""
        return len(self._items) == 0

    def clear(self) -> None:
        """Remove all items from cart."""
        self._items.clear()
