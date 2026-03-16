"""Problem 03: Lazy Loading Collection

Topic: Lazy loading pattern
Difficulty: Medium

Implement a lazy loading collection that defers expensive data loading until needed.
"""

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
        raise NotImplementedError("Implement __init__")
    
    def _load_data(self) -> list[T]:
        """Perform the expensive data loading operation.
        
        Returns:
            The loaded data
            
        Note:
            This method is only called once on first access.
        """
        raise NotImplementedError("Implement _load_data")
    
    def __iter__(self) -> Iterator[T]:
        """Iterate over collection, loading data if needed."""
        raise NotImplementedError("Implement __iter__")
    
    def __len__(self) -> int:
        """Return number of items, loading data if needed."""
        raise NotImplementedError("Implement __len__")
    
    def __getitem__(self, index: int) -> T:
        """Get item by index, loading data if needed."""
        raise NotImplementedError("Implement __getitem__")
    
    @property
    def is_loaded(self) -> bool:
        """Return True if data has been loaded."""
        raise NotImplementedError("Implement is_loaded property")
    
    def reload(self) -> None:
        """Force reload of data on next access."""
        raise NotImplementedError("Implement reload")


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
        raise NotImplementedError("Implement __init__")
    
    def _fetch_page(self, page_number: int) -> list[T]:
        """Fetch a specific page of data.
        
        Args:
            page_number: Zero-based page number
            
        Returns:
            List of items in that page
        """
        raise NotImplementedError("Implement _fetch_page")
    
    def get_page(self, page_number: int) -> list[T]:
        """Get a page, using cache if available.
        
        Args:
            page_number: Zero-based page number
            
        Returns:
            List of items in that page
        """
        raise NotImplementedError("Implement get_page")
    
    def iter_pages(self, start_page: int = 0) -> Iterator[list[T]]:
        """Iterate through pages starting from start_page.
        
        Args:
            start_page: Page number to start from
            
        Yields:
            Lists of items for each page
        """
        raise NotImplementedError("Implement iter_pages")
    
    def clear_cache(self) -> None:
        """Clear the page cache."""
        raise NotImplementedError("Implement clear_cache")
    
    @property
    def pages_loaded(self) -> int:
        """Return number of pages currently loaded in cache."""
        raise NotImplementedError("Implement pages_loaded property")
