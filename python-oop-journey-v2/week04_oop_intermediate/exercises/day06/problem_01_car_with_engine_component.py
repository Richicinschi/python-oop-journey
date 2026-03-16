"""Problem 01: Car with Engine Component

Topic: Composition vs Inheritance
Difficulty: Medium

Refactor a car class hierarchy to use composition instead of inheritance.
The engine behavior should be extracted into separate component classes.

Classes to implement:
- Engine (base component with start(), stop(), get_power())
- GasolineEngine (displacement, cylinders)
- ElectricEngine (kwh_capacity, motor_type)
- HybridEngine (combines both)
- Car (uses composition to include an engine)

Benefits of this approach:
- Car can have any engine type without inheritance
- Engines can be swapped at runtime
- Engine types can be developed independently
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Engine(ABC):
    """Base engine component."""

    def __init__(self, engine_id: str) -> None:
        raise NotImplementedError("Implement __init__")

    @abstractmethod
    def start(self) -> str:
        """Start the engine, return status message."""
        raise NotImplementedError("Implement start")

    @abstractmethod
    def stop(self) -> str:
        """Stop the engine, return status message."""
        raise NotImplementedError("Implement stop")

    @abstractmethod
    def get_power(self) -> float:
        """Return horsepower."""
        raise NotImplementedError("Implement get_power")

    @abstractmethod
    def get_specs(self) -> dict[str, Any]:
        """Return engine specifications."""
        raise NotImplementedError("Implement get_specs")

    @property
    @abstractmethod
    def engine_type(self) -> str:
        """Return engine type identifier."""
        raise NotImplementedError("Implement engine_type")


class GasolineEngine(Engine):
    """Traditional gasoline engine component."""

    def __init__(self, engine_id: str, displacement: float, cylinders: int) -> None:
        raise NotImplementedError("Implement __init__")

    def start(self) -> str:
        raise NotImplementedError("Implement start")

    def stop(self) -> str:
        raise NotImplementedError("Implement stop")

    def get_power(self) -> float:
        """Calculate horsepower: displacement * cylinders * 12.5."""
        raise NotImplementedError("Implement get_power")

    def get_specs(self) -> dict[str, Any]:
        raise NotImplementedError("Implement get_specs")

    @property
    def engine_type(self) -> str:
        raise NotImplementedError("Implement engine_type")


class ElectricEngine(Engine):
    """Electric motor component."""

    def __init__(
        self,
        engine_id: str,
        kwh_capacity: float,
        motor_type: str,
    ) -> None:
        raise NotImplementedError("Implement __init__")

    def start(self) -> str:
        raise NotImplementedError("Implement start")

    def stop(self) -> str:
        raise NotImplementedError("Implement stop")

    def get_power(self) -> float:
        """Calculate horsepower: kwh_capacity * 15."""
        raise NotImplementedError("Implement get_power")

    def get_specs(self) -> dict[str, Any]:
        raise NotImplementedError("Implement get_specs")

    @property
    def engine_type(self) -> str:
        raise NotImplementedError("Implement engine_type")


class HybridEngine(Engine):
    """Hybrid engine combining gas and electric."""

    def __init__(
        self,
        engine_id: str,
        gas_engine: GasolineEngine,
        electric_engine: ElectricEngine,
    ) -> None:
        raise NotImplementedError("Implement __init__")

    def start(self) -> str:
        """Start both engines."""
        raise NotImplementedError("Implement start")

    def stop(self) -> str:
        """Stop both engines."""
        raise NotImplementedError("Implement stop")

    def get_power(self) -> float:
        """Return combined horsepower."""
        raise NotImplementedError("Implement get_power")

    def get_specs(self) -> dict[str, Any]:
        raise NotImplementedError("Implement get_specs")

    @property
    def engine_type(self) -> str:
        raise NotImplementedError("Implement engine_type")

    def get_efficiency_mode(self) -> str:
        """Return 'eco' or 'power' based on which engine is primary."""
        raise NotImplementedError("Implement get_efficiency_mode")


class Car:
    """Car class using composition for engine.
    
    This class demonstrates composition over inheritance - the Car HAS-A engine
    rather than IS-A engine. This allows:
    - Changing engines at runtime
    - Testing car behavior with mock engines
    - Adding new engine types without modifying Car
    """

    def __init__(self, make: str, model: str, year: int, engine: Engine) -> None:
        raise NotImplementedError("Implement __init__")

    def start(self) -> str:
        """Start the car by starting its engine."""
        raise NotImplementedError("Implement start")

    def stop(self) -> str:
        """Stop the car by stopping its engine."""
        raise NotImplementedError("Implement stop")

    def get_performance_stats(self) -> dict[str, Any]:
        """Return car performance based on engine specs."""
        raise NotImplementedError("Implement get_performance_stats")

    def swap_engine(self, new_engine: Engine) -> str:
        """Change the car's engine (demonstrates flexibility of composition)."""
        raise NotImplementedError("Implement swap_engine")

    def get_engine_info(self) -> dict[str, Any]:
        """Return information about the current engine."""
        raise NotImplementedError("Implement get_engine_info")
