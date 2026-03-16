"""Problem 03: Event Stream Processor

Topic: Data Processing with Objects
Difficulty: Medium

Implement an event-driven data processing system using OOP principles.

Event streaming is a common pattern where data arrives as discrete events
that need to be processed by registered handlers. This problem implements
a flexible event processing framework.

Classes to implement:
- Event - Represents a domain event with type, payload, and metadata
- EventHandler (ABC) - Abstract base for event handlers
- LoggingHandler - Logs all events it receives
- FilteringHandler - Delegates to another handler based on event type
- EventStreamProcessor - Manages handlers and processes event streams
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable


class EventPriority(Enum):
    """Priority levels for events."""
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()
    CRITICAL = auto()


class Event:
    """Represents a domain event in the system.
    
    Events carry a type identifier, payload data, metadata, and
    processing state.
    
    Attributes:
        event_type: String identifier for the event type
        payload: Dictionary containing event data
        timestamp: When the event occurred (UTC)
        priority: Event priority level
        processed: Whether the event has been processed
        processing_time: How long processing took (in seconds)
    """
    
    def __init__(
        self,
        event_type: str,
        payload: dict[str, Any],
        timestamp: datetime | None = None,
        priority: EventPriority = EventPriority.NORMAL,
    ) -> None:
        """Initialize an event.
        
        Args:
            event_type: Type identifier for this event
            payload: Event data as a dictionary
            timestamp: Event creation time (default: now)
            priority: Event priority level (default: NORMAL)
        """
        raise NotImplementedError("Implement __init__")
    
    @property
    def event_id(self) -> str:
        """Generate a unique event ID based on type and timestamp."""
        raise NotImplementedError("Implement event_id")
    
    def mark_processed(self, processing_time: float) -> None:
        """Mark the event as processed.
        
        Args:
            processing_time: Time taken to process in seconds
        """
        raise NotImplementedError("Implement mark_processed")
    
    def __repr__(self) -> str:
        """String representation of the event."""
        raise NotImplementedError("Implement __repr__")


class EventHandler(ABC):
    """Abstract base class for event handlers.
    
    Handlers implement the strategy for processing specific event types.
    Each handler can declare which event types it can handle.
    """
    
    def __init__(self, name: str, handled_types: list[str] | None = None) -> None:
        """Initialize the handler.
        
        Args:
            name: Handler name for identification
            handled_types: List of event types this handler can process.
                          If None, handler must override can_handle.
        """
        raise NotImplementedError("Implement __init__")
    
    @property
    def name(self) -> str:
        """Get the handler name."""
        raise NotImplementedError("Implement name")
    
    def can_handle(self, event: Event) -> bool:
        """Check if this handler can process the event.
        
        Default implementation checks if event.event_type is in
        handled_types. Subclasses can override for custom logic.
        
        Args:
            event: The event to check
            
        Returns:
            True if this handler can process the event
        """
        raise NotImplementedError("Implement can_handle")
    
    @abstractmethod
    def handle(self, event: Event) -> dict[str, Any]:
        """Process the event.
        
        Args:
            event: The event to process
            
        Returns:
            Dictionary with processing results
        """
        raise NotImplementedError("Implement handle")


class LoggingHandler(EventHandler):
    """Handler that logs all events it receives.
    
    Useful for debugging and auditing. Can optionally filter
    by minimum priority level.
    """
    
    def __init__(
        self,
        name: str = "logger",
        min_priority: EventPriority = EventPriority.LOW,
    ) -> None:
        """Initialize the logging handler.
        
        Args:
            name: Handler name
            min_priority: Minimum priority level to log
        """
        raise NotImplementedError("Implement __init__")
    
    def can_handle(self, event: Event) -> bool:
        """Can handle events at or above min_priority."""
        raise NotImplementedError("Implement can_handle")
    
    def handle(self, event: Event) -> dict[str, Any]:
        """Log the event and return log entry.
        
        Returns:
            Dictionary with logged event details
        """
        raise NotImplementedError("Implement handle")
    
    def get_logs(self) -> list[dict[str, Any]]:
        """Get all logged events.
        
        Returns:
            List of logged event dictionaries
        """
        raise NotImplementedError("Implement get_logs")


class FilteringHandler(EventHandler):
    """Handler that filters events before delegating to another handler.
    
    Only forwards events matching specific criteria to the wrapped handler.
    """
    
    def __init__(
        self,
        name: str,
        wrapped: EventHandler,
        event_types: list[str] | None = None,
        min_priority: EventPriority | None = None,
    ) -> None:
        """Initialize filtering handler.
        
        Args:
            name: Handler name
            wrapped: The handler to delegate matching events to
            event_types: If specified, only forward these event types
            min_priority: If specified, only forward events at or above this priority
        """
        raise NotImplementedError("Implement __init__")
    
    def can_handle(self, event: Event) -> bool:
        """Can handle if wrapped handler can and filters pass."""
        raise NotImplementedError("Implement can_handle")
    
    def handle(self, event: Event) -> dict[str, Any]:
        """Handle by delegating to wrapped handler if filters pass.
        
        Returns empty result if filters don't pass.
        """
        raise NotImplementedError("Implement handle")


class EventStreamProcessor:
    """Processes a stream of events through registered handlers.
    
    Maintains statistics about event processing and coordinates
    between events and their handlers.
    
    Example:
        processor = EventStreamProcessor()
        processor.register_handler(LoggingHandler())
        processor.register_handler(OrderHandler())
        
        processor.process_event(Event("order_created", {"id": 123}))
        stats = processor.get_statistics()
    """
    
    def __init__(self) -> None:
        """Initialize the processor with empty state."""
        raise NotImplementedError("Implement __init__")
    
    @property
    def handler_count(self) -> int:
        """Get the number of registered handlers."""
        raise NotImplementedError("Implement handler_count")
    
    def register_handler(self, handler: EventHandler) -> None:
        """Register an event handler.
        
        Args:
            handler: Handler to register
        """
        raise NotImplementedError("Implement register_handler")
    
    def process_event(self, event: Event) -> list[dict[str, Any]]:
        """Process a single event through all matching handlers.
        
        The event is passed to all handlers where can_handle() returns True.
        Updates processing statistics.
        
        Args:
            event: The event to process
            
        Returns:
            List of results from all handlers that processed the event
        """
        raise NotImplementedError("Implement process_event")
    
    def process_batch(self, events: list[Event]) -> dict[str, list[dict[str, Any]]]:
        """Process multiple events.
        
        Args:
            events: List of events to process
            
        Returns:
            Dictionary mapping event IDs to their handler results
        """
        raise NotImplementedError("Implement process_batch")
    
    def get_statistics(self) -> dict[str, Any]:
        """Get processing statistics.
        
        Returns:
            Dictionary with:
            - total_events: Total events received
            - processed_events: Events that were handled
            - unhandled_events: Events with no matching handlers
            - handler_stats: Per-handler event counts
        """
        raise NotImplementedError("Implement get_statistics")
    
    def reset_statistics(self) -> None:
        """Reset all processing statistics to zero."""
        raise NotImplementedError("Implement reset_statistics")
