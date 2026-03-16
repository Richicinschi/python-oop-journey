"""Tests for Problem 04: State Order Lifecycle."""

from __future__ import annotations

import pytest
from abc import ABC

from week06_patterns.solutions.day03.problem_04_state_order_lifecycle import (
    OrderState,
    PendingState,
    ProcessingState,
    ShippedState,
    DeliveredState,
    CancelledState,
    Order,
)


class TestOrderState:
    """Test OrderState abstract base class."""
    
    def test_order_state_is_abstract(self) -> None:
        """Test that OrderState cannot be instantiated directly."""
        assert issubclass(OrderState, ABC)
    
    def test_default_methods_return_error(self) -> None:
        """Test default state methods return error messages."""
        # Create a minimal concrete implementation for testing
        class TestState(OrderState):
            @property
            def name(self) -> str:
                return "Test"
        
        order = Order("ORD-001", 100.0)
        state = TestState(order)
        
        assert "Cannot pay" in state.pay()
        assert "Cannot ship" in state.ship()
        assert "Cannot deliver" in state.deliver()
        assert "Cannot cancel" in state.cancel()


class TestPendingState:
    """Test PendingState."""
    
    def test_name(self) -> None:
        """Test state name."""
        order = Order("ORD-001", 100.0)
        state = PendingState(order)
        assert state.name == "Pending"
    
    def test_pay_transitions_to_processing(self) -> None:
        """Test pay transitions to Processing."""
        order = Order("ORD-001", 100.0)
        result = order.pay()
        
        assert "Payment processed" in result
        assert order.state_name == "Processing"
    
    def test_cancel_transitions_to_cancelled(self) -> None:
        """Test cancel transitions to Cancelled."""
        order = Order("ORD-001", 100.0)
        result = order.cancel()
        
        assert "cancelled" in result.lower()
        assert order.state_name == "Cancelled"
    
    def test_cannot_ship_from_pending(self) -> None:
        """Test ship from Pending fails."""
        order = Order("ORD-001", 100.0)
        result = order.ship()
        
        assert "Cannot ship" in result
        assert order.state_name == "Pending"
    
    def test_cannot_deliver_from_pending(self) -> None:
        """Test deliver from Pending fails."""
        order = Order("ORD-001", 100.0)
        result = order.deliver()
        
        assert "Cannot deliver" in result
        assert order.state_name == "Pending"


class TestProcessingState:
    """Test ProcessingState."""
    
    def test_name(self) -> None:
        """Test state name."""
        order = Order("ORD-001", 100.0)
        order.pay()  # Transition to Processing
        assert order.state_name == "Processing"
    
    def test_ship_transitions_to_shipped(self) -> None:
        """Test ship transitions to Shipped."""
        order = Order("ORD-001", 100.0)
        order.pay()
        result = order.ship()
        
        assert "shipped" in result.lower()
        assert order.state_name == "Shipped"
    
    def test_cancel_transitions_to_cancelled(self) -> None:
        """Test cancel from Processing transitions to Cancelled."""
        order = Order("ORD-001", 100.0)
        order.pay()
        result = order.cancel()
        
        assert "cancelled" in result.lower()
        assert order.state_name == "Cancelled"
    
    def test_cannot_pay_from_processing(self) -> None:
        """Test pay from Processing fails."""
        order = Order("ORD-001", 100.0)
        order.pay()
        result = order.pay()
        
        assert "Cannot pay" in result
        assert order.state_name == "Processing"
    
    def test_cannot_deliver_from_processing(self) -> None:
        """Test deliver from Processing fails."""
        order = Order("ORD-001", 100.0)
        order.pay()
        result = order.deliver()
        
        assert "Cannot deliver" in result
        assert order.state_name == "Processing"


class TestShippedState:
    """Test ShippedState."""
    
    def test_name(self) -> None:
        """Test state name."""
        order = Order("ORD-001", 100.0)
        order.pay()
        order.ship()
        assert order.state_name == "Shipped"
    
    def test_deliver_transitions_to_delivered(self) -> None:
        """Test deliver transitions to Delivered."""
        order = Order("ORD-001", 100.0)
        order.pay()
        order.ship()
        result = order.deliver()
        
        assert "delivered" in result.lower()
        assert order.state_name == "Delivered"
    
    def test_cannot_pay_from_shipped(self) -> None:
        """Test pay from Shipped fails."""
        order = Order("ORD-001", 100.0)
        order.pay()
        order.ship()
        result = order.pay()
        
        assert "Cannot pay" in result
        assert order.state_name == "Shipped"
    
    def test_cannot_ship_from_shipped(self) -> None:
        """Test ship from Shipped fails."""
        order = Order("ORD-001", 100.0)
        order.pay()
        order.ship()
        result = order.ship()
        
        assert "Cannot ship" in result
        assert order.state_name == "Shipped"
    
    def test_cannot_cancel_from_shipped(self) -> None:
        """Test cancel from Shipped fails."""
        order = Order("ORD-001", 100.0)
        order.pay()
        order.ship()
        result = order.cancel()
        
        assert "Cannot cancel" in result
        assert order.state_name == "Shipped"


class TestDeliveredState:
    """Test DeliveredState."""
    
    def test_name(self) -> None:
        """Test state name."""
        order = Order("ORD-001", 100.0)
        order.pay()
        order.ship()
        order.deliver()
        assert order.state_name == "Delivered"
    
    def test_no_transitions_allowed(self) -> None:
        """Test no transitions allowed from Delivered."""
        order = Order("ORD-001", 100.0)
        order.pay()
        order.ship()
        order.deliver()
        
        assert "Cannot" in order.pay()
        assert "Cannot" in order.ship()
        assert "Cannot" in order.deliver()
        assert "Cannot" in order.cancel()
        assert order.state_name == "Delivered"


class TestCancelledState:
    """Test CancelledState."""
    
    def test_name(self) -> None:
        """Test state name."""
        order = Order("ORD-001", 100.0)
        order.cancel()
        assert order.state_name == "Cancelled"
    
    def test_no_transitions_allowed(self) -> None:
        """Test no transitions allowed from Cancelled."""
        order = Order("ORD-001", 100.0)
        order.cancel()
        
        assert "Cannot" in order.pay()
        assert "Cannot" in order.ship()
        assert "Cannot" in order.deliver()
        assert "Cannot" in order.cancel()
        assert order.state_name == "Cancelled"


class TestOrder:
    """Test Order context class."""
    
    def test_initialization(self) -> None:
        """Test order initialization."""
        order = Order("ORD-001", 100.0)
        
        assert order.order_id == "ORD-001"
        assert order.amount == 100.0
        assert order.state_name == "Pending"
    
    def test_full_lifecycle(self) -> None:
        """Test complete order lifecycle."""
        order = Order("ORD-001", 100.0)
        
        assert order.state_name == "Pending"
        
        order.pay()
        assert order.state_name == "Processing"
        
        order.ship()
        assert order.state_name == "Shipped"
        
        order.deliver()
        assert order.state_name == "Delivered"
    
    def test_cancel_from_pending(self) -> None:
        """Test cancel from pending."""
        order = Order("ORD-001", 100.0)
        order.cancel()
        
        assert order.state_name == "Cancelled"
    
    def test_cancel_from_processing(self) -> None:
        """Test cancel from processing."""
        order = Order("ORD-001", 100.0)
        order.pay()
        order.cancel()
        
        assert order.state_name == "Cancelled"
    
    def test_cannot_cancel_after_shipped(self) -> None:
        """Test cannot cancel after shipped."""
        order = Order("ORD-001", 100.0)
        order.pay()
        order.ship()
        result = order.cancel()
        
        assert "Cannot cancel" in result
        assert order.state_name == "Shipped"
    
    def test_can_cancel(self) -> None:
        """Test can_cancel method."""
        order = Order("ORD-001", 100.0)
        assert order.can_cancel() is True
        
        order.pay()
        assert order.can_cancel() is True
        
        order.ship()
        assert order.can_cancel() is False
        
        order.deliver()
        assert order.can_cancel() is False
    
    def test_history_records_transitions(self) -> None:
        """Test history records state transitions."""
        order = Order("ORD-001", 100.0)
        
        history = order.get_history()
        assert len(history) == 1  # Created -> Pending
        assert history[0]["from"] == "Created"
        assert history[0]["to"] == "Pending"
        
        order.pay()
        history = order.get_history()
        assert len(history) == 2
        assert history[1]["from"] == "Pending"
        assert history[1]["to"] == "Processing"
    
    def test_history_includes_timestamps(self) -> None:
        """Test history entries include timestamps."""
        order = Order("ORD-001", 100.0)
        history = order.get_history()
        
        assert "timestamp" in history[0]
        assert isinstance(history[0]["timestamp"], str)
    
    def test_get_history_returns_copy(self) -> None:
        """Test get_history returns a copy."""
        order = Order("ORD-001", 100.0)
        history = order.get_history()
        history.append({"from": "Test", "to": "Test", "timestamp": "now"})
        
        # Original should be unchanged
        assert len(order.get_history()) == 1
    
    def test_invalid_transitions_preserve_state(self) -> None:
        """Test that invalid transitions don't change state."""
        order = Order("ORD-001", 100.0)
        
        # Try invalid transitions
        order.ship()  # Can't ship from Pending
        assert order.state_name == "Pending"
        
        order.deliver()  # Can't deliver from Pending
        assert order.state_name == "Pending"
    
    def test_complex_scenario_with_multiple_orders(self) -> None:
        """Test multiple orders with different paths."""
        order1 = Order("ORD-001", 100.0)
        order2 = Order("ORD-002", 200.0)
        order3 = Order("ORD-003", 300.0)
        
        # Order 1: Full lifecycle
        order1.pay()
        order1.ship()
        order1.deliver()
        
        # Order 2: Cancelled from pending
        order2.cancel()
        
        # Order 3: Cancelled from processing
        order3.pay()
        order3.cancel()
        
        assert order1.state_name == "Delivered"
        assert order2.state_name == "Cancelled"
        assert order3.state_name == "Cancelled"
