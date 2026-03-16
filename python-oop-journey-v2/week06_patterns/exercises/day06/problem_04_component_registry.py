"""Problem 04: Component Registry

Topic: Registry Pattern, Factory Pattern
Difficulty: Hard

Implement a component registry system using the Registry and Factory patterns.

HINTS:
- Hint 1 (Conceptual): Registry stores types and instances. Factory creates 
  instances from registered types. Generic typing allows type-safe registries.
- Hint 2 (Structural): ComponentRegistry is Generic[T]. _types: Dict[str, Type[T]]. 
  _instances: Dict[str, T]. Methods: register_type(), create(), register_singleton(), get().
- Hint 3 (Edge Case): create() returns None if type not registered. get() returns 
  None for missing instances. Singletons are created once and reused.

PATTERN EXPLANATION:
The Registry pattern provides a global access point to instances or types
without using global variables. Combined with Factory, it enables runtime
registration and creation of components.

STRUCTURE:
- Registry: Maintains mapping of names to types/instances
- Component Interface: Contract for registrable components
- Factory Methods: Create instances from registered types
- Singleton Storage: For shared component instances

WHEN TO USE:
- For plugin systems
- When types need to be registered at runtime
- For dependency injection containers
- To avoid hard-coding class names

EXAMPLE USAGE:
    registry = ComponentRegistry[Weapon]()
    
    # Register types
    registry.register_type("sword", Sword)
    registry.register_type("bow", Bow)
    
    # Create instances
    weapon1 = registry.create("sword", damage=10)
    weapon2 = registry.create("bow", damage=5, range=100)
    
    # Register singleton
    registry.register_singleton("excalibur", Sword(damage=100))

Your task:
1. Create a ComponentRegistry that manages component types and instances
2. Support registering component types (factories)
3. Support creating instances by name
4. Support registering and retrieving singleton instances
5. Implement lifecycle hooks (on_register, on_create)

Requirements:
- register_type(name, component_type) - Register a factory for creating components
- create(name, **kwargs) - Create a new instance of a registered type
- register_singleton(name, instance) - Register a singleton instance
- get_singleton(name) - Retrieve a registered singleton
- Support lifecycle callbacks on components
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol, TypeVar, Generic


T = TypeVar("T")


class Component(Protocol):
    """Protocol for components that support lifecycle hooks."""
    
    def on_register(self) -> None:
        """Called when component type is registered."""
        ...
    
    def on_create(self) -> None:
        """Called when component instance is created."""
        ...


class ComponentRegistry(Generic[T]):
    """Registry for managing component types and instances."""
    
    def __init__(self) -> None:
        # TODO: Initialize data structures for types and singletons
        pass
    
    def register_type(self, name: str, component_type: type[T]) -> None:
        """
        Register a component type.
        
        Args:
            name: Unique identifier for this component type
            component_type: Class to instantiate when create() is called
        """
        raise NotImplementedError("Implement register_type")
    
    def create(self, type_name: str, **kwargs: Any) -> T | None:
        """
        Create an instance of a registered component type.
        
        Args:
            type_name: Registered type name
            **kwargs: Arguments to pass to the component constructor
            
        Returns:
            New instance or None if type not registered
        """
        raise NotImplementedError("Implement create")
    
    def register_singleton(self, name: str, instance: T) -> None:
        """
        Register a singleton instance.
        
        Args:
            name: Unique identifier for this singleton
            instance: The singleton instance
        """
        raise NotImplementedError("Implement register_singleton")
    
    def get_singleton(self, name: str) -> T | None:
        """
        Get a registered singleton.
        
        Returns:
            The singleton instance or None if not found
        """
        raise NotImplementedError("Implement get_singleton")
    
    def is_registered(self, name: str) -> bool:
        """Check if a type or singleton is registered."""
        raise NotImplementedError("Implement is_registered")
    
    def get_registered_types(self) -> list[str]:
        """Get all registered type names."""
        raise NotImplementedError("Implement get_registered_types")
    
    def get_singleton_names(self) -> list[str]:
        """Get all registered singleton names."""
        raise NotImplementedError("Implement get_singleton_names")
    
    def unregister(self, name: str) -> bool:
        """
        Unregister a type or singleton.
        
        Returns:
            True if found and removed, False otherwise
        """
        raise NotImplementedError("Implement unregister")
    
    def clear(self) -> None:
        """Remove all registrations."""
        raise NotImplementedError("Implement clear")


# TODO: Implement example components for a game system
# Example: Weapon, Armor, Potion components
