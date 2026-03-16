"""Problem 01: Inventory Item

Topic: Instance, Class, and Static Methods
Difficulty: Easy

Create an InventoryItem class with instance methods and a @classmethod
alternative constructor.

Example:
    >>> item = InventoryItem("Laptop", 999.99, 5)
    >>> item.name
    'Laptop'
    >>> item.get_total_value()
    4999.95
    >>> 
    >>> # Alternative constructor from string
    >>> item2 = InventoryItem.from_string("Mouse,29.99,10")
    >>> item2.name
    'Mouse'
    >>> item2.price
    29.99
    >>> item2.quantity
    10

Requirements:
    - __init__ takes name (str), price (float), quantity (int)
    - get_total_value() returns price * quantity (instance method)
    - from_string(cls, data: str) parses "name,price,quantity" format
    - All classes must have type hints
"""

from __future__ import annotations


class InventoryItem:
    """Represents an item in inventory with name, price, and quantity."""
    
    def __init__(self, name: str, price: float, quantity: int) -> None:
        """Initialize an inventory item.
        
        Args:
            name: The item name
            price: The unit price
            quantity: The quantity in stock
        """
        raise NotImplementedError("Implement __init__")
    
    def get_total_value(self) -> float:
        """Calculate total value of this inventory item.
        
        Returns:
            price multiplied by quantity
        """
        raise NotImplementedError("Implement get_total_value")
    
    @classmethod
    def from_string(cls, data: str) -> InventoryItem:
        """Create an InventoryItem from a comma-separated string.
        
        Args:
            data: String in format "name,price,quantity"
        
        Returns:
            New InventoryItem instance
        """
        raise NotImplementedError("Implement from_string")
