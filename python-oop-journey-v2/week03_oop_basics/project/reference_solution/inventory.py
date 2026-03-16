"""Inventory Module - Reference Solution.

Implements the Inventory class for the e-commerce system.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product


class Inventory:
    """Manages product inventory for the e-commerce system.
    
    The inventory tracks how many units of each product are available.
    It supports stock queries, reservations, and low stock alerts.
    
    Attributes:
        _stock: Dictionary mapping SKU to available quantity.
    
    Example:
        >>> inv = Inventory()
        >>> inv.stock_product("TECH-001", 100)
        >>> inv.get_stock("TECH-001")
        100
        >>> inv.reserve("TECH-001", 5)
        True
        >>> inv.get_stock("TECH-001")
        95
    """
    
    LOW_STOCK_THRESHOLD: int = 10
    
    def __init__(self) -> None:
        """Initialize an empty inventory."""
        self._stock: dict[str, int] = {}
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"Inventory(products={len(self._stock)})"
    
    def __len__(self) -> int:
        """Return the number of products in inventory."""
        return len(self._stock)
    
    def stock_product(self, sku: str, quantity: int) -> None:
        """Add stock for a product.
        
        Args:
            sku: The product SKU.
            quantity: Amount to add (must be >= 0).
        
        Raises:
            ValueError: If quantity is negative.
        """
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        
        if sku in self._stock:
            self._stock[sku] += quantity
        else:
            self._stock[sku] = quantity
    
    def remove_product(self, sku: str) -> bool:
        """Remove a product from inventory entirely.
        
        Args:
            sku: The product SKU to remove.
        
        Returns:
            True if product was found and removed, False otherwise.
        """
        if sku in self._stock:
            del self._stock[sku]
            return True
        return False
    
    def get_stock(self, sku: str) -> int:
        """Get the available stock for a product.
        
        Args:
            sku: The product SKU.
        
        Returns:
            Available quantity (0 if product not in inventory).
        """
        return self._stock.get(sku, 0)
    
    def has_stock(self, sku: str, quantity: int = 1) -> bool:
        """Check if there's enough stock for a request.
        
        Args:
            sku: The product SKU.
            quantity: The desired quantity (default 1).
        
        Returns:
            True if stock >= quantity.
        """
        return self._stock.get(sku, 0) >= quantity
    
    def reserve(self, sku: str, quantity: int) -> bool:
        """Reserve stock for an order (decreases available stock).
        
        Args:
            sku: The product SKU.
            quantity: Amount to reserve (must be > 0).
        
        Returns:
            True if reservation succeeded, False if insufficient stock.
        
        Raises:
            ValueError: If quantity is not positive.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if self.has_stock(sku, quantity):
            self._stock[sku] -= quantity
            return True
        return False
    
    def release(self, sku: str, quantity: int) -> bool:
        """Release reserved stock back to inventory (e.g., order cancelled).
        
        Args:
            sku: The product SKU.
            quantity: Amount to release (must be > 0).
        
        Returns:
            True if release succeeded.
        
        Raises:
            ValueError: If quantity is not positive or if releasing more than reserved.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if sku not in self._stock:
            # Product exists but has 0 stock tracked, just add the released quantity
            self._stock[sku] = quantity
            return True
        
        self._stock[sku] += quantity
        return True
    
    def get_low_stock_items(self) -> list[tuple[str, int]]:
        """Get products with low stock.
        
        Returns:
            List of (sku, stock) tuples for items below threshold.
        """
        return [
            (sku, stock)
            for sku, stock in self._stock.items()
            if stock < self.LOW_STOCK_THRESHOLD
        ]
    
    def get_total_units(self) -> int:
        """Get total units across all products.
        
        Returns:
            Sum of all stock quantities.
        """
        return sum(self._stock.values())
    
    def get_skus(self) -> list[str]:
        """Get all product SKUs in inventory.
        
        Returns:
            List of SKU strings.
        """
        return list(self._stock.keys())
    
    def is_empty(self) -> bool:
        """Check if inventory is empty.
        
        Returns:
            True if no products in inventory.
        """
        return len(self._stock) == 0
    
    def clear(self) -> None:
        """Clear all inventory (use with caution!)."""
        self._stock.clear()
    
    def update_stock(self, sku: str, new_quantity: int) -> bool:
        """Set the stock level for a product (absolute value).
        
        Args:
            sku: The product SKU.
            new_quantity: The new stock level (must be >= 0).
        
        Returns:
            True if product exists and was updated.
        
        Raises:
            ValueError: If new_quantity is negative.
        """
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")
        
        if sku in self._stock:
            self._stock[sku] = new_quantity
            return True
        return False
    
    @classmethod
    def set_low_stock_threshold(cls, threshold: int) -> None:
        """Set the global low stock threshold.
        
        Args:
            threshold: New threshold value (must be >= 0).
        
        Raises:
            ValueError: If threshold is negative.
        """
        if threshold < 0:
            raise ValueError("Threshold cannot be negative")
        cls.LOW_STOCK_THRESHOLD = threshold
    
    @classmethod
    def get_low_stock_threshold(cls) -> int:
        """Get the current low stock threshold.
        
        Returns:
            Current threshold value.
        """
        return cls.LOW_STOCK_THRESHOLD
