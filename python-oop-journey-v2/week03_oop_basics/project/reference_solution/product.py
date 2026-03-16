"""Product Module - Reference Solution.

Implements the Product class for the e-commerce system.
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
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")
        if not category or not isinstance(category, str):
            raise ValueError("Category must be a non-empty string")
        if not sku or not isinstance(sku, str):
            raise ValueError("SKU must be a non-empty string")
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        if price < 0:
            raise ValueError("Price cannot be negative")
        
        self._name = name
        self._price = float(price)
        self._category = category
        self._sku = sku
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return (
            f"Product(name='{self._name}', price={self._price}, "
            f"category='{self._category}', sku='{self._sku}')"
        )
    
    def __eq__(self, other: object) -> bool:
        """Two products are equal if they have the same SKU."""
        if not isinstance(other, Product):
            return NotImplemented
        return self._sku == other._sku
    
    def __hash__(self) -> int:
        """Hash based on SKU for use in sets and dicts."""
        return hash(self._sku)
    
    @property
    def name(self) -> str:
        """Get the product name."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the product name with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string")
        self._name = value
    
    @property
    def price(self) -> float:
        """Get the product price."""
        return self._price
    
    @price.setter
    def price(self, value: float) -> None:
        """Set the product price with validation (must be >= 0)."""
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a number")
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = float(value)
    
    @property
    def category(self) -> str:
        """Get the product category."""
        return self._category
    
    @category.setter
    def category(self, value: str) -> None:
        """Set the product category with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Category must be a non-empty string")
        self._category = value
    
    @property
    def sku(self) -> str:
        """Get the product SKU (read-only)."""
        return self._sku
    
    def apply_discount(self, percentage: float) -> float:
        """Calculate discounted price.
        
        Args:
            percentage: Discount percentage (0-100).
        
        Returns:
            The price after discount.
        
        Raises:
            ValueError: If percentage is not between 0 and 100.
        """
        if not isinstance(percentage, (int, float)):
            raise ValueError("Percentage must be a number")
        if percentage < 0 or percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        
        discount_amount = self._price * (percentage / 100)
        return round(self._price - discount_amount, 2)
    
    def to_dict(self) -> dict[str, str | float]:
        """Convert product to dictionary representation.
        
        Returns:
            Dictionary with product data.
        """
        return {
            "name": self._name,
            "price": self._price,
            "category": self._category,
            "sku": self._sku,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, str | float]) -> Product:
        """Create a Product from a dictionary.
        
        Args:
            data: Dictionary containing name, price, category, sku.
        
        Returns:
            A new Product instance.
        """
        required_keys = {"name", "price", "category", "sku"}
        if not all(key in data for key in required_keys):
            missing = required_keys - set(data.keys())
            raise ValueError(f"Missing required keys: {missing}")
        
        return cls(
            name=str(data["name"]),
            price=float(data["price"]),
            category=str(data["category"]),
            sku=str(data["sku"]),
        )
