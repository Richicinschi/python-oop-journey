"""Problem 07: Memoized Callable - Solution

Implement a memoization decorator and a callable class with caching
to optimize expensive function calls.
"""

from __future__ import annotations

from functools import wraps
from typing import Callable, Dict, TypeVar

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
    cache: dict = {}

    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        # Create a hashable key from arguments
        # Convert kwargs to sorted tuple for consistent hashing
        key = (args, tuple(sorted(kwargs.items())))

        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    # Expose cache for inspection/clearing
    wrapper._cache = cache  # type: ignore
    wrapper.clear_cache = lambda: cache.clear()  # type: ignore

    return wrapper


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
        self.func = func
        self._cache: dict = {}
        self._call_count = 0

    def __call__(self, *args, **kwargs) -> T:
        """Call the wrapped function with memoization.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            The result of the function call.
        """
        # Create a hashable key from arguments
        key = (args, tuple(sorted(kwargs.items())))

        if key not in self._cache:
            self._cache[key] = self.func(*args, **kwargs)
            self._call_count += 1

        return self._cache[key]

    def clear_cache(self) -> None:
        """Clear the memoization cache."""
        self._cache.clear()
        self._call_count = 0

    def get_stats(self) -> dict:
        """Get statistics about cache usage.

        Returns:
            Dictionary with 'cache_size' and 'call_count'.
        """
        return {
            "cache_size": len(self._cache),
            "call_count": self._call_count
        }


class FibonacciMemoized:
    """A memoized Fibonacci calculator implemented as a callable class."""

    def __init__(self) -> None:
        """Initialize the Fibonacci calculator."""
        # Initialize cache with base cases
        self._cache: dict[int, int] = {0: 0, 1: 1}
        self._call_count = 0

    def __call__(self, n: int) -> int:
        """Calculate the nth Fibonacci number.

        Args:
            n: The index (0-based) in the Fibonacci sequence.

        Returns:
            The nth Fibonacci number.

        Raises:
            ValueError: If n is negative.
        """
        if n < 0:
            raise ValueError("n must be non-negative")

        if n in self._cache:
            return self._cache[n]

        # Calculate and cache
        self._call_count += 1
        result = self(n - 1) + self(n - 2)
        self._cache[n] = result
        return result

    def sequence(self, count: int) -> list[int]:
        """Generate the first 'count' Fibonacci numbers.

        Args:
            count: Number of Fibonacci numbers to generate.

        Returns:
            List of Fibonacci numbers.
        """
        if count <= 0:
            return []
        return [self(i) for i in range(count)]
