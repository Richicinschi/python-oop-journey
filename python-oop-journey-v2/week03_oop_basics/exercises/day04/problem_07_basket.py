"""Problem 07: Basket

Topic: Magic Methods - Container with Arithmetic Operations
Difficulty: Medium

Implement a shopping basket with collection operations and arithmetic.
"""

from __future__ import annotations

from typing import Iterator


class Item:
    """Represents an item that can be added to a basket.
    
    Attributes:
        name: The item name.
        price: The item price.
        quantity: The quantity of this item.
    """
    
    def __init__(self, name: str, price: float, quantity: int = 1) -> None:
        """Initialize an item.
        
        Args:
            name: The item name.
            price: The unit price.
            quantity: The quantity (default 1).
        """
        raise NotImplementedError("Implement __init__")
    
    def total_price(self) -> float:
        """Calculate the total price for this item (price * quantity)."""
        raise NotImplementedError("Implement total_price")
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on name and price."""
        raise NotImplementedError("Implement __eq__")
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        raise NotImplementedError("Implement __repr__")


class Basket:
    """A shopping basket supporting collection and arithmetic operations.
    
    Attributes:
        items: List of items in the basket.
    
    Example:
        >>> basket = Basket()
        >>> basket += Item("Apple", 0.50, 3)
        >>> basket += Item("Banana", 0.30, 2)
        >>> len(basket)
        2
        >>> basket.total()
        2.1
        >>> basket2 = Basket()
        >>> basket2 += Item("Orange", 0.60)
        >>> combined = basket + basket2
    """
    
    def __init__(self) -> None:
        """Initialize an empty basket."""
        raise NotImplementedError("Implement __init__")
    
    def add_item(self, item: Item) -> None:
        """Add an item to the basket.
        
        Args:
            item: The item to add.
        """
        raise NotImplementedError("Implement add_item")
    
    def __iadd__(self, item: Item) -> Basket:
        """Add an item using += operator.
        
        Args:
            item: The item to add.
        
        Returns:
            The basket itself (for chaining).
        """
        raise NotImplementedError("Implement __iadd__")
    
    def __add__(self, other: Basket) -> Basket:
        """Combine two baskets into a new basket.
        
        Args:
            other: The basket to combine with.
        
        Returns:
            A new Basket containing items from both.
        
        Raises:
            TypeError: If other is not a Basket.
        """
        raise NotImplementedError("Implement __add__")
    
    def __len__(self) -> int:
        """Return the number of distinct items (not total quantity)."""
        raise NotImplementedError("Implement __len__")
    
    def __iter__(self) -> Iterator[Item]:
        """Return an iterator over the items."""
        raise NotImplementedError("Implement __iter__")
    
    def __contains__(self, item_name: str) -> bool:
        """Check if an item with the given name is in the basket.
        
        Args:
            item_name: The name of the item to check for.
        
        Returns:
            True if any item has this name, False otherwise.
        """
        raise NotImplementedError("Implement __contains__")
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        raise NotImplementedError("Implement __repr__")
    
    def total(self) -> float:
        """Calculate the total value of all items in the basket.
        
        Returns:
            The sum of all item totals.
        """
        raise NotImplementedError("Implement total")
    
    def item_count(self) -> int:
        """Calculate the total quantity of all items.
        
        Returns:
            The sum of quantities across all items.
        """
        raise NotImplementedError("Implement item_count")
