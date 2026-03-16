"""Solution for Problem 03: Order Management System.

Demonstrates class design principles:
- Encapsulation: Product manages its own stock
- Cohesion: OrderLine groups product and quantity with subtotal logic
- State Management: Order tracks status and manages inventory lifecycle
- Separation of Concerns: OrderManager handles workflow, Order handles data
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
        self._sku = sku
        self._name = name
        self._price = price
        self._stock_quantity = stock_quantity
        self._reserved_quantity = 0
    
    @property
    def sku(self) -> str:
        return self._sku
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def price(self) -> float:
        return self._price
    
    @property
    def stock_quantity(self) -> int:
        return self._stock_quantity
    
    @property
    def available_quantity(self) -> int:
        """Quantity available for reservation."""
        return self._stock_quantity - self._reserved_quantity
    
    def reserve_stock(self, quantity: int) -> bool:
        """Reserve stock for an order.
        
        Args:
            quantity: Amount to reserve
            
        Returns:
            True if reservation successful
        """
        if quantity > self.available_quantity:
            return False
        self._reserved_quantity += quantity
        return True
    
    def release_stock(self, quantity: int) -> None:
        """Release reserved stock (order cancelled).
        
        Args:
            quantity: Amount to release
        """
        self._reserved_quantity = max(0, self._reserved_quantity - quantity)
    
    def confirm_sale(self, quantity: int) -> None:
        """Confirm sale (order shipped) - stock already reserved.
        
        Args:
            quantity: Amount sold
        """
        self._reserved_quantity -= quantity
        self._stock_quantity -= quantity
    
    def is_available(self, quantity: int = 1) -> bool:
        """Check if quantity is available.
        
        Args:
            quantity: Amount needed
            
        Returns:
            True if available
        """
        return self.available_quantity >= quantity


class Customer:
    """Customer placing orders.
    
    Attributes:
        customer_id: Unique customer identifier
        name: Customer name
        email: Customer email address
    """
    
    def __init__(self, customer_id: str, name: str, email: str) -> None:
        self._customer_id = customer_id
        self._name = name
        self._email = email
    
    @property
    def customer_id(self) -> str:
        return self._customer_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def email(self) -> str:
        return self._email


class OrderLine:
    """Single line item in an order.
    
    Attributes:
        product: Product being ordered
        quantity: Quantity ordered
        unit_price: Price at time of order
    """
    
    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self._product = product
        self._quantity = quantity
        self._unit_price = product.price  # Snapshot price at order time
    
    @property
    def product(self) -> Product:
        return self._product
    
    @property
    def quantity(self) -> int:
        return self._quantity
    
    @property
    def unit_price(self) -> float:
        return self._unit_price
    
    @property
    def subtotal(self) -> float:
        """Calculate line subtotal."""
        return self._unit_price * self._quantity
    
    def can_fulfill(self) -> bool:
        """Check if product is available in requested quantity."""
        return self._product.is_available(self._quantity)


class Order:
    """Customer order containing multiple line items.
    
    Attributes:
        order_id: Unique order identifier
        customer: Customer who placed order
        status: Current order status
        created_at: When order was created
    """
    
    def __init__(self, order_id: str, customer: Customer) -> None:
        self._order_id = order_id
        self._customer = customer
        self._lines: list[OrderLine] = []
        self._status = OrderStatus.PENDING
        self._created_at = datetime.now()
    
    @property
    def order_id(self) -> str:
        return self._order_id
    
    @property
    def customer(self) -> Customer:
        return self._customer
    
    @property
    def status(self) -> OrderStatus:
        return self._status
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def lines(self) -> list[OrderLine]:
        return self._lines.copy()
    
    def add_line(self, product: Product, quantity: int) -> bool:
        """Add a product line to the order.
        
        Args:
            product: Product to add
            quantity: Quantity to order
            
        Returns:
            True if added successfully
        """
        if self._status != OrderStatus.PENDING:
            return False
        try:
            line = OrderLine(product, quantity)
            self._lines.append(line)
            return True
        except ValueError:
            return False
    
    @property
    def total(self) -> float:
        """Calculate order total."""
        return sum(line.subtotal for line in self._lines)
    
    def can_fulfill(self) -> bool:
        """Check if all items are available."""
        return all(line.can_fulfill() for line in self._lines)
    
    def reserve_inventory(self) -> bool:
        """Reserve stock for all items."""
        if not self.can_fulfill():
            return False
        for line in self._lines:
            if not line.product.reserve_stock(line.quantity):
                # Rollback on failure
                for prev_line in self._lines:
                    if prev_line is line:
                        break
                    prev_line.product.release_stock(prev_line.quantity)
                return False
        return True
    
    def release_inventory(self) -> None:
        """Release reserved stock."""
        for line in self._lines:
            line.product.release_stock(line.quantity)
    
    def _set_status(self, status: OrderStatus) -> None:
        """Internal status update (used by OrderManager)."""
        self._status = status


class OrderManager:
    """Manages order lifecycle and state transitions.
    
    Coordinates order creation, confirmation, shipping, and cancellation.
    Single Responsibility: Order workflow management.
    """
    
    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}
    
    def create_order(self, order_id: str, customer: Customer) -> Order:
        """Create a new order.
        
        Args:
            order_id: Unique order identifier
            customer: Customer placing order
            
        Returns:
            New order instance
        """
        order = Order(order_id, customer)
        self._orders[order_id] = order
        return order
    
    def confirm_order(self, order: Order) -> bool:
        """Confirm a pending order.
        
        Reserves inventory and updates status.
        
        Args:
            order: Order to confirm
            
        Returns:
            True if confirmed successfully
        """
        if order.status != OrderStatus.PENDING:
            return False
        if not order.reserve_inventory():
            return False
        order._set_status(OrderStatus.CONFIRMED)
        return True
    
    def ship_order(self, order: Order) -> bool:
        """Ship a confirmed order.
        
        Args:
            order: Order to ship
            
        Returns:
            True if shipped successfully
        """
        if order.status != OrderStatus.CONFIRMED:
            return False
        # Confirm the actual sale (remove from stock)
        for line in order.lines:
            line.product.confirm_sale(line.quantity)
        order._set_status(OrderStatus.SHIPPED)
        return True
    
    def cancel_order(self, order: Order) -> bool:
        """Cancel an order.
        
        Releases reserved inventory.
        
        Args:
            order: Order to cancel
            
        Returns:
            True if cancelled successfully
        """
        if order.status not in (OrderStatus.PENDING, OrderStatus.CONFIRMED):
            return False
        order.release_inventory()
        order._set_status(OrderStatus.CANCELLED)
        return True
