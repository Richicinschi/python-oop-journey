"""Tests for Problem 01: Inventory Item."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day02.problem_01_inventory_item import (
    InventoryItem,
)


class TestInventoryItem:
    """Test suite for InventoryItem class."""
    
    def test_init(self) -> None:
        """Test basic initialization."""
        item = InventoryItem("Laptop", 999.99, 5)
        assert item.name == "Laptop"
        assert item.price == 999.99
        assert item.quantity == 5
    
    def test_get_total_value(self) -> None:
        """Test get_total_value method."""
        item = InventoryItem("Laptop", 100.0, 5)
        assert item.get_total_value() == 500.0
        
        item2 = InventoryItem("Mouse", 25.5, 4)
        assert item2.get_total_value() == 102.0
    
    def test_get_total_value_with_zero_quantity(self) -> None:
        """Test total value with zero quantity."""
        item = InventoryItem("Empty", 100.0, 0)
        assert item.get_total_value() == 0.0


class TestFromString:
    """Test suite for from_string class method."""
    
    def test_from_string_basic(self) -> None:
        """Test from_string with basic input."""
        item = InventoryItem.from_string("Mouse,29.99,10")
        assert item.name == "Mouse"
        assert item.price == 29.99
        assert item.quantity == 10
    
    def test_from_string_with_spaces_in_name(self) -> None:
        """Test from_string with spaces in name."""
        item = InventoryItem.from_string("Wireless Keyboard,49.99,3")
        assert item.name == "Wireless Keyboard"
        assert item.price == 49.99
        assert item.quantity == 3
    
    def test_from_string_returns_correct_type(self) -> None:
        """Test that from_string returns an InventoryItem instance."""
        item = InventoryItem.from_string("Test,10.0,1")
        assert isinstance(item, InventoryItem)
    
    def test_from_string_and_total_value(self) -> None:
        """Test that from_string creates item with correct total value."""
        item = InventoryItem.from_string("Chair,150.0,4")
        assert item.get_total_value() == 600.0
