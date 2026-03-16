"""Problem 02: Countdown Iterator

Topic: Reverse Iteration
Difficulty: Easy

Create a Countdown iterator that counts down from a starting number to zero.
Demonstrates reverse iteration with the iterator protocol.
"""

from __future__ import annotations


class Countdown:
    """An iterator that counts down from start to 0.
    
    Attributes:
        start: The initial countdown value
    """
    
    def __init__(self, start: int) -> None:
        """Initialize the countdown.
        
        Args:
            start: The starting value (must be >= 0)
            
        Raises:
            ValueError: If start is negative
        """
        raise NotImplementedError("Implement __init__")
    
    def __iter__(self) -> Countdown:
        """Return the iterator object, resetting the current value.
        
        Returns:
            self
        """
        raise NotImplementedError("Implement __iter__")
    
    def __next__(self) -> int:
        """Return the next value in the countdown.
        
        Raises:
            StopIteration: When countdown reaches below 0
            
        Returns:
            The current countdown value before decrementing
        """
        raise NotImplementedError("Implement __next__")


class CountdownWithMessage:
    """A countdown iterator that yields messages instead of numbers.
    
    Yields "T-minus X" for each value, then "Liftoff!" at the end.
    
    Attributes:
        start: The initial countdown value
    """
    
    def __init__(self, start: int) -> None:
        """Initialize the countdown with message.
        
        Args:
            start: The starting value (must be >= 0)
        """
        raise NotImplementedError("Implement __init__")
    
    def __iter__(self) -> CountdownWithMessage:
        """Return the iterator object.
        
        Returns:
            self
        """
        raise NotImplementedError("Implement __iter__")
    
    def __next__(self) -> str:
        """Return the next message in the countdown.
        
        Yields "T-minus X" for numbers > 0, "Liftoff!" at 0, then stops.
        
        Raises:
            StopIteration: After yielding "Liftoff!"
            
        Returns:
            The countdown message
        """
        raise NotImplementedError("Implement __next__")
