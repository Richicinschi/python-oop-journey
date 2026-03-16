"""Problem 05: History Buffer (Ring Buffer)

Topic: Circular Buffer with Iteration
Difficulty: Medium

Implement a fixed-size ring buffer with full iteration support.
Useful for keeping a rolling history of recent items.
"""

from __future__ import annotations
from typing import Iterator


class HistoryBuffer:
    """A fixed-size ring buffer with iteration support.
    
    When full, adding new items overwrites the oldest items.
    Iteration yields items from oldest to newest.
    
    Attributes:
        capacity: Maximum number of items to store
        size: Current number of items in buffer
    """
    
    def __init__(self, capacity: int) -> None:
        """Initialize the history buffer.
        
        Args:
            capacity: Maximum number of items (must be > 0)
            
        Raises:
            ValueError: If capacity is not positive
        """
        raise NotImplementedError("Implement __init__")
    
    def append(self, item: any) -> None:
        """Add an item to the buffer.
        
        If at capacity, overwrites the oldest item.
        
        Args:
            item: The item to add
        """
        raise NotImplementedError("Implement append")
    
    def __iter__(self) -> Iterator[any]:
        """Iterate over items from oldest to newest.
        
        Yields:
            Items in chronological order (oldest first)
        """
        raise NotImplementedError("Implement __iter__")
    
    def __len__(self) -> int:
        """Return the current number of items.
        
        Returns:
            Number of items currently stored
        """
        raise NotImplementedError("Implement __len__")
    
    def __getitem__(self, index: int) -> any:
        """Get item at index (0 is oldest, -1 is newest).
        
        Args:
            index: Index from oldest (0) or from newest (-1)
            
        Returns:
            The item at the specified position
            
        Raises:
            IndexError: If index is out of range
        """
        raise NotImplementedError("Implement __getitem__")
    
    def is_full(self) -> bool:
        """Check if buffer is at capacity.
        
        Returns:
            True if buffer contains capacity items
        """
        raise NotImplementedError("Implement is_full")
    
    def clear(self) -> None:
        """Remove all items from the buffer."""
        raise NotImplementedError("Implement clear")
    
    def peek_newest(self) -> any:
        """Get the most recently added item.
        
        Returns:
            The newest item
            
        Raises:
            IndexError: If buffer is empty
        """
        raise NotImplementedError("Implement peek_newest")
    
    def peek_oldest(self) -> any:
        """Get the oldest item in the buffer.
        
        Returns:
            The oldest item
            
        Raises:
            IndexError: If buffer is empty
        """
        raise NotImplementedError("Implement peek_oldest")


class ReversibleHistoryBuffer(HistoryBuffer):
    """History buffer that supports reverse iteration.
    
    Inherits from HistoryBuffer and adds reverse iteration support.
    """
    
    def __reversed__(self) -> Iterator[any]:
        """Iterate over items from newest to oldest.
        
        Yields:
            Items in reverse chronological order (newest first)
        """
        raise NotImplementedError("Implement __reversed__")


# Hints for History Buffer (Medium):
# 
# Hint 1 - Conceptual nudge:
# A circular buffer wraps around when full. Use modulo arithmetic to map logical
# indices to physical array indices.
#
# Hint 2 - Structural plan:
# - Store items in a list of fixed size
# - Track write position (next slot to write) and count (items stored)
# - On append: write at position, increment position modulo capacity,
#   update count (capped at capacity)
# - __iter__ yields items from oldest to newest
# - __reversed__ yields from newest to oldest
#
# Hint 3 - Edge-case warning:
# When buffer is not full yet, oldest is at index 0. When full and wrapped,
# oldest is at write position. Be careful with indexing calculations.
