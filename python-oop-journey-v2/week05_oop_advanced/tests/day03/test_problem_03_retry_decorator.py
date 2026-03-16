"""Tests for Problem 03: Retry Decorator."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day03.problem_03_retry_decorator import (
    retry, flaky_function, specific_exception_only, FlakyCounter
)


class TestRetryDecorator:
    """Tests for the retry decorator."""
    
    def test_retry_succeeds_after_failures(self) -> None:
        """Test that retry eventually succeeds after failures."""
        FlakyCounter.count = 0
        
        result = flaky_function()
        
        assert result == "Success!"
        assert FlakyCounter.count == 3
    
    def test_retry_respects_max_attempts(self) -> None:
        """Test that retry respects max_attempts parameter."""
        
        attempts = 0
        
        @retry(max_attempts=2, delay=0.01)
        def always_fails() -> str:
            nonlocal attempts
            attempts += 1
            raise RuntimeError("Always fails")
        
        with pytest.raises(RuntimeError):
            always_fails()
        
        assert attempts == 2
    
    def test_retry_no_delay(self) -> None:
        """Test that retry works without delay."""
        
        attempts = 0
        
        @retry(max_attempts=3)
        def fails_twice() -> str:
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise ValueError(f"Attempt {attempts}")
            return "Success"
        
        result = fails_twice()
        assert result == "Success"
        assert attempts == 3
    
    def test_retry_specific_exception(self) -> None:
        """Test that retry only catches specified exceptions."""
        
        attempts = 0
        
        @retry(max_attempts=3, exceptions=(ValueError,))
        def raises_type_error() -> str:
            nonlocal attempts
            attempts += 1
            raise TypeError("Should not be caught")
        
        with pytest.raises(TypeError):
            raises_type_error()
        
        assert attempts == 1  # Should not retry on TypeError
    
    def test_retry_on_success_no_retry(self) -> None:
        """Test that successful call doesn't retry."""
        
        attempts = 0
        
        @retry(max_attempts=5)
        def always_succeeds() -> str:
            nonlocal attempts
            attempts += 1
            return "Success"
        
        result = always_succeeds()
        
        assert result == "Success"
        assert attempts == 1


class TestRetrySpecificException:
    """Tests for specific exception handling."""
    
    def test_specific_exception_retries(self) -> None:
        """Test retry on specific exception type."""
        assert specific_exception_only(5) == 10
    
    def test_specific_exception_not_caught(self) -> None:
        """Test that non-matching exceptions are not caught."""
        
        @retry(max_attempts=3, exceptions=(ValueError, TypeError))
        def raises_key_error() -> str:
            raise KeyError("Not caught")
        
        with pytest.raises(KeyError):
            raises_key_error()


class TestRetryEdgeCases:
    """Tests for retry edge cases."""
    
    def test_retry_with_function_arguments(self) -> None:
        """Test retry with function arguments."""
        
        attempts = 0
        
        @retry(max_attempts=3)
        def divide(a: float, b: float) -> float:
            nonlocal attempts
            attempts += 1
            if attempts < 2:
                raise RuntimeError("Transient error")
            return a / b
        
        result = divide(10, 2)
        assert result == 5.0
    
    def test_retry_preserves_function_name(self) -> None:
        """Test that retry decorator preserves function name."""
        assert flaky_function.__name__ == "flaky_function"
