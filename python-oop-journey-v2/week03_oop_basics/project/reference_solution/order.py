"""Order Module - Reference Solution.

Implements the Order, OrderItem, and OrderStatus classes for the e-commerce system.
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
        return self.value


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
        self._product_name = product_name
        self._product_sku = product_sku
        self._unit_price = unit_price
        self._quantity = quantity
    
    @property
    def product_name(self) -> str:
        """Get the product name."""
        return self._product_name
    
    @property
    def product_sku(self) -> str:
        """Get the product SKU."""
        return self._product_sku
    
    @property
    def unit_price(self) -> float:
        """Get the unit price."""
        return self._unit_price
    
    @property
    def quantity(self) -> int:
        """Get the quantity."""
        return self._quantity
    
    def get_subtotal(self) -> float:
        """Calculate the subtotal for this item.
        
        Returns:
            unit_price * quantity
        """
        return round(self._unit_price * self._quantity, 2)
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return (
            f"OrderItem(sku='{self._product_sku}', "
            f"quantity={self._quantity})"
        )


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
        self._order_id = order_id
        self._user_id = user_id
        self._items = list(items)
        self._status = status
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return (
            f"Order(order_id='{self._order_id}', user_id='{self._user_id}', "
            f"status={self._status}, items={len(self._items)})"
        )
    
    @property
    def order_id(self) -> str:
        """Get the order ID (read-only)."""
        return self._order_id
    
    @property
    def user_id(self) -> str:
        """Get the user ID (read-only)."""
        return self._user_id
    
    @property
    def items(self) -> list[OrderItem]:
        """Get the order items (read-only copy)."""
        return self._items.copy()
    
    @property
    def status(self) -> OrderStatus:
        """Get the order status."""
        return self._status
    
    @property
    def total(self) -> float:
        """Calculate the order total.
        
        Returns:
            Sum of all item subtotals.
        """
        return round(sum(item.get_subtotal() for item in self._items), 2)
    
    @property
    def item_count(self) -> int:
        """Get the total number of items in the order.
        
        Returns:
            Sum of all item quantities.
        """
        return sum(item.quantity for item in self._items)
    
    def update_status(self, new_status: OrderStatus) -> None:
        """Update the order status.
        
        Args:
            new_status: The new status to set.
        
        Raises:
            ValueError: If status transition is invalid.
        """
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
            OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
            OrderStatus.DELIVERED: [],
            OrderStatus.CANCELLED: [],
        }
        
        if new_status not in valid_transitions[self._status]:
            raise ValueError(
                f"Invalid status transition from {self._status} to {new_status}"
            )
        
        self._status = new_status
    
    def cancel(self) -> bool:
        """Cancel the order if possible.
        
        Returns:
            True if cancelled successfully, False if already shipped/delivered.
        """
        if self.can_cancel():
            self._status = OrderStatus.CANCELLED
            return True
        return False
    
    def can_cancel(self) -> bool:
        """Check if the order can be cancelled.
        
        Returns:
            True if status is PENDING or CONFIRMED.
        """
        return self._status in (OrderStatus.PENDING, OrderStatus.CONFIRMED)
    
    @classmethod
    def generate_order_id(cls) -> str:
        """Generate a unique order ID.
        
        Returns:
            A unique order ID string (e.g., "ORD-0001").
        """
        cls._order_counter += 1
        return f"ORD-{cls._order_counter:04d}"
    
    @classmethod
    def reset_counter(cls) -> None:
        """Reset the order ID counter (useful for testing)."""
        cls._order_counter = 0
    
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
        if order_id is None:
            order_id = cls.generate_order_id()
        
        order_items = [
            OrderItem(
                product_name=item.product.name,
                product_sku=item.product.sku,
                unit_price=item.product.price,
                quantity=item.quantity
            )
            for item in cart_items
        ]
        
        return cls(order_id, user_id, order_items)
