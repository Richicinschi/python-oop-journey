"""Tests for Problem 01: Timer Decorator."""

from __future__ import annotations

import pytest
from io import StringIO
from unittest.mock import patch

from week05_oop_advanced.solutions.day03.problem_01_timer_decorator import (
    timer, slow_function, add
)


class TestTimerDecorator:
    """Tests for the timer decorator."""
    
    def test_timer_preserves_function_name(self) -> None:
        """Test that timer preserves the original function name."""
        assert slow_function.__name__ == "slow_function"
    
    def test_timer_preserves_docstring(self) -> None:
        """Test that timer preserves the original docstring."""
        assert slow_function.__doc__ == "A slow function for testing."
    
    def test_timer_prints_elapsed_time(self) -> None:
        """Test that timer prints the elapsed time."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            result = slow_function()
            output = fake_stdout.getvalue()
        
        assert result == "Done"
        assert "slow_function took" in output
        assert "seconds" in output
    
    def test_timer_works_with_arguments(self) -> None:
        """Test that timer works with function arguments."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            result = add(3, 4)
            output = fake_stdout.getvalue()
        
        assert result == 7
        assert "add took" in output
    
    def test_timer_works_with_decorator_syntax(self) -> None:
        """Test that timer can be applied with decorator syntax."""
        
        @timer
        def multiply(a: int, b: int) -> int:
            """Multiply two numbers."""
            return a * b
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            result = multiply(5, 6)
            output = fake_stdout.getvalue()
        
        assert result == 30
        assert "multiply took" in output
    
    def test_timer_returns_correct_result(self) -> None:
        """Test that timer returns the correct function result."""
        with patch('sys.stdout', new=StringIO()):
            result = add(10, 20)
        
        assert result == 30


class TestTimerEdgeCases:
    """Tests for timer edge cases."""
    
    def test_timer_with_no_args(self) -> None:
        """Test timer with function that takes no arguments."""
        
        @timer
        def no_args() -> str:
            return "no args"
        
        with patch('sys.stdout', new=StringIO()):
            result = no_args()
        
        assert result == "no args"
    
    def test_timer_with_kwargs(self) -> None:
        """Test timer with keyword arguments."""
        
        @timer
        def with_kwargs(a: int, b: int = 0) -> int:
            return a + b
        
        with patch('sys.stdout', new=StringIO()):
            result = with_kwargs(5, b=3)
        
        assert result == 8
