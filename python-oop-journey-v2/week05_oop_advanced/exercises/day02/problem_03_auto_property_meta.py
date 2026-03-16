"""Problem 03: Auto Property Generation Metaclass

Topic: Metaclasses
Difficulty: Medium

Implement a metaclass that automatically generates properties from type
annotations. This eliminates boilerplate getter/setter code for simple
attribute access control.

Classes to implement:
- AutoPropertyMeta: Metaclass that converts annotations to properties
- Person: Example class with auto-generated properties
- Config: Example class with typed configuration options

Requirements:
- Read the class annotations in __new__
- Generate a private attribute (e.g., _name) for each annotation
- Generate a property with getter and setter for each attribute
- The setter should perform type checking
- Support default values via class attributes
"""

from __future__ import annotations

from typing import Any, get_type_hints


class AutoPropertyMeta(type):
    """Metaclass that auto-generates properties from type annotations.
    
    For each annotated attribute, this metaclass:
    1. Creates a private storage attribute (e.g., _name for name)
    2. Generates a property with getter and setter
    3. The setter performs runtime type checking
    
    Example:
        class Person(metaclass=AutoPropertyMeta):
            name: str
            age: int
        
        p = Person()
        p.name = "Alice"  # Uses generated setter with type checking
        print(p.name)     # Uses generated getter
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
        raise NotImplementedError("Implement __new__")
    
    @staticmethod
    def _make_property(name: str, expected_type: type) -> property:
        """Create a property with type-checked getter and setter.
        
        Args:
            name: The public attribute name
            expected_type: The expected type for the attribute
            
        Returns:
            A property object with getter and setter
        """
        raise NotImplementedError("Implement _make_property")


class Person(metaclass=AutoPropertyMeta):
    """Person class with auto-generated type-checked properties.
    
    The metaclass will automatically generate:
    - name property backed by _name attribute
    - age property backed by _age attribute
    - email property backed by _email attribute
    
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
        raise NotImplementedError("Implement __init__")
    
    def __str__(self) -> str:
        """Return string representation.
        
        Returns:
            Formatted person info
        """
        raise NotImplementedError("Implement __str__")


class Config(metaclass=AutoPropertyMeta):
    """Configuration class with type-safe auto-properties.
    
    Attributes:
        debug: Debug mode flag (bool)
        timeout: Connection timeout in seconds (int)
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
        raise NotImplementedError("Implement __init__")
    
    def as_dict(self) -> dict[str, Any]:
        """Convert config to dictionary.
        
        Returns:
            Dictionary of configuration values
        """
        raise NotImplementedError("Implement as_dict")


# Hints for Auto-Property Metaclass (Hard):
# 
# Hint 1 - Conceptual nudge:
# You need to inspect the class namespace for private attributes (starting with _ but not __)
# and automatically create properties for them.
#
# Hint 2 - Structural plan:
# - In __new__, scan the namespace for private attributes
# - For each _attr found, create a property getter (and setter if not _readonly)
# - Insert these properties into the namespace before calling super().__new__
# - The property should access instance.__dict__[f'_{name}']
#
# Hint 3 - Edge-case warning:
# Don't create properties for dunder attributes (like __init__). Be careful about
# attributes that are methods - you only want to expose data attributes as properties.
