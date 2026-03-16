"""Tests for Problem 03: Lazy Loading Collection."""

from __future__ import annotations

from week07_real_world.solutions.day06.problem_03_lazy_loading_collection import (
    LazyCollection,
    PaginatedLoader,
)


def test_lazy_collection_not_loaded_initially() -> None:
    """Test that collection is not loaded on creation."""
    collection: LazyCollection[int] = LazyCollection()
    assert not collection.is_loaded


def test_lazy_collection_loaded_after_iteration() -> None:
    """Test that collection loads when iterated."""
    collection = LazyCollection([1, 2, 3])
    items = list(collection)
    assert collection.is_loaded
    assert items == [1, 2, 3]


def test_lazy_collection_loaded_after_len() -> None:
    """Test that collection loads when len is called."""
    collection = LazyCollection([1, 2, 3, 4, 5])
    length = len(collection)
    assert collection.is_loaded
    assert length == 5


def test_lazy_collection_loaded_after_getitem() -> None:
    """Test that collection loads when item is accessed."""
    collection = LazyCollection([10, 20, 30])
    item = collection[1]
    assert collection.is_loaded
    assert item == 20


def test_lazy_collection_preserves_data() -> None:
    """Test that loaded data is preserved correctly."""
    source = ["a", "b", "c", "d"]
    collection = LazyCollection(source)
    assert list(collection) == source


def test_lazy_collection_empty_source() -> None:
    """Test collection with empty source."""
    collection: LazyCollection[int] = LazyCollection([])
    assert list(collection) == []
    assert len(collection) == 0


def test_lazy_collection_iteration_multiple_times() -> None:
    """Test that collection can be iterated multiple times."""
    collection = LazyCollection([1, 2, 3])
    first = list(collection)
    second = list(collection)
    assert first == second == [1, 2, 3]


def test_lazy_collection_reload() -> None:
    """Test reload clears loaded data."""
    collection = LazyCollection([1, 2, 3])
    list(collection)  # Load data
    assert collection.is_loaded
    
    collection.reload()
    assert not collection.is_loaded
    
    # Can still access after reload
    assert list(collection) == [1, 2, 3]


def test_lazy_collection_getitem_negative_index() -> None:
    """Test getitem with negative index."""
    collection = LazyCollection([1, 2, 3, 4, 5])
    assert collection[-1] == 5
    assert collection[-2] == 4


def test_lazy_collection_getitem_out_of_range() -> None:
    """Test getitem raises IndexError for out of range index."""
    collection = LazyCollection([1, 2, 3])
    try:
        _ = collection[10]
        assert False, "Should have raised IndexError"
    except IndexError:
        pass


def test_lazy_collection_load_count() -> None:
    """Test that data is only loaded once."""
    collection = LazyCollection([1, 2, 3])
    assert collection.load_count == 0
    
    list(collection)  # First load
    assert collection.load_count == 1
    
    len(collection)  # Should not reload
    assert collection.load_count == 1
    
    collection[0]  # Should not reload
    assert collection.load_count == 1


def test_lazy_collection_load_count_after_reload() -> None:
    """Test load count after reload."""
    collection = LazyCollection([1, 2, 3])
    list(collection)
    assert collection.load_count == 1
    
    collection.reload()
    list(collection)
    assert collection.load_count == 2


def test_paginated_loader_init() -> None:
    """Test PaginatedLoader initialization."""
    loader: PaginatedLoader[str] = PaginatedLoader(page_size=5)
    assert loader.pages_loaded == 0


def test_paginated_loader_get_page() -> None:
    """Test getting a single page."""
    loader: PaginatedLoader[str] = PaginatedLoader(page_size=3)
    page = loader.get_page(0)
    assert len(page) == 3
    assert page[0] == "item_0"
    assert page[1] == "item_1"
    assert page[2] == "item_2"


def test_paginated_loader_caches_pages() -> None:
    """Test that pages are cached after first fetch."""
    loader: PaginatedLoader[str] = PaginatedLoader(page_size=5)
    page1 = loader.get_page(0)
    assert loader.pages_loaded == 1
    
    page2 = loader.get_page(0)
    assert loader.pages_loaded == 1  # Should not fetch again
    assert page1 is page2  # Same cached list


def test_paginated_loader_multiple_pages() -> None:
    """Test fetching multiple different pages."""
    loader: PaginatedLoader[str] = PaginatedLoader(page_size=2)
    page0 = loader.get_page(0)
    page1 = loader.get_page(1)
    page2 = loader.get_page(2)
    
    assert page0 == ["item_0", "item_1"]
    assert page1 == ["item_2", "item_3"]
    assert page2 == ["item_4", "item_5"]
    assert loader.pages_loaded == 3


def test_paginated_loader_negative_page() -> None:
    """Test that negative page number raises ValueError."""
    loader: PaginatedLoader[str] = PaginatedLoader(page_size=5)
    try:
        loader.get_page(-1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_paginated_loader_clear_cache() -> None:
    """Test clearing the cache."""
    loader: PaginatedLoader[str] = PaginatedLoader(page_size=5)
    loader.get_page(0)
    loader.get_page(1)
    assert loader.pages_loaded == 2
    
    loader.clear_cache()
    assert loader.pages_loaded == 0


def test_paginated_loader_iter_pages() -> None:
    """Test iterating through pages."""
    loader: PaginatedLoader[str] = PaginatedLoader(page_size=2)
    
    pages = []
    for page in loader.iter_pages(start_page=0):
        pages.append(page)
        if len(pages) >= 3:  # Limit for testing
            break
    
    assert len(pages) == 3
    assert pages[0] == ["item_0", "item_1"]
    assert pages[1] == ["item_2", "item_3"]
    assert pages[2] == ["item_4", "item_5"]


def test_paginated_loader_iter_pages_start_offset() -> None:
    """Test iterating from a specific start page."""
    loader: PaginatedLoader[str] = PaginatedLoader(page_size=2)
    
    pages = []
    for page in loader.iter_pages(start_page=2):
        pages.append(page)
        if len(pages) >= 2:
            break
    
    assert pages[0] == ["item_4", "item_5"]
    assert pages[1] == ["item_6", "item_7"]


def test_paginated_loader_pages_loaded_tracking() -> None:
    """Test pages_loaded tracks loaded pages correctly."""
    loader: PaginatedLoader[str] = PaginatedLoader(page_size=10)
    
    assert loader.pages_loaded == 0
    loader.get_page(0)
    assert loader.pages_loaded == 1
    loader.get_page(0)  # Cached
    assert loader.pages_loaded == 1
    loader.get_page(1)
    assert loader.pages_loaded == 2
