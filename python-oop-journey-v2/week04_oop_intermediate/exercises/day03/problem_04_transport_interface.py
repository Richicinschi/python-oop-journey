"""Exercise: Transport Interface.

Create an abstract base class for transport vehicles with movement and
location tracking capabilities.

TODO:
1. Create Transport ABC with abstract methods move() and get_location()
2. Add abstract property max_speed -> float
3. Implement Car with fuel-based movement
4. Implement Bicycle with human-powered movement
5. Implement ElectricScooter with battery-based movement
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple


class Transport(ABC):
    """Abstract base class for transport vehicles.
    
    All transport vehicles can move and track their location.
    """
    
    def __init__(self, name: str) -> None:
        """Initialize transport vehicle.
        
        Args:
            name: The vehicle name/identifier.
        """
        # TODO: Set name and initialize location at (0, 0)
        raise NotImplementedError("Initialize transport")
    
    @property
    @abstractmethod
    def max_speed(self) -> float:
        """Return the maximum speed of the vehicle (km/h)."""
        # TODO: Define abstract property
        raise NotImplementedError("max_speed property must be implemented")
    
    @abstractmethod
    def move(self, distance: float, direction: float) -> None:
        """Move the vehicle.
        
        Args:
            distance: Distance to travel (km).
            direction: Direction in degrees (0 = North, 90 = East, etc.).
        """
        # TODO: Implement abstract method
        raise NotImplementedError("move must be implemented")
    
    @abstractmethod
    def get_location(self) -> Tuple[float, float]:
        """Get current location coordinates.
        
        Returns:
            Tuple of (x, y) coordinates.
        """
        # TODO: Implement abstract method
        raise NotImplementedError("get_location must be implemented")
    
    def distance_from_origin(self) -> float:
        """Calculate Euclidean distance from origin (0, 0).
        
        Returns:
            Distance from origin.
        """
        # TODO: Calculate sqrt(x² + y²)
        raise NotImplementedError("Calculate distance from origin")


class Car(Transport):
    """A car with fuel-based movement."""
    
    FUEL_EFFICIENCY = 0.1  # liters per km
    
    def __init__(self, name: str, fuel_capacity: float) -> None:
        """Initialize car.
        
        Args:
            name: The car name.
            fuel_capacity: Maximum fuel capacity in liters.
        """
        # TODO: Call parent __init__, set fuel_capacity and current_fuel
        raise NotImplementedError("Initialize car")
    
    @property
    def max_speed(self) -> float:
        """Return car's max speed."""
        # TODO: Return 120.0 km/h
        raise NotImplementedError("Return max speed")
    
    def move(self, distance: float, direction: float) -> None:
        """Move car, consuming fuel.
        
        Raises:
            ValueError: If insufficient fuel for the distance.
        """
        # TODO: Check if enough fuel
        # TODO: Update location based on direction
        # TODO: Consume fuel
        raise NotImplementedError("Implement car movement")
    
    def get_location(self) -> Tuple[float, float]:
        """Return current location."""
        # TODO: Return current (x, y)
        raise NotImplementedError("Return location")
    
    def refuel(self, amount: float) -> None:
        """Add fuel to the tank.
        
        Args:
            amount: Liters to add.
        """
        # TODO: Add fuel without exceeding capacity
        raise NotImplementedError("Implement refuel")


class Bicycle(Transport):
    """A human-powered bicycle."""
    
    def __init__(self, name: str, rider_fatigue: float = 0.0) -> None:
        """Initialize bicycle.
        
        Args:
            name: The bicycle name.
            rider_fatigue: Initial fatigue level (0-100).
        """
        # TODO: Call parent __init__, set rider_fatigue
        raise NotImplementedError("Initialize bicycle")
    
    @property
    def max_speed(self) -> float:
        """Return bicycle's max speed."""
        # TODO: Return 25.0 km/h
        raise NotImplementedError("Return max speed")
    
    def move(self, distance: float, direction: float) -> None:
        """Move bicycle, increasing rider fatigue.
        
        Fatigue increases by 1 point per km traveled.
        """
        # TODO: Update location based on direction
        # TODO: Increase fatigue by distance
        raise NotImplementedError("Implement bicycle movement")
    
    def get_location(self) -> Tuple[float, float]:
        """Return current location."""
        # TODO: Return current (x, y)
        raise NotImplementedError("Return location")
    
    def rest(self) -> None:
        """Rest to reduce fatigue to 0."""
        # TODO: Reset fatigue to 0
        raise NotImplementedError("Implement rest")


class ElectricScooter(Transport):
    """An electric scooter with battery-based movement."""
    
    BATTERY_CONSUMPTION = 0.5  # percent per km
    
    def __init__(self, name: str) -> None:
        """Initialize electric scooter.
        
        Args:
            name: The scooter name.
        """
        # TODO: Call parent __init__, set battery to 100
        raise NotImplementedError("Initialize scooter")
    
    @property
    def max_speed(self) -> float:
        """Return scooter's max speed."""
        # TODO: Return 20.0 km/h
        raise NotImplementedError("Return max speed")
    
    def move(self, distance: float, direction: float) -> None:
        """Move scooter, consuming battery.
        
        Raises:
            ValueError: If insufficient battery for the distance.
        """
        # TODO: Check if enough battery
        # TODO: Update location based on direction
        # TODO: Consume battery
        raise NotImplementedError("Implement scooter movement")
    
    def get_location(self) -> Tuple[float, float]:
        """Return current location."""
        # TODO: Return current (x, y)
        raise NotImplementedError("Return location")
    
    def charge(self) -> None:
        """Charge battery to 100%."""
        # TODO: Set battery to 100
        raise NotImplementedError("Implement charge")
