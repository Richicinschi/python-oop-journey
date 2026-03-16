"""Shopping Cart Module - Reference Solution.

Implements the ShoppingCart and CartItem classes for the e-commerce system.
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
    
    def __init__(self, product: Product, quantity: int = 1) -> None:
        """Initialize a CartItem.
        
        Args:
            product: The product to add.
            quantity: The quantity (must be > 0).
        
        Raises:
            ValueError: If quantity is not positive.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        self._product = product
        self._quantity = quantity
    
    @property
    def product(self) -> Product:
        """Get the product."""
        return self._product
    
    @property
    def quantity(self) -> int:
        """Get the quantity."""
        return self._quantity
    
    @quantity.setter
    def quantity(self, value: int) -> None:
        """Set the quantity with validation (must be > 0)."""
        if value <= 0:
            raise ValueError("Quantity must be positive")
        self._quantity = value
    
    def get_subtotal(self) -> float:
        """Calculate the subtotal for this item.
        
        Returns:
            product.price * quantity
        """
        return round(self._product.price * self._quantity, 2)
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"CartItem(product={self._product.sku}, quantity={self._quantity})"


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
        self._items: dict[str, CartItem] = {}
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"ShoppingCart(items={len(self._items)})"
    
    def __len__(self) -> int:
        """Return the number of unique items in cart."""
        return len(self._items)
    
    def __iter__(self):
        """Allow iteration over cart items."""
        return iter(self._items.values())
    
    def add_item(self, product: Product, quantity: int = 1) -> None:
        """Add a product to the cart.
        
        If the product is already in the cart, increment the quantity.
        
        Args:
            product: The product to add.
            quantity: The quantity to add (must be > 0).
        
        Raises:
            ValueError: If quantity is not positive.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        sku = product.sku
        if sku in self._items:
            self._items[sku].quantity += quantity
        else:
            self._items[sku] = CartItem(product, quantity)
    
    def remove_item(self, sku: str) -> bool:
        """Remove a product from the cart.
        
        Args:
            sku: The SKU of the product to remove.
        
        Returns:
            True if item was found and removed, False otherwise.
        """
        if sku in self._items:
            del self._items[sku]
            return True
        return False
    
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
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if sku in self._items:
            self._items[sku].quantity = quantity
            return True
        return False
    
    def get_item(self, sku: str) -> CartItem | None:
        """Get a cart item by SKU.
        
        Args:
            sku: The SKU to look up.
        
        Returns:
            The CartItem if found, None otherwise.
        """
        return self._items.get(sku)
    
    def has_item(self, sku: str) -> bool:
        """Check if a product is in the cart.
        
        Args:
            sku: The SKU to check.
        
        Returns:
            True if the product is in the cart.
        """
        return sku in self._items
    
    def get_total_quantity(self) -> int:
        """Get the total number of items in cart (sum of all quantities).
        
        Returns:
            Total item count.
        """
        return sum(item.quantity for item in self._items.values())
    
    def get_total(self) -> float:
        """Calculate the total price of all items in cart.
        
        Returns:
            Total price.
        """
        return round(sum(item.get_subtotal() for item in self._items.values()), 2)
    
    def clear(self) -> None:
        """Remove all items from the cart."""
        self._items.clear()
    
    def is_empty(self) -> bool:
        """Check if the cart is empty.
        
        Returns:
            True if cart has no items.
        """
        return len(self._items) == 0
    
    def get_items(self) -> list[CartItem]:
        """Get a list of all cart items.
        
        Returns:
            List of CartItem objects.
        """
        return list(self._items.values())
    
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
        total = self.get_total()
        
        discounts = {
            "SAVE10": 0.10,
            "SAVE20": 0.20,
            "SAVE50": 0.50,
        }
        
        if code not in discounts:
            raise ValueError(f"Invalid discount code: {code}")
        
        return round(total * discounts[code], 2)
