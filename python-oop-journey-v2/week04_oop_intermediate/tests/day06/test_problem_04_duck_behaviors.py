"""Tests for Problem 04: Duck Behaviors."""

from __future__ import annotations

import pytest
from week04_oop_intermediate.solutions.day06.problem_04_duck_behaviors import (
    DecoyDuck,
    Duck,
    FlyBehavior,
    FlyNoWay,
    FlyWithRocket,
    FlyWithWings,
    MallardDuck,
    MuteQuack,
    Quack,
    QuackBehavior,
    RocketDuck,
    RubberDuck,
    Squeak,
)


class TestFlyWithWings:
    """Tests for FlyWithWings class."""

    def test_fly(self) -> None:
        fly = FlyWithWings()
        result = fly.fly()
        assert "flying" in result

    def test_is_fly_behavior(self) -> None:
        fly = FlyWithWings()
        assert isinstance(fly, FlyBehavior)


class TestFlyNoWay:
    """Tests for FlyNoWay class."""

    def test_fly(self) -> None:
        fly = FlyNoWay()
        result = fly.fly()
        assert "can't fly" in result


class TestFlyWithRocket:
    """Tests for FlyWithRocket class."""

    def test_fly(self) -> None:
        fly = FlyWithRocket()
        result = fly.fly()
        assert "rocket" in result


class TestQuack:
    """Tests for Quack class."""

    def test_quack(self) -> None:
        quack = Quack()
        result = quack.quack()
        assert result == "Quack!"

    def test_is_quack_behavior(self) -> None:
        quack = Quack()
        assert isinstance(quack, QuackBehavior)


class TestSqueak:
    """Tests for Squeak class."""

    def test_quack(self) -> None:
        squeak = Squeak()
        result = squeak.quack()
        assert result == "Squeak!"

    def test_squeak_method(self) -> None:
        squeak = Squeak()
        result = squeak.squeak()
        assert result == "Squeak!"


class TestMuteQuack:
    """Tests for MuteQuack class."""

    def test_quack(self) -> None:
        mute = MuteQuack()
        result = mute.quack()
        assert "silence" in result


class TestDuck:
    """Tests for Duck base class."""

    def test_perform_fly(self) -> None:
        duck = Duck("Test", FlyWithWings(), Quack())
        result = duck.perform_fly()
        assert "flying" in result

    def test_perform_quack(self) -> None:
        duck = Duck("Test", FlyWithWings(), Quack())
        result = duck.perform_quack()
        assert result == "Quack!"

    def test_swim(self) -> None:
        duck = Duck("Test", FlyWithWings(), Quack())
        result = duck.swim()
        assert "float" in result

    def test_set_fly_behavior(self) -> None:
        duck = Duck("Test", FlyNoWay(), Quack())
        duck.set_fly_behavior(FlyWithRocket())
        result = duck.perform_fly()
        assert "rocket" in result

    def test_set_quack_behavior(self) -> None:
        duck = Duck("Test", FlyWithWings(), Quack())
        duck.set_quack_behavior(Squeak())
        result = duck.perform_quack()
        assert "Squeak" in result

    def test_get_info(self) -> None:
        duck = Duck("Test", FlyWithWings(), Quack())
        info = duck.get_info()
        assert info["name"] == "Test"
        assert "FlyWithWings" in info["fly_behavior"]


class TestMallardDuck:
    """Tests for MallardDuck class."""

    def test_display(self) -> None:
        duck = MallardDuck("Mallory")
        result = duck.display()
        assert "real Mallard" in result

    def test_default_behaviors(self) -> None:
        duck = MallardDuck("Mallory")
        assert "flying" in duck.perform_fly()
        assert duck.perform_quack() == "Quack!"


class TestRubberDuck:
    """Tests for RubberDuck class."""

    def test_display(self) -> None:
        duck = RubberDuck("Rubby")
        result = duck.display()
        assert "rubber duck toy" in result

    def test_default_behaviors(self) -> None:
        duck = RubberDuck("Rubby")
        assert "can't fly" in duck.perform_fly()
        assert "Squeak" in duck.perform_quack()


class TestDecoyDuck:
    """Tests for DecoyDuck class."""

    def test_display(self) -> None:
        duck = DecoyDuck("Woody")
        result = duck.display()
        assert "decoy" in result

    def test_default_behaviors(self) -> None:
        duck = DecoyDuck("Woody")
        assert "can't fly" in duck.perform_fly()
        assert "silence" in duck.perform_quack()


class TestRocketDuck:
    """Tests for RocketDuck class."""

    def test_display(self) -> None:
        duck = RocketDuck("Rocket")
        result = duck.display()
        assert "rocket-powered" in result

    def test_default_behaviors(self) -> None:
        duck = RocketDuck("Rocket")
        assert "rocket" in duck.perform_fly()
        assert duck.perform_quack() == "Quack!"

    def test_runtime_behavior_change(self) -> None:
        """Test changing behavior at runtime."""
        duck = RocketDuck("Rocket")
        
        # Change to no fly
        duck.set_fly_behavior(FlyNoWay())
        assert "can't fly" in duck.perform_fly()
        
        # Change back to wings
        duck.set_fly_behavior(FlyWithWings())
        assert "flying" in duck.perform_fly()

    def test_composition_differentiation(self) -> None:
        """Test that different ducks have different composed behaviors."""
        ducks = [
            MallardDuck("M1"),
            RubberDuck("R1"),
            DecoyDuck("D1"),
            RocketDuck("R2"),
        ]
        
        fly_results = [d.perform_fly() for d in ducks]
        quack_results = [d.perform_quack() for d in ducks]
        
        # Should have 3 unique fly behaviors (2 ducks don't fly)
        assert len(set(fly_results)) == 3
        # Should have 3 unique quack behaviors (2 ducks quack normally)
        assert len(set(quack_results)) == 3
