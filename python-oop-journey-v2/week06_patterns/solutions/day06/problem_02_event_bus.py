"""Reference solution for Problem 02: Event Bus."""

from __future__ import annotations

from typing import Callable, Any
from dataclasses import dataclass, field


@dataclass(order=True)
class HandlerEntry:
    """Entry for a handler with priority."""
    priority: int
    handler: Callable[..., None] = field(compare=False)


class EventBus:
    """Publish-subscribe event bus implementation."""
    
    def __init__(self) -> None:
        # Store handlers as (priority, handler) tuples per event type
        self._subscribers: dict[str, list[tuple[int, Callable[..., None]]]] = {}
        self._wildcards: list[tuple[int, Callable[..., None]]] = []
    
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
        if event_type == "*":
            self._wildcards.append((priority, handler))
            self._wildcards.sort(key=lambda x: x[0], reverse=True)
        else:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append((priority, handler))
            self._subscribers[event_type].sort(key=lambda x: x[0], reverse=True)
    
    def unsubscribe(self, event_type: str, handler: Callable[..., None]) -> bool:
        """
        Unsubscribe a handler from an event type.
        
        Returns:
            True if handler was found and removed, False otherwise
        """
        target_list = self._wildcards if event_type == "*" else self._subscribers.get(event_type, [])
        
        for i, (_, h) in enumerate(target_list):
            if h == handler:  # Use == for bound method comparison
                target_list.pop(i)
                return True
        return False
    
    def publish(self, event_type: str, **kwargs: Any) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event being published
            **kwargs: Data to pass to handlers
        """
        # Call specific subscribers first (sorted by priority)
        if event_type in self._subscribers:
            for _, handler in self._subscribers[event_type]:
                handler(event_type=event_type, **kwargs)
        
        # Call wildcard subscribers
        for _, handler in self._wildcards:
            handler(event_type=event_type, **kwargs)
    
    def get_subscriber_count(self, event_type: str) -> int:
        """Get number of subscribers for an event type."""
        count = len(self._wildcards)  # Wildcards receive all events
        if event_type != "*":
            count += len(self._subscribers.get(event_type, []))
        return count
    
    def clear(self) -> None:
        """Remove all subscribers."""
        self._subscribers.clear()
        self._wildcards.clear()


class EventLogger:
    """Utility to log events for testing/demonstration."""
    
    def __init__(self) -> None:
        self._events: list[dict[str, Any]] = []
    
    def on_event(self, **kwargs: Any) -> None:
        """Generic event handler that logs all received events."""
        self._events.append(dict(kwargs))
    
    def get_events(self) -> list[dict[str, Any]]:
        """Get all logged events."""
        return self._events.copy()
    
    def clear(self) -> None:
        """Clear event log."""
        self._events.clear()
    
    def get_event_count(self) -> int:
        """Get number of logged events."""
        return len(self._events)


class ScoreBoard:
    """Example: Game score board that listens to events."""
    
    def __init__(self) -> None:
        self.score = 0
        self.kills = 0
        self.deaths = 0
    
    def on_player_score(self, **kwargs: Any) -> None:
        """Handle player score event."""
        points = kwargs.get("points", 0)
        self.score += points
    
    def on_player_kill(self, **kwargs: Any) -> None:
        """Handle player kill event."""
        self.kills += 1
    
    def on_player_death(self, **kwargs: Any) -> None:
        """Handle player death event."""
        self.deaths += 1


class HealthMonitor:
    """Example: Health monitoring that listens to events."""
    
    def __init__(self) -> None:
        self.health_events: list[dict[str, Any]] = []
    
    def on_damage(self, **kwargs: Any) -> None:
        """Handle damage event."""
        self.health_events.append({"type": "damage", "data": kwargs})
    
    def on_heal(self, **kwargs: Any) -> None:
        """Handle heal event."""
        self.health_events.append({"type": "heal", "data": kwargs})
