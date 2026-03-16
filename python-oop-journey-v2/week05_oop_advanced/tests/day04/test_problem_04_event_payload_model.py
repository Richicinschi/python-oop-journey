"""Tests for Problem 04: Event Payload Model."""

from __future__ import annotations

import json
from datetime import datetime

import pytest

from week05_oop_advanced.solutions.day04.problem_04_event_payload_model import (
    Event
)


class TestEventCreation:
    """Tests for basic Event creation."""
    
    def test_event_creation_basic(self) -> None:
        """Test creating an event with basic fields."""
        event = Event(
            event_type="test.event",
            payload={"key": "value"}
        )
        
        assert event.event_type == "test.event"
        assert event.payload == {"key": "value"}
        assert event.source == "unknown"
        assert event.version == "1.0"
    
    def test_event_auto_generates_id(self) -> None:
        """Test that event_id is auto-generated."""
        event = Event(event_type="test", payload={})
        
        assert event.event_id is not None
        assert len(event.event_id) > 0
        assert event.event_id != ""
    
    def test_event_auto_generates_timestamp(self) -> None:
        """Test that timestamp is auto-generated."""
        event = Event(event_type="test", payload={})
        
        assert event.timestamp is not None
        # Should be a valid ISO format timestamp
        assert "T" in event.timestamp or "-" in event.timestamp
    
    def test_event_unique_ids(self) -> None:
        """Test that each event gets a unique ID."""
        event1 = Event(event_type="test", payload={})
        event2 = Event(event_type="test", payload={})
        
        assert event1.event_id != event2.event_id


class TestEventFactoryUserSignup:
    """Tests for user_signup factory method."""
    
    def test_user_signup_event_type(self) -> None:
        """Test that user_signup creates correct event type."""
        event = Event.user_signup("user123", "user@example.com")
        
        assert event.event_type == "user.signup"
    
    def test_user_signup_payload(self) -> None:
        """Test user_signup payload contents."""
        event = Event.user_signup("user123", "user@example.com")
        
        assert event.payload["user_id"] == "user123"
        assert event.payload["email"] == "user@example.com"
        assert event.payload["signup_method"] == "email"
    
    def test_user_signup_source(self) -> None:
        """Test user_signup default source."""
        event = Event.user_signup("user123", "user@example.com")
        
        assert event.source == "auth_service"
    
    def test_user_signup_custom_source(self) -> None:
        """Test user_signup with custom source."""
        event = Event.user_signup("user123", "user@example.com", source="oauth_service")
        
        assert event.source == "oauth_service"


class TestEventFactoryOrderPlaced:
    """Tests for order_placed factory method."""
    
    def test_order_placed_event_type(self) -> None:
        """Test that order_placed creates correct event type."""
        event = Event.order_placed(
            order_id="ORD-123",
            user_id="user456",
            items=[{"product_id": "P1", "name": "Item", "quantity": 1, "price": 10.0}],
            total_amount=100.0
        )
        
        assert event.event_type == "order.placed"
    
    def test_order_placed_payload(self) -> None:
        """Test order_placed payload contents."""
        items = [
            {"product_id": "P1", "name": "Widget", "quantity": 2, "price": 25.0}
        ]
        event = Event.order_placed(
            order_id="ORD-123",
            user_id="user456",
            items=items,
            total_amount=50.0,
            currency="EUR"
        )
        
        assert event.payload["order_id"] == "ORD-123"
        assert event.payload["user_id"] == "user456"
        assert event.payload["items"] == items
        assert event.payload["total_amount"] == 50.0
        assert event.payload["currency"] == "EUR"
        assert event.payload["item_count"] == 1
    
    def test_order_placed_calculates_item_count(self) -> None:
        """Test that order_placed calculates item count."""
        items = [
            {"product_id": "P1", "name": "Item1", "quantity": 1, "price": 10.0},
            {"product_id": "P2", "name": "Item2", "quantity": 1, "price": 20.0},
            {"product_id": "P3", "name": "Item3", "quantity": 1, "price": 30.0}
        ]
        event = Event.order_placed(
            order_id="ORD-123",
            user_id="user456",
            items=items,
            total_amount=60.0
        )
        
        assert event.payload["item_count"] == 3


class TestEventFactoryPaymentProcessed:
    """Tests for payment_processed factory method."""
    
    def test_payment_processed_event_type(self) -> None:
        """Test that payment_processed creates correct event type."""
        event = Event.payment_processed(
            payment_id="PAY-123",
            order_id="ORD-456",
            amount=100.0,
            status="success",
            payment_method="credit_card"
        )
        
        assert event.event_type == "payment.processed"
    
    def test_payment_processed_payload(self) -> None:
        """Test payment_processed payload contents."""
        event = Event.payment_processed(
            payment_id="PAY-123",
            order_id="ORD-456",
            amount=99.99,
            status="success",
            payment_method="paypal"
        )
        
        assert event.payload["payment_id"] == "PAY-123"
        assert event.payload["order_id"] == "ORD-456"
        assert event.payload["amount"] == 99.99
        assert event.payload["status"] == "success"
        assert event.payload["payment_method"] == "paypal"


class TestEventFactoryErrorOccurred:
    """Tests for error_occurred factory method."""
    
    def test_error_occurred_event_type(self) -> None:
        """Test that error_occurred creates correct event type."""
        event = Event.error_occurred(
            error_code="E001",
            message="Something went wrong"
        )
        
        assert event.event_type == "system.error"
    
    def test_error_occurred_payload(self) -> None:
        """Test error_occurred payload contents."""
        context = {"endpoint": "/api/users", "method": "POST"}
        event = Event.error_occurred(
            error_code="E002",
            message="Database connection failed",
            severity="critical",
            context=context
        )
        
        assert event.payload["error_code"] == "E002"
        assert event.payload["message"] == "Database connection failed"
        assert event.payload["severity"] == "critical"
        assert event.payload["context"] == context
    
    def test_error_occurred_default_severity(self) -> None:
        """Test error_occurred with default severity."""
        event = Event.error_occurred(
            error_code="E001",
            message="Error"
        )
        
        assert event.payload["severity"] == "error"
    
    def test_error_occurred_default_context(self) -> None:
        """Test error_occurred with default empty context."""
        event = Event.error_occurred(
            error_code="E001",
            message="Error"
        )
        
        assert event.payload["context"] == {}


class TestEventSerialization:
    """Tests for Event serialization/deserialization."""
    
    def test_to_dict(self) -> None:
        """Test converting event to dictionary."""
        event = Event(
            event_type="test.event",
            payload={"key": "value"},
            event_id="test-id",
            timestamp="2024-01-01T00:00:00",
            source="test_source",
            version="2.0",
            metadata={"meta": "data"}
        )
        
        result = event.to_dict()
        
        assert result["event_type"] == "test.event"
        assert result["payload"] == {"key": "value"}
        assert result["event_id"] == "test-id"
        assert result["timestamp"] == "2024-01-01T00:00:00"
        assert result["source"] == "test_source"
        assert result["version"] == "2.0"
        assert result["metadata"] == {"meta": "data"}
    
    def test_from_dict(self) -> None:
        """Test creating event from dictionary."""
        data = {
            "event_type": "test.event",
            "payload": {"key": "value"},
            "event_id": "test-id",
            "timestamp": "2024-01-01T00:00:00",
            "source": "test_source",
            "version": "2.0",
            "metadata": {"meta": "data"}
        }
        
        event = Event.from_dict(data)
        
        assert event.event_type == "test.event"
        assert event.payload == {"key": "value"}
        assert event.event_id == "test-id"
        assert event.timestamp == "2024-01-01T00:00:00"
        assert event.source == "test_source"
        assert event.version == "2.0"
        assert event.metadata == {"meta": "data"}
    
    def test_from_dict_defaults(self) -> None:
        """Test from_dict with missing fields gets defaults."""
        data = {
            "event_type": "test.event",
            "payload": {}
        }
        
        event = Event.from_dict(data)
        
        assert event.event_id is not None  # Generated
        assert event.timestamp is not None  # Generated
        assert event.source == "unknown"
        assert event.version == "1.0"
        assert event.metadata == {}
    
    def test_round_trip(self) -> None:
        """Test that to_dict -> from_dict preserves data."""
        original = Event.user_signup("user123", "user@example.com")
        
        data = original.to_dict()
        restored = Event.from_dict(data)
        
        assert restored.event_type == original.event_type
        assert restored.payload == original.payload
        assert restored.event_id == original.event_id
        assert restored.source == original.source


class TestEventPayloadAccess:
    """Tests for payload field access."""
    
    def test_get_payload_field_existing(self) -> None:
        """Test getting an existing payload field."""
        event = Event(
            event_type="test",
            payload={"user_id": "123", "action": "click"}
        )
        
        assert event.get_payload_field("user_id") == "123"
        assert event.get_payload_field("action") == "click"
    
    def test_get_payload_field_missing(self) -> None:
        """Test getting a missing payload field returns default."""
        event = Event(event_type="test", payload={})
        
        assert event.get_payload_field("missing") is None
        assert event.get_payload_field("missing", "default") == "default"


class TestEventMetadata:
    """Tests for event metadata."""
    
    def test_add_metadata(self) -> None:
        """Test adding metadata to an event."""
        event = Event(event_type="test", payload={})
        
        event.add_metadata("key1", "value1")
        event.add_metadata("key2", 123)
        
        assert event.metadata["key1"] == "value1"
        assert event.metadata["key2"] == 123
    
    def test_metadata_in_factory_events(self) -> None:
        """Test that factory methods set metadata."""
        event = Event.user_signup("user123", "user@example.com")
        
        assert event.metadata.get("event_category") == "user"
    
    def test_error_event_metadata(self) -> None:
        """Test that error events have appropriate metadata."""
        event = Event.error_occurred("E001", "Error", severity="critical")
        
        assert event.metadata.get("event_category") == "error"
        assert event.metadata.get("alert") is True
    
    def test_error_event_metadata_not_critical(self) -> None:
        """Test that non-critical errors don't alert."""
        event = Event.error_occurred("E001", "Error", severity="warning")
        
        assert event.metadata.get("alert") is False
