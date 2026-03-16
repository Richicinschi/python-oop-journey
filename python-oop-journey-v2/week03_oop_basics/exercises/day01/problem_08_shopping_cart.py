"""Problem 08: Shopping Cart

Topic: Collection management, operations
Difficulty: Medium

Create a ShoppingCart class that manages items.

Examples:
    >>> cart = ShoppingCart()
    >>> cart.add_item("Apple", 1.50, 3)
    >>> cart.add_item("Banana", 0.75, 2)
    >>> cart.get_item_count()
    5
    >>> cart.get_total()
    6.0
    >>> cart.remove_item("Apple")
    True
    >>> cart.get_item_count()
    2
    >>> cart.get_items()
    [('Banana', 0.75, 2)]
    >>> cart.clear()
    >>> cart.is_empty()
    True

Requirements:
    - Items stored as tuples (name, price_per_unit, quantity)
    - add_item(name, price, quantity) adds an item
    - remove_item(name) removes item by name, returns True if found
    - get_items() returns list of all items
    - get_total() returns total cost of all items
    - get_item_count() returns total number of items (sum of quantities)
    - is_empty() returns True if cart has no items
    - clear() removes all items

Hints:
    - Hint 1: Use a dictionary to store items with name as key for O(1) lookup
    - Hint 2: Structure: __init__ creates empty dict, methods manipulate dict items
    - Hint 3: Remember to validate price >= 0 and quantity > 0 in add_item
"""

from __future__ import annotations


class ShoppingCart:
    """A class representing a shopping cart with items."""

    def __init__(self) -> None:
        """Initialize an empty shopping cart."""
        raise NotImplementedError("Initialize items storage")

    def add_item(self, name: str, price: float, quantity: int) -> None:
        """Add an item to the cart.
        
        Args:
            name: Name of the item
            price: Price per unit (must be non-negative)
            quantity: Quantity to add (must be positive)
        """
        raise NotImplementedError("Implement add_item method")

    def remove_item(self, name: str) -> bool:
        """Remove an item from the cart by name.
        
        Returns:
            True if item was found and removed, False otherwise
        """
        raise NotImplementedError("Implement remove_item method")

    def get_items(self) -> list[tuple[str, float, int]]:
        """Return a list of all items as (name, price, quantity) tuples."""
        raise NotImplementedError("Implement get_items method")

    def get_total(self) -> float:
        """Calculate and return the total cost of all items."""
        raise NotImplementedError("Implement get_total method")

    def get_item_count(self) -> int:
        """Return the total number of items (sum of quantities)."""
        raise NotImplementedError("Implement get_item_count method")

    def is_empty(self) -> bool:
        """Return True if the cart is empty."""
        raise NotImplementedError("Implement is_empty method")

    def clear(self) -> None:
        """Remove all items from the cart."""
        raise NotImplementedError("Implement clear method")

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        raise NotImplementedError("Implement __str__ method")

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        raise NotImplementedError("Implement __repr__ method")
