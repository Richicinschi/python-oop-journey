"""Reference solution for Problem 03: Product Catalog Item."""

from __future__ import annotations


class ProductCatalogItem:
    """Represents a product in a catalog with proper equality and hashing.
    
    Products are identified by their SKU (Stock Keeping Unit), making them
    suitable for use in sets and as dictionary keys.
    
    Attributes:
        sku: The unique stock keeping unit (immutable identifier).
        name: The product name.
        price: The product price.
        category: The product category.
    """
    
    def __init__(
        self,
        sku: str,
        name: str,
        price: float,
        category: str,
    ) -> None:
        """Initialize a product catalog item.
        
        Args:
            sku: The unique stock keeping unit (immutable).
            name: The product name.
            price: The product price.
            category: The product category.
        """
        self._sku = sku
        self.name = name
        self.price = price
        self.category = category
    
    @property
    def sku(self) -> str:
        """Return the SKU (immutable identifier)."""
        return self._sku
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on SKU only.
        
        Two products are equal if they have the same SKU, regardless
        of other attributes (name, price may change over time).
        """
        if not isinstance(other, ProductCatalogItem):
            return NotImplemented
        return self._sku == other._sku
    
    def __hash__(self) -> int:
        """Return a hash based on the immutable SKU.
        
        This enables ProductCatalogItem to be used in sets and as dict keys.
        """
        return hash(self._sku)
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        return (
            f"ProductCatalogItem("
            f"sku={self._sku!r}, "
            f"name={self.name!r}, "
            f"price={self.price!r}, "
            f"category={self.category!r}"
            f")"
        )
    
    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"{self.name} ({self._sku}) - ${self.price:.2f}"
