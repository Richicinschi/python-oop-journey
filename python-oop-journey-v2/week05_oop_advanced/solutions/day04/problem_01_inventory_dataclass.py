"""Reference solution for Problem 01: Inventory Dataclass."""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Product:
    """A product in the inventory system.
    
    Attributes:
        sku: Unique product identifier (e.g., "LAPTOP-001")
        name: Human-readable product name
        price: Price per unit (must be non-negative)
        quantity: Current stock quantity (default: 0)
        category: Product category (default: "general")
        tags: List of searchable tags (default: empty list)
    """
    
    sku: str
    name: str
    price: float
    quantity: int = 0
    category: str = "general"
    tags: list[str] = field(default_factory=list)
    
    def total_value(self) -> float:
        """Calculate total value of inventory for this product.
        
        Returns:
            price * quantity
        """
        return self.price * self.quantity
    
    def is_in_stock(self) -> bool:
        """Check if product is available.
        
        Returns:
            True if quantity > 0
        """
        return self.quantity > 0
    
    def add_tags(self, *new_tags: str) -> None:
        """Add one or more tags to the product.
        
        Args:
            new_tags: Variable number of tags to add
        """
        self.tags.extend(new_tags)
    
    def to_dict(self) -> dict[str, object]:
        """Convert product to dictionary representation.
        
        Returns:
            Dictionary with all field values
        """
        return {
            "sku": self.sku,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category,
            "tags": self.tags.copy()
        }
