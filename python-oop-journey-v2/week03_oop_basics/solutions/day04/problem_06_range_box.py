"""Reference solution for Problem 06: Range Box."""

from __future__ import annotations

from typing import Iterator


class RangeBox:
    """A closed range [min, max] supporting membership testing and iteration.
    
    The range includes both endpoints. Can be used to check if values
    fall within bounds or to iterate over the range.
    
    Attributes:
        min_val: The minimum value (inclusive).
        max_val: The maximum value (inclusive).
    """
    
    def __init__(self, min_val: int, max_val: int) -> None:
        """Initialize a range box.
        
        Args:
            min_val: The minimum value (inclusive).
            max_val: The maximum value (inclusive).
        
        Raises:
            ValueError: If min_val > max_val.
        """
        if min_val > max_val:
            raise ValueError(f"min_val ({min_val}) must be <= max_val ({max_val})")
        self.min_val = min_val
        self.max_val = max_val
    
    def __contains__(self, value: int | float) -> bool:
        """Check if a value is within the range (inclusive).
        
        Args:
            value: The value to check.
        
        Returns:
            True if min_val <= value <= max_val, False otherwise.
        """
        return self.min_val <= value <= self.max_val
    
    def __iter__(self) -> Iterator[int]:
        """Iterate over all integers in the range.
        
        Yields:
            Integers from min_val to max_val (inclusive).
        """
        return iter(range(self.min_val, self.max_val + 1))
    
    def __len__(self) -> int:
        """Return the number of integers in the range."""
        return self.max_val - self.min_val + 1
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        return f"RangeBox({self.min_val}, {self.max_val})"
    
    def is_empty(self) -> bool:
        """Check if the range is empty (min > max).
        
        Returns:
            True if the range contains no values.
        """
        return self.min_val > self.max_val
    
    def clamp(self, value: int | float) -> int | float:
        """Clamp a value to the range.
        
        Args:
            value: The value to clamp.
        
        Returns:
            The value if within range, min_val if below, max_val if above.
        """
        if value < self.min_val:
            return self.min_val
        if value > self.max_val:
            return self.max_val
        return value
