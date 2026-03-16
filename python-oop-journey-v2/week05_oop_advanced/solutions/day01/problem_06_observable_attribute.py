"""Reference solution for Problem 06: Observable Attribute."""

from __future__ import annotations

from typing import Any, Callable


class Observable:
    """A descriptor that notifies observers on value changes."""
    
    def __init__(self, default: Any = None) -> None:
        self.default = default
        self.name = ""
        self.storage_name = ""
        self.callbacks: dict[int, list[Callable[[object, Any, Any], None]]] = {}
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.storage_name = f"_{name}"
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.storage_name, self.default)
    
    def __set__(self, instance: object, value: Any) -> None:
        old_value = getattr(instance, self.storage_name, self.default)
        setattr(instance, self.storage_name, value)
        
        if old_value != value:
            for callback in self.callbacks.get(id(instance), []):
                callback(instance, old_value, value)
    
    def add_callback(
        self, 
        instance: object, 
        callback: Callable[[object, Any, Any], None]
    ) -> None:
        if id(instance) not in self.callbacks:
            self.callbacks[id(instance)] = []
        self.callbacks[id(instance)].append(callback)
    
    def remove_callback(
        self, 
        instance: object, 
        callback: Callable[[object, Any, Any], None]
    ) -> None:
        if id(instance) in self.callbacks:
            self.callbacks[id(instance)].remove(callback)


class Stock:
    """A stock with observable price."""
    
    price = Observable(0.0)
    volume = Observable(0)
    
    def __init__(self, symbol: str, price: float = 0.0, volume: int = 0) -> None:
        self.symbol = symbol
        self.price = price
        self.volume = volume
    
    def on_price_change(
        self, 
        callback: Callable[[object, float, float], None]
    ) -> None:
        type(self).price.add_callback(self, callback)
    
    def on_volume_change(
        self, 
        callback: Callable[[object, int, int], None]
    ) -> None:
        type(self).volume.add_callback(self, callback)


class FormField:
    """A form field with observable value changes."""
    
    value = Observable(None)
    error = Observable("")
    dirty = Observable(False)
    
    def __init__(self, name: str, label: str, initial_value: Any = None) -> None:
        self.name = name
        self.label = label
        self.value = initial_value
        self.dirty = False
    
    def on_change(
        self, 
        callback: Callable[[object, Any, Any], None]
    ) -> None:
        type(self).value.add_callback(self, callback)
    
    def clear(self) -> None:
        self.value = None
        self.error = ""
        self.dirty = False
    
    def is_valid(self) -> bool:
        return self.error == ""
