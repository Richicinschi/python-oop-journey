"""Tests for Problem 04: Stateful Object Regression Tests."""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from uuid import UUID

import pytest

from week07_real_world.solutions.day02.problem_04_stateful_object_regression_tests import (
    InvalidStateTransition,
    Order,
    OrderItem,
    OrderService,
    OrderStatus,
    PaymentInfo,
    ShippingInfo,
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def empty_order() -> Order:
    """Fresh draft order with no items."""
    return Order(customer_id="cust_123")


@pytest.fixture
def order_with_items() -> Order:
    """Draft order with sample items."""
    order = Order(customer_id="cust_123")
    order.add_item(OrderItem("prod_1", "Widget", 2, Decimal("29.99")))
    order.add_item(OrderItem("prod_2", "Gadget", 1, Decimal("49.99")))
    return order


@pytest.fixture
def pending_order(order_with_items: Order) -> Order:
    """Order in PENDING_PAYMENT state."""
    order_with_items.submit()
    return order_with_items


@pytest.fixture
def paid_order(pending_order: Order) -> Order:
    """Order in PAID state."""
    payment = PaymentInfo(
        transaction_id="txn_123",
        amount_paid=pending_order.total_amount,
        timestamp=datetime.now(),
        method="credit_card"
    )
    pending_order.mark_paid(payment)
    return pending_order


@pytest.fixture
def processing_order(paid_order: Order) -> Order:
    """Order in PROCESSING state."""
    paid_order.start_processing()
    return paid_order


@pytest.fixture
def shipped_order(processing_order: Order) -> Order:
    """Order in SHIPPED state."""
    shipping = ShippingInfo(
        carrier="UPS",
        tracking_number="1Z999AA10123456784",
        shipped_at=datetime.now(),
        estimated_delivery=datetime.now() + timedelta(days=3)
    )
    processing_order.ship(shipping)
    return processing_order


@pytest.fixture
def delivered_order(shipped_order: Order) -> Order:
    """Order in DELIVERED state."""
    shipped_order.mark_delivered()
    return shipped_order


@pytest.fixture
def order_service() -> OrderService:
    """Fresh order service instance."""
    return OrderService()


# ============================================================================
# TESTS - Initial State
# ============================================================================

class TestOrderInitialState:
    """Tests for order creation and initial state."""
    
    def test_new_order_is_draft(self, empty_order: Order) -> None:
        """New orders should start in DRAFT state."""
        assert empty_order.status == OrderStatus.DRAFT
    
    def test_new_order_has_zero_total(self, empty_order: Order) -> None:
        """Empty order should have zero total."""
        assert empty_order.total_amount == Decimal("0")
    
    def test_new_order_has_history_with_draft(self, empty_order: Order) -> None:
        """History should contain initial DRAFT entry."""
        history = empty_order.get_status_history()
        assert len(history) == 1
        assert history[0][0] == OrderStatus.DRAFT


# ============================================================================
# TESTS - Draft State Operations
# ============================================================================

class TestOrderDraftOperations:
    """Tests for operations allowed in DRAFT state."""
    
    def test_add_item_increases_total(self, empty_order: Order) -> None:
        """Adding items should update total."""
        item = OrderItem("prod_1", "Widget", 2, Decimal("10.00"))
        
        empty_order.add_item(item)
        
        assert empty_order.total_amount == Decimal("20.00")
    
    def test_add_multiple_items(self, order_with_items: Order) -> None:
        """Should support multiple items."""
        # 2 * 29.99 + 1 * 49.99 = 109.97
        assert order_with_items.total_amount == Decimal("109.97")
    
    def test_submit_empty_order_raises(self, empty_order: Order) -> None:
        """Should not allow submitting empty order."""
        with pytest.raises(ValueError, match="empty"):
            empty_order.submit()
    
    def test_submit_with_items_transitions_to_pending(self, order_with_items: Order) -> None:
        """Submit should transition to PENDING_PAYMENT."""
        order_with_items.submit()
        
        assert order_with_items.status == OrderStatus.PENDING_PAYMENT


# ============================================================================
# TESTS - Invalid State Transitions
# ============================================================================

class TestOrderInvalidTransitions:
    """Tests for transitions that should fail."""
    
    def test_cannot_add_item_after_submit(self, pending_order: Order) -> None:
        """Should not allow modifications after submission."""
        with pytest.raises(InvalidStateTransition):
            pending_order.add_item(OrderItem("prod_3", "New", 1, Decimal("10.00")))
    
    def test_cannot_submit_twice(self, pending_order: Order) -> None:
        """Should not allow double submission."""
        with pytest.raises(InvalidStateTransition):
            pending_order.submit()
    
    def test_cannot_ship_unprocessed_order(self, paid_order: Order) -> None:
        """Cannot ship before processing."""
        shipping = ShippingInfo("UPS", "123", datetime.now(), datetime.now())
        
        with pytest.raises(InvalidStateTransition):
            paid_order.ship(shipping)
    
    def test_cannot_deliver_unshipped_order(self, processing_order: Order) -> None:
        """Cannot mark delivered before shipping."""
        with pytest.raises(InvalidStateTransition):
            processing_order.mark_delivered()
    
    def test_cannot_rewind_state(self, pending_order: Order) -> None:
        """Cannot go back to DRAFT."""
        with pytest.raises(InvalidStateTransition):
            # Try to submit again (would require DRAFT state)
            pending_order.add_item(OrderItem("x", "Y", 1, Decimal("1.00")))


# ============================================================================
# TESTS - Payment Flow
# ============================================================================

class TestOrderPaymentFlow:
    """Tests for payment-related transitions."""
    
    def test_mark_paid_transitions_to_paid(self, pending_order: Order) -> None:
        """Payment should transition to PAID."""
        payment = PaymentInfo(
            transaction_id="txn_123",
            amount_paid=pending_order.total_amount,
            timestamp=datetime.now(),
            method="credit_card"
        )
        
        pending_order.mark_paid(payment)
        
        assert pending_order.status == OrderStatus.PAID
    
    def test_mark_paid_with_wrong_amount_raises(self, pending_order: Order) -> None:
        """Payment amount must match order total."""
        payment = PaymentInfo(
            transaction_id="txn_123",
            amount_paid=pending_order.total_amount + Decimal("1.00"),
            timestamp=datetime.now(),
            method="credit_card"
        )
        
        with pytest.raises(ValueError, match="match"):
            pending_order.mark_paid(payment)
    
    def test_payment_info_stored(self, paid_order: Order) -> None:
        """Payment details should be accessible."""
        assert paid_order.payment_info is not None
        assert paid_order.payment_info.transaction_id == "txn_123"


# ============================================================================
# TESTS - Fulfillment Flow
# ============================================================================

class TestOrderFulfillmentFlow:
    """Tests for fulfillment-related transitions."""
    
    def test_start_processing_transitions_to_processing(self, paid_order: Order) -> None:
        """Should transition to PROCESSING."""
        paid_order.start_processing()
        
        assert paid_order.status == OrderStatus.PROCESSING
    
    def test_ship_transitions_to_shipped(self, processing_order: Order) -> None:
        """Should transition to SHIPPED."""
        shipping = ShippingInfo(
            carrier="UPS",
            tracking_number="1Z999",
            shipped_at=datetime.now(),
            estimated_delivery=datetime.now() + timedelta(days=3)
        )
        
        processing_order.ship(shipping)
        
        assert processing_order.status == OrderStatus.SHIPPED
    
    def test_shipping_info_stored(self, shipped_order: Order) -> None:
        """Shipping details should be accessible."""
        assert shipped_order.shipping_info is not None
        assert shipped_order.shipping_info.carrier == "UPS"
    
    def test_mark_delivered_transitions_to_delivered(self, shipped_order: Order) -> None:
        """Should transition to DELIVERED."""
        shipped_order.mark_delivered()
        
        assert shipped_order.status == OrderStatus.DELIVERED


# ============================================================================
# TESTS - Cancellation
# ============================================================================

class TestOrderCancellation:
    """Tests for order cancellation."""
    
    def test_can_cancel_pending_payment(self, pending_order: Order) -> None:
        """Should allow cancellation in PENDING_PAYMENT."""
        assert pending_order.can_cancel is True
        
        pending_order.cancel("Changed my mind")
        
        assert pending_order.status == OrderStatus.CANCELLED
    
    def test_can_cancel_paid(self, paid_order: Order) -> None:
        """Should allow cancellation in PAID state."""
        assert paid_order.can_cancel is True
        
        paid_order.cancel("Out of stock")
        
        assert paid_order.status == OrderStatus.CANCELLED
    
    def test_cannot_cancel_delivered(self, delivered_order: Order) -> None:
        """Should not allow cancellation after delivery."""
        assert delivered_order.can_cancel is False
        
        with pytest.raises(InvalidStateTransition):
            delivered_order.cancel("Too late")
    
    def test_cannot_cancel_already_cancelled(self, pending_order: Order) -> None:
        """Should not allow double cancellation."""
        pending_order.cancel("First cancel")
        
        with pytest.raises(InvalidStateTransition):
            pending_order.cancel("Second cancel")


# ============================================================================
# TESTS - Refunds
# ============================================================================

class TestOrderRefunds:
    """Tests for refund operations."""
    
    def test_can_refund_paid_order(self, paid_order: Order) -> None:
        """Should allow refund of paid order."""
        assert paid_order.can_refund is True
    
    def test_can_refund_shipped_order(self, shipped_order: Order) -> None:
        """Should allow refund of shipped order."""
        assert shipped_order.can_refund is True
    
    def test_can_refund_delivered_order(self, delivered_order: Order) -> None:
        """Should allow refund of delivered order."""
        assert delivered_order.can_refund is True
    
    def test_cannot_refund_pending(self, pending_order: Order) -> None:
        """Should not allow refund before payment."""
        assert pending_order.can_refund is False
        
        with pytest.raises(InvalidStateTransition):
            pending_order.refund()
    
    def test_full_refund_transitions_to_refunded(self, paid_order: Order) -> None:
        """Full refund should change status."""
        paid_order.refund(reason="Defective")
        
        assert paid_order.status == OrderStatus.REFUNDED
    
    def test_partial_refund_keeps_status(self, paid_order: Order) -> None:
        """Partial refund should not change status."""
        paid_order.refund(amount=Decimal("20.00"), reason="Partial")
        
        assert paid_order.status == OrderStatus.PAID  # Unchanged
    
    def test_refund_exceeding_total_raises(self, paid_order: Order) -> None:
        """Cannot refund more than paid."""
        with pytest.raises(ValueError, match="exceeds"):
            paid_order.refund(amount=paid_order.total_amount + Decimal("1.00"))
    
    def test_cumulative_refunds_tracked(self, paid_order: Order) -> None:
        """Multiple partial refunds should be tracked."""
        paid_order.refund(amount=Decimal("20.00"), reason="First")
        paid_order.refund(amount=Decimal("30.00"), reason="Second")
        
        history = paid_order.get_status_history()
        refund_notes = [h[2] for h in history if h[2] and "refund" in h[2].lower()]
        assert len(refund_notes) == 2


# ============================================================================
# TESTS - History Tracking
# ============================================================================

class TestOrderHistory:
    """Tests for state history tracking."""
    
    def test_history_tracks_all_transitions(self, delivered_order: Order) -> None:
        """Should record every state change."""
        history = delivered_order.get_status_history()
        states = [h[0] for h in history]
        
        assert states == [
            OrderStatus.DRAFT,
            OrderStatus.PENDING_PAYMENT,
            OrderStatus.PAID,
            OrderStatus.PROCESSING,
            OrderStatus.SHIPPED,
            OrderStatus.DELIVERED,
        ]
    
    def test_history_includes_timestamps(self, pending_order: Order) -> None:
        """Each entry should have a timestamp."""
        history = pending_order.get_status_history()
        
        for entry in history:
            assert isinstance(entry[1], datetime)


# ============================================================================
# TESTS - OrderService
# ============================================================================

class TestOrderService:
    """Tests for OrderService."""
    
    def test_create_order_returns_draft(self, order_service: OrderService) -> None:
        """Should create new draft order."""
        order = order_service.create_order("cust_123")
        
        assert isinstance(order.id, UUID)
        assert order.customer_id == "cust_123"
        assert order.status == OrderStatus.DRAFT
    
    def test_process_payment_and_fulfill(self, order_service: OrderService) -> None:
        """Should handle complete payment and fulfillment flow."""
        order = order_service.create_order("cust_123")
        order.add_item(OrderItem("p1", "Item", 1, Decimal("50.00")))
        order.submit()
        
        payment = PaymentInfo("txn_1", Decimal("50.00"), datetime.now(), "card")
        order_service.process_payment_and_fulfill(order, payment)
        
        assert order.status == OrderStatus.PROCESSING
    
    def test_get_orders_by_status(self, order_service: OrderService) -> None:
        """Should filter orders by status."""
        order1 = order_service.create_order("cust_1")
        order2 = order_service.create_order("cust_2")
        
        # Add items and submit order1
        order1.add_item(OrderItem("p1", "Item", 1, Decimal("10.00")))
        order1.submit()
        
        drafts = order_service.get_orders_by_status(OrderStatus.DRAFT)
        pending = order_service.get_orders_by_status(OrderStatus.PENDING_PAYMENT)
        
        assert len(drafts) == 1  # order2
        assert len(pending) == 1  # order1
