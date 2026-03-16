"""Tests for Problem 01: Pagination API Client."""

from __future__ import annotations

import pytest

from week07_real_world.solutions.day01.problem_01_pagination_api_client import (
    MockAPIClient,
    Page,
    PaginatedAPIClient,
)


class TestPage:
    """Tests for Page dataclass."""
    
    def test_page_properties(self) -> None:
        """Test all page boolean properties."""
        # First page
        page = Page(items=[{"id": 1}], page_number=1, total_pages=5, total_items=25)
        assert page.is_first is True
        assert page.is_last is False
        assert page.has_next is True
        assert page.has_prev is False
        
        # Middle page
        page = Page(items=[{"id": 1}], page_number=3, total_pages=5, total_items=25)
        assert page.is_first is False
        assert page.is_last is False
        assert page.has_next is True
        assert page.has_prev is True
        
        # Last page
        page = Page(items=[{"id": 1}], page_number=5, total_pages=5, total_items=25)
        assert page.is_first is False
        assert page.is_last is True
        assert page.has_next is False
        assert page.has_prev is True
        
        # Single page
        page = Page(items=[{"id": 1}], page_number=1, total_pages=1, total_items=1)
        assert page.is_first is True
        assert page.is_last is True
        assert page.has_next is False
        assert page.has_prev is False


class TestMockAPIClient:
    """Tests for MockAPIClient."""
    
    def test_get_page_first_page(self) -> None:
        """Test fetching the first page."""
        client = MockAPIClient()
        page = client.get_page("/items", 1)
        
        assert page.page_number == 1
        assert len(page.items) == 5
        assert page.total_items == 25
        assert page.total_pages == 5
    
    def test_get_page_last_page(self) -> None:
        """Test fetching the last page."""
        client = MockAPIClient()
        page = client.get_page("/items", 5)
        
        assert page.page_number == 5
        assert len(page.items) == 5
    
    def test_get_page_beyond_range(self) -> None:
        """Test fetching page beyond total pages."""
        client = MockAPIClient()
        page = client.get_page("/items", 100)
        
        assert page.page_number == 5  # Clamped to last page
    
    def test_get_page_invalid_page_number(self) -> None:
        """Test invalid page number raises error."""
        client = MockAPIClient()
        with pytest.raises(ValueError, match="Page must be >= 1"):
            client.get_page("/items", 0)
    
    def test_get_page_empty_endpoint(self) -> None:
        """Test empty endpoint raises error."""
        client = MockAPIClient()
        with pytest.raises(ValueError, match="Endpoint cannot be empty"):
            client.get_page("", 1)
    
    def test_get_page_custom_page_size(self) -> None:
        """Test custom page size."""
        data = [{"id": i} for i in range(1, 11)]
        client = MockAPIClient(data)
        page = client.get_page("/items", 1, page_size=3)
        
        assert len(page.items) == 3
        assert page.total_pages == 4
    
    def test_get_page_empty_data(self) -> None:
        """Test with empty data."""
        client = MockAPIClient([])
        page = client.get_page("/items", 1)
        
        assert page.total_items == 0
        assert page.total_pages == 1
        assert len(page.items) == 0


class TestPaginatedAPIClient:
    """Tests for PaginatedAPIClient."""
    
    def test_get_page(self) -> None:
        """Test getting a specific page."""
        mock = MockAPIClient()
        client = PaginatedAPIClient(mock)
        page = client.get_page("/items", 2)
        
        assert page.page_number == 2
        assert len(page.items) == 5
    
    def test_iter_pages(self) -> None:
        """Test iterating over all pages."""
        mock = MockAPIClient()
        client = PaginatedAPIClient(mock)
        pages = list(client.iter_pages("/items"))
        
        assert len(pages) == 5
        assert pages[0].page_number == 1
        assert pages[-1].page_number == 5
    
    def test_iter_items(self) -> None:
        """Test iterating over all items."""
        mock = MockAPIClient()
        client = PaginatedAPIClient(mock)
        items = list(client.iter_items("/items"))
        
        assert len(items) == 25
        assert items[0]["id"] == 1
        assert items[-1]["id"] == 25
    
    def test_get_all_items(self) -> None:
        """Test getting all items as a list."""
        mock = MockAPIClient()
        client = PaginatedAPIClient(mock)
        items = client.get_all_items("/items")
        
        assert len(items) == 25
        assert isinstance(items, list)
    
    def test_count_items(self) -> None:
        """Test counting total items."""
        mock = MockAPIClient()
        client = PaginatedAPIClient(mock)
        count = client.count_items("/items")
        
        assert count == 25
    
    def test_count_items_custom_data(self) -> None:
        """Test counting with custom data."""
        custom_data = [{"id": i} for i in range(1, 101)]
        mock = MockAPIClient(custom_data)
        client = PaginatedAPIClient(mock)
        count = client.count_items("/items")
        
        assert count == 100


class TestIntegration:
    """Integration tests for the pagination system."""
    
    def test_full_pagination_workflow(self) -> None:
        """Test complete pagination workflow."""
        mock = MockAPIClient([{"value": i} for i in range(1, 16)])
        client = PaginatedAPIClient(mock)
        
        # Count items
        assert client.count_items("/data") == 15
        
        # Get all via iteration
        items = client.get_all_items("/data")
        assert len(items) == 15
        
        # Verify page iteration
        pages = list(client.iter_pages("/data"))
        assert len(pages) == 3  # 15 items / 5 per page = 3 pages
        
        # Verify item iteration
        item_values = [item["value"] for item in client.iter_items("/data")]
        assert item_values == list(range(1, 16))
