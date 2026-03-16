"""Tests for Problem 10: Rate Limit Decorator."""

from __future__ import annotations

import pytest
import time

from week05_oop_advanced.solutions.day03.problem_10_rate_limit_decorator import (
    rate_limit, api_call, process_data
)


class TestRateLimitDecorator:
    """Tests for the rate limit decorator."""
    
    def test_rate_limit_allows_calls_within_limit(self) -> None:
        """Test that calls within rate limit succeed."""
        
        @rate_limit(max_calls=3, period=1.0)
        def limited_func() -> str:
            return "success"
        
        # First 3 calls should succeed
        assert limited_func() == "success"
        assert limited_func() == "success"
        assert limited_func() == "success"
    
    def test_rate_limit_raises_after_limit(self) -> None:
        """Test that calls exceeding rate limit raise RuntimeError."""
        
        @rate_limit(max_calls=2, period=1.0)
        def limited_func() -> str:
            return "success"
        
        # First 2 calls succeed
        limited_func()
        limited_func()
        
        # Third call should fail
        with pytest.raises(RuntimeError) as exc_info:
            limited_func()
        
        assert "Rate limit exceeded" in str(exc_info.value)
    
    def test_rate_limit_allows_after_period(self) -> None:
        """Test that rate limit resets after period."""
        
        @rate_limit(max_calls=1, period=0.1)
        def limited_func() -> str:
            return "success"
        
        # First call succeeds
        assert limited_func() == "success"
        
        # Wait for period to expire
        time.sleep(0.15)
        
        # Should be able to call again
        assert limited_func() == "success"
    
    def test_rate_limit_with_api_call(self) -> None:
        """Test rate limit with api_call function."""
        # Make calls up to limit
        api_call("/users")
        api_call("/posts")
        api_call("/comments")
        
        # Next call should fail
        with pytest.raises(RuntimeError):
            api_call("/data")


class TestRateLimitEdgeCases:
    """Tests for rate limit edge cases."""
    
    def test_rate_limit_preserves_function_name(self) -> None:
        """Test that rate limit preserves function name."""
        assert api_call.__name__ == "api_call"
    
    def test_rate_limit_with_kwargs(self) -> None:
        """Test rate limit with keyword arguments."""
        
        @rate_limit(max_calls=5, period=1.0)
        def func_with_kwargs(value: str, prefix: str = "") -> str:
            return prefix + value
        
        assert func_with_kwargs("test") == "test"
        assert func_with_kwargs("test", prefix="pre_") == "pre_test"
    
    def test_rate_limit_different_functions_independent(self) -> None:
        """Test that different rate-limited functions have independent limits."""
        
        @rate_limit(max_calls=1, period=1.0)
        def func1() -> str:
            return "func1"
        
        @rate_limit(max_calls=1, period=1.0)
        def func2() -> str:
            return "func2"
        
        # Each should be able to call once
        assert func1() == "func1"
        assert func2() == "func2"
        
        # Both should be rate limited now
        with pytest.raises(RuntimeError):
            func1()
        
        with pytest.raises(RuntimeError):
            func2()
