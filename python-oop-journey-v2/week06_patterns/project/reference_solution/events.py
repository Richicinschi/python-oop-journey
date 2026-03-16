"""
Event System - Observer Pattern Implementation

This module implements the Observer pattern for decoupled communication
between game subsystems.
"""

from typing import Any, Callable, Dict, List, Optional
from collections import defaultdict


class Event:
    """
    Represents a game event with a type and data.
    
    Attributes:
        event_type (str): The type/category of the event
        data (Any): Event-specific data payload
        sender (Any): The object that published the event
    """
    
    def __init__(self, event_type: str, data: Any = None, sender: Any = None):
        """
        Initialize an event.
        
        Args:
            event_type: The type of event (e.g., "collision", "health_changed")
            data: Optional data payload
            sender: The object that created this event
        """
        self.event_type = event_type
        self.data = data
        self.sender = sender
    
    def __repr__(self) -> str:
        """Return string representation of the event."""
        return f"Event(type='{self.event_type}', data={self.data}, sender={self.sender})"


class EventBus:
    """
    Central event bus implementing the Observer pattern.
    
    The EventBus allows publishers and subscribers to communicate
    without direct references to each other.
    
    Example:
        >>> bus = EventBus()
        >>> bus.subscribe("collision", lambda e: print(f"Collision: {e.data}"))
        >>> bus.publish("collision", {"entity1": player, "entity2": enemy})
    """
    
    def __init__(self):
        """Initialize the event bus with empty subscriber lists."""
        self._subscribers: Dict[str, List[Callable[[Event], None]]] = defaultdict(list)
    
    def subscribe(self, event_type: str, callback: Callable[[Event], None]) -> None:
        """
        Subscribe a callback to an event type.
        
        Args:
            event_type: The type of event to listen for
            callback: Function to call when event occurs
        """
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable[[Event], None]) -> bool:
        """
        Unsubscribe a callback from an event type.
        
        Args:
            event_type: The event type to unsubscribe from
            callback: The callback to remove
            
        Returns:
            bool: True if callback was found and removed, False otherwise
        """
        if event_type in self._subscribers:
            if callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)
                return True
        return False
    
    def publish(self, event_type: str, data: Any = None, sender: Any = None) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: The type of event to publish
            data: Optional data payload
            sender: The object publishing the event
        """
        event = Event(event_type, data, sender)
        # Iterate over a copy in case subscribers modify the list
        for callback in self._subscribers[event_type][:]:
            callback(event)
    
    def clear(self) -> None:
        """Remove all subscribers from all event types."""
        self._subscribers.clear()
    
    def subscriber_count(self, event_type: str) -> int:
        """
        Get the number of subscribers for an event type.
        
        Args:
            event_type: The event type to query
            
        Returns:
            int: Number of subscribers
        """
        return len(self._subscribers.get(event_type, []))


# Global event bus instance
_global_event_bus: Optional[EventBus] = None


def get_global_event_bus() -> EventBus:
    """
    Get or create the global event bus singleton.
    
    Returns:
        EventBus: The global event bus instance
    """
    global _global_event_bus
    if _global_event_bus is None:
        _global_event_bus = EventBus()
    return _global_event_bus


def reset_global_event_bus() -> None:
    """Reset the global event bus (useful for testing)."""
    global _global_event_bus
    _global_event_bus = None
