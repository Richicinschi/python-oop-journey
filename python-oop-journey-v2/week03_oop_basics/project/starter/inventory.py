"""Inventory Module - Starter.

TODO: Implement the Inventory class for the e-commerce system.

WEEK 3 CONCEPT CONNECTIONS:
- Day 2 (Method Types): LOW_STOCK_THRESHOLD class attribute, set_low_stock_threshold() classmethod
- Day 3 (Encapsulation): _stock dictionary is private, validation in methods
- Day 1 (Collections): Dictionary operations for stock tracking
- Day 6 (Design): Single Responsibility - Inventory only manages stock quantities

IMPLEMENT AFTER: product.py (understands SKU concept from Product)
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
        # TODO: Initialize empty inventory
        raise NotImplementedError("Implement __init__")
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        # TODO: Implement __repr__
        raise NotImplementedError("Implement __repr__")
    
    def __len__(self) -> int:
        """Return the number of products in inventory."""
        # TODO: Implement __len__
        raise NotImplementedError("Implement __len__")
    
    def stock_product(self, sku: str, quantity: int) -> None:
        """Add stock for a product.
        
        Args:
            sku: The product SKU.
            quantity: Amount to add (must be >= 0).
        
        Raises:
            ValueError: If quantity is negative.
        """
        # TODO: Implement stock addition with validation
        raise NotImplementedError("Implement stock_product")
    
    def remove_product(self, sku: str) -> bool:
        """Remove a product from inventory entirely.
        
        Args:
            sku: The product SKU to remove.
        
        Returns:
            True if product was found and removed, False otherwise.
        """
        # TODO: Implement product removal
        raise NotImplementedError("Implement remove_product")
    
    def get_stock(self, sku: str) -> int:
        """Get the available stock for a product.
        
        Args:
            sku: The product SKU.
        
        Returns:
            Available quantity (0 if product not in inventory).
        """
        # TODO: Implement stock query
        raise NotImplementedError("Implement get_stock")
    
    def has_stock(self, sku: str, quantity: int = 1) -> bool:
        """Check if there's enough stock for a request.
        
        Args:
            sku: The product SKU.
            quantity: The desired quantity (default 1).
        
        Returns:
            True if stock >= quantity.
        """
        # TODO: Implement stock check
        raise NotImplementedError("Implement has_stock")
    
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
        # TODO: Implement reservation logic
        raise NotImplementedError("Implement reserve")
    
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
        # TODO: Implement release logic
        raise NotImplementedError("Implement release")
    
    def get_low_stock_items(self) -> list[tuple[str, int]]:
        """Get products with low stock.
        
        Returns:
            List of (sku, stock) tuples for items below threshold.
        """
        # TODO: Implement low stock check
        raise NotImplementedError("Implement get_low_stock_items")
    
    def get_total_units(self) -> int:
        """Get total units across all products.
        
        Returns:
            Sum of all stock quantities.
        """
        # TODO: Implement total units calculation
        raise NotImplementedError("Implement get_total_units")
    
    def get_skus(self) -> list[str]:
        """Get all product SKUs in inventory.
        
        Returns:
            List of SKU strings.
        """
        # TODO: Implement SKU listing
        raise NotImplementedError("Implement get_skus")
    
    def is_empty(self) -> bool:
        """Check if inventory is empty.
        
        Returns:
            True if no products in inventory.
        """
        # TODO: Implement empty check
        raise NotImplementedError("Implement is_empty")
    
    def clear(self) -> None:
        """Clear all inventory (use with caution!)."""
        # TODO: Implement clear
        raise NotImplementedError("Implement clear")
    
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
        # TODO: Implement stock update
        raise NotImplementedError("Implement update_stock")
    
    @classmethod
    def set_low_stock_threshold(cls, threshold: int) -> None:
        """Set the global low stock threshold.
        
        Args:
            threshold: New threshold value (must be >= 0).
        
        Raises:
            ValueError: If threshold is negative.
        """
        # TODO: Implement threshold setter
        raise NotImplementedError("Implement set_low_stock_threshold")
    
    @classmethod
    def get_low_stock_threshold(cls) -> int:
        """Get the current low stock threshold.
        
        Returns:
            Current threshold value.
        """
        # TODO: Implement threshold getter
        raise NotImplementedError("Implement get_low_stock_threshold")
