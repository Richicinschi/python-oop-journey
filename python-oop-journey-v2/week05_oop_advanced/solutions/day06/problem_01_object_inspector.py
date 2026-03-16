"""Reference solution for Problem 01: Object Inspector."""

from __future__ import annotations

import inspect
from typing import Any


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
        self.target = target
    
    def _get_kind(self, name: str, value: Any) -> str:
        """Determine the kind of an attribute.
        
        Args:
            name: The attribute name.
            value: The attribute value.
        
        Returns:
            Kind classification: 'data', 'method', 'property', or 'callable'.
        """
        # Check if it's a property by looking at the class
        # Properties are descriptors in the class, not the instance
        if hasattr(self.target, '__class__'):
            cls = self.target.__class__
            if name in cls.__dict__:
                attr = cls.__dict__[name]
                if isinstance(attr, property):
                    return 'property'
        
        # Check if it's a method
        if inspect.ismethod(value):
            return 'method'
        
        # Check if it's any callable
        if callable(value):
            return 'callable'
        
        # Otherwise it's data
        return 'data'
    
    def _get_value_repr(self, value: Any) -> Any:
        """Get a representation of a value.
        
        For callables, returns a description string.
        For other values, returns the value itself.
        
        Args:
            value: The value to represent.
        
        Returns:
            Representation of the value.
        """
        if callable(value) and not isinstance(value, property):
            if inspect.ismethod(value):
                return f"<bound method {value.__qualname__}>"
            elif inspect.isfunction(value):
                return f"<function {value.__name__}>"
            else:
                return f"<callable {type(value).__name__}>"
        return value
    
    def list_attributes(self, include_private: bool = False) -> dict[str, dict[str, Any]]:
        """List all attributes with their types and values.
        
        Args:
            include_private: Whether to include private attributes
                           (those starting with single underscore).
        
        Returns:
            Dictionary mapping attribute names to their info dictionaries.
        """
        result: dict[str, dict[str, Any]] = {}
        
        # Get all attributes using dir()
        for name in dir(self.target):
            # Skip dunder methods unless explicitly private
            if name.startswith('__') and name.endswith('__'):
                continue
            
            # Skip private attributes unless requested
            if name.startswith('_') and not include_private:
                continue
            
            try:
                value = getattr(self.target, name)
                kind = self._get_kind(name, value)
                
                result[name] = {
                    'type': type(value).__name__,
                    'value': self._get_value_repr(value),
                    'kind': kind,
                }
            except (AttributeError, Exception):
                # Some attributes may raise on access
                result[name] = {
                    'type': 'unknown',
                    'value': '<inaccessible>',
                    'kind': 'unknown',
                }
        
        return result
    
    def get_attribute_info(self, name: str) -> dict[str, Any] | None:
        """Get detailed information about a specific attribute.
        
        Args:
            name: The attribute name to look up.
        
        Returns:
            Dictionary with attribute details, or None if not found.
        """
        if not hasattr(self.target, name):
            return None
        
        try:
            value = getattr(self.target, name)
            kind = self._get_kind(name, value)
            
            info: dict[str, Any] = {
                'name': name,
                'type': type(value),
                'value': value,
                'kind': kind,
            }
            
            # Add docstring if available
            if kind in ('method', 'callable'):
                info['doc'] = inspect.getdoc(value)
            elif kind == 'property':
                cls = self.target.__class__
                prop = cls.__dict__.get(name)
                if isinstance(prop, property):
                    info['doc'] = prop.__doc__
            
            return info
        except Exception:
            return None
    
    def filter_by_type(self, kind: str) -> dict[str, Any]:
        """Filter attributes by their kind.
        
        Args:
            kind: One of 'data', 'method', 'property', 'callable', 'all'.
        
        Returns:
            Dictionary of attribute names to values matching the kind.
        """
        result: dict[str, Any] = {}
        
        for name in dir(self.target):
            # Skip dunder methods
            if name.startswith('__') and name.endswith('__'):
                continue
            
            try:
                value = getattr(self.target, name)
                attr_kind = self._get_kind(name, value)
                
                if kind == 'all' or attr_kind == kind:
                    result[name] = value
            except Exception:
                continue
        
        return result
    
    def find_by_pattern(self, pattern: str) -> dict[str, Any]:
        """Find attributes matching a name pattern.
        
        Args:
            pattern: Substring to search for in attribute names.
        
        Returns:
            Dictionary of matching attribute names to their values.
        """
        result: dict[str, Any] = {}
        
        for name in dir(self.target):
            if pattern in name:
                try:
                    result[name] = getattr(self.target, name)
                except Exception:
                    continue
        
        return result
    
    def compare_with(self, other: object) -> dict[str, dict[str, Any]]:
        """Compare this object's attributes with another object.
        
        Args:
            other: The object to compare against.
        
        Returns:
            Dictionary with comparison results.
        """
        self_attrs = set(dir(self.target))
        other_attrs = set(dir(other))
        
        only_in_self = self_attrs - other_attrs
        only_in_other = other_attrs - self_attrs
        both = self_attrs & other_attrs
        
        different: dict[str, tuple[Any, Any]] = {}
        same: list[str] = []
        
        for attr in both:
            # Skip dunder methods for comparison
            if attr.startswith('__') and attr.endswith('__'):
                continue
            
            try:
                self_val = getattr(self.target, attr)
                other_val = getattr(other, attr)
                
                # Compare values (handle unhashable types)
                try:
                    if self_val != other_val:
                        different[attr] = (self_val, other_val)
                    else:
                        same.append(attr)
                except Exception:
                    # If comparison fails, treat as different
                    different[attr] = (self_val, other_val)
            except Exception:
                continue
        
        return {
            'only_in_self': {name: getattr(self.target, name) for name in only_in_self 
                           if not (name.startswith('__') and name.endswith('__'))},
            'only_in_other': {name: getattr(other, name) for name in only_in_other
                            if not (name.startswith('__') and name.endswith('__'))},
            'different': different,
            'same': same,
        }
