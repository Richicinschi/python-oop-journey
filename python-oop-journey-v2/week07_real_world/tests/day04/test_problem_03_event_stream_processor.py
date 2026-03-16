"""Tests for Problem 03: Event Stream Processor."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pytest

from week07_real_world.solutions.day04.problem_03_event_stream_processor import (
    Event,
    EventHandler,
    EventPriority,
    EventStreamProcessor,
    FilteringHandler,
    LoggingHandler,
)


class TestEvent:
    """Tests for Event class."""
    
    def test_event_creation(self) -> None:
        event = Event(
            "user_created",
            {"user_id": 123, "name": "Alice"},
        )
        
        assert event.event_type == "user_created"
        assert event.payload == {"user_id": 123, "name": "Alice"}
        assert event.processed is False
        assert event.priority == EventPriority.NORMAL
    
    def test_event_with_custom_priority(self) -> None:
        event = Event(
            "critical_error",
            {"message": "System failure"},
            priority=EventPriority.CRITICAL,
        )
        
        assert event.priority == EventPriority.CRITICAL
    
    def test_event_with_custom_timestamp(self) -> None:
        ts = datetime(2024, 1, 1, 12, 0, 0)
        event = Event("test", {}, timestamp=ts)
        
        assert event.timestamp == ts
    
    def test_event_id_format(self) -> None:
        ts = datetime(2024, 6, 15, 10, 30, 45)
        event = Event("order_placed", {"id": 1}, timestamp=ts)
        
        event_id = event.event_id
        assert event_id.startswith("order_placed_20240615103045_")
    
    def test_mark_processed(self) -> None:
        event = Event("test", {})
        event.mark_processed(0.5)
        
        assert event.processed is True
        assert event.processing_time == 0.5
    
    def test_event_repr(self) -> None:
        event = Event("test_type", {})
        repr_str = repr(event)
        
        assert "test_type" in repr_str
        assert "processed" in repr_str


class MockHandler(EventHandler):
    """Mock handler for testing."""
    
    def __init__(self, name: str, types: list[str] | None = None) -> None:
        super().__init__(name, types)
        self.handled_events: list[Event] = []
    
    def handle(self, event: Event) -> dict[str, Any]:
        self.handled_events.append(event)
        return {"handler": self.name, "event_type": event.event_type}


class TestEventHandler:
    """Tests for EventHandler base class."""
    
    def test_handler_name(self) -> None:
        handler = MockHandler("test_handler")
        assert handler.name == "test_handler"
    
    def test_can_handle_specific_types(self) -> None:
        handler = MockHandler("orders", ["order_created", "order_updated"])
        
        assert handler.can_handle(Event("order_created", {})) is True
        assert handler.can_handle(Event("order_updated", {})) is True
        assert handler.can_handle(Event("user_login", {})) is False
    
    def test_can_handle_all_types_when_empty(self) -> None:
        handler = MockHandler("catch_all", [])
        
        assert handler.can_handle(Event("any_type", {})) is True
    
    def test_can_handle_all_types_when_none(self) -> None:
        handler = MockHandler("catch_all", None)
        
        assert handler.can_handle(Event("any_type", {})) is True


class TestLoggingHandler:
    """Tests for LoggingHandler."""
    
    def test_logs_event(self) -> None:
        handler = LoggingHandler("logger")
        event = Event("user_login", {"user_id": 123})
        
        result = handler.handle(event)
        
        assert result["logged"] is True
        assert len(handler.get_logs()) == 1
    
    def test_log_entry_content(self) -> None:
        handler = LoggingHandler("logger")
        event = Event("test_event", {"key": "value"}, priority=EventPriority.HIGH)
        
        handler.handle(event)
        log = handler.get_logs()[0]
        
        assert log["event_type"] == "test_event"
        assert log["priority"] == "HIGH"
        assert "payload_keys" in log
    
    def test_respects_min_priority(self) -> None:
        handler = LoggingHandler("logger", min_priority=EventPriority.HIGH)
        
        low_event = Event("low", {}, priority=EventPriority.LOW)
        high_event = Event("high", {}, priority=EventPriority.HIGH)
        
        assert handler.can_handle(low_event) is False
        assert handler.can_handle(high_event) is True
    
    def test_multiple_logs(self) -> None:
        handler = LoggingHandler("logger")
        
        for i in range(3):
            handler.handle(Event(f"event_{i}", {}))
        
        assert len(handler.get_logs()) == 3
    
    def test_logs_are_copied(self) -> None:
        handler = LoggingHandler("logger")
        handler.handle(Event("test", {}))
        
        logs = handler.get_logs()
        logs.clear()  # Modify returned list
        
        assert len(handler.get_logs()) == 1  # Original unchanged


class TestFilteringHandler:
    """Tests for FilteringHandler."""
    
    def test_filters_by_event_type(self) -> None:
        wrapped = MockHandler("wrapped")
        filter_handler = FilteringHandler(
            "filter",
            wrapped,
            event_types=["allowed_type"],
        )
        
        allowed = Event("allowed_type", {})
        blocked = Event("blocked_type", {})
        
        assert filter_handler.can_handle(allowed) is True
        assert filter_handler.can_handle(blocked) is False
    
    def test_filters_by_priority(self) -> None:
        wrapped = MockHandler("wrapped")
        filter_handler = FilteringHandler(
            "filter",
            wrapped,
            min_priority=EventPriority.HIGH,
        )
        
        low = Event("test", {}, priority=EventPriority.LOW)
        high = Event("test", {}, priority=EventPriority.HIGH)
        critical = Event("test", {}, priority=EventPriority.CRITICAL)
        
        assert filter_handler.can_handle(low) is False
        assert filter_handler.can_handle(high) is True
        assert filter_handler.can_handle(critical) is True
    
    def test_delegates_to_wrapped_handler(self) -> None:
        wrapped = MockHandler("wrapped")
        filter_handler = FilteringHandler("filter", wrapped, event_types=["test"])
        
        event = Event("test", {"data": "value"})
        result = filter_handler.handle(event)
        
        assert result["handler"] == "wrapped"
        assert len(wrapped.handled_events) == 1
    
    def test_returns_empty_when_filtered(self) -> None:
        wrapped = MockHandler("wrapped")
        filter_handler = FilteringHandler("filter", wrapped, event_types=["allowed"])
        
        event = Event("blocked", {})
        result = filter_handler.handle(event)
        
        assert result["filtered"] is True
        assert result["handled"] is False
        assert len(wrapped.handled_events) == 0


class TestEventStreamProcessor:
    """Tests for EventStreamProcessor."""
    
    def test_empty_processor(self) -> None:
        processor = EventStreamProcessor()
        
        assert processor.handler_count == 0
    
    def test_register_handler(self) -> None:
        processor = EventStreamProcessor()
        handler = MockHandler("test")
        
        processor.register_handler(handler)
        
        assert processor.handler_count == 1
    
    def test_process_event_with_matching_handler(self) -> None:
        processor = EventStreamProcessor()
        handler = MockHandler("orders", ["order_created"])
        processor.register_handler(handler)
        
        event = Event("order_created", {"id": 123})
        results = processor.process_event(event)
        
        assert len(results) == 1
        assert event.processed is True
    
    def test_process_event_no_matching_handler(self) -> None:
        processor = EventStreamProcessor()
        handler = MockHandler("orders", ["order_created"])
        processor.register_handler(handler)
        
        event = Event("user_login", {})
        results = processor.process_event(event)
        
        assert len(results) == 0
        assert event.processed is False
    
    def test_multiple_handlers_can_process(self) -> None:
        processor = EventStreamProcessor()
        handler1 = MockHandler("logger")
        handler2 = MockHandler("metrics")
        processor.register_handler(handler1)
        processor.register_handler(handler2)
        
        event = Event("any_event", {})
        results = processor.process_event(event)
        
        assert len(results) == 2
        assert len(handler1.handled_events) == 1
        assert len(handler2.handled_events) == 1
    
    def test_process_batch(self) -> None:
        processor = EventStreamProcessor()
        handler = MockHandler("handler")
        processor.register_handler(handler)
        
        events = [
            Event("type1", {}),
            Event("type2", {}),
        ]
        results = processor.process_batch(events)
        
        assert len(results) == 2
        assert all(len(results[eid]) == 1 for eid in results)
    
    def test_statistics_tracking(self) -> None:
        processor = EventStreamProcessor()
        handler = MockHandler("handler", ["processed_type"])
        processor.register_handler(handler)
        
        processor.process_event(Event("processed_type", {}))
        processor.process_event(Event("processed_type", {}))
        processor.process_event(Event("unhandled_type", {}))
        
        stats = processor.get_statistics()
        
        assert stats["total_events"] == 3
        assert stats["processed_events"] == 2
        assert stats["unhandled_events"] == 1
        assert stats["handler_stats"]["handler"] == 2
    
    def test_reset_statistics(self) -> None:
        processor = EventStreamProcessor()
        handler = MockHandler("handler")
        processor.register_handler(handler)
        
        processor.process_event(Event("test", {}))
        processor.reset_statistics()
        stats = processor.get_statistics()
        
        assert stats["total_events"] == 0
        assert stats["processed_events"] == 0
        assert stats["handler_stats"]["handler"] == 0


class TestEventStreamIntegration:
    """Integration tests for event processing."""
    
    def test_complete_event_processing_workflow(self) -> None:
        processor = EventStreamProcessor()
        
        # Add logging handler for all events
        logger = LoggingHandler("audit_logger", min_priority=EventPriority.NORMAL)
        processor.register_handler(logger)
        
        # Add specific handler for order events
        order_handler = MockHandler("order_processor", ["order_created"])
        processor.register_handler(order_handler)
        
        # Process events
        events = [
            Event("order_created", {"order_id": 1}, priority=EventPriority.HIGH),
            Event("user_login", {"user_id": 123}, priority=EventPriority.NORMAL),
            Event("order_created", {"order_id": 2}, priority=EventPriority.HIGH),
            Event("system_ping", {}, priority=EventPriority.LOW),  # Below logger threshold
        ]
        
        for event in events:
            processor.process_event(event)
        
        # Verify
        stats = processor.get_statistics()
        assert stats["total_events"] == 4
        assert stats["processed_events"] == 3  # All except system_ping (LOW < NORMAL)
        assert len(order_handler.handled_events) == 2  # Only order_created events
        assert len(logger.get_logs()) == 3  # NORMAL, HIGH, HIGH (not LOW)
    
    def test_filtered_handler_chain(self) -> None:
        processor = EventStreamProcessor()
        
        # Create a handler that only processes critical errors
        error_handler = MockHandler("critical_errors", ["error"])
        filtered = FilteringHandler(
            "critical_filter",
            error_handler,
            min_priority=EventPriority.CRITICAL,
        )
        processor.register_handler(filtered)
        
        # Test various error severities
        processor.process_event(Event("error", {"msg": "minor"}, priority=EventPriority.LOW))
        processor.process_event(Event("error", {"msg": "critical!"}, priority=EventPriority.CRITICAL))
        
        # Only critical should be handled
        assert len(error_handler.handled_events) == 1
        assert error_handler.handled_events[0].payload["msg"] == "critical!"
