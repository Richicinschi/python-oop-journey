"""Problem 01: Pagination API Client

Topic: API Design with Classes - Pagination
Difficulty: Medium

Implement an API client that automatically handles pagination.
The client should provide both page-by-page access and automatic
iteration over all items across all pages.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator


@dataclass
class Page:
    """Represents a single page of paginated results.
    
    Attributes:
        items: List of items on this page
        page_number: Current page number (1-based)
        total_pages: Total number of pages available
        total_items: Total number of items across all pages
    """
    items: list[dict]
    page_number: int
    total_pages: int
    total_items: int
    
    @property
    def is_first(self) -> bool:
        """Return True if this is the first page."""
        raise NotImplementedError("Implement Page.is_first")
    
    @property
    def is_last(self) -> bool:
        """Return True if this is the last page."""
        raise NotImplementedError("Implement Page.is_last")
    
    @property
    def has_next(self) -> bool:
        """Return True if there is a next page."""
        raise NotImplementedError("Implement Page.has_next")
    
    @property
    def has_prev(self) -> bool:
        """Return True if there is a previous page."""
        raise NotImplementedError("Implement Page.has_prev")


class MockAPIClient:
    """Simulates an API that returns paginated responses.
    
    This is provided for testing - you don't need to modify it.
    """
    
    def __init__(self, data: list[dict] | None = None) -> None:
        """Initialize with sample data.
        
        Args:
            data: List of items to paginate. If None, uses default test data.
        """
        if data is None:
            data = [{"id": i, "name": f"Item {i}"} for i in range(1, 26)]
        self._data = data
        self._default_page_size = 5
    
    def get_page(self, endpoint: str, page: int, page_size: int | None = None) -> Page:
        """Simulate fetching a page from an API endpoint.
        
        Args:
            endpoint: API endpoint path (e.g., "/users")
            page: Page number to fetch (1-based)
            page_size: Number of items per page (default: 5)
            
        Returns:
            Page object containing the requested items
            
        Raises:
            ValueError: If page < 1 or endpoint is empty
        """
        raise NotImplementedError("Implement MockAPIClient.get_page")


class PaginatedAPIClient:
    """API client with automatic pagination support.
    
    Wraps a MockAPIClient and provides convenient pagination methods.
    """
    
    def __init__(self, api_client: MockAPIClient) -> None:
        """Initialize with an API client.
        
        Args:
            api_client: The underlying API client to wrap
        """
        raise NotImplementedError("Implement PaginatedAPIClient.__init__")
    
    def get_page(self, endpoint: str, page_number: int) -> Page:
        """Get a specific page from the API.
        
        Args:
            endpoint: API endpoint path
            page_number: Page number to fetch (1-based)
            
        Returns:
            Page object
        """
        raise NotImplementedError("Implement PaginatedAPIClient.get_page")
    
    def iter_pages(self, endpoint: str) -> Iterator[Page]:
        """Iterate over all pages for an endpoint.
        
        Automatically fetches each page in sequence.
        
        Args:
            endpoint: API endpoint path
            
        Yields:
            Page objects for each page
        """
        raise NotImplementedError("Implement PaginatedAPIClient.iter_pages")
    
    def iter_items(self, endpoint: str) -> Iterator[dict]:
        """Iterate over all items across all pages.
        
        Automatically paginates through all pages and yields
        individual items.
        
        Args:
            endpoint: API endpoint path
            
        Yields:
            Individual item dictionaries
        """
        raise NotImplementedError("Implement PaginatedAPIClient.iter_items")
    
    def get_all_items(self, endpoint: str) -> list[dict]:
        """Get all items from all pages as a list.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            List of all items across all pages
        """
        raise NotImplementedError("Implement PaginatedAPIClient.get_all_items")
    
    def count_items(self, endpoint: str) -> int:
        """Get the total count of items for an endpoint.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            Total number of items
        """
        raise NotImplementedError("Implement PaginatedAPIClient.count_items")
