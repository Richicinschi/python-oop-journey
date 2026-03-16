"""Tests for Problem 12: Once Decorator."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day03.problem_12_once_decorator import (
    once, initialize, expensive_computation, configure
)


class TestOnceDecorator:
    """Tests for the once decorator."""
    
    def test_once_runs_only_once(self) -> None:
        """Test that decorated function runs only once."""
        call_count = 0
        
        @once
        def counter() -> int:
            nonlocal call_count
            call_count += 1
            return call_count
        
        result1 = counter()
        result2 = counter()
        result3 = counter()
        
        assert result1 == result2 == result3 == 1
        assert call_count == 1
    
    def test_once_returns_first_result(self) -> None:
        """Test that once returns result from first call."""
        
        @once
        def timestamp() -> float:
            import time
            return time.time()
        
        result1 = timestamp()
        # Even if we wait, we get the same result
        import time
        time.sleep(0.01)
        result2 = timestamp()
        
        assert result1 == result2
    
    def test_once_preserves_arguments_from_first_call(self) -> None:
        """Test that only first call's arguments are used."""
        
        @once
        def multiply(x: int, y: int) -> int:
            return x * y
        
        result1 = multiply(5, 6)  # 30
        result2 = multiply(10, 20)  # Should still return 30
        
        assert result1 == 30
        assert result2 == 30
    
    def test_once_with_configure(self) -> None:
        """Test once with configure function."""
        result1 = configure({"debug": True})
        result2 = configure({"debug": False})
        
        # Should return the first configuration
        assert result1 == {"debug": True}
        assert result2 == {"debug": True}


class TestOnceWithGlobals:
    """Tests for once using global state."""
    
    def test_once_initialize(self) -> None:
        """Test the global initialize function."""
        global call_count
        call_count = 0
        
        result1 = initialize()
        result2 = initialize()
        
        assert "Initialized" in result1
        assert result1 == result2


class TestOnceEdgeCases:
    """Tests for once edge cases."""
    
    def test_once_preserves_function_name(self) -> None:
        """Test that once preserves function name."""
        
        @once
        def test_func() -> str:
            return "test"
        
        assert test_func.__name__ == "test_func"
    
    def test_once_with_exception(self) -> None:
        """Test that once still marks as run even if function raises."""
        
        @once
        def may_fail() -> str:
            raise ValueError("Always fails")
        
        # First call raises
        with pytest.raises(ValueError):
            may_fail()
        
        # Subsequent calls don't raise (returns cached exception? or cached None?)
        # Implementation choice: we'll check if has_run is set
        assert may_fail.has_run is True
