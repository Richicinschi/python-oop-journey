"""Reference solution for Problem 05: Profiling Refactor."""

from __future__ import annotations

import re
import time
from typing import Any


class SlowDataProcessor:
    """Data processor with intentionally inefficient operations.
    
    This serves as a baseline for profiling and comparison.
    """
    
    def __init__(self) -> None:
        """Initialize processor."""
        self._call_count = 0
    
    def slow_fibonacci(self, n: int) -> int:
        """Calculate fibonacci - naive recursive (very slow for large n).
        
        Args:
            n: Position in Fibonacci sequence
            
        Returns:
            nth Fibonacci number
        """
        self._call_count += 1
        if n < 2:
            return n
        return self.slow_fibonacci(n - 1) + self.slow_fibonacci(n - 2)
    
    def find_duplicates(self, items: list[str]) -> list[str]:
        """Find all duplicate strings in a list - O(n^2) implementation.
        
        Args:
            items: List of strings to check
            
        Returns:
            List of duplicate strings (each appears once in result)
        """
        self._call_count += 1
        duplicates = []
        for i, item in enumerate(items):
            # Inefficient: scans entire list for each item
            if items.count(item) > 1 and item not in duplicates:
                duplicates.append(item)
        return duplicates
    
    def count_word_frequencies(self, text: str) -> dict[str, int]:
        """Count frequency of each word in text - no caching.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary mapping words to their frequencies
        """
        self._call_count += 1
        words = re.findall(r'\b\w+\b', text.lower())
        frequencies: dict[str, int] = {}
        for word in words:
            frequencies[word] = frequencies.get(word, 0) + 1
        return frequencies
    
    def get_stats(self) -> dict[str, Any]:
        """Return processing statistics."""
        return {'calls': self._call_count}
    
    def clear_cache(self) -> None:
        """Clear any internal caches - no-op for slow version."""
        self._call_count = 0


class OptimizedDataProcessor:
    """Optimized version of SlowDataProcessor.
    
    Uses memoization, efficient data structures, and better algorithms.
    """
    
    def __init__(self) -> None:
        """Initialize optimized processor."""
        self._fib_cache: dict[int, int] = {}
        self._word_cache: dict[str, dict[str, int]] = {}
        self._call_count = 0
        self._cache_hits = 0
    
    def fibonacci(self, n: int) -> int:
        """Calculate fibonacci efficiently with memoization.
        
        Args:
            n: Position in Fibonacci sequence
            
        Returns:
            nth Fibonacci number
        """
        self._call_count += 1
        
        if n in self._fib_cache:
            self._cache_hits += 1
            return self._fib_cache[n]
        
        # Iterative approach is more memory efficient for large n
        if n < 2:
            result = n
        else:
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            result = b
        
        self._fib_cache[n] = result
        return result
    
    def find_duplicates(self, items: list[str]) -> list[str]:
        """Find all duplicate strings efficiently - O(n).
        
        Args:
            items: List of strings to check
            
        Returns:
            List of duplicate strings (each appears once in result)
        """
        self._call_count += 1
        seen: set[str] = set()
        duplicates: set[str] = set()
        
        for item in items:
            if item in seen:
                duplicates.add(item)
            seen.add(item)
        
        return list(duplicates)
    
    def count_word_frequencies(self, text: str) -> dict[str, int]:
        """Count word frequencies with caching.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary mapping words to their frequencies
        """
        self._call_count += 1
        
        # Use cached result if available
        if text in self._word_cache:
            self._cache_hits += 1
            return self._word_cache[text].copy()
        
        words = re.findall(r'\b\w+\b', text.lower())
        frequencies: dict[str, int] = {}
        for word in words:
            frequencies[word] = frequencies.get(word, 0) + 1
        
        # Cache the result
        self._word_cache[text] = frequencies.copy()
        return frequencies
    
    def get_stats(self) -> dict[str, Any]:
        """Return processing statistics."""
        return {
            'calls': self._call_count,
            'cache_hits': self._cache_hits,
        }
    
    def clear_cache(self) -> None:
        """Clear all internal caches."""
        self._fib_cache.clear()
        self._word_cache.clear()
        self._call_count = 0
        self._cache_hits = 0
    
    @property
    def cache_info(self) -> dict[str, Any]:
        """Return cache statistics."""
        total_requests = self._call_count + self._cache_hits
        hit_rate = self._cache_hits / total_requests if total_requests > 0 else 0
        
        return {
            'fib_cache_size': len(self._fib_cache),
            'word_cache_size': len(self._word_cache),
            'cache_hits': self._cache_hits,
            'cache_misses': self._call_count,
            'hit_rate': hit_rate,
        }


class ProfileReport:
    """Container for profiling results."""
    
    def __init__(
        self,
        operation: str,
        before_time: float,
        after_time: float,
        before_result: Any,
        after_result: Any
    ) -> None:
        """Initialize profile report.
        
        Args:
            operation: Name of the operation tested
            before_time: Time taken by slow implementation
            after_time: Time taken by optimized implementation
            before_result: Result from slow implementation
            after_result: Result from optimized implementation
        """
        self.operation = operation
        self.before_time = before_time
        self.after_time = after_time
        self.before_result = before_result
        self.after_result = after_result
    
    @property
    def speedup_factor(self) -> float:
        """Calculate speedup (before_time / after_time)."""
        if self.after_time == 0:
            return float('inf')
        return self.before_time / self.after_time
    
    @property
    def results_match(self) -> bool:
        """Check if both implementations produced the same result."""
        return self.before_result == self.after_result
    
    def __repr__(self) -> str:
        """String representation of the report."""
        return (
            f"ProfileReport("
            f"operation='{self.operation}', "
            f"speedup={self.speedup_factor:.2f}x, "
            f"match={self.results_match}"
            f")"
        )


def profile_operation(
    operation: str,
    slow_processor: SlowDataProcessor,
    fast_processor: OptimizedDataProcessor,
    slow_method: str,
    fast_method: str,
    *args: Any
) -> ProfileReport:
    """Profile and compare two implementations.
    
    Args:
        operation: Name of the operation
        slow_processor: Instance of slow processor
        fast_processor: Instance of fast processor
        slow_method: Method name to call on slow processor
        fast_method: Method name to call on fast processor
        *args: Arguments to pass to both methods
        
    Returns:
        ProfileReport comparing the two implementations
    """
    # Time slow implementation
    start = time.perf_counter()
    slow_result = getattr(slow_processor, slow_method)(*args)
    slow_time = time.perf_counter() - start
    
    # Time optimized implementation
    start = time.perf_counter()
    fast_result = getattr(fast_processor, fast_method)(*args)
    fast_time = time.perf_counter() - start
    
    return ProfileReport(
        operation=operation,
        before_time=slow_time,
        after_time=fast_time,
        before_result=slow_result,
        after_result=fast_result
    )
