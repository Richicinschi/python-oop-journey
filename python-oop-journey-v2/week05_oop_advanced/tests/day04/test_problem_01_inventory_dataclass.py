"""Tests for Problem 01: Inventory Dataclass."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day04.problem_01_inventory_dataclass import (
    Product
)


class TestProductBasics:
    """Tests for basic Product functionality."""
    
    def test_product_creation(self) -> None:
        """Test creating a Product with all fields."""
        product = Product(
            sku="LAPTOP-001",
            name="Gaming Laptop",
            price=999.99,
            quantity=10,
            category="electronics",
            tags=["gaming", "laptop"]
        )
        
        assert product.sku == "LAPTOP-001"
        assert product.name == "Gaming Laptop"
        assert product.price == 999.99
        assert product.quantity == 10
        assert product.category == "electronics"
        assert product.tags == ["gaming", "laptop"]
    
    def test_product_defaults(self) -> None:
        """Test default values for optional fields."""
        product = Product(sku="TEST-001", name="Test Product", price=10.0)
        
        assert product.quantity == 0
        assert product.category == "general"
        assert product.tags == []
    
    def test_product_repr(self) -> None:
        """Test that repr shows all fields."""
        product = Product(sku="SKU-001", name="Test", price=50.0, quantity=5)
        repr_str = repr(product)
        
        assert "Product" in repr_str
        assert "sku='SKU-001'" in repr_str
        assert "name='Test'" in repr_str
        assert "price=50.0" in repr_str
        assert "quantity=5" in repr_str


class TestProductEquality:
    """Tests for Product equality comparison."""
    
    def test_equal_products(self) -> None:
        """Test that identical products are equal."""
        p1 = Product(sku="SKU-001", name="Test", price=10.0, quantity=5)
        p2 = Product(sku="SKU-001", name="Test", price=10.0, quantity=5)
        
        assert p1 == p2
    
    def test_unequal_products(self) -> None:
        """Test that different products are not equal."""
        p1 = Product(sku="SKU-001", name="Test", price=10.0)
        p2 = Product(sku="SKU-002", name="Test", price=10.0)
        
        assert p1 != p2
    
    def test_different_quantity_not_equal(self) -> None:
        """Test that products with different quantities are not equal."""
        p1 = Product(sku="SKU-001", name="Test", price=10.0, quantity=5)
        p2 = Product(sku="SKU-001", name="Test", price=10.0, quantity=10)
        
        assert p1 != p2


class TestProductTotalValue:
    """Tests for total_value method."""
    
    def test_total_value_basic(self) -> None:
        """Test total value calculation."""
        product = Product(sku="SKU-001", name="Test", price=25.0, quantity=4)
        
        assert product.total_value() == 100.0
    
    def test_total_value_zero_quantity(self) -> None:
        """Test total value with zero quantity."""
        product = Product(sku="SKU-001", name="Test", price=100.0, quantity=0)
        
        assert product.total_value() == 0.0
    
    def test_total_value_decimal(self) -> None:
        """Test total value with decimal prices."""
        product = Product(sku="SKU-001", name="Test", price=9.99, quantity=3)
        
        assert product.total_value() == pytest.approx(29.97)


class TestProductInStock:
    """Tests for is_in_stock method."""
    
    def test_in_stock_positive(self) -> None:
        """Test product with quantity > 0 is in stock."""
        product = Product(sku="SKU-001", name="Test", price=10.0, quantity=5)
        
        assert product.is_in_stock() is True
    
    def test_in_stock_zero(self) -> None:
        """Test product with quantity = 0 is not in stock."""
        product = Product(sku="SKU-001", name="Test", price=10.0, quantity=0)
        
        assert product.is_in_stock() is False
    
    def test_in_stock_negative(self) -> None:
        """Test product with negative quantity."""
        product = Product(sku="SKU-001", name="Test", price=10.0, quantity=-1)
        
        assert product.is_in_stock() is False


class TestProductAddTags:
    """Tests for add_tags method."""
    
    def test_add_single_tag(self) -> None:
        """Test adding a single tag."""
        product = Product(sku="SKU-001", name="Test", price=10.0)
        product.add_tags("new")
        
        assert "new" in product.tags
    
    def test_add_multiple_tags(self) -> None:
        """Test adding multiple tags at once."""
        product = Product(sku="SKU-001", name="Test", price=10.0)
        product.add_tags("tag1", "tag2", "tag3")
        
        assert product.tags == ["tag1", "tag2", "tag3"]
    
    def test_add_tags_preserves_existing(self) -> None:
        """Test that adding tags preserves existing ones."""
        product = Product(
            sku="SKU-001", name="Test", price=10.0, tags=["existing"]
        )
        product.add_tags("new1", "new2")
        
        assert "existing" in product.tags
        assert "new1" in product.tags
        assert "new2" in product.tags


class TestProductToDict:
    """Tests for to_dict method."""
    
    def test_to_dict_basic(self) -> None:
        """Test conversion to dictionary."""
        product = Product(
            sku="SKU-001",
            name="Test Product",
            price=50.0,
            quantity=10,
            category="test",
            tags=["tag1", "tag2"]
        )
        
        result = product.to_dict()
        
        assert result["sku"] == "SKU-001"
        assert result["name"] == "Test Product"
        assert result["price"] == 50.0
        assert result["quantity"] == 10
        assert result["category"] == "test"
        assert result["tags"] == ["tag1", "tag2"]
    
    def test_to_dict_returns_copy(self) -> None:
        """Test that to_dict returns a copy, not a reference."""
        product = Product(
            sku="SKU-001", name="Test", price=10.0, tags=["tag1"]
        )
        
        result = product.to_dict()
        result["tags"].append("tag2")
        
        # Original should be unchanged
        assert product.tags == ["tag1"]


class TestProductImmutability:
    """Tests to verify dataclass behavior."""
    
    def test_tags_is_mutable(self) -> None:
        """Test that tags list is mutable (default dataclass behavior)."""
        product = Product(sku="SKU-001", name="Test", price=10.0)
        
        # Should be able to modify the list
        product.tags.append("new_tag")
        assert "new_tag" in product.tags
    
    def test_field_modification(self) -> None:
        """Test that fields can be modified (non-frozen dataclass)."""
        product = Product(sku="SKU-001", name="Test", price=10.0, quantity=5)
        
        product.quantity = 10
        assert product.quantity == 10
