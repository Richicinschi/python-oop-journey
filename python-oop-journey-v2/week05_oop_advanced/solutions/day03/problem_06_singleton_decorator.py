"""Reference solution for Problem 06: Singleton Decorator."""

from __future__ import annotations

from typing import Type, Any, Dict


def singleton(cls: Type) -> Type:
    """A class decorator that implements the Singleton pattern.
    
    Ensures only one instance of the decorated class exists.
    All subsequent instantiations return the same instance.
    
    Args:
        cls: The class to decorate
        
    Returns:
        A wrapper that manages the singleton instance
    """
    _instance: list = []
    
    def get_instance(*args: Any, **kwargs: Any) -> Any:
        if not _instance:
            _instance.append(cls(*args, **kwargs))
        return _instance[0]
    
    # Copy class metadata
    get_instance.__name__ = cls.__name__
    get_instance.__doc__ = cls.__doc__
    get_instance.__module__ = cls.__module__
    
    return get_instance


# Example usage for testing
@singleton
class Database:
    """A singleton database connection."""
    
    def __init__(self, connection_string: str = "default") -> None:
        self.connection_string = connection_string
        self.connected = False
    
    def connect(self) -> str:
        """Connect to the database."""
        self.connected = True
        return f"Connected to {self.connection_string}"
    
    def disconnect(self) -> str:
        """Disconnect from the database."""
        self.connected = False
        return "Disconnected"


@singleton
class Configuration:
    """A singleton configuration."""
    
    def __init__(self) -> None:
        self.settings: dict[str, Any] = {}
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self.settings[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.settings.get(key, default)
