"""Tests for Problem 02: Class Registry Metaclass."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day02.problem_02_class_registry_meta import (
    BaseModel,
    Order,
    Product,
    RegistryMeta,
    User,
)


class TestRegistryMeta:
    """Tests for the RegistryMeta metaclass."""
    
    def setup_method(self) -> None:
        """Clear registry before each test."""
        RegistryMeta.clear_registry()
        # Force re-registration by re-importing or accessing
        # The classes are already imported, they'll be in registry
    
    def test_metaclass_exists(self) -> None:
        """Test that RegistryMeta is defined."""
        assert isinstance(RegistryMeta, type)
        assert RegistryMeta.__name__ == 'RegistryMeta'
    
    def test_base_class_not_registered(self) -> None:
        """Test that BaseModel is not in the registry."""
        # Note: The classes were already created before clear_registry
        # So we check that 'BaseModel' is not a registered name
        assert 'BaseModel' not in RegistryMeta.get_registry()
    
    def test_subclasses_registered(self) -> None:
        """Test that subclasses are automatically registered."""
        RegistryMeta.clear_registry()
        
        # Define a new class to trigger registration
        class TestModel(BaseModel):
            pass
        
        assert 'TestModel' in RegistryMeta.get_registry()
        assert RegistryMeta.get_registry()['TestModel'] is TestModel
    
    def test_get_registry_returns_copy(self) -> None:
        """Test that get_registry returns a copy."""
        RegistryMeta.clear_registry()
        
        class TestModel1(BaseModel):
            pass
        
        registry = RegistryMeta.get_registry()
        registry['fake'] = str
        
        # Original registry should not be modified
        assert 'fake' not in RegistryMeta._registry
    
    def test_get_class(self) -> None:
        """Test get_class method."""
        RegistryMeta.clear_registry()
        
        class TestModel2(BaseModel):
            pass
        
        assert RegistryMeta.get_class('TestModel2') is TestModel2
        assert RegistryMeta.get_class('NonExistent') is None
    
    def test_clear_registry(self) -> None:
        """Test clear_registry method."""
        class TestModel3(BaseModel):
            pass
        
        assert len(RegistryMeta.get_registry()) > 0
        RegistryMeta.clear_registry()
        assert len(RegistryMeta.get_registry()) == 0


class TestUser:
    """Tests for the User model."""
    
    def test_user_init(self) -> None:
        """Test User initialization."""
        user = User(username="alice", email="alice@example.com")
        assert user.username == "alice"
        assert user.email == "alice@example.com"
    
    def test_user_to_dict(self) -> None:
        """Test User to_dict method."""
        user = User(username="bob", email="bob@example.com")
        assert user.to_dict() == {'username': 'bob', 'email': 'bob@example.com'}
    
    def test_user_get_model_name(self) -> None:
        """Test User get_model_name method."""
        assert User.get_model_name() == "User"


class TestProduct:
    """Tests for the Product model."""
    
    def test_product_init(self) -> None:
        """Test Product initialization."""
        product = Product(name="Widget", price=9.99)
        assert product.name == "Widget"
        assert product.price == 9.99
    
    def test_product_to_dict(self) -> None:
        """Test Product to_dict method."""
        product = Product(name="Gadget", price=29.99)
        assert product.to_dict() == {'name': 'Gadget', 'price': 29.99}


class TestOrder:
    """Tests for the Order model."""
    
    def test_order_init(self) -> None:
        """Test Order initialization."""
        order = Order(order_id="ORD-001", total=99.99)
        assert order.order_id == "ORD-001"
        assert order.total == 99.99
    
    def test_order_to_dict(self) -> None:
        """Test Order to_dict method."""
        order = Order(order_id="ORD-002", total=50.00)
        assert order.to_dict() == {'order_id': 'ORD-002', 'total': 50.00}
