"""Reference solution for Problem 07: Basket."""

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
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def total_price(self) -> float:
        """Calculate the total price for this item (price * quantity)."""
        return self.price * self.quantity
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on name and price."""
        if not isinstance(other, Item):
            return NotImplemented
        return self.name == other.name and self.price == other.price
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        return f"Item(name={self.name!r}, price={self.price!r}, quantity={self.quantity!r})"


class Basket:
    """A shopping basket supporting collection and arithmetic operations.
    
    Attributes:
        items: List of items in the basket.
    """
    
    def __init__(self) -> None:
        """Initialize an empty basket."""
        self._items: list[Item] = []
    
    def add_item(self, item: Item) -> None:
        """Add an item to the basket.
        
        Args:
            item: The item to add.
        """
        self._items.append(item)
    
    def __iadd__(self, item: Item) -> Basket:
        """Add an item using += operator.
        
        Args:
            item: The item to add.
        
        Returns:
            The basket itself (for chaining).
        """
        self.add_item(item)
        return self
    
    def __add__(self, other: Basket) -> Basket:
        """Combine two baskets into a new basket.
        
        Args:
            other: The basket to combine with.
        
        Returns:
            A new Basket containing items from both.
        
        Raises:
            TypeError: If other is not a Basket.
        """
        if not isinstance(other, Basket):
            return NotImplemented
        new_basket = Basket()
        for item in self._items:
            new_basket.add_item(Item(item.name, item.price, item.quantity))
        for item in other._items:
            new_basket.add_item(Item(item.name, item.price, item.quantity))
        return new_basket
    
    def __len__(self) -> int:
        """Return the number of distinct items (not total quantity)."""
        return len(self._items)
    
    def __iter__(self) -> Iterator[Item]:
        """Return an iterator over the items."""
        return iter(self._items)
    
    def __contains__(self, item_name: str) -> bool:
        """Check if an item with the given name is in the basket.
        
        Args:
            item_name: The name of the item to check for.
        
        Returns:
            True if any item has this name, False otherwise.
        """
        return any(item.name == item_name for item in self._items)
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        return f"Basket(items={self._items!r})"
    
    def total(self) -> float:
        """Calculate the total value of all items in the basket.
        
        Returns:
            The sum of all item totals.
        """
        return sum(item.total_price() for item in self._items)
    
    def item_count(self) -> int:
        """Calculate the total quantity of all items.
        
        Returns:
            The sum of quantities across all items.
        """
        return sum(item.quantity for item in self._items)
