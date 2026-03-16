"""Tests for Problem 06: Game Character Actions."""

from __future__ import annotations

import random

import pytest

from week04_oop_intermediate.solutions.day02.problem_06_game_character_actions import (
    Archer,
    Character,
    Mage,
    Warrior,
)


class TestCharacter:
    """Tests for Character base class."""

    def test_init_sets_attributes(self) -> None:
        """Test that attributes are set correctly."""
        char = Character("Hero", 100, 10)
        assert char.name == "Hero"
        assert char.health == 100
        assert char.max_health == 100
        assert char.attack_power == 10

    def test_init_validates_health(self) -> None:
        """Test that non-positive health raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            Character("Hero", 0, 10)

    def test_init_validates_attack_power(self) -> None:
        """Test that non-positive attack_power raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            Character("Hero", 100, 0)

    def test_attack_returns_expected_string(self) -> None:
        """Test attack() returns correct format."""
        char = Character("Hero", 100, 10)
        result = char.attack()
        assert "Hero attacks for 10 damage!" in result

    def test_take_damage_reduces_health(self) -> None:
        """Test take_damage() reduces health."""
        char = Character("Hero", 100, 10)
        remaining = char.take_damage(30)
        assert remaining == 70
        assert char.health == 70

    def test_take_damage_does_not_go_below_zero(self) -> None:
        """Test take_damage() doesn't reduce health below 0."""
        char = Character("Hero", 100, 10)
        remaining = char.take_damage(150)
        assert remaining == 0
        assert char.health == 0

    def test_heal_increases_health(self) -> None:
        """Test heal() increases health."""
        char = Character("Hero", 100, 10)
        char.take_damage(50)
        result = char.heal(30)
        assert result == 80
        assert char.health == 80

    def test_heal_caps_at_max(self) -> None:
        """Test heal() doesn't exceed max_health."""
        char = Character("Hero", 100, 10)
        char.take_damage(10)
        result = char.heal(100)
        assert result == 100
        assert char.health == 100

    def test_is_alive_returns_true_when_health_positive(self) -> None:
        """Test is_alive() returns True when health > 0."""
        char = Character("Hero", 100, 10)
        assert char.is_alive() is True

    def test_is_alive_returns_false_when_health_zero(self) -> None:
        """Test is_alive() returns False when health is 0."""
        char = Character("Hero", 100, 10)
        char.take_damage(100)
        assert char.is_alive() is False

    def test_get_health_percent_returns_percentage(self) -> None:
        """Test get_health_percent() returns correct percentage."""
        char = Character("Hero", 100, 10)
        char.take_damage(25)
        assert char.get_health_percent() == 75.0

    def test_get_status_returns_dict(self) -> None:
        """Test get_status() returns expected dict."""
        char = Character("Hero", 100, 10)
        status = char.get_status()
        assert status["name"] == "Hero"
        assert status["health"] == 100
        assert status["max_health"] == 100
        assert status["attack_power"] == 10
        assert status["alive"] is True


class TestWarrior:
    """Tests for Warrior class."""

    def test_max_rage_constant(self) -> None:
        """Test MAX_RAGE is 100."""
        assert Warrior.MAX_RAGE == 100

    def test_init_sets_rage_to_zero(self) -> None:
        """Test warrior starts with 0 rage."""
        warrior = Warrior("Conan", 150, 15)
        assert warrior.rage == 0

    def test_attack_builds_rage(self) -> None:
        """Test attack() builds rage."""
        warrior = Warrior("Conan", 150, 15)
        warrior.attack()
        assert warrior.rage == Warrior.RAGE_PER_ATTACK

    def test_attack_caps_rage_at_max(self) -> None:
        """Test rage doesn't exceed MAX_RAGE."""
        warrior = Warrior("Conan", 150, 15)
        for _ in range(10):
            warrior.attack()
        assert warrior.rage == Warrior.MAX_RAGE

    def test_attack_includes_rage_in_message(self) -> None:
        """Test attack() message includes rage info."""
        warrior = Warrior("Conan", 150, 15)
        result = warrior.attack()
        assert "Rage:" in result
        assert "20/100" in result

    def test_heavy_attack_requires_rage(self) -> None:
        """Test heavy_attack() requires sufficient rage."""
        warrior = Warrior("Conan", 150, 15)
        result = warrior.heavy_attack()
        assert "needs 40 rage" in result

    def test_heavy_attack_consumes_rage(self) -> None:
        """Test heavy_attack() consumes rage and deals double damage."""
        warrior = Warrior("Conan", 150, 15)
        # Build enough rage with 2 attacks
        warrior.attack()
        warrior.attack()
        assert warrior.rage >= Warrior.RAGE_FOR_HEAVY
        result = warrior.heavy_attack()
        assert warrior.rage == 0
        assert "HEAVY attacks for 30 damage" in result

    def test_get_rage_returns_rage(self) -> None:
        """Test get_rage() returns current rage."""
        warrior = Warrior("Conan", 150, 15)
        warrior.attack()
        assert warrior.get_rage() == 20

    def test_get_status_extends_parent(self) -> None:
        """Test get_status() extends parent's dict."""
        warrior = Warrior("Conan", 150, 15)
        status = warrior.get_status()
        assert status["rage"] == 0
        assert status["max_rage"] == 100
        assert status["character_type"] == "warrior"

    def test_inheritance_from_character(self) -> None:
        """Test that Warrior inherits from Character."""
        assert issubclass(Warrior, Character)


class TestMage:
    """Tests for Mage class."""

    def test_max_mana_constant(self) -> None:
        """Test MAX_MANA is 100."""
        assert Mage.MAX_MANA == 100

    def test_init_sets_mana_to_max(self) -> None:
        """Test mage starts with full mana."""
        mage = Mage("Gandalf", 80, 20)
        assert mage.mana == Mage.MAX_MANA

    def test_attack_regenerates_mana(self) -> None:
        """Test attack() regenerates mana."""
        mage = Mage("Gandalf", 80, 20)
        mage.mana = 50
        mage.attack()
        assert mage.mana == 60  # 50 + 10 regen

    def test_attack_caps_mana_at_max(self) -> None:
        """Test mana regeneration doesn't exceed MAX_MANA."""
        mage = Mage("Gandalf", 80, 20)
        mage.mana = 95
        mage.attack()
        assert mage.mana == Mage.MAX_MANA

    def test_attack_mentions_staff(self) -> None:
        """Test attack() mentions staff attack."""
        mage = Mage("Gandalf", 80, 20)
        result = mage.attack()
        assert "attacks with staff" in result

    def test_cast_spell_requires_mana(self) -> None:
        """Test cast_spell() requires sufficient mana."""
        mage = Mage("Gandalf", 80, 20)
        mage.mana = 10
        result = mage.cast_spell("Fireball")
        assert "not enough mana" in result

    def test_cast_spell_consumes_mana(self) -> None:
        """Test cast_spell() consumes mana and deals double damage."""
        mage = Mage("Gandalf", 80, 20)
        result = mage.cast_spell("Fireball")
        assert mage.mana == 80  # 100 - 20 cost
        assert "casts Fireball for 40 damage" in result

    def test_regenerate_mana_adds_amount(self) -> None:
        """Test regenerate_mana() adds specified amount."""
        mage = Mage("Gandalf", 80, 20)
        mage.mana = 50
        result = mage.regenerate_mana(25)
        assert result == 75
        assert mage.mana == 75

    def test_regenerate_mana_uses_default(self) -> None:
        """Test regenerate_mana() uses default amount."""
        mage = Mage("Gandalf", 80, 20)
        mage.mana = 50
        result = mage.regenerate_mana()
        assert result == 60  # 50 + 10 default

    def test_get_mana_returns_mana(self) -> None:
        """Test get_mana() returns current mana."""
        mage = Mage("Gandalf", 80, 20)
        assert mage.get_mana() == 100

    def test_get_status_extends_parent(self) -> None:
        """Test get_status() extends parent's dict."""
        mage = Mage("Gandalf", 80, 20)
        status = mage.get_status()
        assert status["mana"] == 100
        assert status["max_mana"] == 100
        assert status["character_type"] == "mage"

    def test_inheritance_from_character(self) -> None:
        """Test that Mage inherits from Character."""
        assert issubclass(Mage, Character)


class TestArcher:
    """Tests for Archer class."""

    def test_default_arrows_constant(self) -> None:
        """Test DEFAULT_ARROWS is 20."""
        assert Archer.DEFAULT_ARROWS == 20

    def test_init_sets_arrows(self) -> None:
        """Test archer is initialized with arrows."""
        archer = Archer("Legolas", 90, 12)
        assert archer.arrows == 20

    def test_init_accepts_custom_arrows(self) -> None:
        """Test archer accepts custom arrow count."""
        archer = Archer("Legolas", 90, 12, arrows=50)
        assert archer.arrows == 50

    def test_attack_uses_dagger(self) -> None:
        """Test attack() uses dagger with half damage."""
        archer = Archer("Legolas", 90, 12)
        result = archer.attack()
        assert "dagger for 6 damage" in result  # 12 / 2 = 6

    def test_ranged_attack_consumes_arrow(self) -> None:
        """Test ranged_attack() consumes an arrow."""
        archer = Archer("Legolas", 90, 12)
        initial_arrows = archer.arrows
        archer.ranged_attack()
        assert archer.arrows == initial_arrows - 1

    def test_ranged_attack_no_arrows(self) -> None:
        """Test ranged_attack() when out of arrows."""
        archer = Archer("Legolas", 90, 12, arrows=0)
        result = archer.ranged_attack()
        assert "no arrows" in result

    def test_ranged_attack_with_forced_critical(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test ranged_attack() with forced critical hit."""
        archer = Archer("Legolas", 90, 12)
        # Force critical hit by mocking random.random()
        monkeypatch.setattr(random, "random", lambda: 0.1)  # Below CRITICAL_CHANCE
        result = archer.ranged_attack()
        assert "CRITICAL" in result
        assert "30 damage" in result  # 12 * 2.5 = 30

    def test_ranged_attack_normal_hit(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test ranged_attack() with forced normal hit."""
        archer = Archer("Legolas", 90, 12)
        # Force normal hit by mocking random.random()
        monkeypatch.setattr(random, "random", lambda: 0.5)  # Above CRITICAL_CHANCE
        result = archer.ranged_attack()
        assert "shoots for 12 damage" in result
        assert "CRITICAL" not in result

    def test_reload_adds_arrows(self) -> None:
        """Test reload() adds arrows."""
        archer = Archer("Legolas", 90, 12, arrows=5)
        result = archer.reload(10)
        assert result == 15
        assert archer.arrows == 15

    def test_get_arrows_returns_arrows(self) -> None:
        """Test get_arrows() returns arrow count."""
        archer = Archer("Legolas", 90, 12, arrows=30)
        assert archer.get_arrows() == 30

    def test_get_status_extends_parent(self) -> None:
        """Test get_status() extends parent's dict."""
        archer = Archer("Legolas", 90, 12)
        status = archer.get_status()
        assert status["arrows"] == 20
        assert status["critical_chance"] == 0.25
        assert status["character_type"] == "archer"

    def test_inheritance_from_character(self) -> None:
        """Test that Archer inherits from Character."""
        assert issubclass(Archer, Character)
