"""Solution for Problem 04: Transport Interface.

Demonstrates abstract methods and properties for transport vehicles.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import math
from typing import Tuple


class Transport(ABC):
    """Abstract base class for transport vehicles.
    
    All transport vehicles can move and track their location.
    
    Attributes:
        name: The vehicle name/identifier.
        _x: Current x-coordinate.
        _y: Current y-coordinate.
    """
    
    def __init__(self, name: str) -> None:
        """Initialize transport vehicle.
        
        Args:
            name: The vehicle name/identifier.
        """
        self.name = name
        self._x = 0.0
        self._y = 0.0
    
    @property
    @abstractmethod
    def max_speed(self) -> float:
        """Return the maximum speed of the vehicle (km/h)."""
        pass
    
    @abstractmethod
    def move(self, distance: float, direction: float) -> None:
        """Move the vehicle.
        
        Args:
            distance: Distance to travel (km).
            direction: Direction in degrees (0 = North, 90 = East, etc.).
        """
        pass
    
    @abstractmethod
    def get_location(self) -> Tuple[float, float]:
        """Get current location coordinates.
        
        Returns:
            Tuple of (x, y) coordinates.
        """
        pass
    
    def distance_from_origin(self) -> float:
        """Calculate Euclidean distance from origin (0, 0).
        
        Returns:
            Distance from origin.
        """
        return math.sqrt(self._x ** 2 + self._y ** 2)


class Car(Transport):
    """A car with fuel-based movement.
    
    Attributes:
        fuel_capacity: Maximum fuel capacity in liters.
        current_fuel: Current fuel level.
    """
    
    FUEL_EFFICIENCY = 0.1  # liters per km
    
    def __init__(self, name: str, fuel_capacity: float) -> None:
        """Initialize car.
        
        Args:
            name: The car name.
            fuel_capacity: Maximum fuel capacity in liters.
        """
        super().__init__(name)
        self.fuel_capacity = float(fuel_capacity)
        self.current_fuel = float(fuel_capacity)
    
    @property
    def max_speed(self) -> float:
        """Return car's max speed."""
        return 120.0
    
    def move(self, distance: float, direction: float) -> None:
        """Move car, consuming fuel.
        
        Args:
            distance: Distance to travel (km).
            direction: Direction in degrees.
        
        Raises:
            ValueError: If insufficient fuel for the distance.
        """
        fuel_needed = distance * self.FUEL_EFFICIENCY
        if fuel_needed > self.current_fuel:
            raise ValueError("Insufficient fuel")
        
        # Convert direction to radians
        rad = math.radians(direction)
        self._x += distance * math.sin(rad)
        self._y += distance * math.cos(rad)
        self.current_fuel -= fuel_needed
    
    def get_location(self) -> Tuple[float, float]:
        """Return current location."""
        return (self._x, self._y)
    
    def refuel(self, amount: float) -> None:
        """Add fuel to the tank.
        
        Args:
            amount: Liters to add.
        """
        self.current_fuel = min(self.current_fuel + amount, self.fuel_capacity)


class Bicycle(Transport):
    """A human-powered bicycle.
    
    Attributes:
        rider_fatigue: Current fatigue level (0-100).
    """
    
    def __init__(self, name: str, rider_fatigue: float = 0.0) -> None:
        """Initialize bicycle.
        
        Args:
            name: The bicycle name.
            rider_fatigue: Initial fatigue level (0-100).
        """
        super().__init__(name)
        self.rider_fatigue = float(rider_fatigue)
    
    @property
    def max_speed(self) -> float:
        """Return bicycle's max speed."""
        return 25.0
    
    def move(self, distance: float, direction: float) -> None:
        """Move bicycle, increasing rider fatigue.
        
        Args:
            distance: Distance to travel (km).
            direction: Direction in degrees.
        
        Note:
            Fatigue increases by 1 point per km traveled.
        """
        rad = math.radians(direction)
        self._x += distance * math.sin(rad)
        self._y += distance * math.cos(rad)
        self.rider_fatigue += distance
    
    def get_location(self) -> Tuple[float, float]:
        """Return current location."""
        return (self._x, self._y)
    
    def rest(self) -> None:
        """Rest to reduce fatigue to 0."""
        self.rider_fatigue = 0.0


class ElectricScooter(Transport):
    """An electric scooter with battery-based movement.
    
    Attributes:
        battery: Current battery percentage (0-100).
    """
    
    BATTERY_CONSUMPTION = 0.5  # percent per km
    
    def __init__(self, name: str) -> None:
        """Initialize electric scooter.
        
        Args:
            name: The scooter name.
        """
        super().__init__(name)
        self.battery = 100.0
    
    @property
    def max_speed(self) -> float:
        """Return scooter's max speed."""
        return 20.0
    
    def move(self, distance: float, direction: float) -> None:
        """Move scooter, consuming battery.
        
        Args:
            distance: Distance to travel (km).
            direction: Direction in degrees.
        
        Raises:
            ValueError: If insufficient battery for the distance.
        """
        battery_needed = distance * self.BATTERY_CONSUMPTION
        if battery_needed > self.battery:
            raise ValueError("Insufficient battery")
        
        rad = math.radians(direction)
        self._x += distance * math.sin(rad)
        self._y += distance * math.cos(rad)
        self.battery -= battery_needed
    
    def get_location(self) -> Tuple[float, float]:
        """Return current location."""
        return (self._x, self._y)
    
    def charge(self) -> None:
        """Charge battery to 100%."""
        self.battery = 100.0
