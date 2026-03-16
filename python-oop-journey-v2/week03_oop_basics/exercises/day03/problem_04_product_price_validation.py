"""Exercise: Product Price Validation.

Implement a Product class with business rule validation.

TODO:
1. Implement @property for price with validation (non-negative)
2. Implement @property for discount_percent with validation (0-50)
3. Implement read-only properties: final_price, discount_amount
4. Implement apply_discount method
"""

from __future__ import annotations


class Product:
    """A product with validated price and discount.
    
    Attributes:
        product_id: The unique product identifier (read-only).
        name: The product name.
    """
    
    MAX_DISCOUNT_PERCENT = 50
    
    def __init__(self, product_id: str, name: str, price: float) -> None:
        """Initialize a product."""
        self._product_id = product_id.strip()
        self._name = name.strip()
        self._discount_percent: float = 0.0
        self._price: float = 0.0
        self.price = price  # Use setter
    
    @property
    def product_id(self) -> str:
        """Get the product ID."""
        return self._product_id
    
    @property
    def name(self) -> str:
        """Get the product name."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the product name."""
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @property
    def price(self) -> float:
        """Get the base price."""
        # TODO: Return the price
        raise NotImplementedError("Return price")
    
    @price.setter
    def price(self, value: float) -> None:
        """Set the base price."""
        # TODO: Validate value is non-negative
        # TODO: Set _price
        raise NotImplementedError("Validate and set price")
    
    @property
    def discount_percent(self) -> float:
        """Get the discount percentage."""
        # TODO: Return discount_percent
        raise NotImplementedError("Return discount")
    
    @discount_percent.setter
    def discount_percent(self, value: float) -> None:
        """Set the discount percentage."""
        # TODO: Validate value is between 0 and MAX_DISCOUNT_PERCENT
        # TODO: Set _discount_percent
        raise NotImplementedError("Validate and set discount")
    
    @property
    def final_price(self) -> float:
        """Calculate final price after discount (read-only)."""
        # TODO: Calculate and return price - discount_amount
        raise NotImplementedError("Calculate final price")
    
    @property
    def discount_amount(self) -> float:
        """Calculate the discount amount (read-only)."""
        # TODO: Calculate price * (discount_percent / 100)
        raise NotImplementedError("Calculate discount amount")
    
    def apply_discount(self, percent: float) -> float:
        """Apply a discount and return the final price."""
        # TODO: Set discount_percent using the setter
        # TODO: Return final_price
        raise NotImplementedError("Apply discount and return final price")
