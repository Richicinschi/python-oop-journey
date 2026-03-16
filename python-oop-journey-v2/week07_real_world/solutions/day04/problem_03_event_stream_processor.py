"""Problem 03: Event Stream Processor - Solution

Event-driven data processing system using OOP.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, auto
from typing import Any


class EventPriority(Enum):
    """Priority levels for events."""
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()
    CRITICAL = auto()


class Event:
    """Represents a domain event in the system."""
    
    def __init__(
        self,
        event_type: str,
        payload: dict[str, Any],
        timestamp: datetime | None = None,
        priority: EventPriority = EventPriority.NORMAL,
    ) -> None:
        self.event_type = event_type
        self.payload = payload
        self.timestamp = timestamp or datetime.now()
        self.priority = priority
        self.processed = False
        self.processing_time: float = 0.0
    
    @property
    def event_id(self) -> str:
        ts = self.timestamp.strftime("%Y%m%d%H%M%S")
        return f"{self.event_type}_{ts}_{id(self) % 10000}"
    
    def mark_processed(self, processing_time: float) -> None:
        self.processed = True
        self.processing_time = processing_time
    
    def __repr__(self) -> str:
        return f"Event({self.event_type}, processed={self.processed})"


class EventHandler(ABC):
    """Abstract base class for event handlers."""
    
    def __init__(self, name: str, handled_types: list[str] | None = None) -> None:
        self._name = name
        self._handled_types = handled_types or []
    
    @property
    def name(self) -> str:
        return self._name
    
    def can_handle(self, event: Event) -> bool:
        if self._handled_types:
            return event.event_type in self._handled_types
        return True
    
    @abstractmethod
    def handle(self, event: Event) -> dict[str, Any]:
        pass


class LoggingHandler(EventHandler):
    """Handler that logs all events it receives."""
    
    def __init__(
        self,
        name: str = "logger",
        min_priority: EventPriority = EventPriority.LOW,
    ) -> None:
        super().__init__(name)
        self._min_priority = min_priority
        self._logs: list[dict[str, Any]] = []
    
    def can_handle(self, event: Event) -> bool:
        priority_order = {
            EventPriority.LOW: 0,
            EventPriority.NORMAL: 1,
            EventPriority.HIGH: 2,
            EventPriority.CRITICAL: 3,
        }
        return priority_order.get(event.priority, 0) >= priority_order.get(self._min_priority, 0)
    
    def handle(self, event: Event) -> dict[str, Any]:
        log_entry = {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "timestamp": event.timestamp,
            "priority": event.priority.name,
            "payload_keys": list(event.payload.keys()),
        }
        self._logs.append(log_entry)
        return {"logged": True, "entry": log_entry}
    
    def get_logs(self) -> list[dict[str, Any]]:
        return self._logs.copy()


class FilteringHandler(EventHandler):
    """Handler that filters events before delegating."""
    
    def __init__(
        self,
        name: str,
        wrapped: EventHandler,
        event_types: list[str] | None = None,
        min_priority: EventPriority | None = None,
    ) -> None:
        super().__init__(name)
        self._wrapped = wrapped
        self._event_types = event_types
        self._min_priority = min_priority
    
    def can_handle(self, event: Event) -> bool:
        if self._event_types and event.event_type not in self._event_types:
            return False
        if self._min_priority:
            priority_order = {
                EventPriority.LOW: 0,
                EventPriority.NORMAL: 1,
                EventPriority.HIGH: 2,
                EventPriority.CRITICAL: 3,
            }
            if priority_order.get(event.priority, 0) < priority_order.get(self._min_priority, 0):
                return False
        return self._wrapped.can_handle(event)
    
    def handle(self, event: Event) -> dict[str, Any]:
        if not self.can_handle(event):
            return {"filtered": True, "handled": False}
        return self._wrapped.handle(event)


class EventStreamProcessor:
    """Processes a stream of events through registered handlers."""
    
    def __init__(self) -> None:
        self._handlers: list[EventHandler] = []
        self._total_events = 0
        self._processed_events = 0
        self._unhandled_events = 0
        self._handler_stats: dict[str, int] = {}
    
    @property
    def handler_count(self) -> int:
        return len(self._handlers)
    
    def register_handler(self, handler: EventHandler) -> None:
        self._handlers.append(handler)
        self._handler_stats[handler.name] = 0
    
    def process_event(self, event: Event) -> list[dict[str, Any]]:
        self._total_events += 1
        results = []
        handled = False
        
        for handler in self._handlers:
            if handler.can_handle(event):
                result = handler.handle(event)
                results.append(result)
                handled = True
                self._handler_stats[handler.name] = self._handler_stats.get(handler.name, 0) + 1
        
        if handled:
            event.processed = True
            self._processed_events += 1
        else:
            self._unhandled_events += 1
        
        return results
    
    def process_batch(self, events: list[Event]) -> dict[str, list[dict[str, Any]]]:
        results = {}
        for event in events:
            event_results = self.process_event(event)
            results[event.event_id] = event_results
        return results
    
    def get_statistics(self) -> dict[str, Any]:
        return {
            "total_events": self._total_events,
            "processed_events": self._processed_events,
            "unhandled_events": self._unhandled_events,
            "handler_stats": self._handler_stats.copy(),
        }
    
    def reset_statistics(self) -> None:
        self._total_events = 0
        self._processed_events = 0
        self._unhandled_events = 0
        self._handler_stats = {name: 0 for name in self._handler_stats}
