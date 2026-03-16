"""Problem 04: Stateful Object Regression Tests

Topic: State-based testing
Difficulty: Medium

Learn to thoroughly test stateful objects with complex state machines.
Cover valid transitions, invalid transitions, and state invariants.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto
from typing import Optional, Callable
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
    """Line item in an order.
    
    Attributes:
        product_id: Product identifier
        product_name: Human-readable name
        quantity: Number ordered
        unit_price: Price per unit
    """
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
    """Payment details for an order.
    
    Attributes:
        transaction_id: External payment reference
        amount_paid: Actual amount charged
        timestamp: When payment was processed
        method: Payment method used
    """
    transaction_id: str
    amount_paid: Decimal
    timestamp: datetime
    method: str


@dataclass
class ShippingInfo:
    """Shipping details for an order.
    
    Attributes:
        carrier: Shipping carrier name
        tracking_number: Tracking reference
        shipped_at: When order was shipped
        estimated_delivery: Expected arrival date
    """
    carrier: str
    tracking_number: str
    shipped_at: datetime
    estimated_delivery: datetime


class Order:
    """Stateful order entity with lifecycle management.
    
    Implements a state machine governing valid transitions.
    Tracks history of all state changes.
    
    Valid transitions:
    - DRAFT → PENDING_PAYMENT (submit)
    - PENDING_PAYMENT → PAID (mark_paid)
    - PENDING_PAYMENT → CANCELLED (cancel)
    - PAID → PROCESSING (start_processing)
    - PAID → CANCELLED (cancel with refund)
    - PROCESSING → SHIPPED (ship)
    - PROCESSING → CANCELLED (cancel)
    - SHIPPED → DELIVERED (mark_delivered)
    - PAID → REFUNDED (refund)
    - SHIPPED → REFUNDED (refund)
    - DELIVERED → REFUNDED (refund)
    
    TODO: Implement the order state machine.
    """
    
    def __init__(self, customer_id: str, items: Optional[list[OrderItem]] = None) -> None:
        """Initialize a new order in DRAFT state.
        
        Args:
            customer_id: The customer placing the order
            items: Initial items (optional)
        """
        raise NotImplementedError("Implement __init__")
    
    @property
    def status(self) -> OrderStatus:
        """Current order status."""
        raise NotImplementedError("Implement status property")
    
    @property
    def total_amount(self) -> Decimal:
        """Calculate total order amount."""
        raise NotImplementedError("Implement total_amount property")
    
    @property
    def can_cancel(self) -> bool:
        """Check if order can be cancelled in current state."""
        raise NotImplementedError("Implement can_cancel property")
    
    @property
    def can_refund(self) -> bool:
        """Check if order can be refunded in current state."""
        raise NotImplementedError("Implement can_refund property")
    
    def add_item(self, item: OrderItem) -> None:
        """Add an item to the order.
        
        Only allowed in DRAFT state.
        
        Args:
            item: The item to add
            
        Raises:
            InvalidStateTransition: If not in DRAFT state
        """
        raise NotImplementedError("Implement add_item")
    
    def submit(self) -> None:
        """Submit the order for payment.
        
        Transitions: DRAFT → PENDING_PAYMENT
        
        Raises:
            InvalidStateTransition: If not in DRAFT state
            ValueError: If no items in order
        """
        raise NotImplementedError("Implement submit")
    
    def mark_paid(self, payment_info: PaymentInfo) -> None:
        """Mark order as paid.
        
        Transitions: PENDING_PAYMENT → PAID
        
        Args:
            payment_info: Details of the payment
            
        Raises:
            InvalidStateTransition: If not in PENDING_PAYMENT
            ValueError: If payment amount doesn't match order total
        """
        raise NotImplementedError("Implement mark_paid")
    
    def start_processing(self) -> None:
        """Begin order fulfillment.
        
        Transitions: PAID → PROCESSING
        
        Raises:
            InvalidStateTransition: If not in PAID state
        """
        raise NotImplementedError("Implement start_processing")
    
    def ship(self, shipping_info: ShippingInfo) -> None:
        """Mark order as shipped.
        
        Transitions: PROCESSING → SHIPPED
        
        Args:
            shipping_info: Shipping details
            
        Raises:
            InvalidStateTransition: If not in PROCESSING
        """
        raise NotImplementedError("Implement ship")
    
    def mark_delivered(self) -> None:
        """Mark order as delivered.
        
        Transitions: SHIPPED → DELIVERED
        
        Raises:
            InvalidStateTransition: If not in SHIPPED
        """
        raise NotImplementedError("Implement mark_delivered")
    
    def cancel(self, reason: str) -> None:
        """Cancel the order.
        
        Valid from: PENDING_PAYMENT, PAID, PROCESSING
        
        Args:
            reason: Cancellation reason
            
        Raises:
            InvalidStateTransition: If cancellation not allowed
        """
        raise NotImplementedError("Implement cancel")
    
    def refund(self, amount: Optional[Decimal] = None, reason: str = "") -> None:
        """Refund all or part of the order.
        
        Valid from: PAID, SHIPPED, DELIVERED
        Full refund transitions to REFUNDED.
        Partial refund stays in current state.
        
        Args:
            amount: Amount to refund (None for full)
            reason: Refund reason
            
        Raises:
            InvalidStateTransition: If refund not allowed
            ValueError: If refund amount invalid
        """
        raise NotImplementedError("Implement refund")
    
    def get_status_history(self) -> list[tuple[OrderStatus, datetime, Optional[str]]]:
        """Get complete history of state transitions.
        
        Returns:
            List of (status, timestamp, notes) tuples
        """
        raise NotImplementedError("Implement get_status_history")


class OrderService:
    """Service for order operations with validation.
    
    Provides higher-level operations on orders with
    additional business rules.
    
    TODO: Implement service methods.
    """
    
    def __init__(self, order_repository: Optional[object] = None) -> None:
        """Initialize with optional repository.
        
        Args:
            order_repository: Storage for orders
        """
        raise NotImplementedError("Implement __init__")
    
    def create_order(self, customer_id: str) -> Order:
        """Create a new draft order.
        
        Args:
            customer_id: The customer
            
        Returns:
            New order in DRAFT state
        """
        raise NotImplementedError("Implement create_order")
    
    def process_payment_and_fulfill(self, order: Order, payment_info: PaymentInfo) -> None:
        """Complete payment and start fulfillment.
        
        Convenience method that handles the PAID → PROCESSING transition.
        
        Args:
            order: The order to process
            payment_info: Payment details
        """
        raise NotImplementedError("Implement process_payment_and_fulfill")
    
    def get_orders_by_status(self, status: OrderStatus) -> list[Order]:
        """Find all orders in a given status.
        
        Args:
            status: Status to filter by
            
        Returns:
            Matching orders
        """
        raise NotImplementedError("Implement get_orders_by_status")
