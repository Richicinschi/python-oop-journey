"""Reference solution for Problem 05: Logged Class Decorator."""

from __future__ import annotations

from functools import wraps
from typing import Type, Any, Callable


def logged(cls: Type) -> Type:
    """A class decorator that logs all method calls.
    
    Wraps all callable attributes (except magic methods) to log their calls.
    Prints: "Calling <method_name> with args=<args>, kwargs=<kwargs>"
    
    Args:
        cls: The class to decorate
        
    Returns:
        The decorated class with logging
    """
    for attr_name in dir(cls):
        # Skip magic methods and properties
        if attr_name.startswith('_'):
            continue
            
        attr = getattr(cls, attr_name)
        if callable(attr) and not isinstance(attr, property):
            setattr(cls, attr_name, _make_logged_method(attr_name, attr))
    
    return cls


def _make_logged_method(name: str, method: Callable) -> Callable:
    """Create a logged version of a method."""
    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        print(f"Calling {name} with args={args}, kwargs={kwargs}")
        return method(self, *args, **kwargs)
    return wrapper


# Example usage for testing
@logged
class Calculator:
    """A calculator with logged methods."""
    
    def __init__(self) -> None:
        self._history: list[str] = []
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        result = a + b
        self._history.append(f"add({a:g}, {b:g}) = {result:g}")
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a."""
        result = a - b
        self._history.append(f"subtract({a:g}, {b:g}) = {result:g}")
        return result
    
    def get_history(self) -> list[str]:
        """Get calculation history."""
        return self._history.copy()


@logged
class Greeter:
    """A greeter with logged methods."""
    
    def __init__(self, greeting: str = "Hello") -> None:
        self.greeting = greeting
    
    def greet(self, name: str) -> str:
        """Greet someone."""
        return f"{self.greeting}, {name}!"
