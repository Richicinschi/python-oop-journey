"""Product Module - Starter.

TODO: Implement the Product class for the e-commerce system.

WEEK 3 CONCEPT CONNECTIONS:
- Day 1 (Classes & Objects): Class definition, __init__, instance attributes
- Day 3 (Encapsulation): Private attributes (_name, _price), @property decorators
- Day 4 (Magic Methods): __repr__, __eq__, __hash__
- Day 2 (Method Types): from_dict() classmethod for factory pattern

START HERE: This is the simplest class with no dependencies.
"""

from __future__ import annotations


class Product:
    """Represents a product in the e-commerce system.
    
    A product has a name, price, category, and SKU (Stock Keeping Unit).
    The price should be validated to be non-negative.
    The SKU should be unique and immutable.
    
    Attributes:
        name: The product name.
        price: The product price (must be >= 0).
        category: The product category (e.g., "Electronics", "Clothing").
        sku: The unique stock keeping unit (immutable).
    
    Example:
        >>> product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        >>> product.name
        'Laptop'
        >>> product.price
        999.99
    """
    
    def __init__(self, name: str, price: float, category: str, sku: str) -> None:
        """Initialize a Product.
        
        Args:
            name: The product name.
            price: The product price (must be >= 0).
            category: The product category.
            sku: The unique stock keeping unit.
        
        Raises:
            ValueError: If price is negative or if any string argument is empty.
        """
        # TODO: Implement initialization with validation
        raise NotImplementedError("Implement __init__")
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        # TODO: Implement __repr__
        raise NotImplementedError("Implement __repr__")
    
    def __eq__(self, other: object) -> bool:
        """Two products are equal if they have the same SKU."""
        # TODO: Implement equality comparison based on SKU
        raise NotImplementedError("Implement __eq__")
    
    def __hash__(self) -> int:
        """Hash based on SKU for use in sets and dicts."""
        # TODO: Implement __hash__
        raise NotImplementedError("Implement __hash__")
    
    @property
    def name(self) -> str:
        """Get the product name."""
        # TODO: Implement name property getter
        raise NotImplementedError("Implement name getter")
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the product name with validation."""
        # TODO: Implement name property setter with validation
        raise NotImplementedError("Implement name setter")
    
    @property
    def price(self) -> float:
        """Get the product price."""
        # TODO: Implement price property getter
        raise NotImplementedError("Implement price getter")
    
    @price.setter
    def price(self, value: float) -> None:
        """Set the product price with validation (must be >= 0)."""
        # TODO: Implement price property setter with validation
        raise NotImplementedError("Implement price setter")
    
    @property
    def category(self) -> str:
        """Get the product category."""
        # TODO: Implement category property getter
        raise NotImplementedError("Implement category getter")
    
    @category.setter
    def category(self, value: str) -> None:
        """Set the product category with validation."""
        # TODO: Implement category property setter with validation
        raise NotImplementedError("Implement category setter")
    
    @property
    def sku(self) -> str:
        """Get the product SKU (read-only)."""
        # TODO: Implement SKU property getter (read-only)
        raise NotImplementedError("Implement sku getter")
    
    def apply_discount(self, percentage: float) -> float:
        """Calculate discounted price.
        
        Args:
            percentage: Discount percentage (0-100).
        
        Returns:
            The price after discount.
        
        Raises:
            ValueError: If percentage is not between 0 and 100.
        """
        # TODO: Implement discount calculation with validation
        raise NotImplementedError("Implement apply_discount")
    
    def to_dict(self) -> dict[str, str | float]:
        """Convert product to dictionary representation.
        
        Returns:
            Dictionary with product data.
        """
        # TODO: Implement dictionary conversion
        raise NotImplementedError("Implement to_dict")
    
    @classmethod
    def from_dict(cls, data: dict[str, str | float]) -> Product:
        """Create a Product from a dictionary.
        
        Args:
            data: Dictionary containing name, price, category, sku.
        
        Returns:
            A new Product instance.
        """
        # TODO: Implement factory method from dictionary
        raise NotImplementedError("Implement from_dict")
