"""Problem 07: Memoized Callable

Implement a memoization decorator and a callable class with caching
to optimize expensive function calls.

Hints:
    * Hint 1: Memoization stores function results in a dictionary keyed
      by arguments. The key must be hashable - use tuple(args) for
      positional args and frozenset(kwargs.items()) for keyword args.
    
    * Hint 2: For the @memoize decorator:
      - Create a dict to store cached results
      - The wrapper function checks if args/kwargs are in cache
      - If yes, return cached value; if no, call function and store result
      - Use @functools.wraps to preserve function metadata
    
    * Hint 3: For MemoizedCallable class:
      - __init__ stores the function and initializes _cache and _call_count
      - __call__ checks cache, increments count only on cache miss
      - get_stats() returns {'cache_size': len(_cache), 'call_count': _call_count}
      - clear_cache() resets both cache and counter

Debugging Tips:
    - "Unhashable type" error: Your cache key includes a list or dict.
      Convert to tuple or frozenset before using as dict key
    - Cache never hits: Are you including 'self' in the key for methods?
      Each instance will have different self objects
    - Fibonacci still slow: Ensure the memoized version calls itself,
      not the original un-memoized function
    - Memory growing unbounded: This is expected! Real memoization
      might need LRU eviction, but that's beyond this exercise
"""

from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def memoize(func: Callable[..., T]) -> Callable[..., T]:
    """A decorator that memoizes function results.

    Stores results of previous calls and returns cached result
    for the same arguments.

    Args:
        func: The function to memoize.

    Returns:
        A wrapped function with memoization.

    Example:
        >>> @memoize
        ... def fib(n: int) -> int:
        ...     if n < 2:
        ...         return n
        ...     return fib(n - 1) + fib(n - 2)
        >>> fib(10)  # Fast due to memoization
        55
    """
    raise NotImplementedError("Implement memoize")


class MemoizedCallable:
    """A callable class that memoizes its results.

    This class wraps a function and caches its results.

    Attributes:
        func: The wrapped function.
        _cache: Dictionary storing cached results.
        _call_count: Number of times the function was actually called.
    """

    def __init__(self, func: Callable[..., T]) -> None:
        """Initialize with the function to wrap.

        Args:
            func: The function to memoize.
        """
        raise NotImplementedError("Implement __init__")

    def __call__(self, *args, **kwargs) -> T:
        """Call the wrapped function with memoization.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            The result of the function call.
        """
        raise NotImplementedError("Implement __call__")

    def clear_cache(self) -> None:
        """Clear the memoization cache."""
        raise NotImplementedError("Implement clear_cache")

    def get_stats(self) -> dict:
        """Get statistics about cache usage.

        Returns:
            Dictionary with 'cache_size' and 'call_count'.
        """
        raise NotImplementedError("Implement get_stats")


class FibonacciMemoized:
    """A memoized Fibonacci calculator implemented as a callable class."""

    def __init__(self) -> None:
        """Initialize the Fibonacci calculator."""
        raise NotImplementedError("Implement __init__")

    def __call__(self, n: int) -> int:
        """Calculate the nth Fibonacci number.

        Args:
            n: The index (0-based) in the Fibonacci sequence.

        Returns:
            The nth Fibonacci number.

        Raises:
            ValueError: If n is negative.
        """
        raise NotImplementedError("Implement __call__")

    def sequence(self, count: int) -> list[int]:
        """Generate the first 'count' Fibonacci numbers.

        Args:
            count: Number of Fibonacci numbers to generate.

        Returns:
            List of Fibonacci numbers.
        """
    raise NotImplementedError("Implement sequence")
