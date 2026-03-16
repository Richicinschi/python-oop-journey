"""Problem 05: Restaurant Menu.

Implement a Restaurant class that composes MenuItems and aggregates Orders.
This demonstrates composition (menu items owned by restaurant) and aggregation (orders created externally).

Classes to implement:
- MenuItem: with attributes name, price, category
- Order: with attributes items, table_number, status
- Restaurant: composes MenuItems, aggregates Orders

Methods required:
- MenuItem.get_price() -> float
- Order.add_item(item: MenuItem) -> None
- Order.get_total() -> float
- Order.set_status(status: str) -> None
- Restaurant.add_menu_item(item: MenuItem) - composition
- Restaurant.place_order(order: Order) - aggregation
- Restaurant.get_menu_by_category(category: str) -> list[MenuItem]
"""

from __future__ import annotations
from typing import Optional


class MenuItem:
    """A menu item owned by the restaurant."""
    
    def __init__(self, name: str, price: float, category: str) -> None:
        # TODO: Initialize name, price, category
        pass
    
    def get_price(self) -> float:
        # TODO: Return price
        pass


class Order:
    """An order created by customers."""
    
    def __init__(self, table_number: int) -> None:
        # TODO: Initialize table_number, items (empty list), status ('pending')
        pass
    
    def add_item(self, item: MenuItem) -> None:
        # TODO: Add menu item to order
        pass
    
    def remove_item(self, item_name: str) -> bool:
        # TODO: Remove first item matching name, return True if found
        pass
    
    def get_total(self) -> float:
        # TODO: Return sum of all item prices
        pass
    
    def set_status(self, status: str) -> None:
        # TODO: Set order status (pending, preparing, ready, served)
        pass


class Restaurant:
    """A restaurant composing menu items and aggregating orders."""
    
    def __init__(self, name: str) -> None:
        # TODO: Initialize name, menu_items (empty list), orders (empty list)
        pass
    
    def add_menu_item(self, item: MenuItem) -> None:
        # TODO: Add menu item to restaurant's menu
        pass
    
    def get_menu(self) -> list[MenuItem]:
        # TODO: Return all menu items
        pass
    
    def get_menu_by_category(self, category: str) -> list[MenuItem]:
        # TODO: Return menu items matching category
        pass
    
    def place_order(self, order: Order) -> str:
        # TODO: Add order to restaurant's orders, return confirmation
        pass
    
    def get_pending_orders(self) -> list[Order]:
        # TODO: Return orders with status 'pending'
        pass
    
    def complete_order(self, order_index: int) -> str:
        # TODO: Mark order as served by index, return status
        pass
