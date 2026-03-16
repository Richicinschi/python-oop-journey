"""Solution for Problem 04: Product Price Validation.

Demonstrates property with business rules for product pricing.
"""

from __future__ import annotations


class Product:
    """A product with validated price and discount properties.
    
    This class demonstrates business rule validation using properties,
    including dependency between price and discount.
    
    Attributes:
        product_id: The unique product identifier (read-only).
        name: The product name.
    
    Example:
        >>> product = Product("P001", "Laptop", 1000.0)
        >>> product.price
        1000.0
        >>> product.discount_percent = 10
        >>> product.final_price
        900.0
    """
    
    MAX_DISCOUNT_PERCENT = 50  # Class constant for maximum allowed discount
    
    def __init__(self, product_id: str, name: str, price: float) -> None:
        """Initialize a product.
        
        Args:
            product_id: The unique product identifier.
            name: The product name.
            price: The base price of the product.
        
        Raises:
            TypeError: If types are incorrect.
            ValueError: If values are invalid.
        """
        if not isinstance(product_id, str):
            raise TypeError("Product ID must be a string")
        if not product_id.strip():
            raise ValueError("Product ID cannot be empty")
        self._product_id = product_id.strip()
        
        self.name = name  # Use property setter
        self._discount_percent: float = 0.0
        self.price = price  # Use property setter
    
    @property
    def product_id(self) -> str:
        """Get the product ID.
        
        Returns:
            The unique product identifier.
        """
        return self._product_id
    
    @property
    def name(self) -> str:
        """Get the product name.
        
        Returns:
            The product name.
        """
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the product name.
        
        Args:
            value: The new product name.
        
        Raises:
            TypeError: If value is not a string.
            ValueError: If name is empty.
        """
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @property
    def price(self) -> float:
        """Get the base price.
        
        Returns:
            The base price of the product.
        """
        return self._price
    
    @price.setter
    def price(self, value: float) -> None:
        """Set the base price.
        
        Args:
            value: The new base price.
        
        Raises:
            TypeError: If value is not a number.
            ValueError: If price is negative.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = float(value)
    
    @property
    def discount_percent(self) -> float:
        """Get the discount percentage.
        
        Returns:
            The discount percentage (0-50).
        """
        return self._discount_percent
    
    @discount_percent.setter
    def discount_percent(self, value: float) -> None:
        """Set the discount percentage.
        
        Args:
            value: The discount percentage (0-50).
        
        Raises:
            TypeError: If value is not a number.
            ValueError: If discount is not between 0 and MAX_DISCOUNT_PERCENT.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Discount must be a number")
        if value < 0 or value > self.MAX_DISCOUNT_PERCENT:
            raise ValueError(f"Discount must be between 0 and {self.MAX_DISCOUNT_PERCENT}")
        self._discount_percent = float(value)
    
    @property
    def final_price(self) -> float:
        """Calculate the final price after discount (read-only).
        
        Returns:
            The price after applying discount.
        """
        discount_amount = self._price * (self._discount_percent / 100)
        return self._price - discount_amount
    
    @property
    def discount_amount(self) -> float:
        """Calculate the discount amount (read-only).
        
        Returns:
            The amount saved due to discount.
        """
        return self._price * (self._discount_percent / 100)
    
    def apply_discount(self, percent: float) -> float:
        """Apply a discount and return the final price.
        
        Args:
            percent: The discount percentage to apply.
        
        Returns:
            The final price after discount.
        """
        self.discount_percent = percent
        return self.final_price
