"""Problem 02: Iterator Menu System

Topic: Iterator Pattern
Difficulty: Medium

Implement a custom iterator for a restaurant menu system.
Create a Menu class that can be traversed in different ways using iterators.

HINTS:
- Hint 1 (Conceptual): Iterator separates traversal from collection. Multiple 
  iterators can traverse the same collection independently.
- Hint 2 (Structural): MenuIterator needs: __init__(items), __iter__(), __next__().
  Menu.__iter__() returns a new MenuIterator. Filtered iterator accepts a 
  predicate function to filter items.
- Hint 3 (Edge Case): __next__() must raise StopIteration when done. Filtered 
  iterator should skip items that don't match the predicate. Empty menu should 
  raise StopIteration immediately.
"""

from __future__ import annotations

from typing import Iterator as TypingIterator


class MenuItem:
    """Represents a single menu item."""
    
    def __init__(self, name: str, price: float, category: str) -> None:
        """Initialize a menu item.
        
        Args:
            name: Name of the menu item
            price: Price in dollars
            category: Category (e.g., 'appetizer', 'main', 'dessert', 'beverage')
        """
        raise NotImplementedError("Implement MenuItem.__init__")
    
    def __repr__(self) -> str:
        """String representation of the menu item."""
        raise NotImplementedError("Implement MenuItem.__repr__")


class Menu:
    """A collection of menu items that supports different iteration strategies."""
    
    def __init__(self) -> None:
        """Initialize an empty menu."""
        raise NotImplementedError("Implement Menu.__init__")
    
    def add_item(self, item: MenuItem) -> None:
        """Add an item to the menu."""
        raise NotImplementedError("Implement Menu.add_item")
    
    def __iter__(self) -> MenuIterator:
        """Return a default iterator (in insertion order)."""
        raise NotImplementedError("Implement Menu.__iter__")
    
    def by_price(self) -> PriceSortedIterator:
        """Return an iterator that yields items sorted by price (low to high)."""
        raise NotImplementedError("Implement Menu.by_price")
    
    def by_category(self, category: str) -> CategoryFilterIterator:
        """Return an iterator that yields only items of a specific category."""
        raise NotImplementedError("Implement Menu.by_category")
    
    def __len__(self) -> int:
        """Return the number of items in the menu."""
        raise NotImplementedError("Implement Menu.__len__")


class MenuIterator:
    """Default iterator that yields items in insertion order.
    
    Implements Python's iterator protocol.
    """
    
    def __init__(self, items: list[MenuItem]) -> None:
        """Initialize with list of menu items.
        
        Args:
            items: List of MenuItem objects to iterate over
        """
        raise NotImplementedError("Implement MenuIterator.__init__")
    
    def __iter__(self) -> MenuIterator:
        """Return self as iterator."""
        raise NotImplementedError("Implement MenuIterator.__iter__")
    
    def __next__(self) -> MenuItem:
        """Return the next menu item.
        
        Raises:
            StopIteration: When no more items
        """
        raise NotImplementedError("Implement MenuIterator.__next__")


class PriceSortedIterator:
    """Iterator that yields items sorted by price (ascending).
    
    Each iterator maintains its own sorted view independently.
    """
    
    def __init__(self, items: list[MenuItem]) -> None:
        """Initialize with items sorted by price.
        
        Args:
            items: List of MenuItem objects (will be sorted by price)
        """
        raise NotImplementedError("Implement PriceSortedIterator.__init__")
    
    def __iter__(self) -> PriceSortedIterator:
        """Return self as iterator."""
        raise NotImplementedError("Implement PriceSortedIterator.__iter__")
    
    def __next__(self) -> MenuItem:
        """Return the next menu item (in price order)."""
        raise NotImplementedError("Implement PriceSortedIterator.__next__")


class CategoryFilterIterator:
    """Iterator that yields only items matching a specific category.
    
    Skips items that don't match the target category.
    """
    
    def __init__(self, items: list[MenuItem], category: str) -> None:
        """Initialize with items and target category.
        
        Args:
            items: List of MenuItem objects to filter
            category: Category name to filter by
        """
        raise NotImplementedError("Implement CategoryFilterIterator.__init__")
    
    def __iter__(self) -> CategoryFilterIterator:
        """Return self as iterator."""
        raise NotImplementedError("Implement CategoryFilterIterator.__iter__")
    
    def __next__(self) -> MenuItem:
        """Return the next menu item matching the category.
        
        Skips non-matching items until finding one or exhausting the list.
        
        Raises:
            StopIteration: When no more matching items
        """
        raise NotImplementedError("Implement CategoryFilterIterator.__next__")
