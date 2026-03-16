"""
Event System - Observer Pattern Implementation

This module implements the Observer pattern for decoupled communication
between game subsystems.

TODO: Complete the following:
1. Implement Event class for typed events
2. Implement EventBus with subscribe, unsubscribe, and publish methods
3. Ensure thread-safety (optional but recommended)
"""

from typing import Any, Callable, Dict, List, Optional
from collections import defaultdict


class Event:
    """
    Represents a game event with a type and data.
    
    TODO: Implement this class
    
    Attributes:
        event_type (str): The type/category of the event
        data (Any): Event-specific data payload
        sender (Any): The object that published the event
    """
    
    def __init__(self, event_type: str, data: Any = None, sender: Any = None):
        """
        TODO: Initialize an event.
        
        Args:
            event_type: The type of event (e.g., "collision", "health_changed")
            data: Optional data payload
            sender: The object that created this event
        """
        # TODO: Implement initialization
        raise NotImplementedError("Event.__init__ not implemented")
    
    def __repr__(self) -> str:
        """TODO: Return string representation of the event."""
        raise NotImplementedError("Event.__repr__ not implemented")


class EventBus:
    """
    Central event bus implementing the Observer pattern.
    
    TODO: Implement this class
    
    The EventBus allows publishers and subscribers to communicate
    without direct references to each other.
    
    Example:
        >>> bus = EventBus()
        >>> bus.subscribe("collision", lambda e: print(f"Collision: {e.data}"))
        >>> bus.publish("collision", {"entity1": player, "entity2": enemy})
    """
    
    def __init__(self):
        """TODO: Initialize the event bus with empty subscriber lists."""
        # TODO: Initialize _subscribers dictionary
        raise NotImplementedError("EventBus.__init__ not implemented")
    
    def subscribe(self, event_type: str, callback: Callable[[Event], None]) -> None:
        """
        TODO: Subscribe a callback to an event type.
        
        Args:
            event_type: The type of event to listen for
            callback: Function to call when event occurs
        """
        raise NotImplementedError("EventBus.subscribe not implemented")
    
    def unsubscribe(self, event_type: str, callback: Callable[[Event], None]) -> bool:
        """
        TODO: Unsubscribe a callback from an event type.
        
        Args:
            event_type: The event type to unsubscribe from
            callback: The callback to remove
            
        Returns:
            bool: True if callback was found and removed, False otherwise
        """
        raise NotImplementedError("EventBus.unsubscribe not implemented")
    
    def publish(self, event_type: str, data: Any = None, sender: Any = None) -> None:
        """
        TODO: Publish an event to all subscribers.
        
        Args:
            event_type: The type of event to publish
            data: Optional data payload
            sender: The object publishing the event
        """
        raise NotImplementedError("EventBus.publish not implemented")
    
    def clear(self) -> None:
        """TODO: Remove all subscribers from all event types."""
        raise NotImplementedError("EventBus.clear not implemented")
    
    def subscriber_count(self, event_type: str) -> int:
        """
        TODO: Get the number of subscribers for an event type.
        
        Args:
            event_type: The event type to query
            
        Returns:
            int: Number of subscribers
        """
        raise NotImplementedError("EventBus.subscriber_count not implemented")


# Global event bus instance
_global_event_bus: Optional[EventBus] = None


def get_global_event_bus() -> EventBus:
    """
    TODO: Get or create the global event bus singleton.
    
    Returns:
        EventBus: The global event bus instance
    """
    global _global_event_bus
    # TODO: Initialize if None, then return
    raise NotImplementedError("get_global_event_bus not implemented")


def reset_global_event_bus() -> None:
    """TODO: Reset the global event bus (useful for testing)."""
    global _global_event_bus
    # TODO: Reset to None
    raise NotImplementedError("reset_global_event_bus not implemented")
