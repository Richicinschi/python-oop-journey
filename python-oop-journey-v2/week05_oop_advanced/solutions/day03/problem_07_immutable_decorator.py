"""Reference solution for Problem 07: Immutable Decorator."""

from __future__ import annotations

from typing import Type, Any


def immutable(cls: Type) -> Type:
    """A class decorator that makes instances immutable.
    
    Prevents setting new attributes or modifying existing ones after __init__.
    Raises AttributeError on any attempt to modify the instance.
    
    Args:
        cls: The class to decorate
        
    Returns:
        The decorated class with immutability enforcement
    """
    original_init = cls.__init__
    original_setattr = cls.__setattr__
    original_delattr = cls.__delattr__
    
    def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
        # Mark as initializing
        object.__setattr__(self, '_initializing', True)
        original_init(self, *args, **kwargs)
        # Remove initializing mark
        object.__setattr__(self, '_initializing', False)
    
    def new_setattr(self: Any, name: str, value: Any) -> None:
        if getattr(self, '_initializing', False):
            # Allow setting during initialization
            original_setattr(self, name, value)
        else:
            # Block all modifications after init
            raise AttributeError(
                f"Cannot set attribute '{name}': {cls.__name__} is immutable"
            )
    
    def new_delattr(self: Any, name: str) -> None:
        raise AttributeError(
            f"Cannot delete attribute '{name}': {cls.__name__} is immutable"
        )
    
    cls.__init__ = new_init
    cls.__setattr__ = new_setattr
    cls.__delattr__ = new_delattr
    
    return cls


# Example usage for testing
@immutable
class Point:
    """An immutable 2D point."""
    
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


@immutable
class Color:
    """An immutable RGB color."""
    
    def __init__(self, r: int, g: int, b: int) -> None:
        self.r = r
        self.g = g
        self.b = b
    
    def to_hex(self) -> str:
        """Convert to hex string."""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    def __repr__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b})"
