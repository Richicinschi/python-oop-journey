"""Tests for Problem 04: Validation Metaclass."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day02.problem_04_validation_meta import (
    Product,
    User,
    ValidatedModel,
    ValidationMeta,
)


class TestValidationMeta:
    """Tests for the ValidationMeta metaclass."""
    
    def test_metaclass_exists(self) -> None:
        """Test that ValidationMeta is defined."""
        assert isinstance(ValidationMeta, type)
    
    def test_valid_class_creates_successfully(self) -> None:
        """Test that a valid class can be created."""
        # User class should already be defined and valid
        assert User.USERNAME_MIN_LENGTH == 3
        assert User.MAX_LOGIN_ATTEMPTS == 5
    
    def test_missing_required_attribute_fails(self) -> None:
        """Test that missing required attributes raise TypeError."""
        with pytest.raises(TypeError):
            class InvalidClass(metaclass=ValidationMeta):
                _validation_rules = {'missing_attr': {'type': str}}
    
    def test_type_validation(self) -> None:
        """Test type validation at class creation."""
        with pytest.raises(TypeError):
            class WrongType(metaclass=ValidationMeta):
                _validation_rules = {'count': {'type': int}}
                count = "not an int"
    
    def test_min_constraint(self) -> None:
        """Test min value constraint."""
        with pytest.raises(TypeError):
            class TooSmall(metaclass=ValidationMeta):
                _validation_rules = {'value': {'type': int, 'min': 10}}
                value = 5
    
    def test_min_length_constraint(self) -> None:
        """Test min length constraint for strings."""
        with pytest.raises(TypeError):
            class TooShort(metaclass=ValidationMeta):
                _validation_rules = {'name': {'type': str, 'min_length': 5}}
                name = "ab"


class TestValidatedModel:
    """Tests for the ValidatedModel base class."""
    
    def test_validated_model_init(self) -> None:
        """Test ValidatedModel initialization."""
        class TestModel(ValidatedModel):
            _validation_rules = {}
        
        model = TestModel(name="test")
        assert model.name == "test"


class TestUser:
    """Tests for the User model."""
    
    def test_user_class_valid(self) -> None:
        """Test that User class meets validation rules."""
        # User should be validly defined
        assert User.USERNAME_MIN_LENGTH >= 3
        assert User.MAX_LOGIN_ATTEMPTS >= 1
    
    def test_user_init(self) -> None:
        """Test User initialization."""
        user = User(username="alice")
        assert user.username == "alice"
    
    def test_user_validate_username(self) -> None:
        """Test username validation."""
        user = User()
        
        # Valid username (length >= 3)
        assert user.validate_username("alice") is True
        
        # Invalid username (length < 3)
        assert user.validate_username("ab") is False


class TestProduct:
    """Tests for the Product model."""
    
    def test_product_class_valid(self) -> None:
        """Test that Product class meets validation rules."""
        assert Product.MAX_PRICE > 0
        assert Product.name == ""
        assert Product.price == 0.0
    
    def test_product_init(self) -> None:
        """Test Product initialization."""
        product = Product(name="Widget", price=29.99)
        assert product.name == "Widget"
        assert product.price == 29.99
    
    def test_product_is_valid_price(self) -> None:
        """Test price validation."""
        product = Product()
        
        # Invalid: price = 0
        product.price = 0.0
        assert product.is_valid_price() is False
        
        # Invalid: price > MAX_PRICE
        product.price = Product.MAX_PRICE + 1
        assert product.is_valid_price() is False
        
        # Valid price
        product.price = 50.0
        assert product.is_valid_price() is True
