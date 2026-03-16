"""Problem 03: Order Management System.

Topic: Class Design Principles
Difficulty: Medium

Design an order management system with the following classes:
- Product: Product with SKU, name, price, and stock quantity
- Customer: Customer with ID, name, and email
- OrderLine: Single line item in an order (product + quantity)
- Order: Collection of order lines with status and total calculation
- OrderManager: Manages order lifecycle (create, update, cancel)

Requirements:
- Products track stock levels and validate availability
- OrderLines calculate subtotals
- Orders calculate totals and track status (pending, confirmed, shipped, cancelled)
- OrderManager handles order state transitions
- Stock is reserved when order is created, released if cancelled

Hints:
    - Hint 1: Product tracks stock separately: available vs reserved (or check availability on demand)
    - Hint 2: Order status transitions: PENDING -> CONFIRMED -> SHIPPED; can CANCEL from PENDING/CONFIRMED
    - Hint 3: Order.total property iterates over order lines summing line.subtotal for each
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum, auto


class OrderStatus(Enum):
    """Possible order statuses."""
    PENDING = auto()
    CONFIRMED = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()


class Product:
    """Product available for purchase.
    
    Attributes:
        sku: Stock keeping unit (unique identifier)
        name: Product name
        price: Unit price
        stock_quantity: Available stock
    """
    
    def __init__(self, sku: str, name: str, price: float, stock_quantity: int) -> None:
        raise NotImplementedError("Implement Product.__init__")
    
    def reserve_stock(self, quantity: int) -> bool:
        """Reserve stock for an order.
        
        Args:
            quantity: Amount to reserve
            
        Returns:
            True if reservation successful
        """
        raise NotImplementedError("Implement Product.reserve_stock")
    
    def release_stock(self, quantity: int) -> None:
        """Release reserved stock (order cancelled).
        
        Args:
            quantity: Amount to release
        """
        raise NotImplementedError("Implement Product.release_stock")
    
    def confirm_sale(self, quantity: int) -> None:
        """Confirm sale (order shipped) - stock already reserved.
        
        Args:
            quantity: Amount sold
        """
        raise NotImplementedError("Implement Product.confirm_sale")
    
    def is_available(self, quantity: int = 1) -> bool:
        """Check if quantity is available.
        
        Args:
            quantity: Amount needed
            
        Returns:
            True if available
        """
        raise NotImplementedError("Implement Product.is_available")


class Customer:
    """Customer placing orders.
    
    Attributes:
        customer_id: Unique customer identifier
        name: Customer name
        email: Customer email address
    """
    
    def __init__(self, customer_id: str, name: str, email: str) -> None:
        raise NotImplementedError("Implement Customer.__init__")


class OrderLine:
    """Single line item in an order.
    
    Attributes:
        product: Product being ordered
        quantity: Quantity ordered
        unit_price: Price at time of order
    """
    
    def __init__(self, product: Product, quantity: int) -> None:
        raise NotImplementedError("Implement OrderLine.__init__")
    
    @property
    def subtotal(self) -> float:
        """Calculate line subtotal."""
        raise NotImplementedError("Implement OrderLine.subtotal")
    
    def can_fulfill(self) -> bool:
        """Check if product is available in requested quantity."""
        raise NotImplementedError("Implement OrderLine.can_fulfill")


class Order:
    """Customer order containing multiple line items.
    
    Attributes:
        order_id: Unique order identifier
        customer: Customer who placed order
        status: Current order status
        created_at: When order was created
    """
    
    def __init__(self, order_id: str, customer: Customer) -> None:
        raise NotImplementedError("Implement Order.__init__")
    
    def add_line(self, product: Product, quantity: int) -> bool:
        """Add a product line to the order.
        
        Args:
            product: Product to add
            quantity: Quantity to order
            
        Returns:
            True if added successfully
        """
        raise NotImplementedError("Implement Order.add_line")
    
    @property
    def total(self) -> float:
        """Calculate order total."""
        raise NotImplementedError("Implement Order.total")
    
    def can_fulfill(self) -> bool:
        """Check if all items are available."""
        raise NotImplementedError("Implement Order.can_fulfill")
    
    def reserve_inventory(self) -> bool:
        """Reserve stock for all items."""
        raise NotImplementedError("Implement Order.reserve_inventory")
    
    def release_inventory(self) -> None:
        """Release reserved stock."""
        raise NotImplementedError("Implement Order.release_inventory")


class OrderManager:
    """Manages order lifecycle and state transitions.
    
    Coordinates order creation, confirmation, shipping, and cancellation.
    Single Responsibility: Order workflow management.
    """
    
    def __init__(self) -> None:
        raise NotImplementedError("Implement OrderManager.__init__")
    
    def create_order(self, order_id: str, customer: Customer) -> Order:
        """Create a new order.
        
        Args:
            order_id: Unique order identifier
            customer: Customer placing order
            
        Returns:
            New order instance
        """
        raise NotImplementedError("Implement OrderManager.create_order")
    
    def confirm_order(self, order: Order) -> bool:
        """Confirm a pending order.
        
        Reserves inventory and updates status.
        
        Args:
            order: Order to confirm
            
        Returns:
            True if confirmed successfully
        """
        raise NotImplementedError("Implement OrderManager.confirm_order")
    
    def ship_order(self, order: Order) -> bool:
        """Ship a confirmed order.
        
        Args:
            order: Order to ship
            
        Returns:
            True if shipped successfully
        """
        raise NotImplementedError("Implement OrderManager.ship_order")
    
    def cancel_order(self, order: Order) -> bool:
        """Cancel an order.
        
        Releases reserved inventory.
        
        Args:
            order: Order to cancel
            
        Returns:
            True if cancelled successfully
        """
        raise NotImplementedError("Implement OrderManager.cancel_order")
