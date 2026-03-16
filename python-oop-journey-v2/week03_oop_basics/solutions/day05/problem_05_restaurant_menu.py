"""Solution for Problem 05: Restaurant Menu.

Restaurant with MenuItems and Orders - demonstrates composition
(menu items owned) and aggregation (orders created externally).
"""

from __future__ import annotations
from typing import Optional


class MenuItem:
    """A menu item owned by the restaurant.
    
    Menu items are composed by the restaurant - they exist only
    as part of the restaurant's menu.
    """
    
    def __init__(self, name: str, price: float, category: str) -> None:
        """Initialize the menu item.
        
        Args:
            name: Item name.
            price: Item price.
            category: Item category (e.g., 'appetizer', 'main', 'dessert').
        """
        self.name = name
        self.price = price
        self.category = category
    
    def get_price(self) -> float:
        """Get the item price.
        
        Returns:
            Price of the item.
        """
        return self.price


class Order:
    """An order created by customers.
    
    Orders are created externally and aggregated by the restaurant.
    They exist independently and can be moved between systems.
    """
    
    def __init__(self, table_number: int) -> None:
        """Initialize the order.
        
        Args:
            table_number: Table number for the order.
        """
        self.table_number = table_number
        self.items: list[MenuItem] = []
        self.status = "pending"
    
    def add_item(self, item: MenuItem) -> None:
        """Add a menu item to the order.
        
        Args:
            item: MenuItem to add.
        """
        self.items.append(item)
    
    def remove_item(self, item_name: str) -> bool:
        """Remove an item from the order.
        
        Args:
            item_name: Name of item to remove.
            
        Returns:
            True if item was removed, False if not found.
        """
        for i, item in enumerate(self.items):
            if item.name == item_name:
                self.items.pop(i)
                return True
        return False
    
    def get_total(self) -> float:
        """Calculate order total.
        
        Returns:
            Sum of all item prices.
        """
        return sum(item.get_price() for item in self.items)
    
    def set_status(self, status: str) -> None:
        """Set order status.
        
        Args:
            status: New status ('pending', 'preparing', 'ready', 'served').
        """
        self.status = status


class Restaurant:
    """A restaurant composing menu items and aggregating orders.
    
    Menu items are composed (owned by restaurant) while orders
    are aggregated (created externally).
    """
    
    def __init__(self, name: str) -> None:
        """Initialize the restaurant.
        
        Args:
            name: Restaurant name.
        """
        self.name = name
        self.menu_items: list[MenuItem] = []
        self.orders: list[Order] = []
    
    def add_menu_item(self, item: MenuItem) -> None:
        """Add a menu item to the restaurant.
        
        Args:
            item: MenuItem to add (composition).
        """
        self.menu_items.append(item)
    
    def get_menu(self) -> list[MenuItem]:
        """Get all menu items.
        
        Returns:
            List of all menu items.
        """
        return self.menu_items.copy()
    
    def get_menu_by_category(self, category: str) -> list[MenuItem]:
        """Get menu items by category.
        
        Args:
            category: Category to filter by.
            
        Returns:
            List of menu items in the category.
        """
        return [item for item in self.menu_items if item.category == category]
    
    def place_order(self, order: Order) -> str:
        """Place an order at the restaurant.
        
        Args:
            order: Order to place (aggregation).
            
        Returns:
            Confirmation message.
        """
        self.orders.append(order)
        return f"Order placed for table {order.table_number}"
    
    def get_pending_orders(self) -> list[Order]:
        """Get all pending orders.
        
        Returns:
            List of orders with 'pending' status.
        """
        return [order for order in self.orders if order.status == "pending"]
    
    def complete_order(self, order_index: int) -> str:
        """Mark an order as complete.
        
        Args:
            order_index: Index of order in orders list.
            
        Returns:
            Status message.
        """
        if order_index < 0 or order_index >= len(self.orders):
            return "Invalid order index"
        
        order = self.orders[order_index]
        order.set_status("served")
        return f"Order for table {order.table_number} completed"
    
    def get_menu_item_by_name(self, name: str) -> Optional[MenuItem]:
        """Find a menu item by name.
        
        Args:
            name: Name to search for.
            
        Returns:
            MenuItem if found, None otherwise.
        """
        for item in self.menu_items:
            if item.name == name:
                return item
        return None
