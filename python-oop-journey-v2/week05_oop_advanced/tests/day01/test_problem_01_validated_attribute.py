"""Tests for Problem 01: Validated Attribute."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day01.problem_01_validated_attribute import (
    ValidatedAttribute, Person, Product
)


class TestValidatedAttribute:
    """Tests for the ValidatedAttribute descriptor."""
    
    def test_descriptor_returns_self_on_class_access(self) -> None:
        descriptor = Person.__dict__['age']
        assert isinstance(descriptor, ValidatedAttribute)
    
    def test_valid_value_accepted(self) -> None:
        person = Person("Alice", 30)
        assert person.age == 30
    
    def test_invalid_value_raises_error(self) -> None:
        person = Person("Alice", 30)
        with pytest.raises(ValueError):
            person.age = 200
    
    def test_name_validation(self) -> None:
        person = Person("Bob", 25)
        assert person.name == "Bob"
        
        with pytest.raises(ValueError):
            person.name = ""  # Empty string not allowed
    
    def test_default_value(self) -> None:
        class TestClass:
            attr = ValidatedAttribute(default="default_value")
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        assert obj.attr == "default_value"
    
    def test_validation_error_message(self) -> None:
        person = Person("Alice", 30)
        with pytest.raises(ValueError, match="Invalid value"):
            person.age = -5


class TestPerson:
    """Tests for the Person class."""
    
    def test_person_creation_valid(self) -> None:
        person = Person("Alice", 30)
        assert person.name == "Alice"
        assert person.age == 30
    
    def test_person_name_must_be_string(self) -> None:
        with pytest.raises(ValueError):
            person = Person("Alice", 30)
            person.name = 123
    
    def test_person_age_range(self) -> None:
        person = Person("Alice", 30)
        
        # Valid ages
        person.age = 0
        assert person.age == 0
        
        person.age = 150
        assert person.age == 150
        
        # Invalid ages
        with pytest.raises(ValueError):
            person.age = -1
        
        with pytest.raises(ValueError):
            person.age = 151
    
    def test_person_name_non_empty(self) -> None:
        with pytest.raises(ValueError):
            _ = Person("", 30)


class TestProduct:
    """Tests for the Product class."""
    
    def test_product_creation(self) -> None:
        product = Product("Widget", 19.99)
        assert product.name == "Widget"
        assert product.price == 19.99
    
    def test_product_price_must_be_positive(self) -> None:
        with pytest.raises(ValueError):
            _ = Product("Widget", -5.0)
        
        with pytest.raises(ValueError):
            _ = Product("Widget", 0)
    
    def test_product_price_type(self) -> None:
        with pytest.raises(ValueError):
            product = Product("Widget", 10.0)
            product.price = "free"
