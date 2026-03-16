"""Reference solution for Problem 02: Iterator Menu System."""

from __future__ import annotations

from typing import Iterator as TypingIterator


class MenuItem:
    """Represents a single menu item."""
    
    def __init__(self, name: str, price: float, category: str) -> None:
        self.name = name
        self.price = price
        self.category = category
    
    def __repr__(self) -> str:
        return f"MenuItem({self.name!r}, ${self.price:.2f}, {self.category!r})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MenuItem):
            return NotImplemented
        return (
            self.name == other.name and
            self.price == other.price and
            self.category == other.category
        )


class Menu:
    """A collection of menu items that supports different iteration strategies."""
    
    def __init__(self) -> None:
        self._items: list[MenuItem] = []
    
    def add_item(self, item: MenuItem) -> None:
        """Add an item to the menu."""
        self._items.append(item)
    
    def __iter__(self) -> MenuIterator:
        """Return a default iterator (in insertion order)."""
        return MenuIterator(self._items.copy())
    
    def by_price(self) -> PriceSortedIterator:
        """Return an iterator that yields items sorted by price."""
        return PriceSortedIterator(self._items.copy())
    
    def by_category(self, category: str) -> CategoryFilterIterator:
        """Return an iterator that yields only items of a specific category."""
        return CategoryFilterIterator(self._items.copy(), category)
    
    def __len__(self) -> int:
        """Return the number of items in the menu."""
        return len(self._items)


class MenuIterator:
    """Default iterator that yields items in insertion order."""
    
    def __init__(self, items: list[MenuItem]) -> None:
        self._items = items
        self._index = 0
    
    def __iter__(self) -> MenuIterator:
        return self
    
    def __next__(self) -> MenuItem:
        if self._index >= len(self._items):
            raise StopIteration
        item = self._items[self._index]
        self._index += 1
        return item


class PriceSortedIterator:
    """Iterator that yields items sorted by price (ascending)."""
    
    def __init__(self, items: list[MenuItem]) -> None:
        self._items = sorted(items, key=lambda x: x.price)
        self._index = 0
    
    def __iter__(self) -> PriceSortedIterator:
        return self
    
    def __next__(self) -> MenuItem:
        if self._index >= len(self._items):
            raise StopIteration
        item = self._items[self._index]
        self._index += 1
        return item


class CategoryFilterIterator:
    """Iterator that yields only items matching a specific category."""
    
    def __init__(self, items: list[MenuItem], category: str) -> None:
        self._items = items
        self._category = category
        self._index = 0
    
    def __iter__(self) -> CategoryFilterIterator:
        return self
    
    def __next__(self) -> MenuItem:
        while self._index < len(self._items):
            item = self._items[self._index]
            self._index += 1
            if item.category == self._category:
                return item
        raise StopIteration
