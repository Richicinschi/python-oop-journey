"""Problem 02: Order Service

Topic: Service layer with transaction-like operations, validation
Difficulty: Medium

Implement an OrderService that handles order processing with inventory checks,
price calculations, and status management.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum, auto
from typing import Any


class OrderStatus(Enum):
    """Order lifecycle states."""
    PENDING = auto()
    CONFIRMED = auto()
    PAID = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()


@dataclass
class Product:
    """Domain model for a product."""
    id: int
    name: str
    price: Decimal
    stock_quantity: int
    is_active: bool = True


@dataclass
class OrderItem:
    """Line item in an order."""
    product_id: int
    quantity: int
    unit_price: Decimal  # Price at time of order


@dataclass
class Order:
    """Domain model for an order."""
    id: int | None
    user_id: int
    items: list[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    total_amount: Decimal = Decimal("0")


class ProductRepository(ABC):
    """Abstract repository for products."""
    
    @abstractmethod
    def get_by_id(self, product_id: int) -> Product | None:
        """Get product by ID."""
        raise NotImplementedError("Implement get_by_id")
    
    @abstractmethod
    def update_stock(self, product_id: int, quantity: int) -> bool:
        """Update product stock quantity. Returns True if successful."""
        raise NotImplementedError("Implement update_stock")


class OrderRepository(ABC):
    """Abstract repository for orders."""
    
    @abstractmethod
    def save(self, order: Order) -> Order:
        """Save order and return with assigned ID."""
        raise NotImplementedError("Implement save")
    
    @abstractmethod
    def get_by_id(self, order_id: int) -> Order | None:
        """Get order by ID."""
        raise NotImplementedError("Implement get_by_id")
    
    @abstractmethod
    def update_status(self, order_id: int, status: OrderStatus) -> bool:
        """Update order status."""
        raise NotImplementedError("Implement update_status")


class PaymentGateway(ABC):
    """Abstract payment processing service."""
    
    @abstractmethod
    def charge(self, amount: Decimal, order_id: int) -> tuple[bool, str]:
        """Process payment. Returns (success, transaction_id or error)."""
        raise NotImplementedError("Implement charge")


@dataclass
class OrderResult:
    """Result of order operation."""
    success: bool
    order: Order | None = None
    error_message: str | None = None
    transaction_id: str | None = None


class OrderService:
    """Service for order processing and management.
    
    Responsibilities:
    - Create orders with inventory validation
    - Calculate totals with price snapshots
    - Process payments
    - Manage order status lifecycle
    
    Dependencies:
    - product_repo: For inventory checks and updates
    - order_repo: For order persistence
    - payment_gateway: For processing payments
    
    Example:
        >>> service = OrderService(product_repo, order_repo, payment)
        >>> result = service.create_order(
        ...     user_id=1,
        ...     items=[{"product_id": 1, "quantity": 2}]
        ... )
        >>> if result.success:
        ...     print(f"Order {result.order.id} created")
    """
    
    def __init__(
        self,
        product_repo: ProductRepository,
        order_repo: OrderRepository,
        payment_gateway: PaymentGateway,
    ) -> None:
        """Initialize with dependencies.
        
        Args:
            product_repo: Repository for product data
            order_repo: Repository for order persistence
            payment_gateway: Service for payment processing
        """
        raise NotImplementedError("Implement __init__")
    
    def create_order(
        self,
        user_id: int,
        items: list[dict[str, Any]],
    ) -> OrderResult:
        """Create a new order.
        
        Business rules:
        - All products must exist and be active
        - Requested quantity must be available in stock
        - Unit price is snapshot at time of order creation
        - Total is sum of (unit_price * quantity) for all items
        - Initial status is PENDING
        
        Args:
            user_id: ID of user placing order
            items: List of {"product_id": int, "quantity": int}
        
        Returns:
            OrderResult with created order or error details
        """
        raise NotImplementedError("Implement create_order")
    
    def confirm_order(self, order_id: int) -> OrderResult:
        """Confirm order and reserve inventory.
        
        Transitions status from PENDING to CONFIRMED.
        Deducts stock for each item.
        
        Args:
            order_id: ID of order to confirm
            
        Returns:
            OrderResult with updated order or error
        """
        raise NotImplementedError("Implement confirm_order")
    
    def process_payment(self, order_id: int) -> OrderResult:
        """Process payment for an order.
        
        Business rules:
        - Order must be in CONFIRMED status
        - Payment gateway charge must succeed
        - Status changes to PAID on success
        
        Args:
            order_id: ID of order to pay for
            
        Returns:
            OrderResult with transaction ID or error
        """
        raise NotImplementedError("Implement process_payment")
    
    def cancel_order(self, order_id: int) -> OrderResult:
        """Cancel an order.
        
        Business rules:
        - Can cancel if PENDING or CONFIRMED
        - If CONFIRMED, restore inventory
        - Status changes to CANCELLED
        
        Args:
            order_id: ID of order to cancel
            
        Returns:
            OrderResult with updated order or error
        """
        raise NotImplementedError("Implement cancel_order")
    
    def get_order(self, order_id: int) -> Order | None:
        """Retrieve order by ID.
        
        Args:
            order_id: ID of order to retrieve
            
        Returns:
            Order if found, None otherwise
        """
        raise NotImplementedError("Implement get_order")
