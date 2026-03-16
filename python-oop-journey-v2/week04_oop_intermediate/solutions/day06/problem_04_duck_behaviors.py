"""Reference solution for Problem 04: Duck Behaviors."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class FlyBehavior(ABC):
    """Interface for flying behavior."""

    @abstractmethod
    def fly(self) -> str:
        pass


class FlyWithWings(FlyBehavior):
    """Normal flying behavior."""

    def fly(self) -> str:
        return "I'm flying with my wings!"


class FlyNoWay(FlyBehavior):
    """Cannot fly."""

    def fly(self) -> str:
        return "I can't fly."


class FlyWithRocket(FlyBehavior):
    """Rocket-powered flying."""

    def fly(self) -> str:
        return "I'm flying with a rocket!"


class QuackBehavior(ABC):
    """Interface for quacking behavior."""

    @abstractmethod
    def quack(self) -> str:
        pass


class Quack(QuackBehavior):
    """Normal quacking."""

    def quack(self) -> str:
        return "Quack!"


class Squeak(QuackBehavior):
    """Squeaking instead of quacking."""

    def squeak(self) -> str:
        return "Squeak!"

    def quack(self) -> str:
        return self.squeak()


class MuteQuack(QuackBehavior):
    """Silence."""

    def quack(self) -> str:
        return "<< silence >>"


class Duck:
    """Base duck class using composition for behaviors."""

    def __init__(
        self,
        name: str,
        fly_behavior: FlyBehavior,
        quack_behavior: QuackBehavior,
    ) -> None:
        self.name = name
        self._fly_behavior = fly_behavior
        self._quack_behavior = quack_behavior

    def perform_fly(self) -> str:
        return self._fly_behavior.fly()

    def perform_quack(self) -> str:
        return self._quack_behavior.quack()

    def swim(self) -> str:
        return "All ducks float, even decoys!"

    def display(self) -> str:
        return f"I'm {self.name}, a generic duck"

    def set_fly_behavior(self, fly_behavior: FlyBehavior) -> None:
        self._fly_behavior = fly_behavior

    def set_quack_behavior(self, quack_behavior: QuackBehavior) -> None:
        self._quack_behavior = quack_behavior

    def get_info(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "fly_behavior": type(self._fly_behavior).__name__,
            "quack_behavior": type(self._quack_behavior).__name__,
        }


class MallardDuck(Duck):
    """Real mallard duck."""

    def __init__(self, name: str) -> None:
        super().__init__(name, FlyWithWings(), Quack())

    def display(self) -> str:
        return f"I'm {self.name}, a real Mallard duck"


class RubberDuck(Duck):
    """Rubber duck toy."""

    def __init__(self, name: str) -> None:
        super().__init__(name, FlyNoWay(), Squeak())

    def display(self) -> str:
        return f"I'm {self.name}, a rubber duck toy"


class DecoyDuck(Duck):
    """Wooden decoy duck."""

    def __init__(self, name: str) -> None:
        super().__init__(name, FlyNoWay(), MuteQuack())

    def display(self) -> str:
        return f"I'm {self.name}, a wooden decoy"


class RocketDuck(Duck):
    """Duck with rocket pack."""

    def __init__(self, name: str) -> None:
        super().__init__(name, FlyWithRocket(), Quack())

    def display(self) -> str:
        return f"I'm {self.name}, a rocket-powered duck!"
