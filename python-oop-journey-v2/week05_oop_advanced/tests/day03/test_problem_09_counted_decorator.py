"""Tests for Problem 09: Counted Decorator."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day03.problem_09_counted_decorator import (
    counted, increment, greet, factorial
)


class TestCountedDecorator:
    """Tests for the counted decorator."""
    
    def test_counted_starts_at_zero(self) -> None:
        """Test that call_count starts at 0."""
        
        @counted
        def test_func() -> str:
            return "test"
        
        assert test_func.call_count == 0
    
    def test_counted_increments_on_call(self) -> None:
        """Test that call_count increments on each call."""
        
        @counted
        def test_func() -> str:
            return "test"
        
        test_func()
        assert test_func.call_count == 1
        
        test_func()
        assert test_func.call_count == 2
        
        test_func()
        assert test_func.call_count == 3
    
    def test_counted_works_with_args(self) -> None:
        """Test counted with function arguments."""
        assert increment.call_count >= 0  # May have been called in other tests
        
        initial_count = increment.call_count
        
        increment(5)
        assert increment.call_count == initial_count + 1
        
        increment(10)
        assert increment.call_count == initial_count + 2
    
    def test_counted_works_with_kwargs(self) -> None:
        """Test counted with keyword arguments."""
        initial_count = greet.call_count
        
        greet("Alice")
        greet("Bob", greeting="Hi")
        
        assert greet.call_count == initial_count + 2
    
    def test_counted_returns_correct_result(self) -> None:
        """Test that counted doesn't affect return value."""
        assert increment(5) == 6
        assert greet("Alice") == "Hello, Alice!"


class TestCountedFactorial:
    """Tests for counted factorial (recursive function)."""
    
    def test_counted_factorial(self) -> None:
        """Test counted with recursive function."""
        # Note: Each recursive call increments the counter
        factorial.call_count = 0  # Reset
        
        result = factorial(5)
        
        assert result == 120
        # factorial(5) calls factorial(4) calls factorial(3) ... calls factorial(1)
        # That's 5 calls total (5, 4, 3, 2, 1)
        assert factorial.call_count == 5


class TestCountedEdgeCases:
    """Tests for counted edge cases."""
    
    def test_counted_preserves_function_name(self) -> None:
        """Test that counted preserves function name."""
        assert increment.__name__ == "increment"
    
    def test_counted_preserves_docstring(self) -> None:
        """Test that counted preserves docstring."""
        assert increment.__doc__ == "Increment a number."
