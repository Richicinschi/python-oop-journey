"""Tests for Problem 04: Validate Types Decorator."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day03.problem_04_validate_types_decorator import (
    validate_types, add, greet, optional_value
)


class TestValidateTypesDecorator:
    """Tests for the validate_types decorator."""
    
    def test_validate_types_accepts_correct_types(self) -> None:
        """Test that valid types are accepted."""
        assert add(1, 2) == 3
        assert add(0, 0) == 0
        assert add(-5, 10) == 5
    
    def test_validate_types_rejects_wrong_type_first_arg(self) -> None:
        """Test that wrong type for first arg raises TypeError."""
        with pytest.raises(TypeError) as exc_info:
            add("1", 2)
        assert "int" in str(exc_info.value)
    
    def test_validate_types_rejects_wrong_type_second_arg(self) -> None:
        """Test that wrong type for second arg raises TypeError."""
        with pytest.raises(TypeError) as exc_info:
            add(1, "2")
        assert "int" in str(exc_info.value)
    
    def test_validate_types_multiple_args(self) -> None:
        """Test validation with multiple different typed args."""
        assert greet("Alice", 25) == "Hello Alice, you are 25 years old"
        
        with pytest.raises(TypeError):
            greet(123, 25)  # name should be str
        
        with pytest.raises(TypeError):
            greet("Alice", "25")  # age should be int
    
    def test_validate_types_preserves_function_name(self) -> None:
        """Test that decorator preserves function name."""
        assert add.__name__ == "add"
    
    def test_validate_types_preserves_docstring(self) -> None:
        """Test that decorator preserves docstring."""
        assert add.__doc__ == "Add two integers."


class TestValidateTypesOptional:
    """Tests for optional type validation."""
    
    def test_optional_accepts_none(self) -> None:
        """Test that None is accepted for Optional types."""
        assert optional_value(None) == "None"
    
    def test_optional_accepts_value(self) -> None:
        """Test that actual value is accepted."""
        assert optional_value(42) == "42"
    
    def test_optional_rejects_wrong_type(self) -> None:
        """Test that wrong non-None type is rejected."""
        with pytest.raises(TypeError):
            optional_value("string")


class TestValidateTypesEdgeCases:
    """Tests for validate_types edge cases."""
    
    def test_validate_types_with_no_hints(self) -> None:
        """Test function with no type hints passes through."""
        
        @validate_types
        def no_hints(a, b):
            return a + b
        
        # Should work with any types since no hints
        assert no_hints(1, 2) == 3
        assert no_hints("a", "b") == "ab"
    
    def test_validate_types_with_kwargs(self) -> None:
        """Test validation with keyword arguments."""
        
        @validate_types
        def func(a: int, b: str) -> str:
            return f"{a}: {b}"
        
        assert func(a=1, b="test") == "1: test"
        
        with pytest.raises(TypeError):
            func(a="wrong", b="test")
