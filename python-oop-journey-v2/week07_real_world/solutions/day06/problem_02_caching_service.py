"""Reference solution for Problem 02: Caching Service."""

from __future__ import annotations

import time
from typing import TypeVar

K = TypeVar('K')
V = TypeVar('V')


class TimedCache:
    """LRU cache with TTL (Time To Live) support.
    
    Entries expire after a specified time and are evicted based on
    Least Recently Used policy when capacity is reached.
    """
    
    def __init__(self, maxsize: int = 100, ttl_seconds: float = 60.0) -> None:
        """Initialize the cache.
        
        Args:
            maxsize: Maximum number of entries to store
            ttl_seconds: Time-to-live in seconds for each entry
        """
        self._maxsize = maxsize
        self._ttl = ttl_seconds
        self._data: dict[K, tuple[V, float]] = {}
        self._access_order: list[K] = []
    
    def _is_expired(self, timestamp: float) -> bool:
        """Check if a timestamp has expired."""
        return time.time() - timestamp > self._ttl
    
    def _cleanup_expired(self) -> None:
        """Remove all expired entries."""
        now = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self._data.items()
            if now - timestamp > self._ttl
        ]
        for key in expired_keys:
            del self._data[key]
            self._access_order.remove(key)
    
    def get(self, key: K) -> V | None:
        """Get value by key if present and not expired.
        
        Args:
            key: Cache key to look up
            
        Returns:
            The cached value or None if not found or expired
        """
        if key not in self._data:
            return None
        
        value, timestamp = self._data[key]
        
        if self._is_expired(timestamp):
            del self._data[key]
            self._access_order.remove(key)
            return None
        
        # Update access order (LRU)
        self._access_order.remove(key)
        self._access_order.append(key)
        
        return value
    
    def set(self, key: K, value: V) -> None:
        """Store value with key in cache.
        
        Args:
            key: Cache key
            value: Value to store
        """
        # Clean up expired entries periodically
        if len(self._data) >= self._maxsize:
            self._cleanup_expired()
        
        # If key exists, update it
        if key in self._data:
            self._access_order.remove(key)
        elif len(self._data) >= self._maxsize:
            # Evict LRU
            lru_key = self._access_order.pop(0)
            del self._data[lru_key]
        
        self._data[key] = (value, time.time())
        self._access_order.append(key)
    
    def clear(self) -> None:
        """Clear all entries from the cache."""
        self._data.clear()
        self._access_order.clear()
    
    def __len__(self) -> int:
        """Return current number of entries in cache."""
        return len(self._data)
    
    @property
    def size(self) -> int:
        """Return current cache size."""
        return len(self._data)


class CachedCalculator:
    """Calculator with internal caching for expensive operations."""
    
    def __init__(self, cache_maxsize: int = 50) -> None:
        """Initialize calculator with cache.
        
        Args:
            cache_maxsize: Maximum cache entries
        """
        self._cache: dict[str, dict[int, int]] = {
            'fibonacci': {},
            'factorial': {},
        }
        self._maxsize = cache_maxsize
        self._hits = 0
        self._cleared = False
    
    def fibonacci(self, n: int) -> int:
        """Calculate nth Fibonacci number with caching.
        
        Args:
            n: Position in Fibonacci sequence
            
        Returns:
            The nth Fibonacci number
            
        Raises:
            ValueError: If n is negative
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        
        cache = self._cache['fibonacci']
        
        if n in cache:
            self._hits += 1
            return cache[n]
        
        if n <= 1:
            result = n
        else:
            result = self.fibonacci(n - 1) + self.fibonacci(n - 2)
        
        # Simple LRU: if at capacity, clear half
        if len(cache) >= self._maxsize:
            keys_to_remove = list(cache.keys())[:self._maxsize // 2]
            for k in keys_to_remove:
                del cache[k]
        
        cache[n] = result
        return result
    
    def factorial(self, n: int) -> int:
        """Calculate n! with caching.
        
        Args:
            n: Number to calculate factorial for
            
        Returns:
            n factorial
            
        Raises:
            ValueError: If n is negative
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        
        cache = self._cache['factorial']
        
        if n in cache:
            self._hits += 1
            return cache[n]
        
        if n <= 1:
            result = 1
        else:
            result = n * self.factorial(n - 1)
        
        # Simple LRU: if at capacity, clear half
        if len(cache) >= self._maxsize:
            keys_to_remove = list(cache.keys())[:self._maxsize // 2]
            for k in keys_to_remove:
                del cache[k]
        
        cache[n] = result
        return result
    
    def clear_cache(self) -> None:
        """Clear the internal cache."""
        self._cache['fibonacci'].clear()
        self._cache['factorial'].clear()
        self._hits = 0
        self._cleared = True
    
    @property
    def cache_hits(self) -> int:
        """Return number of cache hits since creation or last clear."""
        return self._hits
