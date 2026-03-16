"""Problem 04: Duck Behaviors

Topic: Composition vs Inheritance
Difficulty: Easy

Classic example inspired by "Head First Design Patterns":
Duck behaviors implemented through composition rather than inheritance.

Classes to implement:
- FlyBehavior (fly interface)
- FlyWithWings, FlyNoWay, FlyWithRocket
- QuackBehavior (quack interface)
- Quack, Squeak, MuteQuack
- Duck (composes behaviors)
- MallardDuck, RubberDuck, DecoyDuck, RocketDuck

This demonstrates how composition allows runtime behavior changes
and eliminates code duplication from inheritance hierarchies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class FlyBehavior(ABC):
    """Interface for flying behavior."""

    @abstractmethod
    def fly(self) -> str:
        """Perform fly action, return description."""
        raise NotImplementedError("Implement fly")


class FlyWithWings(FlyBehavior):
    """Normal flying behavior."""

    def fly(self) -> str:
        raise NotImplementedError("Implement fly")


class FlyNoWay(FlyBehavior):
    """Cannot fly."""

    def fly(self) -> str:
        raise NotImplementedError("Implement fly")


class FlyWithRocket(FlyBehavior):
    """Rocket-powered flying."""

    def fly(self) -> str:
        raise NotImplementedError("Implement fly")


class QuackBehavior(ABC):
    """Interface for quacking behavior."""

    @abstractmethod
    def quack(self) -> str:
        """Perform quack action, return description."""
        raise NotImplementedError("Implement quack")


class Quack(QuackBehavior):
    """Normal quacking."""

    def quack(self) -> str:
        raise NotImplementedError("Implement quack")


class Squeak(QuackBehavior):
    """Squeaking instead of quacking."""

    def squeak(self) -> str:
        raise NotImplementedError("Implement squeak")

    def quack(self) -> str:
        """Delegate to squeak for uniform interface."""
        raise NotImplementedError("Implement quack")


class MuteQuack(QuackBehavior):
    """Silence."""

    def quack(self) -> str:
        raise NotImplementedError("Implement quack")


class Duck:
    """Base duck class using composition for behaviors.
    
    Instead of inheriting flying/quacking behaviors, this class
    composes them. This allows:
    - Changing behavior at runtime
    - Sharing behaviors between unrelated duck types
    - Adding new behaviors without modifying ducks
    """

    def __init__(
        self,
        name: str,
        fly_behavior: FlyBehavior,
        quack_behavior: QuackBehavior,
    ) -> None:
        raise NotImplementedError("Implement __init__")

    def perform_fly(self) -> str:
        """Delegate to fly behavior."""
        raise NotImplementedError("Implement perform_fly")

    def perform_quack(self) -> str:
        """Delegate to quack behavior."""
        raise NotImplementedError("Implement perform_quack")

    def swim(self) -> str:
        """All ducks swim the same way."""
        raise NotImplementedError("Implement swim")

    def display(self) -> str:
        """Return duck description."""
        raise NotImplementedError("Implement display")

    def set_fly_behavior(self, fly_behavior: FlyBehavior) -> None:
        """Change fly behavior at runtime."""
        raise NotImplementedError("Implement set_fly_behavior")

    def set_quack_behavior(self, quack_behavior: QuackBehavior) -> None:
        """Change quack behavior at runtime."""
        raise NotImplementedError("Implement set_quack_behavior")

    def get_info(self) -> dict[str, Any]:
        raise NotImplementedError("Implement get_info")


class MallardDuck(Duck):
    """Real mallard duck."""

    def __init__(self, name: str) -> None:
        raise NotImplementedError("Implement __init__")

    def display(self) -> str:
        raise NotImplementedError("Implement display")


class RubberDuck(Duck):
    """Rubber duck toy."""

    def __init__(self, name: str) -> None:
        raise NotImplementedError("Implement __init__")

    def display(self) -> str:
        raise NotImplementedError("Implement display")


class DecoyDuck(Duck):
    """Wooden decoy duck."""

    def __init__(self, name: str) -> None:
        raise NotImplementedError("Implement __init__")

    def display(self) -> str:
        raise NotImplementedError("Implement display")


class RocketDuck(Duck):
    """Duck with rocket pack."""

    def __init__(self, name: str) -> None:
        raise NotImplementedError("Implement __init__")

    def display(self) -> str:
        raise NotImplementedError("Implement display")
