"""Solution for Problem 01: Inventory Item."""

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
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def get_total_value(self) -> float:
        """Calculate total value of this inventory item.
        
        Returns:
            price multiplied by quantity
        """
        return self.price * self.quantity
    
    @classmethod
    def from_string(cls, data: str) -> InventoryItem:
        """Create an InventoryItem from a comma-separated string.
        
        Args:
            data: String in format "name,price,quantity"
        
        Returns:
            New InventoryItem instance
        """
        parts = data.split(",")
        name = parts[0]
        price = float(parts[1])
        quantity = int(parts[2])
        return cls(name, price, quantity)
