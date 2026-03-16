"""Reference solution for Problem 06: Game Character Actions."""

from __future__ import annotations

import random


class Character:
    """Base game character class."""

    def __init__(self, name: str, health: int, attack_power: int) -> None:
        """Initialize character."""
        if health <= 0:
            raise ValueError("Health must be positive")
        if attack_power <= 0:
            raise ValueError("Attack power must be positive")
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power

    def attack(self) -> str:
        """Basic attack."""
        return f"{self.name} attacks for {self.attack_power} damage! [Health: {self.health}/{self.max_health}]"

    def take_damage(self, damage: int) -> int:
        """Take damage and reduce health."""
        self.health = max(0, self.health - damage)
        return self.health

    def heal(self, amount: int) -> int:
        """Heal character."""
        self.health = min(self.max_health, self.health + amount)
        return self.health

    def is_alive(self) -> bool:
        """Check if character is alive."""
        return self.health > 0

    def get_health_percent(self) -> float:
        """Get health as percentage."""
        return (self.health / self.max_health) * 100

    def get_status(self) -> dict[str, object]:
        """Return character status."""
        return {
            "name": self.name,
            "health": self.health,
            "max_health": self.max_health,
            "attack_power": self.attack_power,
            "alive": self.is_alive(),
        }


class Warrior(Character):
    """Warrior character with rage system."""

    MAX_RAGE = 100
    RAGE_PER_ATTACK = 20
    RAGE_FOR_HEAVY = 40
    HEAVY_ATTACK_MULTIPLIER = 2

    def __init__(self, name: str, health: int, attack_power: int) -> None:
        """Initialize warrior with rage."""
        super().__init__(name, health, attack_power)
        self.rage = 0

    def attack(self) -> str:
        """Attack and build rage."""
        base = super().attack()
        self.rage = min(self.MAX_RAGE, self.rage + self.RAGE_PER_ATTACK)
        base_part = base.replace(
            f"[Health: {self.health}/{self.max_health}]",
            ""
        ).strip()
        return f"{base_part} [Rage: {self.rage}/{self.MAX_RAGE}, Health: {self.health}/{self.max_health}]"

    def heavy_attack(self) -> str:
        """Powerful attack that costs rage."""
        if self.rage < self.RAGE_FOR_HEAVY:
            return f"{self.name} tries heavy attack but needs {self.RAGE_FOR_HEAVY} rage! [Rage: {self.rage}/{self.MAX_RAGE}]"
        
        self.rage -= self.RAGE_FOR_HEAVY
        damage = self.attack_power * self.HEAVY_ATTACK_MULTIPLIER
        return f"{self.name} HEAVY attacks for {damage} damage! [Rage: {self.rage}/{self.MAX_RAGE}, Health: {self.health}/{self.max_health}]"

    def get_rage(self) -> int:
        """Get current rage."""
        return self.rage

    def get_status(self) -> dict[str, object]:
        """Return warrior status with rage."""
        details = super().get_status()
        details.update({
            "rage": self.rage,
            "max_rage": self.MAX_RAGE,
            "character_type": "warrior",
        })
        return details


class Mage(Character):
    """Mage character with mana system."""

    MAX_MANA = 100
    MANA_REGEN = 10
    BASE_SPELL_COST = 20
    SPELL_DAMAGE_MULTIPLIER = 2

    def __init__(self, name: str, health: int, attack_power: int) -> None:
        """Initialize mage with mana."""
        super().__init__(name, health, attack_power)
        self.mana = self.MAX_MANA

    def attack(self) -> str:
        """Basic staff attack."""
        base = super().attack()
        self.mana = min(self.MAX_MANA, self.mana + self.MANA_REGEN)
        base_part = base.replace(
            f"[Health: {self.health}/{self.max_health}]",
            ""
        ).strip()
        return f"{base_part.replace('attacks', 'attacks with staff')} [Mana: {self.mana}/{self.MAX_MANA}, Health: {self.health}/{self.max_health}]"

    def cast_spell(self, spell_name: str) -> str:
        """Cast a spell costing mana."""
        if self.mana < self.BASE_SPELL_COST:
            return f"{self.name} cannot cast {spell_name} - not enough mana! [Mana: {self.mana}/{self.MAX_MANA}]"
        
        self.mana -= self.BASE_SPELL_COST
        damage = self.attack_power * self.SPELL_DAMAGE_MULTIPLIER
        return f"{self.name} casts {spell_name} for {damage} damage! [Mana: {self.mana}/{self.MAX_MANA}, Health: {self.health}/{self.max_health}]"

    def regenerate_mana(self, amount: int | None = None) -> int:
        """Regenerate mana."""
        if amount is None:
            amount = self.MANA_REGEN
        self.mana = min(self.MAX_MANA, self.mana + amount)
        return self.mana

    def get_mana(self) -> int:
        """Get current mana."""
        return self.mana

    def get_status(self) -> dict[str, object]:
        """Return mage status with mana."""
        details = super().get_status()
        details.update({
            "mana": self.mana,
            "max_mana": self.MAX_MANA,
            "character_type": "mage",
        })
        return details


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
        super().__init__(name, health, attack_power)
        self.arrows = arrows

    def attack(self) -> str:
        """Melee attack with dagger (when out of arrows)."""
        base = super().attack()
        damage = self.attack_power // 2
        return f"{self.name} attacks with dagger for {damage} damage! [Arrows: {self.arrows}, Health: {self.health}/{self.max_health}]"

    def ranged_attack(self) -> str:
        """Ranged attack with bow."""
        if self.arrows <= 0:
            return f"{self.name} has no arrows! Switch to melee. [Arrows: {self.arrows}]"
        
        self.arrows -= 1
        
        is_critical = random.random() < self.CRITICAL_CHANCE
        if is_critical:
            damage = int(self.attack_power * self.CRITICAL_MULTIPLIER)
            return f"{self.name} CRITICAL shot for {damage} damage! [Arrows: {self.arrows}, Health: {self.health}/{self.max_health}]"
        else:
            return f"{self.name} shoots for {self.attack_power} damage! [Arrows: {self.arrows}, Health: {self.health}/{self.max_health}]"

    def reload(self, arrows: int) -> int:
        """Reload arrows."""
        self.arrows += arrows
        return self.arrows

    def get_arrows(self) -> int:
        """Get remaining arrows."""
        return self.arrows

    def get_status(self) -> dict[str, object]:
        """Return archer status with arrows."""
        details = super().get_status()
        details.update({
            "arrows": self.arrows,
            "critical_chance": self.CRITICAL_CHANCE,
            "character_type": "archer",
        })
        return details
