"""Problem 01: Car with Engine Component.

Refactor from inheritance to composition: A Car should have an Engine,
not inherit from it.

Classes to implement:
- Engine: Represents a car engine with horsepower and fuel type
- ElectricMotor: Alternative engine type for electric vehicles
- Car: Uses composition to include an engine

Example:
    >>> engine = Engine(200, "gasoline")
    >>> car = Car("Toyota", "Camry", engine)
    >>> car.start()
    'Toyota Camry starting: Engine (200 HP, gasoline) roars to life!'
    
    >>> motor = ElectricMotor(150)
    >>> ev = Car("Tesla", "Model 3", motor)
    >>> ev.start()
    'Tesla Model 3 starting: Electric motor (150 kW) hums quietly!'
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class PowerSource(ABC):
    """Abstract base class for power sources.
    
    This demonstrates the Strategy pattern - different power sources
    can be plugged into a car without changing the Car class.
    """
    
    @abstractmethod
    def start(self) -> str:
        """Start the power source.
        
        Returns:
            Description of the starting sound/action.
        """
        ...
    
    @abstractmethod
    def get_specs(self) -> str:
        """Get technical specifications.
        
        Returns:
            Formatted specification string.
        """
        ...


class Engine(PowerSource):
    """A traditional combustion engine.
    
    Attributes:
        horsepower: Engine power in HP.
        fuel_type: Type of fuel (gasoline, diesel, etc.).
    """
    
    def __init__(self, horsepower: int, fuel_type: str) -> None:
        """Initialize an engine.
        
        Args:
            horsepower: Engine power in HP.
            fuel_type: Type of fuel used.
        """
        self.horsepower = horsepower
        self.fuel_type = fuel_type
    
    def start(self) -> str:
        """Start the engine.
        
        Returns:
            Description of the engine starting.
        """
        return f"Engine ({self.horsepower} HP, {self.fuel_type}) roars to life!"
    
    def get_specs(self) -> str:
        """Get engine specifications.
        
        Returns:
            Formatted specification string.
        """
        return f"{self.horsepower} HP {self.fuel_type} engine"


class ElectricMotor(PowerSource):
    """An electric motor for electric vehicles.
    
    Attributes:
        kilowatts: Motor power in kW.
    """
    
    def __init__(self, kilowatts: int) -> None:
        """Initialize an electric motor.
        
        Args:
            kilowatts: Motor power in kW.
        """
        self.kilowatts = kilowatts
    
    def start(self) -> str:
        """Start the electric motor.
        
        Returns:
            Description of the motor starting.
        """
        return f"Electric motor ({self.kilowatts} kW) hums quietly!"
    
    def get_specs(self) -> str:
        """Get motor specifications.
        
        Returns:
            Formatted specification string.
        """
        return f"{self.kilowatts} kW electric motor"


class Car:
    """A car that composes a power source instead of inheriting.
    
    This class demonstrates composition over inheritance. A Car has a
    PowerSource, rather than being a PowerSource.
    
    Attributes:
        make: Car manufacturer.
        model: Car model name.
        power_source: The engine/motor powering the car.
        is_running: Whether the car is currently running.
    """
    
    def __init__(self, make: str, model: str, power_source: PowerSource) -> None:
        """Initialize a car.
        
        Args:
            make: Car manufacturer.
            model: Car model name.
            power_source: The power source (Engine, ElectricMotor, etc.).
        """
        self.make = make
        self.model = model
        self._power_source = power_source
        self._is_running = False
    
    @property
    def power_source(self) -> PowerSource:
        """Get the car's power source.
        
        Returns:
            The current power source.
        """
        return self._power_source
    
    def swap_power_source(self, new_power_source: PowerSource) -> str:
        """Replace the car's power source.
        
        This demonstrates the flexibility of composition - we can
        swap components at runtime.
        
        Args:
            new_power_source: The new power source to install.
        
        Returns:
            Confirmation message of the swap.
        """
        old_specs = self._power_source.get_specs()
        self._power_source = new_power_source
        new_specs = new_power_source.get_specs()
        return f"Swapped {old_specs} for {new_specs}"
    
    def start(self) -> str:
        """Start the car.
        
        Returns:
            Description of the car starting.
        """
        self._is_running = True
        power_start = self._power_source.start()
        return f"{self.make} {self.model} starting: {power_start}"
    
    def stop(self) -> str:
        """Stop the car.
        
        Returns:
            Description of the car stopping.
        """
        self._is_running = False
        return f"{self.make} {self.model} stopped."
    
    def is_running(self) -> bool:
        """Check if the car is running.
        
        Returns:
            True if the car is running, False otherwise.
        """
        return self._is_running
    
    def get_specs(self) -> str:
        """Get car specifications.
        
        Returns:
            Formatted specification string.
        """
        return f"{self.make} {self.model} with {self._power_source.get_specs()}"
    
    def __str__(self) -> str:
        """Return string representation.
        
        Returns:
            Formatted car description.
        """
        status = "running" if self._is_running else "stopped"
        return f"{self.make} {self.model} ({status})"
