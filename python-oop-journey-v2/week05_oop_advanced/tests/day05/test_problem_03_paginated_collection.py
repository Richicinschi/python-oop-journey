"""Tests for Problem 03: Paginated Collection."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day05.problem_03_paginated_collection import (
    PaginatedCollection, PaginatedIterator, PageIterator
)


class TestPaginatedCollectionInit:
    """Tests for PaginatedCollection initialization."""
    
    def test_init_basic(self) -> None:
        items = [1, 2, 3, 4, 5]
        pc = PaginatedCollection(items, 2)
        assert pc.page_size == 2
        assert pc.items == items
    
    def test_init_empty_items(self) -> None:
        pc = PaginatedCollection([], 5)
        assert list(pc.items) == []
    
    def test_init_invalid_page_size_zero(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            PaginatedCollection([1, 2, 3], 0)
    
    def test_init_invalid_page_size_negative(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            PaginatedCollection([1, 2, 3], -1)


class TestPaginatedCollectionPageCount:
    """Tests for page_count method."""
    
    def test_page_count_exact_multiple(self) -> None:
        pc = PaginatedCollection([1, 2, 3, 4, 5, 6], 3)
        assert pc.page_count() == 2
    
    def test_page_count_partial_page(self) -> None:
        pc = PaginatedCollection([1, 2, 3, 4, 5], 2)
        assert pc.page_count() == 3  # [1,2], [3,4], [5]
    
    def test_page_count_empty(self) -> None:
        pc = PaginatedCollection([], 5)
        assert pc.page_count() == 0
    
    def test_page_count_single_item(self) -> None:
        pc = PaginatedCollection([1], 5)
        assert pc.page_count() == 1


class TestPaginatedCollectionGetPage:
    """Tests for get_page method."""
    
    def test_get_page_first(self) -> None:
        pc = PaginatedCollection([1, 2, 3, 4, 5], 2)
        assert pc.get_page(0) == [1, 2]
    
    def test_get_page_second(self) -> None:
        pc = PaginatedCollection([1, 2, 3, 4, 5], 2)
        assert pc.get_page(1) == [3, 4]
    
    def test_get_page_last_partial(self) -> None:
        pc = PaginatedCollection([1, 2, 3, 4, 5], 2)
        assert pc.get_page(2) == [5]
    
    def test_get_page_out_of_range(self) -> None:
        pc = PaginatedCollection([1, 2, 3], 5)
        assert pc.get_page(1) == []
    
    def test_get_page_negative(self) -> None:
        pc = PaginatedCollection([1, 2, 3, 4, 5], 2)
        assert pc.get_page(-1) == []


class TestPaginatedCollectionIteration:
    """Tests for iterating over PaginatedCollection."""
    
    def test_iteration_yields_all_items(self) -> None:
        pc = PaginatedCollection([1, 2, 3, 4, 5], 2)
        result = list(pc)
        assert result == [1, 2, 3, 4, 5]
    
    def test_iteration_empty_collection(self) -> None:
        pc = PaginatedCollection([], 5)
        result = list(pc)
        assert result == []
    
    def test_iteration_single_page(self) -> None:
        pc = PaginatedCollection([1, 2, 3], 5)
        result = list(pc)
        assert result == [1, 2, 3]


class TestPaginatedIterator:
    """Tests for PaginatedIterator class."""
    
    def test_paginated_iterator_yields_all_items(self) -> None:
        pc = PaginatedCollection([1, 2, 3, 4, 5], 2)
        iterator = PaginatedIterator(pc)
        result = list(iterator)
        assert result == [1, 2, 3, 4, 5]
    
    def test_paginated_iterator_reusable(self) -> None:
        pc = PaginatedCollection([1, 2, 3], 2)
        iterator = PaginatedIterator(pc)
        first = list(iterator)
        second = list(iterator)
        assert first == second == [1, 2, 3]
    
    def test_paginated_iterator_next(self) -> None:
        pc = PaginatedCollection([1, 2, 3], 2)
        iterator = PaginatedIterator(pc)
        iterator = iter(iterator)  # Reset
        assert next(iterator) == 1
        assert next(iterator) == 2
        assert next(iterator) == 3
    
    def test_paginated_iterator_stop_iteration(self) -> None:
        pc = PaginatedCollection([1, 2], 5)
        iterator = PaginatedIterator(pc)
        iterator = iter(iterator)  # Reset
        next(iterator)
        next(iterator)
        with pytest.raises(StopIteration):
            next(iterator)


class TestPageIterator:
    """Tests for PageIterator class."""
    
    def test_page_iterator_yields_pages(self) -> None:
        pc = PaginatedCollection([1, 2, 3, 4, 5], 2)
        page_iter = PageIterator(pc)
        result = list(page_iter)
        assert result == [[1, 2], [3, 4], [5]]
    
    def test_page_iterator_reusable(self) -> None:
        pc = PaginatedCollection([1, 2, 3, 4], 2)
        page_iter = PageIterator(pc)
        first = list(page_iter)
        second = list(page_iter)
        assert first == second == [[1, 2], [3, 4]]
    
    def test_page_iterator_empty(self) -> None:
        pc = PaginatedCollection([], 5)
        page_iter = PageIterator(pc)
        result = list(page_iter)
        assert result == []
    
    def test_page_iterator_single_page(self) -> None:
        pc = PaginatedCollection([1, 2, 3], 5)
        page_iter = PageIterator(pc)
        result = list(page_iter)
        assert result == [[1, 2, 3]]


class TestPaginatedCollectionIntegration:
    """Integration tests for the full pagination system."""
    
    def test_large_collection_pagination(self) -> None:
        items = list(range(100))
        pc = PaginatedCollection(items, 10)
        
        assert pc.page_count() == 10
        assert list(pc) == items
    
    def test_page_iterator_and_flat_iterator_together(self) -> None:
        items = list(range(10))
        pc = PaginatedCollection(items, 3)
        
        # Flat iteration
        flat = list(pc)
        assert flat == items
        
        # Page iteration
        pages = list(PageIterator(pc))
        assert pages == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
        
        # Total items match
        assert sum(len(page) for page in pages) == len(flat)
