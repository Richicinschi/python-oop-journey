"""Problem 01: Object Inspector.

Topic: Introspection and Reflection
Difficulty: Medium

Inspect object attributes dynamically using Python's introspection capabilities.

Implement an ObjectInspector class that can:
- List all attributes of an object (public, private, methods, properties)
- Get attribute values dynamically with type information
- Filter attributes by type (methods, properties, data attributes)
- Find attributes by name pattern
- Compare two objects for attribute differences

Example:
    >>> class Person:
    ...     def __init__(self, name: str, age: int) -> None:
    ...         self.name = name
    ...         self._age = age
    ...     def greet(self) -> str:
    ...         return f"Hello, I'm {self.name}"
    ...     @property
    ...     def age(self) -> int:
    ...         return self._age
    
    >>> person = Person("Alice", 30)
    >>> inspector = ObjectInspector(person)
    >>> inspector.list_attributes()
    {'name': {'type': 'data', 'value': 'Alice'}, '_age': {...}, ...}
    
    >>> inspector.get_attribute_info('name')
    {'name': 'name', 'type': str, 'value': 'Alice', 'kind': 'data'}
    
    >>> inspector.filter_by_type('method')
    {'greet': <bound method Person.greet ...>}
"""

from __future__ import annotations

from typing import Any, Callable


class ObjectInspector:
    """Inspects Python objects using introspection.
    
    This class provides tools for examining objects at runtime,
    including attribute listing, filtering, and comparison.
    
    Attributes:
        target: The object being inspected.
    """
    
    def __init__(self, target: object) -> None:
        """Initialize the inspector with a target object.
        
        Args:
            target: The object to inspect.
        """
        raise NotImplementedError("Implement __init__")
    
    def list_attributes(self, include_private: bool = False) -> dict[str, dict[str, Any]]:
        """List all attributes with their types and values.
        
        Args:
            include_private: Whether to include private attributes
                           (those starting with single underscore).
        
        Returns:
            Dictionary mapping attribute names to their info dictionaries.
            Each info dict contains:
            - 'type': The type of the value
            - 'value': The attribute value (repr for callables)
            - 'kind': 'data', 'method', 'property', or 'callable'
        """
        raise NotImplementedError("Implement list_attributes")
    
    def get_attribute_info(self, name: str) -> dict[str, Any] | None:
        """Get detailed information about a specific attribute.
        
        Args:
            name: The attribute name to look up.
        
        Returns:
            Dictionary with attribute details, or None if not found.
            Contains:
            - 'name': The attribute name
            - 'type': The type of the value
            - 'value': The current value
            - 'kind': 'data', 'method', 'property', or 'callable'
            - 'doc': The docstring if available
        """
        raise NotImplementedError("Implement get_attribute_info")
    
    def filter_by_type(self, kind: str) -> dict[str, Any]:
        """Filter attributes by their kind.
        
        Args:
            kind: One of 'data', 'method', 'property', 'callable', 'all'.
        
        Returns:
            Dictionary of attribute names to values matching the kind.
        """
        raise NotImplementedError("Implement filter_by_type")
    
    def find_by_pattern(self, pattern: str) -> dict[str, Any]:
        """Find attributes matching a name pattern.
        
        Args:
            pattern: Substring to search for in attribute names.
        
        Returns:
            Dictionary of matching attribute names to their values.
        """
        raise NotImplementedError("Implement find_by_pattern")
    
    def compare_with(self, other: object) -> dict[str, dict[str, Any]]:
        """Compare this object's attributes with another object.
        
        Args:
            other: The object to compare against.
        
        Returns:
            Dictionary with keys:
            - 'only_in_self': Attributes only in this object
            - 'only_in_other': Attributes only in the other object
            - 'different': Attributes with different values
            - 'same': Attributes with same values
        """
        raise NotImplementedError("Implement compare_with")
