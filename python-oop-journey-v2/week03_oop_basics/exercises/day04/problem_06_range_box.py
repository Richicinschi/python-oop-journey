"""Problem 06: Range Box

Topic: Magic Methods - Membership Testing and Iteration
Difficulty: Medium

Implement a range box that supports containment checks and iteration.
"""

from __future__ import annotations

from typing import Iterator


class RangeBox:
    """A closed range [min, max] supporting membership testing and iteration.
    
    The range includes both endpoints. Can be used to check if values
    fall within bounds or to iterate over the range.
    
    Attributes:
        min_val: The minimum value (inclusive).
        max_val: The maximum value (inclusive).
    
    Example:
        >>> box = RangeBox(1, 5)
        >>> 3 in box
        True
        >>> 0 in box
        False
        >>> list(box)
        [1, 2, 3, 4, 5]
    """
    
    def __init__(self, min_val: int, max_val: int) -> None:
        """Initialize a range box.
        
        Args:
            min_val: The minimum value (inclusive).
            max_val: The maximum value (inclusive).
        
        Raises:
            ValueError: If min_val > max_val.
        """
        raise NotImplementedError("Implement __init__")
    
    def __contains__(self, value: int | float) -> bool:
        """Check if a value is within the range (inclusive).
        
        Args:
            value: The value to check.
        
        Returns:
            True if min_val <= value <= max_val, False otherwise.
        """
        raise NotImplementedError("Implement __contains__")
    
    def __iter__(self) -> Iterator[int]:
        """Iterate over all integers in the range.
        
        Yields:
            Integers from min_val to max_val (inclusive).
        """
        raise NotImplementedError("Implement __iter__")
    
    def __len__(self) -> int:
        """Return the number of integers in the range."""
        raise NotImplementedError("Implement __len__")
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        raise NotImplementedError("Implement __repr__")
    
    def is_empty(self) -> bool:
        """Check if the range is empty (min > max).
        
        Returns:
            True if the range contains no values.
        """
        raise NotImplementedError("Implement is_empty")
    
    def clamp(self, value: int | float) -> int | float:
        """Clamp a value to the range.
        
        Args:
            value: The value to clamp.
        
        Returns:
            The value if within range, min_val if below, max_val if above.
        """
        raise NotImplementedError("Implement clamp")
