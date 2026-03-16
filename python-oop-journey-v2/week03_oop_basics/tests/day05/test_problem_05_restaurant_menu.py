"""Tests for Problem 05: Restaurant Menu."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day05.problem_05_restaurant_menu import (
    MenuItem,
    Order,
    Restaurant,
)


class TestMenuItem:
    """Tests for MenuItem class."""
    
    def test_menu_item_init(self) -> None:
        """Test menu item initialization."""
        item = MenuItem("Burger", 12.99, "main")
        assert item.name == "Burger"
        assert item.price == 12.99
        assert item.category == "main"
    
    def test_menu_item_get_price(self) -> None:
        """Test getting menu item price."""
        item = MenuItem("Burger", 12.99, "main")
        assert item.get_price() == 12.99


class TestOrder:
    """Tests for Order class."""
    
    def test_order_init(self) -> None:
        """Test order initialization."""
        order = Order(5)
        assert order.table_number == 5
        assert order.items == []
        assert order.status == "pending"
    
    def test_order_add_item(self) -> None:
        """Test adding item to order."""
        order = Order(5)
        item = MenuItem("Burger", 12.99, "main")
        order.add_item(item)
        assert len(order.items) == 1
    
    def test_order_remove_item(self) -> None:
        """Test removing item from order."""
        order = Order(5)
        item = MenuItem("Burger", 12.99, "main")
        order.add_item(item)
        result = order.remove_item("Burger")
        assert result is True
        assert len(order.items) == 0
    
    def test_order_remove_item_not_found(self) -> None:
        """Test removing non-existent item."""
        order = Order(5)
        result = order.remove_item("Pizza")
        assert result is False
    
    def test_order_get_total(self) -> None:
        """Test calculating order total."""
        order = Order(5)
        order.add_item(MenuItem("Burger", 12.99, "main"))
        order.add_item(MenuItem("Fries", 4.99, "side"))
        assert order.get_total() == 17.98
    
    def test_order_get_total_empty(self) -> None:
        """Test total of empty order."""
        order = Order(5)
        assert order.get_total() == 0.0
    
    def test_order_set_status(self) -> None:
        """Test setting order status."""
        order = Order(5)
        order.set_status("ready")
        assert order.status == "ready"


class TestRestaurant:
    """Tests for Restaurant class."""
    
    def test_restaurant_init(self) -> None:
        """Test restaurant initialization."""
        restaurant = Restaurant("Bistro")
        assert restaurant.name == "Bistro"
        assert restaurant.menu_items == []
        assert restaurant.orders == []
    
    def test_add_menu_item(self) -> None:
        """Test adding menu item."""
        restaurant = Restaurant("Bistro")
        item = MenuItem("Burger", 12.99, "main")
        restaurant.add_menu_item(item)
        assert len(restaurant.menu_items) == 1
    
    def test_get_menu(self) -> None:
        """Test getting menu."""
        restaurant = Restaurant("Bistro")
        item = MenuItem("Burger", 12.99, "main")
        restaurant.add_menu_item(item)
        menu = restaurant.get_menu()
        assert len(menu) == 1
    
    def test_get_menu_by_category(self) -> None:
        """Test getting menu by category."""
        restaurant = Restaurant("Bistro")
        restaurant.add_menu_item(MenuItem("Burger", 12.99, "main"))
        restaurant.add_menu_item(MenuItem("Cake", 6.99, "dessert"))
        restaurant.add_menu_item(MenuItem("Pizza", 14.99, "main"))
        
        mains = restaurant.get_menu_by_category("main")
        assert len(mains) == 2
        assert all(item.category == "main" for item in mains)
    
    def test_place_order(self) -> None:
        """Test placing an order."""
        restaurant = Restaurant("Bistro")
        order = Order(5)
        result = restaurant.place_order(order)
        assert "order placed" in result.lower()
        assert len(restaurant.orders) == 1
    
    def test_get_pending_orders(self) -> None:
        """Test getting pending orders."""
        restaurant = Restaurant("Bistro")
        order1 = Order(1)
        order2 = Order(2)
        order2.set_status("ready")
        restaurant.place_order(order1)
        restaurant.place_order(order2)
        
        pending = restaurant.get_pending_orders()
        assert len(pending) == 1
        assert pending[0].table_number == 1
    
    def test_complete_order(self) -> None:
        """Test completing an order."""
        restaurant = Restaurant("Bistro")
        order = Order(5)
        restaurant.place_order(order)
        result = restaurant.complete_order(0)
        assert "completed" in result.lower()
        assert order.status == "served"
    
    def test_complete_order_invalid_index(self) -> None:
        """Test completing order with invalid index."""
        restaurant = Restaurant("Bistro")
        result = restaurant.complete_order(0)
        assert "invalid" in result.lower()
    
    def test_get_menu_item_by_name(self) -> None:
        """Test finding menu item by name."""
        restaurant = Restaurant("Bistro")
        item = MenuItem("Burger", 12.99, "main")
        restaurant.add_menu_item(item)
        found = restaurant.get_menu_item_by_name("Burger")
        assert found is item
    
    def test_get_menu_item_by_name_not_found(self) -> None:
        """Test finding non-existent menu item."""
        restaurant = Restaurant("Bistro")
        found = restaurant.get_menu_item_by_name("Pizza")
        assert found is None
