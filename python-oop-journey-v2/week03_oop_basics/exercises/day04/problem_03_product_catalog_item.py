"""Problem 03: Product Catalog Item

Topic: Magic Methods - Equality, Hashing, and Representation
Difficulty: Easy

Implement a product item class suitable for use in sets and as dictionary keys.
"""

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
    
    Example:
        >>> p1 = ProductCatalogItem('ABC123', 'Widget', 29.99, 'Tools')
        >>> p2 = ProductCatalogItem('ABC123', 'Widget Pro', 39.99, 'Tools')
        >>> p1 == p2  # Same SKU
        True
        >>> {p1, p2}  # Only one item in set
        {ProductCatalogItem(sku='ABC123', name='Widget', price=29.99, category='Tools')}
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
        raise NotImplementedError("Implement __init__")
    
    @property
    def sku(self) -> str:
        """Return the SKU (immutable identifier)."""
        raise NotImplementedError("Implement sku property")
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on SKU only.
        
        Two products are equal if they have the same SKU, regardless
        of other attributes (name, price may change over time).
        """
        raise NotImplementedError("Implement __eq__")
    
    def __hash__(self) -> int:
        """Return a hash based on the immutable SKU.
        
        This enables ProductCatalogItem to be used in sets and as dict keys.
        """
        raise NotImplementedError("Implement __hash__")
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        raise NotImplementedError("Implement __repr__")
    
    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        raise NotImplementedError("Implement __str__")
