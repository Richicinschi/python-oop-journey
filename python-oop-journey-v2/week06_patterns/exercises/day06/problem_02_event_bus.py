"""Problem 02: Event Bus

Topic: Observer Pattern, Publish-Subscribe
Difficulty: Hard

Implement an event bus system using the Observer pattern.

HINTS:
- Hint 1 (Conceptual): EventBus is central router. Publishers don't know 
  subscribers. Events are routed by type, not by direct reference.
- Hint 2 (Structural): EventBus stores: Dict[event_type, List[HandlerEntry]]. 
  HandlerEntry needs priority for sorting. Use defaultdict for convenience.
- Hint 3 (Edge Case): Wildcard "*" subscribers receive all events. Sort handlers 
  by priority (descending) before calling. Handle exceptions in handlers without 
  breaking the chain.

PATTERN EXPLANATION:
The Event Bus (Publish-Subscribe) pattern is a variation of Observer where
senders (publishers) don't target specific receivers (subscribers). Instead,
messages are published to a bus that routes them to interested subscribers.

STRUCTURE:
- EventBus: Central message routing system
- Subscribers: Register handlers for specific event types
- Publishers: Send events to the bus
- Events: Messages with type and data

WHEN TO USE:
- For decoupled component communication
- When publishers don't know about subscribers
- For event-driven architectures

EXAMPLE USAGE:
    bus = EventBus()
    
    # Subscribe
    def on_player_died(event_type, **data):
        print(f"Game over! Score: {data['score']}")
    
    bus.subscribe("player_died", on_player_died)
    
    # Publish
    bus.publish("player_died", score=1000)
    
    # Unsubscribe
    bus.unsubscribe("player_died", on_player_died)

Your task:
1. Create an EventBus class that allows publish-subscribe messaging
2. Support multiple subscribers per event type
3. Support event priorities (higher priority = called first)
4. Allow unsubscribing handlers
5. Implement wildcard subscriptions (subscribe to all events)

Requirements:
- subscribe(event_type, handler, priority=0) - higher priority = called first
- publish(event_type, **kwargs) - call all handlers for that event type
- unsubscribe(event_type, handler) - remove a specific handler
- Support wildcard "*" for subscribing to all events
- Handlers receive event_type and **kwargs
"""

from __future__ import annotations

from typing import Callable, Any
from dataclasses import dataclass, field


@dataclass(order=True)
class HandlerEntry:
    """Entry for a handler with priority."""
    # TODO: Implement HandlerEntry for priority queue behavior
    pass


class EventBus:
    """Publish-subscribe event bus implementation."""
    
    def __init__(self) -> None:
        # TODO: Initialize data structures
        pass
    
    def subscribe(
        self,
        event_type: str,
        handler: Callable[..., None],
        priority: int = 0,
    ) -> None:
        """
        Subscribe a handler to an event type.
        
        Args:
            event_type: Type of event to subscribe to, or "*" for all
            handler: Callable to invoke when event is published
            priority: Higher priority handlers are called first (default 0)
        """
        raise NotImplementedError("Implement subscribe")
    
    def unsubscribe(self, event_type: str, handler: Callable[..., None]) -> bool:
        """
        Unsubscribe a handler from an event type.
        
        Returns:
            True if handler was found and removed, False otherwise
        """
        raise NotImplementedError("Implement unsubscribe")
    
    def publish(self, event_type: str, **kwargs: Any) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event being published
            **kwargs: Data to pass to handlers
        """
        raise NotImplementedError("Implement publish")
    
    def get_subscriber_count(self, event_type: str) -> int:
        """Get number of subscribers for an event type."""
        raise NotImplementedError("Implement get_subscriber_count")
    
    def clear(self) -> None:
        """Remove all subscribers."""
        raise NotImplementedError("Implement clear")


class EventLogger:
    """Utility to log events for testing/demonstration."""
    
    def __init__(self) -> None:
        # TODO: Initialize event log
        pass
    
    def on_event(self, **kwargs: Any) -> None:
        """Generic event handler that logs all received events."""
        raise NotImplementedError("Implement on_event")
    
    def get_events(self) -> list[dict[str, Any]]:
        """Get all logged events."""
        raise NotImplementedError("Implement get_events")
    
    def clear(self) -> None:
        """Clear event log."""
        raise NotImplementedError("Implement clear")
