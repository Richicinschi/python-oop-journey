"""Problem 03: Auto Property Generation Metaclass - Solution.

Automatically generates properties from type annotations, eliminating
boilerplate getter/setter code with runtime type checking.
"""

from __future__ import annotations

from typing import Any, get_type_hints


class AutoPropertyMeta(type):
    """Metaclass that auto-generates properties from type annotations.
    
    For each annotated attribute, this metaclass:
    1. Creates a private storage attribute (e.g., _name for name)
    2. Generates a property with getter and setter
    3. The setter performs runtime type checking
    """
    
    def __new__(
        mcs: type,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> type:
        """Create class with auto-generated properties from annotations.
        
        Args:
            mcs: This metaclass
            name: Name of the class being created
            bases: Base classes
            namespace: Class namespace (contains __annotations__)
            
        Returns:
            The newly created class with generated properties
        """
        cls = super().__new__(mcs, name, bases, namespace)
        
        # Get type hints from the class
        hints = get_type_hints(cls)
        
        for attr_name, attr_type in hints.items():
            # Skip dunder attributes
            if attr_name.startswith('_'):
                continue
            
            # Create property with type checking
            prop = mcs._make_property(attr_name, attr_type)
            setattr(cls, attr_name, prop)
        
        return cls
    
    @staticmethod
    def _make_property(name: str, expected_type: type) -> property:
        """Create a property with type-checked getter and setter.
        
        Args:
            name: The public attribute name
            expected_type: The expected type for the attribute
            
        Returns:
            A property object with getter and setter
        """
        private_name = f"_{name}"
        
        def getter(self: Any) -> Any:
            return getattr(self, private_name, None)
        
        def setter(self: Any, value: Any) -> None:
            # Handle Union types (like str | None)
            origin = getattr(expected_type, '__origin__', None)
            args = getattr(expected_type, '__args__', ())
            
            if origin is not None:
                # It's a generic type like Union
                if value is not None and not isinstance(value, args):
                    raise TypeError(
                        f"Expected one of {args}, got {type(value).__name__}"
                    )
            else:
                # Regular type check, but allow None for optional types
                if value is not None and not isinstance(value, expected_type):
                    raise TypeError(
                        f"Expected {expected_type.__name__}, got {type(value).__name__}"
                    )
            
            setattr(self, private_name, value)
        
        return property(getter, setter)


class Person(metaclass=AutoPropertyMeta):
    """Person class with auto-generated type-checked properties.
    
    Attributes:
        name: Person's name (str)
        age: Person's age (int)
        email: Person's email (str)
    """
    name: str
    age: int
    email: str
    
    def __init__(self, name: str = "", age: int = 0, email: str = "") -> None:
        """Initialize person with auto-generated setters.
        
        Args:
            name: Person's name
            age: Person's age
            email: Person's email address
        """
        self._name = name
        self._age = age
        self._email = email
    
    def __str__(self) -> str:
        """Return string representation.
        
        Returns:
            Formatted person info
        """
        return f"Person(name='{self.name}', age={self.age}, email='{self.email}')"


class Config(metaclass=AutoPropertyMeta):
    """Configuration class with type-safe auto-properties.
    
    Attributes:
        debug: Debug mode flag (bool)
        timeout: Connection timeout (int)
        api_url: API endpoint URL (str)
        max_retries: Maximum retry attempts (int)
    """
    debug: bool
    timeout: int
    api_url: str
    max_retries: int
    
    def __init__(
        self,
        debug: bool = False,
        timeout: int = 30,
        api_url: str = "http://localhost",
        max_retries: int = 3,
    ) -> None:
        """Initialize config with defaults.
        
        Args:
            debug: Enable debug mode
            timeout: Connection timeout
            api_url: API endpoint URL
            max_retries: Maximum retry attempts
        """
        self._debug = debug
        self._timeout = timeout
        self._api_url = api_url
        self._max_retries = max_retries
    
    def as_dict(self) -> dict[str, Any]:
        """Convert config to dictionary.
        
        Returns:
            Dictionary of configuration values
        """
        return {
            'debug': self.debug,
            'timeout': self.timeout,
            'api_url': self.api_url,
            'max_retries': self.max_retries,
        }
