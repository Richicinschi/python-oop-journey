"""Reference solution for Problem 03: Paginated Collection."""

from __future__ import annotations
from typing import Iterator


class PaginatedCollection:
    """A collection that yields items one page at a time."""
    
    def __init__(self, items: list, page_size: int) -> None:
        if page_size <= 0:
            raise ValueError("page_size must be positive")
        self._items = list(items)
        self._page_size = page_size
    
    def __iter__(self) -> Iterator[any]:
        """Iterate over all items, one at a time."""
        for item in self._items:
            yield item
    
    def page_count(self) -> int:
        if not self._items:
            return 0
        return (len(self._items) + self._page_size - 1) // self._page_size
    
    def get_page(self, page_number: int) -> list:
        if page_number < 0:
            return []
        start = page_number * self._page_size
        end = start + self._page_size
        return self._items[start:end]
    
    @property
    def items(self) -> list:
        return self._items.copy()
    
    @property
    def page_size(self) -> int:
        return self._page_size


class PaginatedIterator:
    """Iterator that yields items one at a time from paginated data."""
    
    def __init__(self, collection: PaginatedCollection) -> None:
        self._collection = collection
        self._current_page = 0
        self._page_index = 0
        self._cached_page: list = []
    
    def __iter__(self) -> PaginatedIterator:
        self._current_page = 0
        self._page_index = 0
        self._cached_page = self._collection.get_page(0)
        return self
    
    def __next__(self) -> any:
        while True:
            if self._page_index < len(self._cached_page):
                value = self._cached_page[self._page_index]
                self._page_index += 1
                return value
            
            self._current_page += 1
            self._cached_page = self._collection.get_page(self._current_page)
            self._page_index = 0
            
            if not self._cached_page:
                raise StopIteration


class PageIterator:
    """Iterator that yields entire pages instead of individual items."""
    
    def __init__(self, collection: PaginatedCollection) -> None:
        self._collection = collection
        self._current_page = 0
    
    def __iter__(self) -> PageIterator:
        self._current_page = 0
        return self
    
    def __next__(self) -> list:
        page = self._collection.get_page(self._current_page)
        if not page:
            raise StopIteration
        self._current_page += 1
        return page
