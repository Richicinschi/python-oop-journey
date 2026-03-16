"""Reference solution for Problem 04: Stateful Object Regression Tests."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto
from typing import Optional
from uuid import UUID, uuid4


class OrderStatus(Enum):
    """Order lifecycle states."""
    DRAFT = auto()
    PENDING_PAYMENT = auto()
    PAID = auto()
    PROCESSING = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()
    REFUNDED = auto()


class InvalidStateTransition(Exception):
    """Raised when attempting an invalid state transition."""
    pass


@dataclass
class OrderItem:
    """Line item in an order."""
    product_id: str
    product_name: str
    quantity: int
    unit_price: Decimal
    
    @property
    def total_price(self) -> Decimal:
        """Calculate total for this line item."""
        return self.unit_price * self.quantity


@dataclass
class PaymentInfo:
    """Payment details for an order."""
    transaction_id: str
    amount_paid: Decimal
    timestamp: datetime
    method: str


@dataclass
class ShippingInfo:
    """Shipping details for an order."""
    carrier: str
    tracking_number: str
    shipped_at: datetime
    estimated_delivery: datetime


class Order:
    """Stateful order entity with lifecycle management."""
    
    # Valid state transitions
    _VALID_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
        OrderStatus.DRAFT: {OrderStatus.PENDING_PAYMENT},
        OrderStatus.PENDING_PAYMENT: {OrderStatus.PAID, OrderStatus.CANCELLED},
        OrderStatus.PAID: {OrderStatus.PROCESSING, OrderStatus.CANCELLED, OrderStatus.REFUNDED},
        OrderStatus.PROCESSING: {OrderStatus.SHIPPED, OrderStatus.CANCELLED},
        OrderStatus.SHIPPED: {OrderStatus.DELIVERED, OrderStatus.REFUNDED},
        OrderStatus.DELIVERED: {OrderStatus.REFUNDED},
        OrderStatus.CANCELLED: set(),
        OrderStatus.REFUNDED: set(),
    }
    
    def __init__(self, customer_id: str, items: Optional[list[OrderItem]] = None) -> None:
        """Initialize a new order in DRAFT state."""
        self._id = uuid4()
        self._customer_id = customer_id
        self._items: list[OrderItem] = list(items) if items else []
        self._status = OrderStatus.DRAFT
        self._payment_info: Optional[PaymentInfo] = None
        self._shipping_info: Optional[ShippingInfo] = None
        self._history: list[tuple[OrderStatus, datetime, Optional[str]]] = [
            (OrderStatus.DRAFT, datetime.now(), "Order created")
        ]
        self._refunded_amount = Decimal("0")
        self._cancel_reason: Optional[str] = None
    
    @property
    def id(self) -> UUID:
        """Order unique identifier."""
        return self._id
    
    @property
    def customer_id(self) -> str:
        """Customer identifier."""
        return self._customer_id
    
    @property
    def status(self) -> OrderStatus:
        """Current order status."""
        return self._status
    
    @property
    def items(self) -> list[OrderItem]:
        """Order line items."""
        return self._items.copy()
    
    @property
    def total_amount(self) -> Decimal:
        """Calculate total order amount."""
        return sum((item.total_price for item in self._items), Decimal("0"))
    
    @property
    def can_cancel(self) -> bool:
        """Check if order can be cancelled in current state."""
        return OrderStatus.CANCELLED in self._VALID_TRANSITIONS.get(self._status, set())
    
    @property
    def can_refund(self) -> bool:
        """Check if order can be refunded in current state."""
        return OrderStatus.REFUNDED in self._VALID_TRANSITIONS.get(self._status, set())
    
    def _transition_to(self, new_status: OrderStatus, note: Optional[str] = None) -> None:
        """Execute a state transition."""
        valid_targets = self._VALID_TRANSITIONS.get(self._status, set())
        if new_status not in valid_targets:
            raise InvalidStateTransition(
                f"Cannot transition from {self._status.name} to {new_status.name}"
            )
        self._status = new_status
        self._history.append((new_status, datetime.now(), note))
    
    def add_item(self, item: OrderItem) -> None:
        """Add an item to the order."""
        if self._status != OrderStatus.DRAFT:
            raise InvalidStateTransition("Cannot modify order after submission")
        self._items.append(item)
    
    def submit(self) -> None:
        """Submit the order for payment."""
        if not self._items:
            raise ValueError("Cannot submit empty order")
        self._transition_to(OrderStatus.PENDING_PAYMENT, "Order submitted")
    
    def mark_paid(self, payment_info: PaymentInfo) -> None:
        """Mark order as paid."""
        if payment_info.amount_paid != self.total_amount:
            raise ValueError("Payment amount does not match order total")
        self._payment_info = payment_info
        self._transition_to(OrderStatus.PAID, f"Payment received: {payment_info.transaction_id}")
    
    def start_processing(self) -> None:
        """Begin order fulfillment."""
        self._transition_to(OrderStatus.PROCESSING, "Fulfillment started")
    
    def ship(self, shipping_info: ShippingInfo) -> None:
        """Mark order as shipped."""
        self._shipping_info = shipping_info
        self._transition_to(OrderStatus.SHIPPED, f"Shipped via {shipping_info.carrier}")
    
    def mark_delivered(self) -> None:
        """Mark order as delivered."""
        self._transition_to(OrderStatus.DELIVERED, "Delivered to customer")
    
    def cancel(self, reason: str) -> None:
        """Cancel the order."""
        if not self.can_cancel:
            raise InvalidStateTransition(f"Cannot cancel order in {self._status.name} state")
        self._cancel_reason = reason
        self._transition_to(OrderStatus.CANCELLED, f"Cancelled: {reason}")
    
    def refund(self, amount: Optional[Decimal] = None, reason: str = "") -> None:
        """Refund all or part of the order."""
        if not self.can_refund:
            raise InvalidStateTransition(f"Cannot refund order in {self._status.name} state")
        
        refund_amount = amount or (self.total_amount - self._refunded_amount)
        
        if refund_amount <= 0:
            raise ValueError("Refund amount must be positive")
        
        remaining = self.total_amount - self._refunded_amount
        if refund_amount > remaining:
            raise ValueError("Refund amount exceeds remaining balance")
        
        self._refunded_amount += refund_amount
        
        if self._refunded_amount >= self.total_amount:
            self._transition_to(OrderStatus.REFUNDED, f"Fully refunded: {reason}")
        else:
            self._history.append((self._status, datetime.now(), f"Partial refund: {refund_amount} - {reason}"))
    
    def get_status_history(self) -> list[tuple[OrderStatus, datetime, Optional[str]]]:
        """Get complete history of state transitions."""
        return self._history.copy()
    
    @property
    def payment_info(self) -> Optional[PaymentInfo]:
        """Payment information if paid."""
        return self._payment_info
    
    @property
    def shipping_info(self) -> Optional[ShippingInfo]:
        """Shipping information if shipped."""
        return self._shipping_info


class OrderService:
    """Service for order operations with validation."""
    
    def __init__(self, order_repository: Optional[object] = None) -> None:
        """Initialize with optional repository."""
        self._repository = order_repository
        self._orders: list[Order] = []
    
    def create_order(self, customer_id: str) -> Order:
        """Create a new draft order."""
        order = Order(customer_id=customer_id)
        self._orders.append(order)
        return order
    
    def process_payment_and_fulfill(self, order: Order, payment_info: PaymentInfo) -> None:
        """Complete payment and start fulfillment."""
        order.mark_paid(payment_info)
        order.start_processing()
    
    def get_orders_by_status(self, status: OrderStatus) -> list[Order]:
        """Find all orders in a given status."""
        return [o for o in self._orders if o.status == status]
    
    def get_order(self, order_id: UUID) -> Optional[Order]:
        """Get order by ID."""
        for order in self._orders:
            if order.id == order_id:
                return order
        return None
