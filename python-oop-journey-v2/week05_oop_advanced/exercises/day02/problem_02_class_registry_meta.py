"""Problem 02: Class Registry Metaclass

Topic: Metaclasses
Difficulty: Medium

Implement a metaclass that automatically registers all subclasses of a base
class. This pattern is useful for plugin systems, factory patterns, and
when you need to discover all implementations of an interface.

Classes to implement:
- RegistryMeta: Metaclass that maintains a registry of all classes
- BaseModel: Base class using the metaclass
- User, Product, Order: Example models that auto-register

Requirements:
- The metaclass should maintain a class-level registry dictionary
- All classes using the metaclass should be registered automatically
- The base class itself should NOT be registered (only subclasses)
- The registry should map class names to class objects
"""

from __future__ import annotations

from typing import Any


class RegistryMeta(type):
    """Metaclass that automatically registers all created classes.
    
    This is useful for:
    - Plugin systems where you need to discover all implementations
    - ORM systems that need to track all model classes
    - Factory patterns that create objects by name
    
    Attributes:
        _registry: Dictionary mapping class names to class objects
    """
    
    _registry: dict[str, type] = {}
    
    def __new__(
        mcs: type,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> type:
        """Create class and register it if it's not the base class.
        
        Args:
            mcs: This metaclass
            name: Name of the class being created
            bases: Base classes
            namespace: Class namespace dictionary
            
        Returns:
            The newly created class
        """
        raise NotImplementedError("Implement __new__")
    
    @classmethod
    def get_registry(mcs) -> dict[str, type]:
        """Get a copy of the current registry.
        
        Returns:
            Dictionary mapping class names to class objects
        """
        raise NotImplementedError("Implement get_registry")
    
    @classmethod
    def get_class(mcs, name: str) -> type | None:
        """Get a class from the registry by name.
        
        Args:
            name: The class name to look up
            
        Returns:
            The class object or None if not found
        """
        raise NotImplementedError("Implement get_class")
    
    @classmethod
    def clear_registry(mcs) -> None:
        """Clear the registry (useful for testing)."""
        raise NotImplementedError("Implement clear_registry")


class BaseModel(metaclass=RegistryMeta):
    """Base model class that auto-registers subclasses.
    
    This class should NOT appear in the registry itself.
    All direct and indirect subclasses should be registered.
    """
    
    def __init__(self, **kwargs: Any) -> None:
        """Initialize the model with attributes from kwargs."""
        raise NotImplementedError("Implement __init__")
    
    def to_dict(self) -> dict[str, Any]:
        """Convert the model to a dictionary.
        
        Returns:
            Dictionary representation of the model
        """
        raise NotImplementedError("Implement to_dict")


# Hints for Class Registry Metaclass (Hard):
# 
# Hint 1 - Conceptual nudge:
# Every time a class uses this metaclass, you want to automatically add it to a registry.
# The registry should map model names to classes.
#
# Hint 2 - Structural plan:
# - In RegistryMeta.__init__, add the new class to a registry dictionary
# - Use a class attribute on RegistryMeta itself or a module-level dict
# - Provide class methods get_model() and list_models() to access the registry
# - Store both the class reference and the model name
#
# Hint 3 - Edge-case warning:
# Make sure to handle inheritance - subclasses should be registered separately.
# What if someone creates a class with the same name? Should it overwrite or error?
    
    @classmethod
    def get_model_name(cls) -> str:
        """Get the model class name.
        
        Returns:
            The class name
        """
        raise NotImplementedError("Implement get_model_name")


class User(BaseModel):
    """User model representing a system user."""
    
    def __init__(self, username: str, email: str, **kwargs: Any) -> None:
        """Initialize user with username and email.
        
        Args:
            username: The user's username
            email: The user's email address
        """
        raise NotImplementedError("Implement __init__")
    
    def to_dict(self) -> dict[str, Any]:
        """Convert user to dictionary."""
        raise NotImplementedError("Implement to_dict")


class Product(BaseModel):
    """Product model representing a catalog item."""
    
    def __init__(self, name: str, price: float, **kwargs: Any) -> None:
        """Initialize product with name and price.
        
        Args:
            name: Product name
            price: Product price
        """
        raise NotImplementedError("Implement __init__")
    
    def to_dict(self) -> dict[str, Any]:
        """Convert product to dictionary."""
        raise NotImplementedError("Implement to_dict")


class Order(BaseModel):
    """Order model representing a customer order."""
    
    def __init__(self, order_id: str, total: float, **kwargs: Any) -> None:
        """Initialize order with id and total.
        
        Args:
            order_id: Unique order identifier
            total: Order total amount
        """
        raise NotImplementedError("Implement __init__")
    
    def to_dict(self) -> dict[str, Any]:
        """Convert order to dictionary."""
        raise NotImplementedError("Implement to_dict")
