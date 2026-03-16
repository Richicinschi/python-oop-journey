"""Problem 05: Profiling Refactor

Topic: Profile and optimize
Difficulty: Hard

Profile slow code and apply optimizations including caching,
better data structures, and algorithmic improvements.

HINTS AND DEBUGGING:

HINT 1 (Conceptual):
Premature optimization is the root of all evil - but informed 
optimization is valuable. The process is:
1. Measure/profile to find actual bottlenecks
2. Focus on the 20% of code causing 80% of slowdown
3. Optimize with clear before/after benchmarks
4. Verify correctness is preserved

HINT 2 (Structural):
Common optimization patterns:

1. Fibonacci optimization:
   - Naive recursive: O(2^n) - recalculates same values
   - Memoization: O(n) time, O(n) space - cache results
   - Iterative: O(n) time, O(1) space - bottom-up calculation

2. Finding duplicates:
   - Naive: O(n^2) nested loops comparing all pairs
   - Optimized: O(n) using set for seen items
   
   # Pattern
   seen = set()
   duplicates = set()
   for item in items:
       if item in seen:
           duplicates.add(item)
       seen.add(item)

3. Word frequency caching:
   - Cache results by text hash or use functools.lru_cache
   - Clear cache when memory pressure or explicit clear_cache() call

HINT 3 (Edge Cases):
- Fibonacci: n=0 returns 0, n=1 returns 1
- Find duplicates: Empty list returns empty list, no duplicates returns empty
- Word frequencies: Handle empty text, normalize case (lower()), handle punctuation
- Stats tracking: Track cache hits, processing time, memory usage
- Cache invalidation: Implement clear_cache(), set max cache size

DEBUGGING - Common Performance Optimization Pitfalls:

1. Optimizing the wrong thing:
   # Don't guess - measure!
   import cProfile
   cProfile.run('slow_function()')
   
   # Focus on functions with high 'cumulative' or 'tottime'

2. Cache without bounds:
   # WRONG - unbounded memory growth
   _cache = {}
   def expensive(n):
       if n not in _cache:
           _cache[n] = compute(n)
       return _cache[n]
   
   # RIGHT - bounded cache with LRU eviction
   from functools import lru_cache
   @lru_cache(maxsize=128)
   def expensive(n):
       return compute(n)

3. Not clearing/invalidating cache:
   # Caches can become stale
   # Always provide clear_cache() method
   # Consider TTL for time-sensitive data

4. Micro-optimizations that hurt readability:
   # WRONG - hard to understand for minimal gain
   return sum([x**2 for x in range(n)])
   
   # RIGHT - clear and fast enough
   return sum(x**2 for x in range(n))  # Generator saves memory

5. Algorithm choice matters more than micro-optimizations:
   # O(n^2) algorithm with optimized code is still slow for large n
   # Always consider algorithmic complexity first

6. Not verifying results match:
   # Always check optimized code produces same output
   assert slow_version(input) == fast_version(input)
"""

from __future__ import annotations

from typing import Any


class SlowDataProcessor:
    """Data processor with intentionally inefficient operations.
    
    TODO: Profile and optimize this class. Multiple issues exist:
    1. Repeated expensive calculations
    2. Inefficient data structure usage
    3. Missing caching opportunities
    """
    
    def __init__(self) -> None:
        """Initialize processor."""
        raise NotImplementedError("Implement __init__")
    
    def slow_fibonacci(self, n: int) -> int:
        """Calculate fibonacci - naive recursive (very slow for large n).
        
        Args:
            n: Position in Fibonacci sequence
            
        Returns:
            nth Fibonacci number
        """
        raise NotImplementedError("Implement slow_fibonacci")
    
    def find_duplicates(self, items: list[str]) -> list[str]:
        """Find all duplicate strings in a list.
        
        Current implementation is O(n^2). Optimize to O(n).
        
        Args:
            items: List of strings to check
            
        Returns:
            List of duplicate strings (each appears once in result)
        """
        raise NotImplementedError("Implement find_duplicates")
    
    def count_word_frequencies(self, text: str) -> dict[str, int]:
        """Count frequency of each word in text.
        
        Optimize for repeated calls with similar texts.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary mapping words to their frequencies
        """
        raise NotImplementedError("Implement count_word_frequencies")
    
    def get_stats(self) -> dict[str, Any]:
        """Return processing statistics.
        
        Returns:
            Dictionary with stats like cache hits, processing time, etc.
        """
        raise NotImplementedError("Implement get_stats")
    
    def clear_cache(self) -> None:
        """Clear any internal caches."""
        raise NotImplementedError("Implement clear_cache")


class OptimizedDataProcessor:
    """Optimized version of SlowDataProcessor.
    
    This class should provide the same functionality but with
    significantly better performance through:
    - Memoization/caching
    - Efficient data structures
    - Algorithmic improvements
    """
    
    def __init__(self) -> None:
        """Initialize optimized processor."""
        raise NotImplementedError("Implement __init__")
    
    def fibonacci(self, n: int) -> int:
        """Calculate fibonacci efficiently.
        
        Use memoization or iterative approach.
        
        Args:
            n: Position in Fibonacci sequence
            
        Returns:
            nth Fibonacci number
        """
        raise NotImplementedError("Implement fibonacci")
    
    def find_duplicates(self, items: list[str]) -> list[str]:
        """Find all duplicate strings efficiently.
        
        Should be O(n) time complexity.
        
        Args:
            items: List of strings to check
            
        Returns:
            List of duplicate strings (each appears once in result)
        """
        raise NotImplementedError("Implement find_duplicates")
    
    def count_word_frequencies(self, text: str) -> dict[str, int]:
        """Count word frequencies with caching.
        
        Cache results for repeated texts or words.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary mapping words to their frequencies
        """
        raise NotImplementedError("Implement count_word_frequencies")
    
    def get_stats(self) -> dict[str, Any]:
        """Return processing statistics.
        
        Returns:
            Dictionary with stats like cache hits, processing time, etc.
        """
        raise NotImplementedError("Implement get_stats")
    
    def clear_cache(self) -> None:
        """Clear any internal caches."""
        raise NotImplementedError("Implement clear_cache")
    
    @property
    def cache_info(self) -> dict[str, Any]:
        """Return cache statistics.
        
        Returns:
            Dictionary with cache hit rate, size, etc.
        """
        raise NotImplementedError("Implement cache_info property")


class ProfileReport:
    """Container for profiling results.
    
    Used to compare before/after optimization performance.
    """
    
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
        raise NotImplementedError("Implement __init__")
    
    @property
    def speedup_factor(self) -> float:
        """Calculate speedup (before_time / after_time)."""
        raise NotImplementedError("Implement speedup_factor property")
    
    @property
    def results_match(self) -> bool:
        """Check if both implementations produced the same result."""
        raise NotImplementedError("Implement results_match property")
