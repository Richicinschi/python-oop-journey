"""Problem 09: Counted Decorator

Topic: Count Function Calls
Difficulty: Easy

Create a decorator that counts how many times a function is called.

This demonstrates attaching attributes to functions and maintaining state
across calls. Useful for profiling, rate limiting, and debugging.

Example:
    >>> @counted
    ... def greet(name: str) -> str:
    ...     return f"Hello, {name}!"
    
    >>> greet.call_count
    0
    >>> greet("Alice")
    'Hello, Alice!'
    >>> greet.call_count
    1
    >>> greet("Bob")
    'Hello, Bob!'
    >>> greet.call_count
    2

    >>> @counted
    ... def add(a: int, b: int) -> int:
    ...     return a + b
    
    >>> add.call_count
    0
    >>> add(2, 3)
    5
    >>> add(4, 5)
    9
    >>> add.call_count
    2

Behavior Notes:
    - Adds a 'call_count' attribute to the wrapped function
    - call_count starts at 0
    - Increments count before executing the function
    - The attribute is accessible as function.call_count
    - Count persists across multiple uses of the decorator

Edge Cases:
    - Each decorated function has its own independent counter
    - The count increments even if the function raises an exception
    - The wrapper function should be transparent to the original behavior
    - count can be reset by assigning: func.call_count = 0
"""

from __future__ import annotations

from functools import wraps
from typing import Callable, Any


def counted(func: Callable) -> Callable:
    """A decorator that counts function calls.
    
    Adds a `call_count` attribute to the function that tracks
    how many times it has been called.
    
    Args:
        func: The function to decorate
        
    Returns:
        The wrapper function with call counting
    """
    raise NotImplementedError("Implement the counted decorator")
