"""Problem 02: Cache Decorator

Topic: Memoization Decorator
Difficulty: Easy

Create a decorator that caches function results to avoid redundant computations.

This demonstrates memoization - a technique where function results are stored
and returned for subsequent calls with the same arguments. Essential for
optimizing expensive pure functions like Fibonacci calculations.

Example:
    >>> @cache
    ... def fibonacci(n: int) -> int:
    ...     if n < 2:
    ...         return n
    ...     return fibonacci(n - 1) + fibonacci(n - 2)
    
    >>> fibonacci(35)  # Completes instantly due to caching
    9227465

    >>> @cache
    ... def greet(name: str, greeting: str = "Hello") -> str:
    ...     return f"{greeting}, {name}!"
    
    >>> greet("Alice", greeting="Hi")
    'Hi, Alice!'
    >>> greet("Alice", greeting="Hi")  # Returns cached result
    'Hi, Alice!'

Behavior Notes:
    - Uses a dictionary to store cached results
    - Cache key must include both positional and keyword arguments
    - The cache persists for the lifetime of the decorated function
    - Returns cached result immediately if arguments match

Edge Cases:
    - Only works with hashable arguments (raises TypeError for unhashable)
    - Functions with side effects may behave unexpectedly when cached
    - None is a valid cacheable result
    - Memory usage grows with unique argument combinations
"""

from __future__ import annotations

from functools import wraps
from typing import Callable, Any, Hashable


def cache(func: Callable) -> Callable:
    """A decorator that caches function results.
    
    Uses a dictionary to store results keyed by arguments.
    Only works with hashable arguments.
    
    Args:
        func: The function to decorate
        
    Returns:
        The wrapper function with caching
    """
    raise NotImplementedError("Implement the cache decorator")


# Hints for Cache Decorator (Medium):
# 
# Hint 1 - Conceptual nudge:
# You need to store function results keyed by their arguments. A dictionary works
# well for this, but the arguments must be hashable.
#
# Hint 2 - Structural plan:
# - Create a cache dict inside the decorator (not the wrapper)
# - In the wrapper, create a cache key from the arguments
# - Check if key is in cache - if yes, return cached value
# - If not, call the function, store result, return it
# - Use functools.wraps to preserve function metadata
#
# Hint 3 - Edge-case warning:
# What if the arguments are not hashable (like lists)? You might need to convert
# them to tuples. Also, the cache can grow unbounded - consider adding a maxsize.
