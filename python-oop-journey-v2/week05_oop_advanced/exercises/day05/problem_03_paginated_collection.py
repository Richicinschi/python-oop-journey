"""Problem 03: Paginated Collection

Topic: Real-world Iterator Pattern
Difficulty: Medium

Create a paginated collection that iterates through items in chunks (pages),
useful for API pagination or database result sets.
"""

from __future__ import annotations
from typing import Iterator


class PaginatedCollection:
    """A collection that yields items one page at a time.
    
    Simulates paginated data access where items are fetched in batches.
    
    Attributes:
        items: The full list of items
        page_size: Number of items per page
    """
    
    def __init__(self, items: list, page_size: int) -> None:
        """Initialize the paginated collection.
        
        Args:
            items: The complete list of items
            page_size: Number of items per page (must be > 0)
            
        Raises:
            ValueError: If page_size is not positive
        """
        raise NotImplementedError("Implement __init__")
    
    def __iter__(self) -> PaginatedIterator:
        """Return a new iterator over all items (flattened).
        
        Returns:
            Iterator that yields individual items across all pages
        """
        raise NotImplementedError("Implement __iter__")
    
    def page_count(self) -> int:
        """Calculate the total number of pages.
        
        Returns:
            Number of pages needed for all items
        """
        raise NotImplementedError("Implement page_count")
    
    def get_page(self, page_number: int) -> list:
        """Get a specific page of items (0-indexed).
        
        Args:
            page_number: The page index (0-based)
            
        Returns:
            List of items on that page (may be empty if out of range)
        """
        raise NotImplementedError("Implement get_page")


class PaginatedIterator:
    """Iterator that yields items one at a time from paginated data.
    
    Simulates fetching pages on demand as iteration progresses.
    
    Attributes:
        collection: The PaginatedCollection to iterate over
        current_page: The current page being processed
        page_index: Index within the current page
    """
    
    def __init__(self, collection: PaginatedCollection) -> None:
        """Initialize the paginated iterator.
        
        Args:
            collection: The paginated collection to iterate
        """
        raise NotImplementedError("Implement __init__")
    
    def __iter__(self) -> PaginatedIterator:
        """Reset and return the iterator.
        
        Returns:
            self
        """
        raise NotImplementedError("Implement __iter__")
    
    def __next__(self) -> any:
        """Return the next item, fetching pages as needed.
        
        Raises:
            StopIteration: When all items have been yielded
            
        Returns:
            The next item from the collection
        """
        raise NotImplementedError("Implement __next__")


# Hints for Paginated Collection (Medium):
# 
# Hint 1 - Conceptual nudge:
# You need to track which page you're on and return the next page each time.
# Use offset and limit to slice the data.
#
# Hint 2 - Structural plan:
# - __init__ stores data, page_size, and initializes current page index
# - __iter__ returns self
# - __next__ calculates start and end indices, slices data[start:end]
# - If start >= len(data), raise StopIteration
# - Increment page counter after each yield
#
# Hint 3 - Edge-case warning:
# Handle empty data (StopIteration immediately). Handle page_size larger than
# remaining items (return what remains). What about page_size of 0?


class PageIterator:
    """Iterator that yields entire pages instead of individual items.
    
    Useful when processing needs to happen at the page level.
    """
    
    def __init__(self, collection: PaginatedCollection) -> None:
        """Initialize the page iterator.
        
        Args:
            collection: The paginated collection to iterate over pages
        """
        raise NotImplementedError("Implement __init__")
    
    def __iter__(self) -> PageIterator:
        """Reset and return the iterator.
        
        Returns:
            self
        """
        raise NotImplementedError("Implement __iter__")
    
    def __next__(self) -> list:
        """Return the next page of items.
        
        Raises:
            StopIteration: When all pages have been yielded
            
        Returns:
            A list containing the next page of items
        """
        raise NotImplementedError("Implement __next__")
