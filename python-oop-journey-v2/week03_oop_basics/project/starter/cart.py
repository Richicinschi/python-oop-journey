"""Shopping Cart Module - Starter.

TODO: Implement the ShoppingCart class for the e-commerce system.

WEEK 3 CONCEPT CONNECTIONS:
- Day 5 (Composition): Cart contains CartItems (strong ownership)
- Day 4 (Magic Methods): __len__, __iter__ for Pythonic interface
- Day 3 (Encapsulation): _items dictionary is private
- Day 1 (Collections): Managing items with dict for O(1) lookup by SKU

IMPLEMENT AFTER: product.py (CartItem references Product)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product


class CartItem:
    """Represents an item in the shopping cart.
    
    A cart item links a product with a quantity.
    
    Attributes:
        product: The product in the cart.
        quantity: The number of units.
    """
    
    def __init__(self, product: "Product", quantity: int = 1) -> None:
        """Initialize a CartItem.
        
        Args:
            product: The product to add.
            quantity: The quantity (must be > 0).
        
        Raises:
            ValueError: If quantity is not positive.
        """
        # TODO: Implement initialization with validation
        raise NotImplementedError("Implement __init__")
    
    @property
    def product(self) -> "Product":
        """Get the product."""
        # TODO: Implement product getter
        raise NotImplementedError("Implement product getter")
    
    @property
    def quantity(self) -> int:
        """Get the quantity."""
        # TODO: Implement quantity getter
        raise NotImplementedError("Implement quantity getter")
    
    @quantity.setter
    def quantity(self, value: int) -> None:
        """Set the quantity with validation (must be > 0)."""
        # TODO: Implement quantity setter with validation
        raise NotImplementedError("Implement quantity setter")
    
    def get_subtotal(self) -> float:
        """Calculate the subtotal for this item.
        
        Returns:
            product.price * quantity
        """
        # TODO: Implement subtotal calculation
        raise NotImplementedError("Implement get_subtotal")
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        # TODO: Implement __repr__
        raise NotImplementedError("Implement __repr__")


class ShoppingCart:
    """Represents a shopping cart in the e-commerce system.
    
    A shopping cart holds items (products with quantities) and provides
    methods to add, remove, and update items. It calculates totals and
    can be cleared.
    
    Attributes:
        items: Dictionary mapping SKU to CartItem.
    
    Example:
        >>> cart = ShoppingCart()
        >>> cart.add_item(product, 2)
        >>> cart.get_total()
        1999.98
    """
    
    def __init__(self) -> None:
        """Initialize an empty shopping cart."""
        # TODO: Initialize empty cart
        raise NotImplementedError("Implement __init__")
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        # TODO: Implement __repr__
        raise NotImplementedError("Implement __repr__")
    
    def __len__(self) -> int:
        """Return the number of unique items in cart."""
        # TODO: Implement __len__
        raise NotImplementedError("Implement __len__")
    
    def __iter__(self):
        """Allow iteration over cart items."""
        # TODO: Implement __iter__
        raise NotImplementedError("Implement __iter__")
    
    def add_item(self, product: "Product", quantity: int = 1) -> None:
        """Add a product to the cart.
        
        If the product is already in the cart, increment the quantity.
        
        Args:
            product: The product to add.
            quantity: The quantity to add (must be > 0).
        
        Raises:
            ValueError: If quantity is not positive.
        """
        # TODO: Implement add_item with quantity increment logic
        raise NotImplementedError("Implement add_item")
    
    def remove_item(self, sku: str) -> bool:
        """Remove a product from the cart.
        
        Args:
            sku: The SKU of the product to remove.
        
        Returns:
            True if item was found and removed, False otherwise.
        """
        # TODO: Implement remove_item
        raise NotImplementedError("Implement remove_item")
    
    def update_quantity(self, sku: str, quantity: int) -> bool:
        """Update the quantity of a product in the cart.
        
        Args:
            sku: The SKU of the product.
            quantity: The new quantity (must be > 0).
        
        Returns:
            True if item was found and updated, False otherwise.
        
        Raises:
            ValueError: If quantity is not positive.
        """
        # TODO: Implement update_quantity with validation
        raise NotImplementedError("Implement update_quantity")
    
    def get_item(self, sku: str) -> CartItem | None:
        """Get a cart item by SKU.
        
        Args:
            sku: The SKU to look up.
        
        Returns:
            The CartItem if found, None otherwise.
        """
        # TODO: Implement get_item
        raise NotImplementedError("Implement get_item")
    
    def has_item(self, sku: str) -> bool:
        """Check if a product is in the cart.
        
        Args:
            sku: The SKU to check.
        
        Returns:
            True if the product is in the cart.
        """
        # TODO: Implement has_item
        raise NotImplementedError("Implement has_item")
    
    def get_total_quantity(self) -> int:
        """Get the total number of items in cart (sum of all quantities).
        
        Returns:
            Total item count.
        """
        # TODO: Implement total quantity calculation
        raise NotImplementedError("Implement get_total_quantity")
    
    def get_total(self) -> float:
        """Calculate the total price of all items in cart.
        
        Returns:
            Total price.
        """
        # TODO: Implement total calculation
        raise NotImplementedError("Implement get_total")
    
    def clear(self) -> None:
        """Remove all items from the cart."""
        # TODO: Implement clear
        raise NotImplementedError("Implement clear")
    
    def is_empty(self) -> bool:
        """Check if the cart is empty.
        
        Returns:
            True if cart has no items.
        """
        # TODO: Implement is_empty
        raise NotImplementedError("Implement is_empty")
    
    def get_items(self) -> list[CartItem]:
        """Get a list of all cart items.
        
        Returns:
            List of CartItem objects.
        """
        # TODO: Implement get_items
        raise NotImplementedError("Implement get_items")
    
    def apply_discount_code(self, code: str) -> float:
        """Apply a discount code to the cart total.
        
        Supported codes:
        - "SAVE10": 10% off
        - "SAVE20": 20% off
        - "SAVE50": 50% off
        
        Args:
            code: The discount code.
        
        Returns:
            The discount amount.
        
        Raises:
            ValueError: If the code is not recognized.
        """
        # TODO: Implement discount code logic
        raise NotImplementedError("Implement apply_discount_code")
