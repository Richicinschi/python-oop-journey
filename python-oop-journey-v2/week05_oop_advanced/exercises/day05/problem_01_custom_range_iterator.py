"""Problem 01: Custom Range Iterator

Topic: Iterator Protocol
Difficulty: Easy

Create a CustomRange class that mimics Python's built-in range() function
using the iterator protocol with __iter__ and __next__.
"""

from __future__ import annotations


class CustomRange:
    """A custom implementation of range-like iteration.
    
    Supports positive and negative steps, start/stop/step parameters.
    
    Attributes:
        start: The starting value of the range
        stop: The end value (exclusive)
        step: The increment/decrement value
    """
    
    def __init__(self, start: int, stop: int | None = None, step: int = 1) -> None:
        """Initialize the CustomRange.
        
        Args:
            start: If stop is None, this becomes stop and start becomes 0
            stop: The end value (exclusive), or None if start is used as stop
            step: The increment value. Must be non-zero.
            
        Raises:
            ValueError: If step is zero
        """
        raise NotImplementedError("Implement __init__")
    
    def __iter__(self) -> CustomRange:
        """Return the iterator object (self).
        
        Resets the internal state so the range can be iterated multiple times.
        
        Returns:
            self
        """
        raise NotImplementedError("Implement __iter__")
    
    def __next__(self) -> int:
        """Return the next value in the sequence.
        
        Raises:
            StopIteration: When the sequence is exhausted
            
        Returns:
            The next integer value
        """
        raise NotImplementedError("Implement __next__")
    
    def __len__(self) -> int:
        """Return the number of items in the range.
        
        Returns:
            Count of values the range would yield
        """
        raise NotImplementedError("Implement __len__")
