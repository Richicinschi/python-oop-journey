"""Problem 06: Game Character Actions

Topic: Complex method overriding with super() for game mechanics
Difficulty: Hard

Create a game character hierarchy where each character type has unique
attack mechanics that extend base behavior using super().

Classes to implement:
- Character: Base with name, health, attack_power, basic attack()
- Warrior: Adds rage system, special heavy attack with rage cost
- Mage: Adds mana system, spells cost mana, mana regeneration
- Archer: Adds arrow count, ranged attacks, critical hit chance

Example:
    >>> char = Character("Base", 100, 10)
    >>> char.attack()
    'Base attacks for 10 damage! [Health: 100/100]'
    >>> char.is_alive()
    True
    
    >>> warrior = Warrior("Conan", 150, 15)
    >>> warrior.attack()
    'Conan attacks for 15 damage! [Rage: 20/100, Health: 150/150]'
    >>> warrior.heavy_attack()
    'Conan HEAVY attacks for 30 damage! [Rage: 0/100, Health: 150/150]'
    
    >>> mage = Mage("Gandalf", 80, 20)
    >>> mage.cast_spell("Fireball")
    'Gandalf casts Fireball for 40 damage! [Mana: 70/100, Health: 80/80]'

Requirements:
    - Character: name, health, max_health, attack_power, attack(), take_damage()
    - Warrior: rage (0-100), rage_per_attack, heavy_attack() costs rage
    - Mage: mana (0-100), mana_costs dict, cast_spell(), regenerate_mana()
    - Archer: arrows, critical_chance, ranged_attack(), needs_ammo check
    - attack() should be overridden in all children to add resource info
    - Use super().attack() pattern in children
    - take_damage() should reduce health and return remaining health

Hints:
    Hint 1: Each child class should call super().__init__() FIRST, then set its
    own resource attributes (rage, mana, arrows). This ensures the base Character
    is properly initialized.
    
    Hint 2: For attack() overrides, use the pattern:
        base_result = super().attack()  # Get parent's attack string
        # Then add your resource info to the result
    This extends behavior instead of replacing it.
    
    Hint 3: Watch for edge cases:
    - Rage/mana should never exceed their MAX values
    - Health should never go below 0 (use max(0, ...))
    - Health should never exceed max_health when healing (use min(max_health, ...))
    - Heavy attack and spell casting need resource checks before executing
"""

from __future__ import annotations

import random


class Character:
    """Base game character class."""

    def __init__(self, name: str, health: int, attack_power: int) -> None:
        """Initialize character.
        
        Args:
            name: Character name
            health: Maximum health points
            attack_power: Base attack damage
            
        Raises:
            ValueError: If health or attack_power <= 0
        """
        raise NotImplementedError("Initialize with validation")

    def attack(self) -> str:
        """Basic attack.
        
        Returns:
            Attack message with damage and status
        """
        raise NotImplementedError("Return attack message")

    def take_damage(self, damage: int) -> int:
        """Take damage and reduce health.
        
        Args:
            damage: Amount of damage to take
            
        Returns:
            Remaining health (0 if damage would reduce below 0)
        """
        raise NotImplementedError("Reduce health, ensure not below 0")

    def heal(self, amount: int) -> int:
        """Heal character.
        
        Args:
            amount: Health points to restore
            
        Returns:
            Actual health after healing (capped at max_health)
        """
        raise NotImplementedError("Increase health, cap at max")

    def is_alive(self) -> bool:
        """Check if character is alive."""
        raise NotImplementedError("Return health > 0")

    def get_health_percent(self) -> float:
        """Get health as percentage."""
        raise NotImplementedError("Return health / max_health * 100")

    def get_status(self) -> dict[str, object]:
        """Return character status."""
        raise NotImplementedError("Return status dict")


class Warrior(Character):
    """Warrior character with rage system."""

    MAX_RAGE = 100
    RAGE_PER_ATTACK = 20
    RAGE_FOR_HEAVY = 40
    HEAVY_ATTACK_MULTIPLIER = 2

    def __init__(self, name: str, health: int, attack_power: int) -> None:
        """Initialize warrior with rage."""
        raise NotImplementedError("Use super().__init__() and add rage")

    def attack(self) -> str:
        """Attack and build rage.
        
        Format: '{name} attacks for {damage} damage! [Rage: {rage}/{max}, ...]'
        Also gains RAGE_PER_ATTACK (capped at MAX_RAGE).
        """
        raise NotImplementedError("Override with super().attack() + rage logic")

    def heavy_attack(self) -> str:
        """Powerful attack that costs rage.
        
        Requires RAGE_FOR_HEAVY rage. Consumes rage and deals double damage.
        Format: '{name} HEAVY attacks for {damage} damage! [...]'
        
        Returns:
            Attack message or error if not enough rage
        """
        raise NotImplementedError("Check rage, consume, deal heavy damage")

    def get_rage(self) -> int:
        """Get current rage."""
        raise NotImplementedError("Return rage")

    def get_status(self) -> dict[str, object]:
        """Return warrior status with rage."""
        raise NotImplementedError("Extend with super() and add rage")


class Mage(Character):
    """Mage character with mana system."""

    MAX_MANA = 100
    MANA_REGEN = 10
    BASE_SPELL_COST = 20
    SPELL_DAMAGE_MULTIPLIER = 2

    def __init__(self, name: str, health: int, attack_power: int) -> None:
        """Initialize mage with mana."""
        raise NotImplementedError("Use super().__init__() and add mana")

    def attack(self) -> str:
        """Basic staff attack.
        
        Format: '{name} attacks with staff for {damage} damage! [Mana: {...}]'
        Also regenerates MANA_REGEN mana (capped at MAX_MANA).
        """
        raise NotImplementedError("Override with super().attack() + mana regen")

    def cast_spell(self, spell_name: str) -> str:
        """Cast a spell costing mana.
        
        Args:
            spell_name: Name of the spell
            
        Cost: BASE_SPELL_COST mana
        Damage: attack_power * SPELL_DAMAGE_MULTIPLIER
        
        Returns:
            Spell cast message or error if not enough mana
        """
        raise NotImplementedError("Check mana, consume, cast spell")

    def regenerate_mana(self, amount: int | None = None) -> int:
        """Regenerate mana.
        
        Args:
            amount: Amount to regen (defaults to MANA_REGEN)
            
        Returns:
            Current mana after regeneration
        """
        raise NotImplementedError("Regenerate mana, cap at max")

    def get_mana(self) -> int:
        """Get current mana."""
        raise NotImplementedError("Return mana")

    def get_status(self) -> dict[str, object]:
        """Return mage status with mana."""
        raise NotImplementedError("Extend with super() and add mana")


class Archer(Character):
    """Archer character with arrows and critical hits."""

    DEFAULT_ARROWS = 20
    CRITICAL_CHANCE = 0.25
    CRITICAL_MULTIPLIER = 2.5

    def __init__(
        self,
        name: str,
        health: int,
        attack_power: int,
        arrows: int = 20
    ) -> None:
        """Initialize archer with arrows."""
        raise NotImplementedError("Use super().__init__() and add arrows")

    def attack(self) -> str:
        """Melee attack with dagger (when out of arrows).
        
        Format: '{name} attacks with dagger for {damage} damage! [...]'
        Half damage, no arrow used.
        """
        raise NotImplementedError("Override with super().attack()")

    def ranged_attack(self) -> str:
        """Ranged attack with bow.
        
        Uses 1 arrow. Has chance for critical hit (CRITICAL_CHANCE).
        Critical: damage * CRITICAL_MULTIPLIER
        
        Returns:
            Attack message or error if no arrows
        """
        raise NotImplementedError("Check arrows, consume, check crit")

    def reload(self, arrows: int) -> int:
        """Reload arrows.
        
        Args:
            arrows: Number of arrows to add
            
        Returns:
            Total arrows after reload
        """
        raise NotImplementedError("Add arrows to quiver")

    def get_arrows(self) -> int:
        """Get remaining arrows."""
        raise NotImplementedError("Return arrows")

    def get_status(self) -> dict[str, object]:
        """Return archer status with arrows."""
        raise NotImplementedError("Extend with super() and add arrows")
