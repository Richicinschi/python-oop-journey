"""Tests for Problem 04: Component Registry."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day06.problem_04_component_registry import (
    ComponentRegistry,
    Weapon,
    Armor,
    Potion,
    ItemFactory,
    ServiceLocator,
)


class TestComponentRegistry:
    """Test component registry functionality."""
    
    def test_register_type(self) -> None:
        registry = ComponentRegistry()
        
        registry.register_type("weapon", Weapon)
        
        assert "weapon" in registry.get_registered_types()
    
    def test_create_instance(self) -> None:
        registry = ComponentRegistry()
        registry.register_type("weapon", Weapon)
        
        instance = registry.create("weapon", name="Sword", damage=10)
        
        assert instance is not None
        assert isinstance(instance, Weapon)
        assert instance.name == "Sword"
        assert instance.damage == 10
    
    def test_create_unknown_type(self) -> None:
        registry = ComponentRegistry()
        
        instance = registry.create("unknown", name="test")
        
        assert instance is None
    
    def test_register_singleton(self) -> None:
        registry = ComponentRegistry()
        weapon = Weapon("Excalibur", 100)
        
        registry.register_singleton("legendary_weapon", weapon)
        
        assert registry.get_singleton("legendary_weapon") is weapon
    
    def test_get_unknown_singleton(self) -> None:
        registry = ComponentRegistry()
        
        result = registry.get_singleton("unknown")
        
        assert result is None
    
    def test_is_registered_type(self) -> None:
        registry = ComponentRegistry()
        registry.register_type("weapon", Weapon)
        
        assert registry.is_registered("weapon") is True
    
    def test_is_registered_singleton(self) -> None:
        registry = ComponentRegistry()
        registry.register_singleton("service", object())
        
        assert registry.is_registered("service") is True
    
    def test_is_not_registered(self) -> None:
        registry = ComponentRegistry()
        
        assert registry.is_registered("unknown") is False
    
    def test_get_registered_types(self) -> None:
        registry = ComponentRegistry()
        registry.register_type("weapon", Weapon)
        registry.register_type("armor", Armor)
        
        types = registry.get_registered_types()
        
        assert sorted(types) == ["armor", "weapon"]
    
    def test_get_singleton_names(self) -> None:
        registry = ComponentRegistry()
        registry.register_singleton("svc1", object())
        registry.register_singleton("svc2", object())
        
        names = registry.get_singleton_names()
        
        assert sorted(names) == ["svc1", "svc2"]
    
    def test_unregister_type(self) -> None:
        registry = ComponentRegistry()
        registry.register_type("weapon", Weapon)
        
        result = registry.unregister("weapon")
        
        assert result is True
        assert "weapon" not in registry.get_registered_types()
    
    def test_unregister_singleton(self) -> None:
        registry = ComponentRegistry()
        registry.register_singleton("service", object())
        
        result = registry.unregister("service")
        
        assert result is True
        assert registry.get_singleton("service") is None
    
    def test_unregister_unknown(self) -> None:
        registry = ComponentRegistry()
        
        result = registry.unregister("unknown")
        
        assert result is False
    
    def test_clear(self) -> None:
        registry = ComponentRegistry()
        registry.register_type("weapon", Weapon)
        registry.register_singleton("service", object())
        
        registry.clear()
        
        assert registry.get_registered_types() == []
        assert registry.get_singleton_names() == []
    
    def test_creation_count(self) -> None:
        registry = ComponentRegistry()
        registry.register_type("weapon", Weapon)
        
        registry.create("weapon", name="Sword", damage=10)
        registry.create("weapon", name="Axe", damage=15)
        
        assert registry.get_creation_count("weapon") == 2


class TestLifecycleHooks:
    """Test lifecycle hooks."""
    
    def test_on_register_called(self) -> None:
        # Reset class state
        Weapon._registered = False
        
        registry = ComponentRegistry()
        registry.register_type("weapon", Weapon)
        
        assert Weapon.is_registered() is True
    
    def test_on_create_called(self) -> None:
        # Reset class state
        Weapon._created_count = 0
        
        registry = ComponentRegistry()
        registry.register_type("weapon", Weapon)
        
        registry.create("weapon", name="Sword", damage=10)
        registry.create("weapon", name="Axe", damage=15)
        
        assert Weapon.get_created_count() == 2


class TestWeapon:
    """Test weapon component."""
    
    def test_initial_state(self) -> None:
        weapon = Weapon("Sword", 10, durability=50)
        
        assert weapon.name == "Sword"
        assert weapon.damage == 10
        assert weapon.durability == 50
    
    def test_use_reduces_durability(self) -> None:
        weapon = Weapon("Sword", 10, durability=5)
        
        weapon.use()
        
        assert weapon.durability == 4
    
    def test_use_when_broken(self) -> None:
        weapon = Weapon("Broken Sword", 10, durability=0)
        
        result = weapon.use()
        
        assert "broken" in result


class TestArmor:
    """Test armor component."""
    
    def test_initial_state(self) -> None:
        armor = Armor("Plate", 20, slot="chest")
        
        assert armor.name == "Plate"
        assert armor.defense == 20
        assert armor.slot == "chest"
        assert armor.equipped is False
    
    def test_equip(self) -> None:
        armor = Armor("Plate", 20)
        
        result = armor.equip()
        
        assert armor.equipped is True
        assert "Equipped" in result
    
    def test_unequip(self) -> None:
        armor = Armor("Plate", 20)
        armor.equip()
        
        result = armor.unequip()
        
        assert armor.equipped is False
        assert "Unequipped" in result


class TestPotion:
    """Test potion component."""
    
    def test_initial_state(self) -> None:
        potion = Potion("Health Potion", "healing", 50)
        
        assert potion.name == "Health Potion"
        assert potion.effect == "healing"
        assert potion.potency == 50
        assert potion.consumed is False
    
    def test_drink(self) -> None:
        potion = Potion("Health Potion", "healing", 50)
        
        result = potion.drink()
        
        assert potion.consumed is True
        assert "Drank" in result
        assert "healing +50" in result
    
    def test_drink_when_empty(self) -> None:
        potion = Potion("Health Potion", "healing", 50)
        potion.drink()
        
        result = potion.drink()
        
        assert "empty" in result


class TestItemFactory:
    """Test item factory."""
    
    def test_create_weapon(self) -> None:
        factory = ItemFactory()
        
        weapon = factory.create_weapon("Sword", 10, 100)
        
        assert weapon is not None
        assert isinstance(weapon, Weapon)
        assert weapon.name == "Sword"
    
    def test_create_armor(self) -> None:
        factory = ItemFactory()
        
        armor = factory.create_armor("Plate", 20, "chest")
        
        assert armor is not None
        assert isinstance(armor, Armor)
        assert armor.name == "Plate"
    
    def test_create_potion(self) -> None:
        factory = ItemFactory()
        
        potion = factory.create_potion("Health", "healing", 50)
        
        assert potion is not None
        assert isinstance(potion, Potion)
        assert potion.name == "Health"
    
    def test_registry_accessible(self) -> None:
        factory = ItemFactory()
        
        registry = factory.get_registry()
        
        assert "weapon" in registry.get_registered_types()
        assert "armor" in registry.get_registered_types()
        assert "potion" in registry.get_registered_types()


class TestServiceLocator:
    """Test service locator."""
    
    def test_singleton_instance(self) -> None:
        locator1 = ServiceLocator.get_instance()
        locator2 = ServiceLocator.get_instance()
        
        assert locator1 is locator2
    
    def test_register_and_get_service(self) -> None:
        locator = ServiceLocator()
        service = {"name": "test"}
        
        locator.register_service("test_service", service)
        result = locator.get_service("test_service")
        
        assert result is service
    
    def test_has_service(self) -> None:
        locator = ServiceLocator()
        locator.register_service("svc", object())
        
        assert locator.has_service("svc") is True
        assert locator.has_service("unknown") is False
    
    def test_get_unknown_service(self) -> None:
        locator = ServiceLocator()
        
        result = locator.get_service("unknown")
        
        assert result is None


class TestIntegration:
    """Integration tests."""
    
    def test_full_item_system(self) -> None:
        """Test complete item creation system."""
        factory = ItemFactory()
        
        # Create various items
        sword = factory.create_weapon("Longsword", damage=15, durability=100)
        shield = factory.create_armor("Shield", defense=10, slot="offhand")
        potion = factory.create_potion("Mana", "mana_restore", 30)
        
        # Use items
        assert sword is not None
        assert "15 damage" in sword.use()
        
        assert shield is not None
        assert "Equipped" in shield.equip()
        
        assert potion is not None
        assert "mana_restore" in potion.drink()
    
    def test_registry_with_singletons_and_types(self) -> None:
        """Test registry managing both types and singletons."""
        registry = ComponentRegistry()
        
        # Register types
        registry.register_type("weapon", Weapon)
        registry.register_type("armor", Armor)
        
        # Register singletons
        registry.register_singleton("default_weapon", Weapon("Stick", 1))
        registry.register_singleton("default_armor", Armor("Rags", 0))
        
        # Create instances
        sword = registry.create("weapon", name="Sword", damage=10)
        default = registry.get_singleton("default_weapon")
        
        assert sword is not None
        assert default is not None
        assert sword.name == "Sword"
        assert default.name == "Stick"
