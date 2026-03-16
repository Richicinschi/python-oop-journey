"""Reference solution for Problem 04: Component Registry."""

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
        self._types: dict[str, type[T]] = {}
        self._singletons: dict[str, T] = {}
        self._creation_count: dict[str, int] = {}
    
    def register_type(self, name: str, component_type: type[T]) -> None:
        """
        Register a component type.
        
        Args:
            name: Unique identifier for this component type
            component_type: Class to instantiate when create() is called
        """
        self._types[name] = component_type
        self._creation_count[name] = 0
        
        # Call lifecycle hook if available
        if hasattr(component_type, "on_register"):
            try:
                component_type.on_register()
            except TypeError:
                pass  # Static method or class method may raise
    
    def create(self, type_name: str, **kwargs: Any) -> T | None:
        """
        Create an instance of a registered component type.
        
        Args:
            type_name: Registered type name
            **kwargs: Arguments to pass to the component constructor
            
        Returns:
            New instance or None if type not registered
        """
        if component_type := self._types.get(type_name):
            instance = component_type(**kwargs)
            self._creation_count[type_name] = self._creation_count.get(type_name, 0) + 1
            
            # Call lifecycle hook if available
            if hasattr(instance, "on_create"):
                instance.on_create()
            
            return instance
        return None
    
    def register_singleton(self, name: str, instance: T) -> None:
        """
        Register a singleton instance.
        
        Args:
            name: Unique identifier for this singleton
            instance: The singleton instance
        """
        self._singletons[name] = instance
    
    def get_singleton(self, name: str) -> T | None:
        """
        Get a registered singleton.
        
        Returns:
            The singleton instance or None if not found
        """
        return self._singletons.get(name)
    
    def is_registered(self, name: str) -> bool:
        """Check if a type or singleton is registered."""
        return name in self._types or name in self._singletons
    
    def get_registered_types(self) -> list[str]:
        """Get all registered type names."""
        return list(self._types.keys())
    
    def get_singleton_names(self) -> list[str]:
        """Get all registered singleton names."""
        return list(self._singletons.keys())
    
    def get_creation_count(self, type_name: str) -> int:
        """Get number of instances created for a type."""
        return self._creation_count.get(type_name, 0)
    
    def unregister(self, name: str) -> bool:
        """
        Unregister a type or singleton.
        
        Returns:
            True if found and removed, False otherwise
        """
        found = False
        if name in self._types:
            del self._types[name]
            del self._creation_count[name]
            found = True
        if name in self._singletons:
            del self._singletons[name]
            found = True
        return found
    
    def clear(self) -> None:
        """Remove all registrations."""
        self._types.clear()
        self._singletons.clear()
        self._creation_count.clear()


# Example component implementations for a game system

class Weapon:
    """Weapon component."""
    
    _registered = False
    _created_count = 0
    
    def __init__(self, name: str, damage: int, durability: int = 100) -> None:
        self.name = name
        self.damage = damage
        self.durability = durability
    
    @classmethod
    def on_register(cls) -> None:
        cls._registered = True
    
    def on_create(self) -> None:
        Weapon._created_count += 1
    
    @classmethod
    def is_registered(cls) -> bool:
        return cls._registered
    
    @classmethod
    def get_created_count(cls) -> int:
        return cls._created_count
    
    def use(self) -> str:
        if self.durability > 0:
            self.durability -= 1
            return f"{self.name} deals {self.damage} damage"
        return f"{self.name} is broken"


class Armor:
    """Armor component."""
    
    def __init__(self, name: str, defense: int, slot: str = "body") -> None:
        self.name = name
        self.defense = defense
        self.slot = slot
        self.equipped = False
    
    def equip(self) -> str:
        self.equipped = True
        return f"Equipped {self.name}"
    
    def unequip(self) -> str:
        self.equipped = False
        return f"Unequipped {self.name}"


class Potion:
    """Potion component."""
    
    def __init__(self, name: str, effect: str, potency: int) -> None:
        self.name = name
        self.effect = effect
        self.potency = potency
        self.consumed = False
    
    def drink(self) -> str:
        if self.consumed:
            return "Bottle is empty"
        self.consumed = True
        return f"Drank {self.name}: {self.effect} +{self.potency}"


class ItemFactory:
    """Factory that uses the registry to create items."""
    
    def __init__(self) -> None:
        self._registry: ComponentRegistry = ComponentRegistry()
        self._setup_registry()
    
    def _setup_registry(self) -> None:
        """Register all known item types."""
        self._registry.register_type("weapon", Weapon)
        self._registry.register_type("armor", Armor)
        self._registry.register_type("potion", Potion)
    
    def create_weapon(self, name: str, damage: int, durability: int = 100) -> Weapon | None:
        """Create a weapon."""
        weapon = self._registry.create("weapon", name=name, damage=damage, durability=durability)
        return weapon if isinstance(weapon, Weapon) else None
    
    def create_armor(self, name: str, defense: int, slot: str = "body") -> Armor | None:
        """Create armor."""
        armor = self._registry.create("armor", name=name, defense=defense, slot=slot)
        return armor if isinstance(armor, Armor) else None
    
    def create_potion(self, name: str, effect: str, potency: int) -> Potion | None:
        """Create a potion."""
        potion = self._registry.create("potion", name=name, effect=effect, potency=potency)
        return potion if isinstance(potion, Potion) else None
    
    def get_registry(self) -> ComponentRegistry:
        """Get the underlying registry."""
        return self._registry


class ServiceLocator:
    """Service locator pattern using component registry."""
    
    _instance: ServiceLocator | None = None
    
    def __init__(self) -> None:
        self._services: ComponentRegistry[Any] = ComponentRegistry()
    
    @classmethod
    def get_instance(cls) -> ServiceLocator:
        if cls._instance is None:
            cls._instance = ServiceLocator()
        return cls._instance
    
    def register_service(self, name: str, service: Any) -> None:
        """Register a service singleton."""
        self._services.register_singleton(name, service)
    
    def get_service(self, name: str) -> Any | None:
        """Get a registered service."""
        return self._services.get_singleton(name)
    
    def has_service(self, name: str) -> bool:
        """Check if a service is registered."""
        return self._services.get_singleton(name) is not None
