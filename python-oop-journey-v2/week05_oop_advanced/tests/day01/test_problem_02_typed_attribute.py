"""Tests for Problem 02: Typed Attribute."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day01.problem_02_typed_attribute import (
    TypedAttribute, Student, Config
)


class TestTypedAttribute:
    """Tests for the TypedAttribute descriptor."""
    
    def test_descriptor_returns_self_on_class_access(self) -> None:
        descriptor = Student.__dict__['name']
        assert isinstance(descriptor, TypedAttribute)
    
    def test_valid_type_accepted(self) -> None:
        student = Student("Alice", 20, 3.5)
        assert student.name == "Alice"
        assert student.age == 20
        assert student.gpa == 3.5
    
    def test_invalid_type_raises_error(self) -> None:
        student = Student("Alice", 20, 3.5)
        
        with pytest.raises(TypeError):
            student.name = 123
        
        with pytest.raises(TypeError):
            student.age = "twenty"
        
        with pytest.raises(TypeError):
            student.gpa = "four"
    
    def test_error_message_includes_type_info(self) -> None:
        student = Student("Alice", 20, 3.5)
        
        with pytest.raises(TypeError, match="must be of type"):
            student.name = 123
    
    def test_default_value(self) -> None:
        class TestClass:
            value = TypedAttribute(int, default=42)
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        assert obj.value == 42


class TestStudent:
    """Tests for the Student class."""
    
    def test_student_creation(self) -> None:
        student = Student("Alice", 20, 3.5)
        assert student.name == "Alice"
        assert student.age == 20
        assert student.gpa == 3.5
        assert student.grades == []
    
    def test_name_must_be_string(self) -> None:
        with pytest.raises(TypeError):
            _ = Student(123, 20, 3.5)
    
    def test_age_must_be_int(self) -> None:
        with pytest.raises(TypeError):
            _ = Student("Alice", 20.5, 3.5)
    
    def test_gpa_must_be_float(self) -> None:
        # Note: int is accepted since int is subclass of float in type checking
        student = Student("Alice", 20, 3)
        # But let's verify float requirement for non-int
        with pytest.raises(TypeError):
            student.gpa = "3.5"
    
    def test_grades_must_be_list(self) -> None:
        student = Student("Alice", 20, 3.5)
        with pytest.raises(TypeError):
            student.grades = (1, 2, 3)


class TestConfig:
    """Tests for the Config class."""
    
    def test_default_values(self) -> None:
        config = Config()
        assert config.debug is False
        assert config.port == 8080
        assert config.host == "localhost"
    
    def test_custom_values(self) -> None:
        config = Config(debug=True, port=3000, host="example.com")
        assert config.debug is True
        assert config.port == 3000
        assert config.host == "example.com"
    
    def test_type_checking(self) -> None:
        config = Config()
        
        with pytest.raises(TypeError):
            config.debug = "yes"
        
        with pytest.raises(TypeError):
            config.port = "8080"
        
        with pytest.raises(TypeError):
            config.host = 123
