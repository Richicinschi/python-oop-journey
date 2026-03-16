"""Problem 04: State Order Lifecycle

Topic: State Pattern
Difficulty: Medium

Implement the State pattern for an order state machine.

HINTS:
- Hint 1 (Conceptual): Each state is a separate class with its own behavior.
  Let states control their valid transitions, not the Order class.
- Hint 2 (Structural): OrderState has: __init__(order), name property, and 
  methods for each action (pay, ship, deliver, cancel). Concrete states 
  override only the actions they support.
- Hint 3 (Edge Case): Invalid transitions should return a message but NOT 
  change state. Valid transitions should update order.state and record history.

PATTERN EXPLANATION:
The State pattern allows an object to alter its behavior when its internal
state changes. The object will appear to change its class.

STRUCTURE:
- Context (Order): Maintains an instance of a ConcreteState subclass
- State (OrderState): Interface encapsulating state-specific behavior
- ConcreteState (Pending, Processing, Shipped, etc.): Implement state behavior

WHEN TO USE:
- When an object's behavior depends on its state
- When you have complex conditional statements based on state
- For state machines with many transitions

EXAMPLE USAGE:
    order = Order("ORD-001", 150.0)
    print(order.state_name)  # "Pending"
    
    order.pay()  # Pending -> Processing
    print(order.state_name)  # "Processing"
    
    order.ship()  # Processing -> Shipped
    print(order.state_name)  # "Shipped"
    
    order.deliver()  # Shipped -> Delivered
    print(order.state_name)  # "Delivered"
    
    # Invalid transitions return error messages
    print(order.pay())  # "Cannot pay from Delivered"

TODO:
1. Create OrderState abstract base class with methods for each transition
2. Create Order context class that maintains current state
3. Implement concrete states: PendingState, ProcessingState, ShippedState, DeliveredState, CancelledState
4. Each state should handle valid transitions and reject invalid ones
5. Track order history through state transitions
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
        # TODO: Store order reference
        raise NotImplementedError("Initialize state")
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get state name.
        
        Returns:
            State name.
        """
        # TODO: Return state name
        raise NotImplementedError("Return state name")
    
    def pay(self) -> str:
        """Attempt to pay for order.
        
        Returns:
            Result message.
        """
        # TODO: Default implementation returns "Cannot pay from {state}"
        raise NotImplementedError("Handle pay")
    
    def ship(self) -> str:
        """Attempt to ship order.
        
        Returns:
            Result message.
        """
        # TODO: Default implementation returns "Cannot ship from {state}"
        raise NotImplementedError("Handle ship")
    
    def deliver(self) -> str:
        """Attempt to deliver order.
        
        Returns:
            Result message.
        """
        # TODO: Default implementation returns "Cannot deliver from {state}"
        raise NotImplementedError("Handle deliver")
    
    def cancel(self) -> str:
        """Attempt to cancel order.
        
        Returns:
            Result message.
        """
        # TODO: Default implementation returns "Cannot cancel from {state}"
        raise NotImplementedError("Handle cancel")


class PendingState(OrderState):
    """Order is pending payment."""
    
    @property
    def name(self) -> str:
        """Get state name."""
        # TODO: Return "Pending"
        raise NotImplementedError("Return name")
    
    def pay(self) -> str:
        """Pay for order, transition to Processing."""
        # TODO: Transition to ProcessingState, record history, return success message
        raise NotImplementedError("Process payment")
    
    def cancel(self) -> str:
        """Cancel order, transition to Cancelled."""
        # TODO: Transition to CancelledState, record history, return success message
        raise NotImplementedError("Process cancellation")


class ProcessingState(OrderState):
    """Order is being processed."""
    
    @property
    def name(self) -> str:
        """Get state name."""
        # TODO: Return "Processing"
        raise NotImplementedError("Return name")
    
    def ship(self) -> str:
        """Ship order, transition to Shipped."""
        # TODO: Transition to ShippedState, record history, return success message
        raise NotImplementedError("Process shipment")
    
    def cancel(self) -> str:
        """Cancel order, transition to Cancelled."""
        # TODO: Transition to CancelledState, record history, return success message
        raise NotImplementedError("Process cancellation")


class ShippedState(OrderState):
    """Order has been shipped."""
    
    @property
    def name(self) -> str:
        """Get state name."""
        # TODO: Return "Shipped"
        raise NotImplementedError("Return name")
    
    def deliver(self) -> str:
        """Deliver order, transition to Delivered."""
        # TODO: Transition to DeliveredState, record history, return success message
        raise NotImplementedError("Process delivery")


class DeliveredState(OrderState):
    """Order has been delivered."""
    
    @property
    def name(self) -> str:
        """Get state name."""
        # TODO: Return "Delivered"
        raise NotImplementedError("Return name")


class CancelledState(OrderState):
    """Order has been cancelled."""
    
    @property
    def name(self) -> str:
        """Get state name."""
        # TODO: Return "Cancelled"
        raise NotImplementedError("Return name")


class Order:
    """Order context class with state management."""
    
    def __init__(self, order_id: str, amount: float) -> None:
        """Initialize order.
        
        Args:
            order_id: Unique order identifier.
            amount: Order total amount.
        """
        # TODO: Initialize order_id, amount, history list
        # TODO: Set initial state to PendingState
        raise NotImplementedError("Initialize order")
    
    @property
    def order_id(self) -> str:
        """Get order ID."""
        # TODO: Return order_id
        raise NotImplementedError("Return order_id")
    
    @property
    def amount(self) -> float:
        """Get order amount."""
        # TODO: Return amount
        raise NotImplementedError("Return amount")
    
    @property
    def state(self) -> OrderState:
        """Get current state."""
        # TODO: Return current state
        raise NotImplementedError("Return state")
    
    @state.setter
    def state(self, state: OrderState) -> None:
        """Set current state.
        
        Args:
            state: New state.
        """
        # TODO: Update state
        raise NotImplementedError("Set state")
    
    @property
    def state_name(self) -> str:
        """Get current state name."""
        # TODO: Return state.name
        raise NotImplementedError("Return state name")
    
    def pay(self) -> str:
        """Pay for order.
        
        Returns:
            Result message.
        """
        # TODO: Delegate to state.pay()
        raise NotImplementedError("Pay")
    
    def ship(self) -> str:
        """Ship order.
        
        Returns:
            Result message.
        """
        # TODO: Delegate to state.ship()
        raise NotImplementedError("Ship")
    
    def deliver(self) -> str:
        """Deliver order.
        
        Returns:
            Result message.
        """
        # TODO: Delegate to state.deliver()
        raise NotImplementedError("Deliver")
    
    def cancel(self) -> str:
        """Cancel order.
        
        Returns:
            Result message.
        """
        # TODO: Delegate to state.cancel()
        raise NotImplementedError("Cancel")
    
    def record_transition(self, from_state: str, to_state: str) -> None:
        """Record a state transition.
        
        Args:
            from_state: Previous state name.
            to_state: New state name.
        """
        # TODO: Append transition record to history with timestamp
        raise NotImplementedError("Record transition")
    
    def get_history(self) -> List[dict]:
        """Get order state history.
        
        Returns:
            List of transition records.
        """
        # TODO: Return history copy
        raise NotImplementedError("Get history")
    
    def can_cancel(self) -> bool:
        """Check if order can be cancelled.
        
        Returns:
            True if can cancel.
        """
        # TODO: Return True if state is PendingState or ProcessingState
        raise NotImplementedError("Can cancel")
