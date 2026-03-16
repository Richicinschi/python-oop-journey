"""Tests for Problem 05: Logged Class Decorator."""

from __future__ import annotations

import pytest
from io import StringIO
from unittest.mock import patch

from week05_oop_advanced.solutions.day03.problem_05_logged_class_decorator import (
    logged, Calculator, Greeter
)


class TestLoggedClassDecorator:
    """Tests for the logged class decorator."""
    
    def test_logged_class_logs_method_calls(self) -> None:
        """Test that method calls are logged."""
        calc = Calculator()
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            result = calc.add(3, 4)
            output = fake_stdout.getvalue()
        
        assert result == 7
        assert "Calling add" in output
        assert "args=(3, 4)" in output or "args=(3.0, 4.0)" in output
    
    def test_logged_class_logs_multiple_methods(self) -> None:
        """Test that different methods are logged correctly."""
        calc = Calculator()
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            calc.add(1, 2)
            calc.subtract(10, 5)
            output = fake_stdout.getvalue()
        
        assert "Calling add" in output
        assert "Calling subtract" in output
    
    def test_logged_class_works_with_greeter(self) -> None:
        """Test logging with Greeter class."""
        greeter = Greeter("Hi")
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            result = greeter.greet("Bob")
            output = fake_stdout.getvalue()
        
        assert result == "Hi, Bob!"
        assert "Calling greet" in output
    
    def test_logged_class_preserves_method_functionality(self) -> None:
        """Test that logging doesn't break method functionality."""
        calc = Calculator()
        
        with patch('sys.stdout', new=StringIO()):
            calc.add(1, 2)
            calc.add(3, 4)
            history = calc.get_history()
        
        assert len(history) == 2
        assert "add(1" in history[0] and "= 3" in history[0]
    
    def test_logged_class_preserves_return_values(self) -> None:
        """Test that return values are preserved."""
        calc = Calculator()
        
        with patch('sys.stdout', new=StringIO()):
            assert calc.add(5, 3) == 8
            assert calc.subtract(10, 4) == 6
            history = calc.get_history()
        assert len(history) == 2
        assert "add(5" in history[0] and "= 8" in history[0]
        assert "subtract(10" in history[1] and "= 6" in history[1]


class TestLoggedClassEdgeCases:
    """Tests for logged class edge cases."""
    
    def test_logged_class_does_not_log_magic_methods(self) -> None:
        """Test that magic methods like __init__ are not logged."""
        
        @logged
        class TestClass:
            def __init__(self) -> None:
                self.value = 42
            
            def get_value(self) -> int:
                return self.value
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            obj = TestClass()
            output = fake_stdout.getvalue()
        
        # __init__ should not be logged
        assert "Calling __init__" not in output
        assert "Calling get_value" not in output  # Not called yet
