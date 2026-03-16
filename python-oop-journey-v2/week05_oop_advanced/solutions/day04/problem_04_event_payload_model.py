"""Reference solution for Problem 04: Event Payload Model."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import json
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
        """Factory method for user signup events."""
        return cls(
            event_type="user.signup",
            payload={
                "user_id": user_id,
                "email": email,
                "signup_method": "email"
            },
            source=source,
            metadata={"event_category": "user"}
        )
    
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
        """Factory method for order placed events."""
        return cls(
            event_type="order.placed",
            payload={
                "order_id": order_id,
                "user_id": user_id,
                "items": items,
                "total_amount": total_amount,
                "currency": currency,
                "item_count": len(items)
            },
            source=source,
            metadata={"event_category": "commerce"}
        )
    
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
        """Factory method for payment events."""
        return cls(
            event_type="payment.processed",
            payload={
                "payment_id": payment_id,
                "order_id": order_id,
                "amount": amount,
                "status": status,
                "payment_method": payment_method
            },
            source=source,
            metadata={"event_category": "payment"}
        )
    
    @classmethod
    def error_occurred(
        cls,
        error_code: str,
        message: str,
        severity: str = "error",
        context: dict[str, Any] | None = None,
        source: str = "unknown"
    ) -> Event:
        """Factory method for error events."""
        return cls(
            event_type="system.error",
            payload={
                "error_code": error_code,
                "message": message,
                "severity": severity,
                "context": context or {}
            },
            source=source,
            metadata={"event_category": "error", "alert": severity == "critical"}
        )
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Event:
        """Reconstruct Event from dictionary."""
        return cls(
            event_type=data["event_type"],
            payload=data.get("payload", {}),
            event_id=data.get("event_id", str(uuid.uuid4())),
            timestamp=data.get("timestamp", datetime.now().isoformat()),
            source=data.get("source", "unknown"),
            version=data.get("version", "1.0"),
            metadata=data.get("metadata", {})
        )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert Event to dictionary."""
        return {
            "event_type": self.event_type,
            "payload": self.payload,
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "source": self.source,
            "version": self.version,
            "metadata": self.metadata
        }
    
    def get_payload_field(self, field_name: str, default: Any = None) -> Any:
        """Safely get a field from the payload."""
        return self.payload.get(field_name, default)
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the event."""
        self.metadata[key] = value
