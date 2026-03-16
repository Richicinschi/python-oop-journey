"""Reference solution for Problem 01: Pagination API Client."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator


@dataclass
class Page:
    """Represents a single page of paginated results."""
    
    items: list[dict]
    page_number: int
    total_pages: int
    total_items: int
    
    @property
    def is_first(self) -> bool:
        """Return True if this is the first page."""
        return self.page_number == 1
    
    @property
    def is_last(self) -> bool:
        """Return True if this is the last page."""
        return self.page_number >= self.total_pages
    
    @property
    def has_next(self) -> bool:
        """Return True if there is a next page."""
        return self.page_number < self.total_pages
    
    @property
    def has_prev(self) -> bool:
        """Return True if there is a previous page."""
        return self.page_number > 1


class MockAPIClient:
    """Simulates an API that returns paginated responses."""
    
    def __init__(self, data: list[dict] | None = None) -> None:
        """Initialize with sample data."""
        if data is None:
            data = [{"id": i, "name": f"Item {i}"} for i in range(1, 26)]
        self._data = data
        self._default_page_size = 5
    
    def get_page(self, endpoint: str, page: int, page_size: int | None = None) -> Page:
        """Simulate fetching a page from an API endpoint."""
        if not endpoint:
            raise ValueError("Endpoint cannot be empty")
        if page < 1:
            raise ValueError("Page must be >= 1")
        
        page_size = page_size or self._default_page_size
        total_items = len(self._data)
        total_pages = (total_items + page_size - 1) // page_size
        
        # Clamp page to valid range
        page = min(page, total_pages) if total_pages > 0 else 1
        
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, total_items)
        items = self._data[start_idx:end_idx]
        
        return Page(
            items=items,
            page_number=page,
            total_pages=max(1, total_pages),
            total_items=total_items
        )


class PaginatedAPIClient:
    """API client with automatic pagination support."""
    
    def __init__(self, api_client: MockAPIClient) -> None:
        """Initialize with an API client."""
        self._client = api_client
    
    def get_page(self, endpoint: str, page_number: int) -> Page:
        """Get a specific page from the API."""
        return self._client.get_page(endpoint, page_number)
    
    def iter_pages(self, endpoint: str) -> Iterator[Page]:
        """Iterate over all pages for an endpoint."""
        page_num = 1
        while True:
            page = self._client.get_page(endpoint, page_num)
            yield page
            if page.is_last:
                break
            page_num += 1
    
    def iter_items(self, endpoint: str) -> Iterator[dict]:
        """Iterate over all items across all pages."""
        for page in self.iter_pages(endpoint):
            yield from page.items
    
    def get_all_items(self, endpoint: str) -> list[dict]:
        """Get all items from all pages as a list."""
        return list(self.iter_items(endpoint))
    
    def count_items(self, endpoint: str) -> int:
        """Get the total count of items for an endpoint."""
        first_page = self._client.get_page(endpoint, 1)
        return first_page.total_items
