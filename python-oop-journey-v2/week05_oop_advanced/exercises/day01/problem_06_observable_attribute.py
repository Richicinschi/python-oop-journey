"""Problem 06: Observable Attribute

Topic: Descriptor that notifies on change
Difficulty: Medium

Create a descriptor that notifies observers when the attribute value changes.
"""

from __future__ import annotations

from typing import Any, Callable, Protocol


class ChangeCallback(Protocol):
    """Protocol for change notification callbacks."""
    
    def __call__(self, instance: object, old_value: Any, new_value: Any) -> None:
        """Called when the observed value changes.
        
        Args:
            instance: The instance whose attribute changed
            old_value: The previous value
            new_value: The new value
        """
        ...


class Observable:
    """A descriptor that notifies observers on value changes.
    
    The descriptor should:
    - Accept an optional default value
    - Store callbacks per instance
    - Notify all registered callbacks when value changes
    - Allow registering and unregistering callbacks
    
    Attributes:
        default: Default value for new instances
        callbacks: Dictionary mapping instance id to callback list
    """
    
    def __init__(self, default: Any = None) -> None:
        """Initialize with optional default.
        
        Args:
            default: Default value for new instances
        """
        raise NotImplementedError("Implement Observable.__init__")
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Called when descriptor is assigned to class.
        
        Args:
            owner: The class
            name: The attribute name
        """
        raise NotImplementedError("Implement Observable.__set_name__")
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        """Get the attribute value.
        
        Args:
            instance: The instance, or None for class access
            owner: The owner class
            
        Returns:
            The stored value, or self if class access
        """
        raise NotImplementedError("Implement Observable.__get__")
    
    def __set__(self, instance: object, value: Any) -> None:
        """Set the attribute and notify observers.
        
        Args:
            instance: The instance
            value: The new value
            
        Note:
            Should notify callbacks with (instance, old_value, new_value)
        """
        raise NotImplementedError("Implement Observable.__set__")
    
    def add_callback(
        self, 
        instance: object, 
        callback: Callable[[object, Any, Any], None]
    ) -> None:
        """Add a callback for a specific instance.
        
        Args:
            instance: The instance to observe
            callback: Function to call on changes
        """
        raise NotImplementedError("Implement Observable.add_callback")
    
    def remove_callback(
        self, 
        instance: object, 
        callback: Callable[[object, Any, Any], None]
    ) -> None:
        """Remove a callback for a specific instance.
        
        Args:
            instance: The instance
            callback: The callback to remove
        """
        raise NotImplementedError("Implement Observable.remove_callback")


class Stock:
    """A stock with observable price.
    
    Attributes:
        symbol: Stock symbol
        
    Observable Attributes:
        price: Current stock price
        volume: Trading volume
    """
    
    price = Observable(0.0)
    volume = Observable(0)
    
    def __init__(self, symbol: str, price: float = 0.0, volume: int = 0) -> None:
        """Initialize stock.
        
        Args:
            symbol: Stock symbol
            price: Initial price
            volume: Initial volume
        """
        raise NotImplementedError("Implement Stock.__init__")
    
    def on_price_change(
        self, 
        callback: Callable[[object, float, float], None]
    ) -> None:
        """Register a price change callback.
        
        Args:
            callback: Function(instance, old_price, new_price)
        """
        raise NotImplementedError("Implement Stock.on_price_change")
    
    def on_volume_change(
        self, 
        callback: Callable[[object, int, int], None]
    ) -> None:
        """Register a volume change callback.
        
        Args:
            callback: Function(instance, old_volume, new_volume)
        """
        raise NotImplementedError("Implement Stock.on_volume_change")


class FormField:
    """A form field with observable value changes.
    
    Attributes:
        name: Field name
        label: Display label
        
    Observable Attributes:
        value: Current field value
        error: Current error message
        dirty: Whether field has been modified
    """
    
    value = Observable(None)
    error = Observable("")
    dirty = Observable(False)
    
    def __init__(self, name: str, label: str, initial_value: Any = None) -> None:
        """Initialize form field.
        
        Args:
            name: Field name
            label: Display label
            initial_value: Initial value
        """
        raise NotImplementedError("Implement FormField.__init__")
    
    def on_change(
        self, 
        callback: Callable[[object, Any, Any], None]
    ) -> None:
        """Register value change callback.
        
        Args:
            callback: Function(instance, old_value, new_value)
        """
        raise NotImplementedError("Implement FormField.on_change")
    
    def clear(self) -> None:
        """Clear the field value and reset dirty flag."""
        raise NotImplementedError("Implement FormField.clear")
    
    def is_valid(self) -> bool:
        """Check if field has no errors.
        
        Returns:
            True if error is empty
        """
        raise NotImplementedError("Implement FormField.is_valid")


# Hints for Observable Attribute (Medium):
# 
# Hint 1 - Conceptual nudge:
# This descriptor needs to store multiple callbacks per instance. Think about using a
# dictionary that maps instances to lists of callback functions.
#
# Hint 2 - Structural plan:
# - Use __set_name__ to capture the attribute name
# - Store callbacks in a dict: {instance -> [callback1, callback2, ...]}
# - In __set__, after storing the value, iterate through callbacks and call each one
# - Provide add_callback() and remove_callback() methods
# - Consider using WeakKeyDictionary to avoid memory leaks
#
# Hint 3 - Edge-case warning:
# What happens if a callback raises an exception? Should other callbacks still be called?
# Also, be careful with remove_callback - what if the callback isn't registered?
