"""Order Module - Starter.

TODO: Implement the Order and OrderStatus classes for the e-commerce system.

WEEK 3 CONCEPT CONNECTIONS:
- Day 1 (Classes & Objects): OrderStatus Enum for type-safe status values
- Day 6 (Class Design): State machine pattern for status transitions
- Day 2 (Method Types): generate_order_id() classmethod, from_cart() factory method
- Day 5 (Composition/Aggregation): OrderItem captures snapshot (immutable), Order has-a items
- Day 4 (Magic Methods): __str__ on OrderStatus Enum

IMPLEMENT AFTER: cart.py (Order.from_cart() uses CartItem)
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product


class OrderStatus(Enum):
    """Enumeration of possible order statuses."""
    
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    
    def __str__(self) -> str:
        """Return the status value as a string."""
        # TODO: Implement __str__
        raise NotImplementedError("Implement __str__")


class OrderItem:
    """Represents an item in an order.
    
    Unlike CartItem, OrderItem is immutable once created (part of order history).
    
    Attributes:
        product_name: Name of the product at time of order.
        product_sku: SKU of the product.
        unit_price: Price per unit at time of order.
        quantity: Number of units ordered.
    """
    
    def __init__(
        self,
        product_name: str,
        product_sku: str,
        unit_price: float,
        quantity: int
    ) -> None:
        """Initialize an OrderItem.
        
        Args:
            product_name: Name of the product.
            product_sku: SKU of the product.
            unit_price: Price per unit.
            quantity: Number of units.
        """
        # TODO: Implement initialization
        raise NotImplementedError("Implement __init__")
    
    @property
    def product_name(self) -> str:
        """Get the product name."""
        # TODO: Implement product_name getter
        raise NotImplementedError("Implement product_name getter")
    
    @property
    def product_sku(self) -> str:
        """Get the product SKU."""
        # TODO: Implement product_sku getter
        raise NotImplementedError("Implement product_sku getter")
    
    @property
    def unit_price(self) -> float:
        """Get the unit price."""
        # TODO: Implement unit_price getter
        raise NotImplementedError("Implement unit_price getter")
    
    @property
    def quantity(self) -> int:
        """Get the quantity."""
        # TODO: Implement quantity getter
        raise NotImplementedError("Implement quantity getter")
    
    def get_subtotal(self) -> float:
        """Calculate the subtotal for this item.
        
        Returns:
            unit_price * quantity
        """
        # TODO: Implement subtotal calculation
        raise NotImplementedError("Implement get_subtotal")
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        # TODO: Implement __repr__
        raise NotImplementedError("Implement __repr__")


class Order:
    """Represents an order in the e-commerce system.
    
    An order captures a snapshot of cart items at checkout time.
    It has a lifecycle through different statuses and belongs to a user.
    
    Attributes:
        order_id: Unique identifier for the order.
        user_id: ID of the user who placed the order.
        items: List of order items.
        status: Current order status.
    
    Example:
        >>> order = Order("ORD-001", "U001", cart_items)
        >>> order.total
        1999.98
        >>> order.status
        <OrderStatus.PENDING: 'pending'>
    """
    
    _order_counter: int = 0
    
    def __init__(
        self,
        order_id: str,
        user_id: str,
        items: list[OrderItem],
        status: OrderStatus = OrderStatus.PENDING
    ) -> None:
        """Initialize an Order.
        
        Args:
            order_id: Unique identifier for the order.
            user_id: ID of the user who placed the order.
            items: List of order items.
            status: Initial order status (default: PENDING).
        """
        # TODO: Implement initialization
        raise NotImplementedError("Implement __init__")
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        # TODO: Implement __repr__
        raise NotImplementedError("Implement __repr__")
    
    @property
    def order_id(self) -> str:
        """Get the order ID (read-only)."""
        # TODO: Implement order_id getter (read-only)
        raise NotImplementedError("Implement order_id getter")
    
    @property
    def user_id(self) -> str:
        """Get the user ID (read-only)."""
        # TODO: Implement user_id getter (read-only)
        raise NotImplementedError("Implement user_id getter")
    
    @property
    def items(self) -> list[OrderItem]:
        """Get the order items (read-only copy)."""
        # TODO: Implement items getter returning a copy
        raise NotImplementedError("Implement items getter")
    
    @property
    def status(self) -> OrderStatus:
        """Get the order status."""
        # TODO: Implement status getter
        raise NotImplementedError("Implement status getter")
    
    @property
    def total(self) -> float:
        """Calculate the order total.
        
        Returns:
            Sum of all item subtotals.
        """
        # TODO: Implement total calculation
        raise NotImplementedError("Implement total property")
    
    @property
    def item_count(self) -> int:
        """Get the total number of items in the order.
        
        Returns:
            Sum of all item quantities.
        """
        # TODO: Implement item count calculation
        raise NotImplementedError("Implement item_count property")
    
    def update_status(self, new_status: OrderStatus) -> None:
        """Update the order status.
        
        Args:
            new_status: The new status to set.
        
        Raises:
            ValueError: If status transition is invalid.
        """
        # TODO: Implement status update with validation
        # Valid transitions:
        # - PENDING -> CONFIRMED, CANCELLED
        # - CONFIRMED -> SHIPPED, CANCELLED
        # - SHIPPED -> DELIVERED
        # - DELIVERED -> (no further transitions)
        # - CANCELLED -> (no further transitions)
        raise NotImplementedError("Implement update_status")
    
    def cancel(self) -> bool:
        """Cancel the order if possible.
        
        Returns:
            True if cancelled successfully, False if already shipped/delivered.
        """
        # TODO: Implement cancel logic
        raise NotImplementedError("Implement cancel")
    
    def can_cancel(self) -> bool:
        """Check if the order can be cancelled.
        
        Returns:
            True if status is PENDING or CONFIRMED.
        """
        # TODO: Implement can_cancel check
        raise NotImplementedError("Implement can_cancel")
    
    @classmethod
    def generate_order_id(cls) -> str:
        """Generate a unique order ID.
        
        Returns:
            A unique order ID string (e.g., "ORD-0001").
        """
        # TODO: Implement order ID generation
        raise NotImplementedError("Implement generate_order_id")
    
    @classmethod
    def reset_counter(cls) -> None:
        """Reset the order ID counter (useful for testing)."""
        # TODO: Implement counter reset
        raise NotImplementedError("Implement reset_counter")
    
    @classmethod
    def from_cart(
        cls,
        user_id: str,
        cart_items: list,
        order_id: str | None = None
    ) -> Order:
        """Create an Order from cart items.
        
        Args:
            user_id: ID of the user.
            cart_items: List of CartItem objects.
            order_id: Optional order ID (generated if not provided).
        
        Returns:
            A new Order instance.
        """
        # TODO: Implement factory method from cart
        raise NotImplementedError("Implement from_cart")
