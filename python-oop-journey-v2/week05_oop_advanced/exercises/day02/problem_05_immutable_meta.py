"""Problem 05: Immutable Instance Metaclass

Topic: Metaclasses
Difficulty: Medium

Implement a metaclass that makes all instances of a class immutable after
creation. This prevents accidental modification of objects that should be
constant, similar to Python's tuple or frozen dataclass.

Classes to implement:
- ImmutableMeta: Metaclass that enforces immutability
- Point: Immutable 2D point class
- ImmutableConfig: Immutable configuration class

Requirements:
- After __init__ completes, no attributes can be modified
- Attempting to set attributes should raise AttributeError
- The class should have a method to create modified copies
- Frozen instances should be hashable (for use as dict keys)
"""

from __future__ import annotations

from typing import Any


class ImmutableMeta(type):
    """Metaclass that makes instances immutable after initialization.
    
    Classes using this metaclass will:
    1. Allow attribute setting during __init__
    2. Prevent attribute modification after __init__ completes
    3. Support creating modified copies via a replace() method
    4. Be hashable if all attributes are hashable
    
    Example:
        class Point(metaclass=ImmutableMeta):
            def __init__(self, x, y):
                self.x = x
                self.y = y
        
        p = Point(1, 2)
        p.x = 3  # Raises AttributeError
        p2 = p.replace(x=3)  # Creates new Point with x=3
    """
    
    def __new__(
        mcs: type,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> type:
        """Create immutable class with modified __setattr__.
        
        Args:
            mcs: This metaclass
            name: Name of the class being created
            bases: Base classes
            namespace: Class namespace dictionary
            
        Returns:
            The newly created class with immutability support
        """
        raise NotImplementedError("Implement __new__")
    
    @staticmethod
    def _make_setattr(original_setattr: Any) -> Any:
        """Create a __setattr__ that respects immutability.
        
        Args:
            original_setattr: The class's original __setattr__ if any
            
        Returns:
            New __setattr__ method
        """
        raise NotImplementedError("Implement _make_setattr")


class Point(metaclass=ImmutableMeta):
    """Immutable 2D point class.
    
    Attributes:
        x: X coordinate (read-only after creation)
        y: Y coordinate (read-only after creation)
    """
    
    __slots__ = ('_x', '_y', '_initialized')
    
    def __init__(self, x: float, y: float) -> None:
        """Initialize immutable point.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        raise NotImplementedError("Implement __init__")
    
    @property
    def x(self) -> float:
        """Get x coordinate."""
        raise NotImplementedError("Implement x property")
    
    @property
    def y(self) -> float:
        """Get y coordinate."""
        raise NotImplementedError("Implement y property")
    
    def replace(self, x: float | None = None, y: float | None = None) -> Point:
        """Create a new Point with modified values.
        
        Args:
            x: New x coordinate (or None to keep current)
            y: New y coordinate (or None to keep current)
            
        Returns:
            New Point instance
        """
        raise NotImplementedError("Implement replace")
    
    def __eq__(self, other: object) -> bool:
        """Check equality with another point."""
        raise NotImplementedError("Implement __eq__")
    
    def __hash__(self) -> int:
        """Generate hash for use in sets and dicts."""
        raise NotImplementedError("Implement __hash__")


# Hints for Immutable Metaclass (Hard):
# 
# Hint 1 - Conceptual nudge:
# You need to prevent attribute modification after __init__ completes. This means
# controlling __setattr__ at the class level.
#
# Hint 2 - Structural plan:
# - Create a custom __setattr__ that checks if _initialized flag is set
# - During __init__, allow attribute setting; after __init__, raise AttributeError
# - Store _initialized in instance.__dict__ to avoid recursion
# - You may also want to prevent attribute deletion (__delattr__)
#
# Hint 3 - Edge-case warning:
# Be careful with _immutable_fields - check these first if specified. Also, consider
# what happens with mutable objects (lists, dicts) as values - Python's immutability
# is shallow; you might need to make defensive copies.
    
    def __repr__(self) -> str:
        """Return string representation."""
        raise NotImplementedError("Implement __repr__")


class ImmutableConfig(metaclass=ImmutableMeta):
    """Immutable configuration container.
    
    Attributes:
        debug: Debug mode flag
        timeout: Connection timeout
        retries: Max retry attempts
    """
    
    __slots__ = ('_debug', '_timeout', '_retries', '_initialized')
    
    def __init__(self, debug: bool = False, timeout: int = 30, retries: int = 3) -> None:
        """Initialize immutable config.
        
        Args:
            debug: Debug mode flag
            timeout: Connection timeout in seconds
            retries: Maximum retry attempts
        """
        raise NotImplementedError("Implement __init__")
    
    @property
    def debug(self) -> bool:
        """Get debug flag."""
        raise NotImplementedError("Implement debug property")
    
    @property
    def timeout(self) -> int:
        """Get timeout value."""
        raise NotImplementedError("Implement timeout property")
    
    @property
    def retries(self) -> int:
        """Get retries value."""
        raise NotImplementedError("Implement retries property")
    
    def replace(self, **kwargs: Any) -> ImmutableConfig:
        """Create a new config with modified values.
        
        Args:
            **kwargs: Attributes to modify
            
        Returns:
            New ImmutableConfig instance
        """
        raise NotImplementedError("Implement replace")
    
    def __eq__(self, other: object) -> bool:
        """Check equality."""
        raise NotImplementedError("Implement __eq__")
    
    def __hash__(self) -> int:
        """Generate hash."""
        raise NotImplementedError("Implement __hash__")
