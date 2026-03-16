"""Tests for Problem 03: Product Catalog Item."""

from __future__ import annotations

from week03_oop_basics.solutions.day04.problem_03_product_catalog_item import (
    ProductCatalogItem,
)


class TestProductCatalogItemInit:
    """Test ProductCatalogItem initialization."""
    
    def test_init_basic(self) -> None:
        p = ProductCatalogItem("ABC123", "Widget", 29.99, "Tools")
        assert p.sku == "ABC123"
        assert p.name == "Widget"
        assert p.price == 29.99
        assert p.category == "Tools"
    
    def test_sku_is_immutable(self) -> None:
        p = ProductCatalogItem("ABC123", "Widget", 29.99, "Tools")
        # sku should be read-only property
        with pytest.raises(AttributeError):
            p.sku = "DEF456"


class TestProductCatalogItemEquality:
    """Test ProductCatalogItem equality."""
    
    def test_equal_same_sku(self) -> None:
        p1 = ProductCatalogItem("ABC123", "Widget", 29.99, "Tools")
        p2 = ProductCatalogItem("ABC123", "Different Name", 39.99, "Other")
        assert p1 == p2
    
    def test_not_equal_different_sku(self) -> None:
        p1 = ProductCatalogItem("ABC123", "Widget", 29.99, "Tools")
        p2 = ProductCatalogItem("DEF456", "Widget", 29.99, "Tools")
        assert p1 != p2
    
    def test_not_equal_non_product(self) -> None:
        p = ProductCatalogItem("ABC123", "Widget", 29.99, "Tools")
        assert p != "ABC123"
        assert p != None
        assert p != 123


class TestProductCatalogItemHash:
    """Test ProductCatalogItem hashing."""
    
    def test_hash_same_for_equal_products(self) -> None:
        p1 = ProductCatalogItem("ABC123", "Widget", 29.99, "Tools")
        p2 = ProductCatalogItem("ABC123", "Different", 39.99, "Other")
        assert hash(p1) == hash(p2)
    
    def test_hash_can_be_used_in_set(self) -> None:
        p1 = ProductCatalogItem("ABC123", "Widget", 29.99, "Tools")
        p2 = ProductCatalogItem("ABC123", "Widget Pro", 39.99, "Tools")
        p3 = ProductCatalogItem("DEF456", "Gadget", 19.99, "Tools")
        product_set = {p1, p2, p3}
        assert len(product_set) == 2
    
    def test_hash_can_be_used_as_dict_key(self) -> None:
        p1 = ProductCatalogItem("ABC123", "Widget", 29.99, "Tools")
        inventory = {p1: 10}
        # Same SKU should access the same dict entry
        p2 = ProductCatalogItem("ABC123", "Different Name", 39.99, "Other")
        assert inventory[p2] == 10


class TestProductCatalogItemRepr:
    """Test ProductCatalogItem representation."""
    
    def test_repr(self) -> None:
        p = ProductCatalogItem("ABC123", "Widget", 29.99, "Tools")
        expected = "ProductCatalogItem(sku='ABC123', name='Widget', price=29.99, category='Tools')"
        assert repr(p) == expected


class TestProductCatalogItemStr:
    """Test ProductCatalogItem string representation."""
    
    def test_str(self) -> None:
        p = ProductCatalogItem("ABC123", "Widget", 29.99, "Tools")
        assert str(p) == "Widget (ABC123) - $29.99"


import pytest
