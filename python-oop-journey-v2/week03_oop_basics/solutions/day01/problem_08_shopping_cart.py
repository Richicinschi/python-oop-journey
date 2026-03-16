"""Reference solution for Problem 08: Shopping Cart."""

from __future__ import annotations


class ShoppingCart:
    """A class representing a shopping cart with items."""

    def __init__(self) -> None:
        """Initialize an empty shopping cart."""
        self._items: dict[str, tuple[float, int]] = {}

    def add_item(self, name: str, price: float, quantity: int) -> None:
        """Add an item to the cart.
        
        Args:
            name: Name of the item
            price: Price per unit (must be non-negative)
            quantity: Quantity to add (must be positive)
        """
        if price < 0 or quantity <= 0:
            return
        self._items[name] = (price, quantity)

    def remove_item(self, name: str) -> bool:
        """Remove an item from the cart by name.
        
        Returns:
            True if item was found and removed, False otherwise
        """
        if name in self._items:
            del self._items[name]
            return True
        return False

    def get_items(self) -> list[tuple[str, float, int]]:
        """Return a list of all items as (name, price, quantity) tuples."""
        return [(name, price, qty) for name, (price, qty) in self._items.items()]

    def get_total(self) -> float:
        """Calculate and return the total cost of all items."""
        return sum(price * qty for price, qty in self._items.values())

    def get_item_count(self) -> int:
        """Return the total number of items (sum of quantities)."""
        return sum(qty for _, qty in self._items.values())

    def is_empty(self) -> bool:
        """Return True if the cart is empty."""
        return len(self._items) == 0

    def clear(self) -> None:
        """Remove all items from the cart."""
        self._items.clear()

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        item_count = self.get_item_count()
        total = self.get_total()
        return f"ShoppingCart({item_count} items, total=${total:.2f})"

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        items_list = self.get_items()
        return f"ShoppingCart(items={items_list})"
