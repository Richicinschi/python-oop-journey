"""Reference solution for Problem 02: Order Service."""

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
    unit_price: Decimal


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
    """Service for order processing and management."""
    
    def __init__(
        self,
        product_repo: ProductRepository,
        order_repo: OrderRepository,
        payment_gateway: PaymentGateway,
    ) -> None:
        """Initialize with dependencies."""
        self._product_repo = product_repo
        self._order_repo = order_repo
        self._payment_gateway = payment_gateway
    
    def create_order(
        self,
        user_id: int,
        items: list[dict[str, Any]],
    ) -> OrderResult:
        """Create a new order."""
        if not items:
            return OrderResult(
                success=False,
                error_message="Order must contain at least one item",
            )
        
        order_items: list[OrderItem] = []
        total = Decimal("0")
        
        for item_data in items:
            product_id = item_data["product_id"]
            quantity = item_data["quantity"]
            
            # Validate quantity
            if quantity <= 0:
                return OrderResult(
                    success=False,
                    error_message=f"Invalid quantity for product {product_id}",
                )
            
            # Get product
            product = self._product_repo.get_by_id(product_id)
            if product is None:
                return OrderResult(
                    success=False,
                    error_message=f"Product {product_id} not found",
                )
            
            # Check product is active
            if not product.is_active:
                return OrderResult(
                    success=False,
                    error_message=f"Product {product_id} is not available",
                )
            
            # Check stock
            if product.stock_quantity < quantity:
                return OrderResult(
                    success=False,
                    error_message=f"Insufficient stock for product {product_id}",
                )
            
            # Create order item with price snapshot
            order_item = OrderItem(
                product_id=product_id,
                quantity=quantity,
                unit_price=product.price,
            )
            order_items.append(order_item)
            total += product.price * quantity
        
        # Create and save order
        order = Order(
            id=None,
            user_id=user_id,
            items=order_items,
            status=OrderStatus.PENDING,
            total_amount=total,
        )
        saved_order = self._order_repo.save(order)
        
        return OrderResult(success=True, order=saved_order)
    
    def confirm_order(self, order_id: int) -> OrderResult:
        """Confirm order and reserve inventory."""
        order = self._order_repo.get_by_id(order_id)
        if order is None:
            return OrderResult(
                success=False,
                error_message="Order not found",
            )
        
        if order.status != OrderStatus.PENDING:
            return OrderResult(
                success=False,
                error_message="Order must be in PENDING status to confirm",
            )
        
        # Deduct stock for each item
        for item in order.items:
            success = self._product_repo.update_stock(
                item.product_id,
                -item.quantity,
            )
            if not success:
                # In a real system, we'd need to rollback previous deductions
                return OrderResult(
                    success=False,
                    error_message=f"Failed to reserve stock for product {item.product_id}",
                )
        
        # Update order status
        self._order_repo.update_status(order_id, OrderStatus.CONFIRMED)
        order.status = OrderStatus.CONFIRMED
        
        return OrderResult(success=True, order=order)
    
    def process_payment(self, order_id: int) -> OrderResult:
        """Process payment for an order."""
        order = self._order_repo.get_by_id(order_id)
        if order is None:
            return OrderResult(
                success=False,
                error_message="Order not found",
            )
        
        if order.status != OrderStatus.CONFIRMED:
            return OrderResult(
                success=False,
                error_message="Order must be confirmed before payment",
            )
        
        # Process payment
        success, result = self._payment_gateway.charge(
            order.total_amount,
            order_id,
        )
        
        if not success:
            return OrderResult(
                success=False,
                error_message=f"Payment failed: {result}",
            )
        
        # Update status to PAID
        self._order_repo.update_status(order_id, OrderStatus.PAID)
        order.status = OrderStatus.PAID
        
        return OrderResult(
            success=True,
            order=order,
            transaction_id=result,
        )
    
    def cancel_order(self, order_id: int) -> OrderResult:
        """Cancel an order."""
        order = self._order_repo.get_by_id(order_id)
        if order is None:
            return OrderResult(
                success=False,
                error_message="Order not found",
            )
        
        if order.status not in (OrderStatus.PENDING, OrderStatus.CONFIRMED):
            return OrderResult(
                success=False,
                error_message="Cannot cancel order in current status",
            )
        
        # Restore inventory if order was confirmed
        if order.status == OrderStatus.CONFIRMED:
            for item in order.items:
                self._product_repo.update_stock(
                    item.product_id,
                    item.quantity,
                )
        
        # Update status
        self._order_repo.update_status(order_id, OrderStatus.CANCELLED)
        order.status = OrderStatus.CANCELLED
        
        return OrderResult(success=True, order=order)
    
    def get_order(self, order_id: int) -> Order | None:
        """Retrieve order by ID."""
        return self._order_repo.get_by_id(order_id)
