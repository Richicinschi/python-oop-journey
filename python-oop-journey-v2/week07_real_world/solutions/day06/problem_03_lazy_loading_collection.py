"""Reference solution for Problem 03: Lazy Loading Collection."""

from __future__ import annotations

from typing import Generic, Iterator, TypeVar

T = TypeVar('T')


class LazyCollection(Generic[T]):
    """Collection that loads data lazily on first access.
    
    The expensive data loading operation is deferred until the data is
    actually needed, saving resources when the data might not be used.
    """
    
    def __init__(self, data_source: list[T] | None = None) -> None:
        """Initialize lazy collection.
        
        Args:
            data_source: Optional initial data. If None, data will be
                        loaded lazily when first accessed.
        """
        self._data_source = data_source
        self._data: list[T] | None = None
        self._load_count = 0
    
    def _load_data(self) -> list[T]:
        """Perform the expensive data loading operation.
        
        Returns:
            The loaded data
            
        Note:
            This method is only called once on first access.
        """
        self._load_count += 1
        if self._data_source is not None:
            return list(self._data_source)
        # Default implementation returns empty list
        return []
    
    def _ensure_loaded(self) -> list[T]:
        """Ensure data is loaded and return it."""
        if self._data is None:
            self._data = self._load_data()
        return self._data
    
    def __iter__(self) -> Iterator[T]:
        """Iterate over collection, loading data if needed."""
        return iter(self._ensure_loaded())
    
    def __len__(self) -> int:
        """Return number of items, loading data if needed."""
        return len(self._ensure_loaded())
    
    def __getitem__(self, index: int) -> T:
        """Get item by index, loading data if needed."""
        return self._ensure_loaded()[index]
    
    @property
    def is_loaded(self) -> bool:
        """Return True if data has been loaded."""
        return self._data is not None
    
    def reload(self) -> None:
        """Force reload of data on next access."""
        self._data = None
    
    @property
    def load_count(self) -> int:
        """Return number of times data has been loaded (for testing)."""
        return self._load_count


class PaginatedLoader(Generic[T]):
    """Loader that fetches data in pages on demand.
    
    Instead of loading all data at once, fetches pages as they are
    accessed, reducing initial load time and memory usage.
    """
    
    def __init__(self, page_size: int = 10) -> None:
        """Initialize paginated loader.
        
        Args:
            page_size: Number of items per page
        """
        self._page_size = page_size
        self._cache: dict[int, list[T]] = {}
        self._total_pages: int | None = None
    
    def _fetch_page(self, page_number: int) -> list[T]:
        """Fetch a specific page of data.
        
        Args:
            page_number: Zero-based page number
            
        Returns:
            List of items in that page
            
        Note:
            This is a simulation. In real use, this would query a database
            or API for the specific page.
        """
        # Simulate fetching from a data source
        # In real code, this would query a database
        start_idx = page_number * self._page_size
        return [f"item_{start_idx + i}" for i in range(self._page_size)]  # type: ignore[list-item]
    
    def get_page(self, page_number: int) -> list[T]:
        """Get a page, using cache if available.
        
        Args:
            page_number: Zero-based page number
            
        Returns:
            List of items in that page
        """
        if page_number < 0:
            raise ValueError("page_number must be non-negative")
        
        if page_number not in self._cache:
            self._cache[page_number] = self._fetch_page(page_number)
        
        return self._cache[page_number]
    
    def iter_pages(self, start_page: int = 0) -> Iterator[list[T]]:
        """Iterate through pages starting from start_page.
        
        Args:
            start_page: Page number to start from
            
        Yields:
            Lists of items for each page
        """
        page_num = start_page
        while True:
            page = self.get_page(page_num)
            if not page:
                break
            yield page
            page_num += 1
            
            # Safety limit to prevent infinite iteration in tests
            if page_num > start_page + 1000:
                break
    
    def clear_cache(self) -> None:
        """Clear the page cache."""
        self._cache.clear()
    
    @property
    def pages_loaded(self) -> int:
        """Return number of pages currently loaded in cache."""
        return len(self._cache)
