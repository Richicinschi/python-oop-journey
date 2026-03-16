"""Solution: State Order Lifecycle.

Implements the State pattern for order state management.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List
from datetime import datetime


class OrderState(ABC):
    """Abstract base class for order states."""
    
    def __init__(self, order: Order) -> None:
        """Initialize state with order reference.
        
        Args:
            order: The order this state belongs to.
        """
        self._order = order
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get state name.
        
        Returns:
            State name.
        """
        pass
    
    def pay(self) -> str:
        """Attempt to pay for order.
        
        Returns:
            Result message.
        """
        return f"Cannot pay from {self.name} state"
    
    def ship(self) -> str:
        """Attempt to ship order.
        
        Returns:
            Result message.
        """
        return f"Cannot ship from {self.name} state"
    
    def deliver(self) -> str:
        """Attempt to deliver order.
        
        Returns:
            Result message.
        """
        return f"Cannot deliver from {self.name} state"
    
    def cancel(self) -> str:
        """Attempt to cancel order.
        
        Returns:
            Result message.
        """
        return f"Cannot cancel from {self.name} state"


class PendingState(OrderState):
    """Order is pending payment."""
    
    @property
    def name(self) -> str:
        """Get state name."""
        return "Pending"
    
    def pay(self) -> str:
        """Pay for order, transition to Processing."""
        from_state = self._order.state_name
        self._order.state = ProcessingState(self._order)
        self._order.record_transition(from_state, "Processing")
        return "Payment processed. Order is now being processed."
    
    def cancel(self) -> str:
        """Cancel order, transition to Cancelled."""
        from_state = self._order.state_name
        self._order.state = CancelledState(self._order)
        self._order.record_transition(from_state, "Cancelled")
        return "Order cancelled."


class ProcessingState(OrderState):
    """Order is being processed."""
    
    @property
    def name(self) -> str:
        """Get state name."""
        return "Processing"
    
    def ship(self) -> str:
        """Ship order, transition to Shipped."""
        from_state = self._order.state_name
        self._order.state = ShippedState(self._order)
        self._order.record_transition(from_state, "Shipped")
        return "Order shipped."
    
    def cancel(self) -> str:
        """Cancel order, transition to Cancelled."""
        from_state = self._order.state_name
        self._order.state = CancelledState(self._order)
        self._order.record_transition(from_state, "Cancelled")
        return "Order cancelled."


class ShippedState(OrderState):
    """Order has been shipped."""
    
    @property
    def name(self) -> str:
        """Get state name."""
        return "Shipped"
    
    def deliver(self) -> str:
        """Deliver order, transition to Delivered."""
        from_state = self._order.state_name
        self._order.state = DeliveredState(self._order)
        self._order.record_transition(from_state, "Delivered")
        return "Order delivered."


class DeliveredState(OrderState):
    """Order has been delivered."""
    
    @property
    def name(self) -> str:
        """Get state name."""
        return "Delivered"


class CancelledState(OrderState):
    """Order has been cancelled."""
    
    @property
    def name(self) -> str:
        """Get state name."""
        return "Cancelled"


class Order:
    """Order context class with state management."""
    
    def __init__(self, order_id: str, amount: float) -> None:
        """Initialize order.
        
        Args:
            order_id: Unique order identifier.
            amount: Order total amount.
        """
        self._order_id = order_id
        self._amount = amount
        self._state: OrderState = PendingState(self)
        self._history: List[dict] = []
        self.record_transition("Created", "Pending")
    
    @property
    def order_id(self) -> str:
        """Get order ID."""
        return self._order_id
    
    @property
    def amount(self) -> float:
        """Get order amount."""
        return self._amount
    
    @property
    def state(self) -> OrderState:
        """Get current state."""
        return self._state
    
    @state.setter
    def state(self, state: OrderState) -> None:
        """Set current state.
        
        Args:
            state: New state.
        """
        self._state = state
    
    @property
    def state_name(self) -> str:
        """Get current state name."""
        return self._state.name
    
    def pay(self) -> str:
        """Pay for order.
        
        Returns:
            Result message.
        """
        return self._state.pay()
    
    def ship(self) -> str:
        """Ship order.
        
        Returns:
            Result message.
        """
        return self._state.ship()
    
    def deliver(self) -> str:
        """Deliver order.
        
        Returns:
            Result message.
        """
        return self._state.deliver()
    
    def cancel(self) -> str:
        """Cancel order.
        
        Returns:
            Result message.
        """
        return self._state.cancel()
    
    def record_transition(self, from_state: str, to_state: str) -> None:
        """Record a state transition.
        
        Args:
            from_state: Previous state name.
            to_state: New state name.
        """
        self._history.append({
            "from": from_state,
            "to": to_state,
            "timestamp": datetime.now().isoformat(),
        })
    
    def get_history(self) -> List[dict]:
        """Get order state history.
        
        Returns:
            List of transition records.
        """
        return self._history.copy()
    
    def can_cancel(self) -> bool:
        """Check if order can be cancelled.
        
        Returns:
            True if can cancel.
        """
        return isinstance(self._state, (PendingState, ProcessingState))
