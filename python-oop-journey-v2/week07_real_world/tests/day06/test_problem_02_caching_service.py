"""Tests for Problem 02: Caching Service."""

from __future__ import annotations

import time

from week07_real_world.solutions.day06.problem_02_caching_service import (
    CachedCalculator,
    TimedCache,
)


def test_timed_cache_set_and_get() -> None:
    """Test basic set and get operations."""
    cache: TimedCache[str, int] = TimedCache(maxsize=10, ttl_seconds=60.0)
    cache.set("key1", 100)
    assert cache.get("key1") == 100


def test_timed_cache_get_missing() -> None:
    """Test get returns None for missing key."""
    cache: TimedCache[str, int] = TimedCache(maxsize=10, ttl_seconds=60.0)
    assert cache.get("missing") is None


def test_timed_cache_expired_entry() -> None:
    """Test that expired entries return None."""
    cache: TimedCache[str, int] = TimedCache(maxsize=10, ttl_seconds=0.1)
    cache.set("key1", 100)
    time.sleep(0.15)
    assert cache.get("key1") is None


def test_timed_cache_lru_eviction() -> None:
    """Test LRU eviction when maxsize is reached."""
    cache: TimedCache[str, int] = TimedCache(maxsize=3, ttl_seconds=60.0)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)
    cache.set("d", 4)  # Should evict "a"
    
    assert cache.get("a") is None
    assert cache.get("b") == 2
    assert cache.get("c") == 3
    assert cache.get("d") == 4


def test_timed_cache_access_updates_lru() -> None:
    """Test that accessing a key updates its LRU position."""
    cache: TimedCache[str, int] = TimedCache(maxsize=3, ttl_seconds=60.0)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)
    
    # Access "a" to make it recently used
    cache.get("a")
    
    # Add "d", should evict "b" (least recently used)
    cache.set("d", 4)
    
    assert cache.get("a") == 1  # Still there
    assert cache.get("b") is None  # Evicted
    assert cache.get("c") == 3
    assert cache.get("d") == 4


def test_timed_cache_clear() -> None:
    """Test clear removes all entries."""
    cache: TimedCache[str, int] = TimedCache(maxsize=10, ttl_seconds=60.0)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.clear()
    
    assert cache.get("a") is None
    assert cache.get("b") is None
    assert len(cache) == 0


def test_timed_cache_len() -> None:
    """Test __len__ returns correct count."""
    cache: TimedCache[str, int] = TimedCache(maxsize=10, ttl_seconds=60.0)
    assert len(cache) == 0
    cache.set("a", 1)
    assert len(cache) == 1
    cache.set("b", 2)
    assert len(cache) == 2


def test_timed_cache_size_property() -> None:
    """Test size property returns correct count."""
    cache: TimedCache[str, int] = TimedCache(maxsize=10, ttl_seconds=60.0)
    assert cache.size == 0
    cache.set("a", 1)
    assert cache.size == 1


def test_timed_cache_update_existing_key() -> None:
    """Test that setting an existing key updates its value."""
    cache: TimedCache[str, int] = TimedCache(maxsize=10, ttl_seconds=60.0)
    cache.set("key1", 100)
    cache.set("key1", 200)
    assert cache.get("key1") == 200
    assert len(cache) == 1


def test_cached_calculator_fibonacci_base_cases() -> None:
    """Test fibonacci base cases."""
    calc = CachedCalculator(cache_maxsize=50)
    assert calc.fibonacci(0) == 0
    assert calc.fibonacci(1) == 1


def test_cached_calculator_fibonacci_small_values() -> None:
    """Test fibonacci for small values."""
    calc = CachedCalculator(cache_maxsize=50)
    assert calc.fibonacci(2) == 1
    assert calc.fibonacci(3) == 2
    assert calc.fibonacci(4) == 3
    assert calc.fibonacci(5) == 5
    assert calc.fibonacci(6) == 8
    assert calc.fibonacci(10) == 55


def test_cached_calculator_fibonacci_negative() -> None:
    """Test fibonacci raises ValueError for negative input."""
    calc = CachedCalculator(cache_maxsize=50)
    try:
        calc.fibonacci(-1)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "non-negative" in str(e)


def test_cached_calculator_factorial_base_cases() -> None:
    """Test factorial base cases."""
    calc = CachedCalculator(cache_maxsize=50)
    assert calc.factorial(0) == 1
    assert calc.factorial(1) == 1


def test_cached_calculator_factorial_small_values() -> None:
    """Test factorial for small values."""
    calc = CachedCalculator(cache_maxsize=50)
    assert calc.factorial(2) == 2
    assert calc.factorial(3) == 6
    assert calc.factorial(4) == 24
    assert calc.factorial(5) == 120


def test_cached_calculator_factorial_negative() -> None:
    """Test factorial raises ValueError for negative input."""
    calc = CachedCalculator(cache_maxsize=50)
    try:
        calc.factorial(-1)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "non-negative" in str(e)


def test_cached_calculator_cache_hits() -> None:
    """Test cache hits are tracked."""
    calc = CachedCalculator(cache_maxsize=50)
    initial_hits = calc.cache_hits
    
    calc.fibonacci(5)
    after_first = calc.cache_hits
    
    calc.fibonacci(5)  # Should hit cache
    after_second = calc.cache_hits
    
    # Second call should have incremented cache hits
    assert after_second > after_first


def test_cached_calculator_clear_cache() -> None:
    """Test clear_cache resets cache and hits."""
    calc = CachedCalculator(cache_maxsize=50)
    calc.fibonacci(10)
    
    hits_before = calc.cache_hits
    calc.fibonacci(10)  # Cache hit
    hits_after = calc.cache_hits
    
    # Verify we had a cache hit
    assert hits_after > hits_before
    
    calc.clear_cache()
    assert calc.cache_hits == 0


def test_cached_calculator_factorial_cache_hits() -> None:
    """Test factorial cache hits are tracked."""
    calc = CachedCalculator(cache_maxsize=50)
    calc.factorial(5)
    assert calc.cache_hits == 0
    
    calc.factorial(5)  # Should hit cache
    assert calc.cache_hits == 1


def test_cached_calculator_fibonacci_caching_speed() -> None:
    """Test that caching improves performance."""
    calc = CachedCalculator(cache_maxsize=100)
    
    # First computation
    calc.fibonacci(20)
    initial_hits = calc.cache_hits
    
    # Same computation should use cache
    calc.fibonacci(20)
    assert calc.cache_hits == initial_hits + 1
