"""Tests for Problem 02: Order Service."""

from __future__ import annotations

from decimal import Decimal

import pytest

from week07_real_world.solutions.day05.problem_02_order_service import (
    Order,
    OrderItem,
    OrderRepository,
    OrderResult,
    OrderService,
    OrderStatus,
    PaymentGateway,
    Product,
    ProductRepository,
)


class MockProductRepository(ProductRepository):
    """Mock implementation of ProductRepository."""
    
    def __init__(self) -> None:
        self._products: dict[int, Product] = {}
    
    def add_product(self, product: Product) -> None:
        self._products[product.id] = product
    
    def get_by_id(self, product_id: int) -> Product | None:
        return self._products.get(product_id)
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        product = self._products.get(product_id)
        if product is None:
            return False
        new_stock = product.stock_quantity + quantity
        if new_stock < 0:
            return False
        product.stock_quantity = new_stock
        return True


class MockOrderRepository(OrderRepository):
    """Mock implementation of OrderRepository."""
    
    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}
        self._next_id = 1
    
    def save(self, order: Order) -> Order:
        if order.id is None:
            order = Order(
                id=self._next_id,
                user_id=order.user_id,
                items=order.items,
                status=order.status,
                total_amount=order.total_amount,
            )
            self._next_id += 1
        self._orders[order.id] = order
        return order
    
    def get_by_id(self, order_id: int) -> Order | None:
        return self._orders.get(order_id)
    
    def update_status(self, order_id: int, status: OrderStatus) -> bool:
        order = self._orders.get(order_id)
        if order is None:
            return False
        order.status = status
        return True


class MockPaymentGateway(PaymentGateway):
    """Mock implementation of PaymentGateway."""
    
    def __init__(self, should_succeed: bool = True) -> None:
        self._should_succeed = should_succeed
        self._transaction_counter = 0
    
    def charge(self, amount: Decimal, order_id: int) -> tuple[bool, str]:
        self._transaction_counter += 1
        if self._should_succeed:
            return (True, f"txn_{self._transaction_counter}")
        return (False, "Insufficient funds")


@pytest.fixture
def product_repo() -> MockProductRepository:
    """Create a product repository with sample products."""
    repo = MockProductRepository()
    repo.add_product(Product(
        id=1, name="Widget", price=Decimal("10.00"), stock_quantity=100
    ))
    repo.add_product(Product(
        id=2, name="Gadget", price=Decimal("25.50"), stock_quantity=50
    ))
    repo.add_product(Product(
        id=3, name="Inactive", price=Decimal("5.00"),
        stock_quantity=10, is_active=False
    ))
    repo.add_product(Product(
        id=4, name="Low Stock", price=Decimal("100.00"), stock_quantity=2
    ))
    return repo


@pytest.fixture
def order_service(
    product_repo: MockProductRepository,
) -> OrderService:
    """Create an OrderService with mock dependencies."""
    return OrderService(
        product_repo=product_repo,
        order_repo=MockOrderRepository(),
        payment_gateway=MockPaymentGateway(should_succeed=True),
    )


class TestOrderService:
    """Tests for OrderService class."""
    
    def test_create_order_success(self, order_service: OrderService) -> None:
        """Test successful order creation."""
        result = order_service.create_order(
            user_id=1,
            items=[{"product_id": 1, "quantity": 5}],
        )
        
        assert result.success
        assert result.order is not None
        assert result.order.id is not None
        assert result.order.user_id == 1
        assert result.order.status == OrderStatus.PENDING
        assert result.order.total_amount == Decimal("50.00")
    
    def test_create_order_multiple_items(
        self, order_service: OrderService
    ) -> None:
        """Test order with multiple items."""
        result = order_service.create_order(
            user_id=1,
            items=[
                {"product_id": 1, "quantity": 2},  # 2 * 10 = 20
                {"product_id": 2, "quantity": 3},  # 3 * 25.50 = 76.50
            ],
        )
        
        assert result.success
        assert result.order is not None
        assert result.order.total_amount == Decimal("96.50")
        assert len(result.order.items) == 2
    
    def test_create_order_empty_items(self, order_service: OrderService) -> None:
        """Test order creation with empty items list."""
        result = order_service.create_order(user_id=1, items=[])
        
        assert not result.success
        assert "at least one item" in result.error_message
    
    def test_create_order_product_not_found(
        self, order_service: OrderService
    ) -> None:
        """Test order with non-existent product."""
        result = order_service.create_order(
            user_id=1,
            items=[{"product_id": 999, "quantity": 1}],
        )
        
        assert not result.success
        assert "not found" in result.error_message
    
    def test_create_order_inactive_product(
        self, order_service: OrderService
    ) -> None:
        """Test order with inactive product."""
        result = order_service.create_order(
            user_id=1,
            items=[{"product_id": 3, "quantity": 1}],
        )
        
        assert not result.success
        assert "not available" in result.error_message
    
    def test_create_order_insufficient_stock(
        self, order_service: OrderService
    ) -> None:
        """Test order with insufficient stock."""
        result = order_service.create_order(
            user_id=1,
            items=[{"product_id": 4, "quantity": 5}],  # Only 2 in stock
        )
        
        assert not result.success
        assert "Insufficient stock" in result.error_message
    
    def test_create_order_invalid_quantity(
        self, order_service: OrderService
    ) -> None:
        """Test order with invalid quantity."""
        result = order_service.create_order(
            user_id=1,
            items=[{"product_id": 1, "quantity": 0}],
        )
        
        assert not result.success
        assert "Invalid quantity" in result.error_message
    
    def test_confirm_order_success(
        self,
        order_service: OrderService,
        product_repo: MockProductRepository,
    ) -> None:
        """Test successful order confirmation."""
        # Create order first
        create_result = order_service.create_order(
            user_id=1,
            items=[{"product_id": 1, "quantity": 10}],
        )
        assert create_result.order is not None
        
        # Initial stock
        initial_stock = product_repo.get_by_id(1).stock_quantity
        
        # Confirm order
        result = order_service.confirm_order(create_result.order.id)
        
        assert result.success
        assert result.order is not None
        assert result.order.status == OrderStatus.CONFIRMED
        
        # Stock should be reduced
        assert product_repo.get_by_id(1).stock_quantity == initial_stock - 10
    
    def test_confirm_order_not_found(self, order_service: OrderService) -> None:
        """Test confirmation of non-existent order."""
        result = order_service.confirm_order(999)
        
        assert not result.success
        assert "not found" in result.error_message
    
    def test_confirm_order_wrong_status(
        self, order_service: OrderService
    ) -> None:
        """Test confirmation of order in wrong status."""
        # Create and confirm order
        create_result = order_service.create_order(
            user_id=1,
            items=[{"product_id": 1, "quantity": 1}],
        )
        assert create_result.order is not None
        order_service.confirm_order(create_result.order.id)
        
        # Try to confirm again
        result = order_service.confirm_order(create_result.order.id)
        
        assert not result.success
        assert "must be in PENDING" in result.error_message
    
    def test_process_payment_success(self, order_service: OrderService) -> None:
        """Test successful payment processing."""
        # Create and confirm order
        create_result = order_service.create_order(
            user_id=1,
            items=[{"product_id": 1, "quantity": 1}],
        )
        assert create_result.order is not None
        order_service.confirm_order(create_result.order.id)
        
        # Process payment
        result = order_service.process_payment(create_result.order.id)
        
        assert result.success
        assert result.order is not None
        assert result.order.status == OrderStatus.PAID
        assert result.transaction_id is not None
    
    def test_process_payment_not_confirmed(
        self, order_service: OrderService
    ) -> None:
        """Test payment on unconfirmed order."""
        create_result = order_service.create_order(
            user_id=1,
            items=[{"product_id": 1, "quantity": 1}],
        )
        assert create_result.order is not None
        
        result = order_service.process_payment(create_result.order.id)
        
        assert not result.success
        assert "must be confirmed" in result.error_message
    
    def test_process_payment_failure(
        self,
        product_repo: MockProductRepository,
    ) -> None:
        """Test payment failure handling."""
        # Create service with failing payment gateway
        service = OrderService(
            product_repo=product_repo,
            order_repo=MockOrderRepository(),
            payment_gateway=MockPaymentGateway(should_succeed=False),
        )
        
        # Create and confirm order
        create_result = service.create_order(
            user_id=1,
            items=[{"product_id": 1, "quantity": 1}],
        )
        assert create_result.order is not None
        service.confirm_order(create_result.order.id)
        
        # Process payment
        result = service.process_payment(create_result.order.id)
        
        assert not result.success
        assert "Payment failed" in result.error_message
    
    def test_cancel_order_pending(
        self, order_service: OrderService
    ) -> None:
        """Test cancellation of pending order."""
        create_result = order_service.create_order(
            user_id=1,
            items=[{"product_id": 1, "quantity": 5}],
        )
        assert create_result.order is not None
        
        result = order_service.cancel_order(create_result.order.id)
        
        assert result.success
        assert result.order is not None
        assert result.order.status == OrderStatus.CANCELLED
    
    def test_cancel_order_confirmed_restores_stock(
        self,
        order_service: OrderService,
        product_repo: MockProductRepository,
    ) -> None:
        """Test that cancelling confirmed order restores stock."""
        create_result = order_service.create_order(
            user_id=1,
            items=[{"product_id": 1, "quantity": 10}],
        )
        assert create_result.order is not None
        order_service.confirm_order(create_result.order.id)
        
        initial_stock = product_repo.get_by_id(1).stock_quantity
        
        result = order_service.cancel_order(create_result.order.id)
        
        assert result.success
        # Stock should be restored
        assert product_repo.get_by_id(1).stock_quantity == initial_stock + 10
    
    def test_cancel_order_not_found(self, order_service: OrderService) -> None:
        """Test cancellation of non-existent order."""
        result = order_service.cancel_order(999)
        
        assert not result.success
        assert "not found" in result.error_message
    
    def test_cancel_order_already_paid(
        self, order_service: OrderService
    ) -> None:
        """Test cancellation of paid order (should fail)."""
        create_result = order_service.create_order(
            user_id=1,
            items=[{"product_id": 1, "quantity": 1}],
        )
        assert create_result.order is not None
        order_service.confirm_order(create_result.order.id)
        order_service.process_payment(create_result.order.id)
        
        result = order_service.cancel_order(create_result.order.id)
        
        assert not result.success
        assert "Cannot cancel" in result.error_message
    
    def test_get_order_success(self, order_service: OrderService) -> None:
        """Test retrieving an order."""
        create_result = order_service.create_order(
            user_id=1,
            items=[{"product_id": 1, "quantity": 1}],
        )
        assert create_result.order is not None
        
        order = order_service.get_order(create_result.order.id)
        
        assert order is not None
        assert order.id == create_result.order.id
    
    def test_get_order_not_found(self, order_service: OrderService) -> None:
        """Test retrieving non-existent order."""
        order = order_service.get_order(999)
        
        assert order is None
