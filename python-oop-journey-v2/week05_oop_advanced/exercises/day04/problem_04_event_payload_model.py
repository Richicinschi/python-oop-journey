"""Problem 04: Event Payload Model

Topic: Dataclasses with factory methods
Difficulty: Medium

Create an Event dataclass for an event-driven system with multiple
factory methods for different event types.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid


@dataclass
class Event:
    """Generic event for event-driven architecture.
    
    Attributes:
        event_id: Unique event identifier (auto-generated UUID)
        event_type: Event type string (e.g., "user.signup")
        payload: Event data as dictionary
        timestamp: ISO format timestamp (auto-generated)
        source: Service/component that generated the event
        version: Event schema version
        metadata: Additional event metadata
    """
    
    event_type: str
    payload: dict[str, Any]
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    source: str = "unknown"
    version: str = "1.0"
    metadata: dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def user_signup(
        cls,
        user_id: str,
        email: str,
        source: str = "auth_service"
    ) -> Event:
        """Factory method for user signup events.
        
        Args:
            user_id: Unique user identifier
            email: User's email address
            source: Origin service
            
        Returns:
            Event with type "user.signup"
        """
        raise NotImplementedError("Implement Event.user_signup")
    
    @classmethod
    def order_placed(
        cls,
        order_id: str,
        user_id: str,
        items: list[dict[str, Any]],
        total_amount: float,
        currency: str = "USD",
        source: str = "order_service"
    ) -> Event:
        """Factory method for order placed events.
        
        Args:
            order_id: Unique order identifier
            user_id: Customer user ID
            items: List of order items with keys: product_id, name, quantity, price
            total_amount: Total order amount
            currency: Currency code
            source: Origin service
            
        Returns:
            Event with type "order.placed"
        """
        raise NotImplementedError("Implement Event.order_placed")
    
    @classmethod
    def payment_processed(
        cls,
        payment_id: str,
        order_id: str,
        amount: float,
        status: str,
        payment_method: str,
        source: str = "payment_service"
    ) -> Event:
        """Factory method for payment events.
        
        Args:
            payment_id: Unique payment identifier
            order_id: Associated order ID
            amount: Payment amount
            status: Payment status (success, failed, pending)
            payment_method: Method used (card, bank_transfer, etc.)
            source: Origin service
            
        Returns:
            Event with type "payment.processed"
        """
        raise NotImplementedError("Implement Event.payment_processed")
    
    @classmethod
    def error_occurred(
        cls,
        error_code: str,
        message: str,
        severity: str = "error",
        context: dict[str, Any] | None = None,
        source: str = "unknown"
    ) -> Event:
        """Factory method for error events.
        
        Args:
            error_code: Machine-readable error code
            message: Human-readable error message
            severity: error, warning, or critical
            context: Additional error context
            source: Origin service
            
        Returns:
            Event with type "system.error"
        """
        raise NotImplementedError("Implement Event.error_occurred")
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Event:
        """Reconstruct Event from dictionary.
        
        Args:
            data: Dictionary with event data
            
        Returns:
            New Event instance
        """
        raise NotImplementedError("Implement Event.from_dict")
    
    def to_dict(self) -> dict[str, Any]:
        """Convert Event to dictionary.
        
        Returns:
            Dictionary representation of the event
        """
        raise NotImplementedError("Implement Event.to_dict")
    
    def get_payload_field(self, field_name: str, default: Any = None) -> Any:
        """Safely get a field from the payload.
        
        Args:
            field_name: Key to look up in payload
            default: Default value if not found
            
        Returns:
            Payload value or default
        """
        raise NotImplementedError("Implement Event.get_payload_field")
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the event.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        raise NotImplementedError("Implement Event.add_metadata")


# Hints for Event Payload Model (Medium):
# 
# Hint 1 - Conceptual nudge:
# Factory methods are @classmethod that create and return instances with pre-filled
# values.
#
# Hint 2 - Structural plan:
# - Each factory method creates an Event with specific event_type and payload
# - Use cls(...) or Event(...) to instantiate
# - from_dict should use **data unpacking or explicit field assignment
#
# Hint 3 - Edge-case warning:
# Auto-generated fields (UUID, timestamp) need default factories. When reconstructing
# from dict, you may want to preserve the original values rather than generating new ones.
