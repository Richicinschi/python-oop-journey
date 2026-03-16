"""Tests for Problem 04: Cached Validated Objects."""

from __future__ import annotations

import time

import pytest

from week04_oop_intermediate.solutions.day04.problem_04_cached_validated_objects import (
    Cacheable,
    DataObject,
    Product,
    Validatable,
)


class TestCacheable:
    """Tests for the Cacheable mixin."""
    
    def test_cacheable_init(self) -> None:
        """Test Cacheable initialization."""
        
        class TestClass(Cacheable):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        assert obj._cache == {}
        assert obj._cache_timestamps == {}
        assert obj._default_ttl == 60
    
    def test_cacheable_set_and_get(self) -> None:
        """Test setting and getting cached values."""
        
        class TestClass(Cacheable):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        obj.cache_set("key1", "value1")
        
        assert obj.cache_get("key1") == "value1"
    
    def test_cacheable_has(self) -> None:
        """Test checking if key exists."""
        
        class TestClass(Cacheable):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        assert obj.cache_has("nonexistent") is False
        
        obj.cache_set("key", "value")
        assert obj.cache_has("key") is True
    
    def test_cacheable_get_missing_key(self) -> None:
        """Test getting a missing key raises KeyError."""
        
        class TestClass(Cacheable):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        with pytest.raises(KeyError):
            obj.cache_get("nonexistent")
    
    def test_cacheable_expiration(self) -> None:
        """Test that cache entries expire."""
        
        class TestClass(Cacheable):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        obj.cache_set("key", "value", ttl=0.05)  # 50ms TTL
        
        assert obj.cache_has("key") is True
        time.sleep(0.1)
        assert obj.cache_has("key") is False
        
        with pytest.raises(KeyError):
            obj.cache_get("key")
    
    def test_cacheable_clear(self) -> None:
        """Test clearing the cache."""
        
        class TestClass(Cacheable):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        obj.cache_set("key1", "value1")
        obj.cache_set("key2", "value2")
        
        obj.cache_clear()
        
        assert obj.cache_has("key1") is False
        assert obj.cache_has("key2") is False
        assert obj._cache == {}


class TestValidatable:
    """Tests for the Validatable mixin."""
    
    def test_validatable_default_validate(self) -> None:
        """Test default validation returns empty list."""
        
        class TestClass(Validatable):
            pass
        
        obj = TestClass()
        assert obj.validate() == []
        assert obj.is_valid() is True
    
    def test_validatable_custom_validation(self) -> None:
        """Test custom validation."""
        
        class TestClass(Validatable):
            def __init__(self, value: int) -> None:
                self.value = value
            
            def _validate(self) -> list[str]:
                if self.value < 0:
                    return ["value must be >= 0"]
                return []
        
        valid_obj = TestClass(10)
        assert valid_obj.validate() == []
        assert valid_obj.is_valid() is True
        
        invalid_obj = TestClass(-5)
        assert invalid_obj.validate() == ["value must be >= 0"]
        assert invalid_obj.is_valid() is False


class TestDataObject:
    """Tests for the DataObject class."""
    
    def test_data_object_init(self) -> None:
        """Test DataObject initialization."""
        data = {"name": "Test", "value": 42}
        obj = DataObject(1, data)
        
        assert obj.id == 1
        assert obj.get_data() == data
        assert obj.get_data() is not data  # Should be a copy
    
    def test_data_object_get(self) -> None:
        """Test getting values."""
        obj = DataObject(1, {"key": "value"})
        
        assert obj.get("key") == "value"
        assert obj.get("missing") is None
        assert obj.get("missing", "default") == "default"
    
    def test_data_object_set(self) -> None:
        """Test setting values."""
        obj = DataObject(1, {"key": "old"})
        
        obj.set("key", "new")
        
        assert obj.get("key") == "new"
    
    def test_data_object_set_clears_cache(self) -> None:
        """Test that set() clears the cache."""
        obj = DataObject(1, {"key": "value"})
        obj.cache_set("cached", "data")
        
        obj.set("key", "new")
        
        assert obj.cache_has("cached") is False
    
    def test_data_object_is_valid(self) -> None:
        """Test that DataObject is valid by default."""
        obj = DataObject(1, {})
        assert obj.is_valid() is True
    
    def test_data_object_mro(self) -> None:
        """Test DataObject's MRO."""
        expected_mro = (DataObject, Cacheable, Validatable, object)
        assert DataObject.__mro__ == expected_mro


class TestProduct:
    """Tests for the Product class."""
    
    def test_product_init(self) -> None:
        """Test Product initialization."""
        data = {"name": "Widget", "price": 10.0}
        product = Product(1, data)
        
        assert product.id == 1
        assert product.name == "Widget"
        assert product.price == 10.0
    
    def test_product_valid(self) -> None:
        """Test valid product."""
        product = Product(1, {"name": "Widget", "price": 10.0})
        
        assert product.is_valid() is True
        assert product.validate() == []
    
    def test_product_missing_name(self) -> None:
        """Test product without name."""
        product = Product(1, {"price": 10.0})
        
        assert product.is_valid() is False
        errors = product.validate()
        assert any("name" in error.lower() for error in errors)
    
    def test_product_empty_name(self) -> None:
        """Test product with empty name."""
        product = Product(1, {"name": "", "price": 10.0})
        
        assert product.is_valid() is False
    
    def test_product_missing_price(self) -> None:
        """Test product without price."""
        product = Product(1, {"name": "Widget"})
        
        assert product.is_valid() is False
        errors = product.validate()
        assert any("price" in error.lower() for error in errors)
    
    def test_product_negative_price(self) -> None:
        """Test product with negative price."""
        product = Product(1, {"name": "Widget", "price": -5.0})
        
        assert product.is_valid() is False
    
    def test_product_negative_quantity(self) -> None:
        """Test product with negative quantity."""
        product = Product(1, {"name": "Widget", "price": 10.0, "quantity": -1})
        
        assert product.is_valid() is False
    
    def test_product_get_total_value(self) -> None:
        """Test calculating total value."""
        product = Product(1, {"name": "Widget", "price": 10.0, "quantity": 5})
        
        assert product.get_total_value() == 50.0
    
    def test_product_get_total_value_no_quantity(self) -> None:
        """Test calculating total value without quantity."""
        product = Product(1, {"name": "Widget", "price": 10.0})
        
        assert product.get_total_value() == 0.0
    
    def test_product_default_price(self) -> None:
        """Test default price is 0.0."""
        product = Product(1, {"name": "Widget"})
        assert product.price == 0.0
    
    def test_product_default_name(self) -> None:
        """Test default name is empty string."""
        product = Product(1, {"price": 10.0})
        assert product.name == ""
    
    def test_product_cache_functionality(self) -> None:
        """Test that Product inherits caching."""
        product = Product(1, {"name": "Widget", "price": 10.0})
        
        product.cache_set("computed_tax", 1.5)
        assert product.cache_get("computed_tax") == 1.5
    
    def test_product_multiple_validation_errors(self) -> None:
        """Test collecting multiple validation errors."""
        product = Product(1, {})
        
        errors = product.validate()
        assert len(errors) >= 2  # name and price errors
    
    def test_product_mro(self) -> None:
        """Test Product's MRO."""
        expected_mro = (Product, DataObject, Cacheable, Validatable, object)
        assert Product.__mro__ == expected_mro
