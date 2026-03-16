"""Tests for Problem 02: Cache Decorator."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day03.problem_02_cache_decorator import (
    cache, fibonacci, greet
)


class TestCacheDecorator:
    """Tests for the cache decorator."""
    
    def test_cache_preserves_function_name(self) -> None:
        """Test that cache preserves the original function name."""
        assert fibonacci.__name__ == "fibonacci"
    
    def test_cache_returns_correct_result(self) -> None:
        """Test that cached function returns correct results."""
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1
        assert fibonacci(10) == 55
        assert fibonacci(20) == 6765
    
    def test_cache_speeds_up_recursive_function(self) -> None:
        """Test that cache significantly speeds up recursive calls."""
        # First call - computes everything
        result1 = fibonacci(30)
        
        # Cached calls should be instant
        result2 = fibonacci(30)
        result3 = fibonacci(25)
        
        assert result1 == 832040
        assert result2 == 832040
        assert result3 == 75025
    
    def test_cache_works_with_kwargs(self) -> None:
        """Test that cache works with keyword arguments."""
        result1 = greet("Alice", greeting="Hi")
        result2 = greet("Alice", greeting="Hi")
        result3 = greet("Bob", greeting="Hi")
        
        assert result1 == "Hi, Alice!"
        assert result2 == "Hi, Alice!"
        assert result3 == "Hi, Bob!"
    
    def test_cache_different_args_produce_different_cache_entries(self) -> None:
        """Test that different arguments produce different cache entries."""
        
        @cache
        def add(a: int, b: int) -> int:
            """Add two numbers."""
            return a + b
        
        assert add(1, 2) == 3
        assert add(2, 3) == 5
        assert add(1, 2) == 3  # Should use cache
    
    def test_cache_same_result_for_same_args(self) -> None:
        """Test that same args produce same result (from cache)."""
        
        call_count = 0
        
        @cache
        def count_calls(x: int) -> int:
            """Count how many times the function body executes."""
            nonlocal call_count
            call_count += 1
            return x * 2
        
        result1 = count_calls(5)
        result2 = count_calls(5)
        result3 = count_calls(5)
        
        assert result1 == result2 == result3 == 10
        assert call_count == 1  # Function body should only execute once


class TestCacheEdgeCases:
    """Tests for cache edge cases."""
    
    def test_cache_with_unhashable_args_fails(self) -> None:
        """Test that cache fails with unhashable arguments."""
        
        @cache
        def process_list(items: list) -> int:
            return len(items)
        
        with pytest.raises(TypeError):
            process_list([1, 2, 3])
    
    def test_cache_preserves_docstring(self) -> None:
        """Test that cache preserves the original docstring."""
        assert fibonacci.__doc__ == "Calculate fibonacci number (slow without cache)."
