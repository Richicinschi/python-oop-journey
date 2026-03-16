"""Tests for Problem 11: Debug Decorator."""

from __future__ import annotations

import pytest
from io import StringIO
from unittest.mock import patch

from week05_oop_advanced.solutions.day03.problem_11_debug_decorator import (
    debug, add, greet, create_user
)


class TestDebugDecorator:
    """Tests for the debug decorator."""
    
    def test_debug_prints_call_info(self) -> None:
        """Test that debug prints function call information."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            add(3, 4)
            output = fake_stdout.getvalue()
        
        assert "DEBUG: Calling add(" in output
        assert "3" in output
        assert "4" in output
    
    def test_debug_prints_return_value(self) -> None:
        """Test that debug prints return value."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            add(3, 4)
            output = fake_stdout.getvalue()
        
        assert "DEBUG: add returned" in output
        assert "7" in output
    
    def test_debug_returns_correct_result(self) -> None:
        """Test that debug returns the correct result."""
        with patch('sys.stdout', new=StringIO()):
            result = add(10, 20)
        
        assert result == 30
    
    def test_debug_with_kwargs(self) -> None:
        """Test debug with keyword arguments."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            greet("Alice", greeting="Hi")
            output = fake_stdout.getvalue()
        
        assert "DEBUG: Calling greet(" in output
        assert "Alice" in output
        assert "Hi" in output
    
    def test_debug_with_complex_return(self) -> None:
        """Test debug with complex return value."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            result = create_user("alice", 25, active=True)
            output = fake_stdout.getvalue()
        
        assert result["username"] == "alice"
        assert result["age"] == 25
        assert result["active"] is True
        assert "DEBUG: create_user returned" in output


class TestDebugEdgeCases:
    """Tests for debug edge cases."""
    
    def test_debug_preserves_function_name(self) -> None:
        """Test that debug preserves function name."""
        assert add.__name__ == "add"
    
    def test_debug_preserves_docstring(self) -> None:
        """Test that debug preserves docstring."""
        assert add.__doc__ == "Add two numbers."
    
    def test_debug_with_no_args(self) -> None:
        """Test debug with function that takes no arguments."""
        
        @debug
        def no_args() -> str:
            return "no args"
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            result = no_args()
            output = fake_stdout.getvalue()
        
        assert result == "no args"
        assert "DEBUG: Calling no_args()" in output
        assert "no args" in output
