"""Problem 02: Class Registry Metaclass - Solution.

Implements automatic registration of subclasses for plugin systems,
ORM models, and factory patterns.
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
        cls = super().__new__(mcs, name, bases, namespace)
        # Don't register the base class itself, only subclasses
        if name != 'BaseModel':
            mcs._registry[name] = cls
        return cls
    
    @classmethod
    def get_registry(mcs) -> dict[str, type]:
        """Get a copy of the current registry.
        
        Returns:
            Dictionary mapping class names to class objects
        """
        return mcs._registry.copy()
    
    @classmethod
    def get_class(mcs, name: str) -> type | None:
        """Get a class from the registry by name.
        
        Args:
            name: The class name to look up
            
        Returns:
            The class object or None if not found
        """
        return mcs._registry.get(name)
    
    @classmethod
    def clear_registry(mcs) -> None:
        """Clear the registry (useful for testing)."""
        mcs._registry.clear()


class BaseModel(metaclass=RegistryMeta):
    """Base model class that auto-registers subclasses.
    
    This class should NOT appear in the registry itself.
    All direct and indirect subclasses should be registered.
    """
    
    def __init__(self, **kwargs: Any) -> None:
        """Initialize the model with attributes from kwargs."""
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert the model to a dictionary.
        
        Returns:
            Dictionary representation of the model
        """
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith('_')
        }
    
    @classmethod
    def get_model_name(cls) -> str:
        """Get the model class name.
        
        Returns:
            The class name
        """
        return cls.__name__


class User(BaseModel):
    """User model representing a system user."""
    
    def __init__(self, username: str = "", email: str = "", **kwargs: Any) -> None:
        """Initialize user with username and email.
        
        Args:
            username: The user's username
            email: The user's email address
        """
        super().__init__(**kwargs)
        self.username = username
        self.email = email
    
    def to_dict(self) -> dict[str, Any]:
        """Convert user to dictionary."""
        return {'username': self.username, 'email': self.email}


class Product(BaseModel):
    """Product model representing a catalog item."""
    
    def __init__(self, name: str = "", price: float = 0.0, **kwargs: Any) -> None:
        """Initialize product with name and price.
        
        Args:
            name: Product name
            price: Product price
        """
        super().__init__(**kwargs)
        self.name = name
        self.price = price
    
    def to_dict(self) -> dict[str, Any]:
        """Convert product to dictionary."""
        return {'name': self.name, 'price': self.price}


class Order(BaseModel):
    """Order model representing a customer order."""
    
    def __init__(self, order_id: str = "", total: float = 0.0, **kwargs: Any) -> None:
        """Initialize order with id and total.
        
        Args:
            order_id: Unique order identifier
            total: Order total amount
        """
        super().__init__(**kwargs)
        self.order_id = order_id
        self.total = total
    
    def to_dict(self) -> dict[str, Any]:
        """Convert order to dictionary."""
        return {'order_id': self.order_id, 'total': self.total}
