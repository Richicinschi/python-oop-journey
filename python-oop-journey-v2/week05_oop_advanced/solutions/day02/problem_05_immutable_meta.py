"""Problem 05: Immutable Instance Metaclass - Solution.

Makes all instances immutable after creation, preventing accidental
modification of objects that should be constant.
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
        # Store original __setattr__ if it exists
        original_setattr = namespace.get('__setattr__')
        
        def frozen_setattr(self: Any, name: str, value: Any) -> None:
            """Prevent attribute modification after initialization."""
            # Allow setting _initialized during init
            if name == '_initialized':
                if original_setattr:
                    original_setattr(self, name, value)
                else:
                    super(self.__class__, self).__setattr__(name, value)
                return
            
            # Check if already initialized
            initialized = getattr(self, '_initialized', False)
            if initialized:
                raise AttributeError(
                    f"Cannot modify immutable {self.__class__.__name__} instance. "
                    f"Use replace() to create a modified copy."
                )
            
            # Allow during initialization
            if original_setattr:
                original_setattr(self, name, value)
            else:
                super(self.__class__, self).__setattr__(name, value)
        
        namespace['__setattr__'] = frozen_setattr
        
        # Also prevent attribute deletion
        def frozen_delattr(self: Any, name: str) -> None:
            """Prevent attribute deletion."""
            raise AttributeError(
                f"Cannot delete attributes from immutable {self.__class__.__name__}"
            )
        
        namespace['__delattr__'] = frozen_delattr
        
        cls = super().__new__(mcs, name, bases, namespace)
        return cls


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
        self._x = x
        self._y = y
        self._initialized = True
    
    @property
    def x(self) -> float:
        """Get x coordinate."""
        return self._x
    
    @property
    def y(self) -> float:
        """Get y coordinate."""
        return self._y
    
    def replace(self, x: float | None = None, y: float | None = None) -> Point:
        """Create a new Point with modified values.
        
        Args:
            x: New x coordinate (or None to keep current)
            y: New y coordinate (or None to keep current)
            
        Returns:
            New Point instance
        """
        new_x = x if x is not None else self._x
        new_y = y if y is not None else self._y
        return Point(new_x, new_y)
    
    def __eq__(self, other: object) -> bool:
        """Check equality with another point."""
        if not isinstance(other, Point):
            return NotImplemented
        return self._x == other._x and self._y == other._y
    
    def __hash__(self) -> int:
        """Generate hash for use in sets and dicts."""
        return hash((self._x, self._y))
    
    def __repr__(self) -> str:
        """Return string representation."""
        return f"Point({self._x}, {self._y})"


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
        self._debug = debug
        self._timeout = timeout
        self._retries = retries
        self._initialized = True
    
    @property
    def debug(self) -> bool:
        """Get debug flag."""
        return self._debug
    
    @property
    def timeout(self) -> int:
        """Get timeout value."""
        return self._timeout
    
    @property
    def retries(self) -> int:
        """Get retries value."""
        return self._retries
    
    def replace(self, **kwargs: Any) -> ImmutableConfig:
        """Create a new config with modified values.
        
        Args:
            **kwargs: Attributes to modify
            
        Returns:
            New ImmutableConfig instance
        """
        debug = kwargs.get('debug', self._debug)
        timeout = kwargs.get('timeout', self._timeout)
        retries = kwargs.get('retries', self._retries)
        return ImmutableConfig(debug, timeout, retries)
    
    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if not isinstance(other, ImmutableConfig):
            return NotImplemented
        return (
            self._debug == other._debug
            and self._timeout == other._timeout
            and self._retries == other._retries
        )
    
    def __hash__(self) -> int:
        """Generate hash."""
        return hash((self._debug, self._timeout, self._retries))
