"""Solution for Problem 04: Transport Simulator.

Demonstrates polymorphic transport simulation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Transport(ABC):
    """Abstract base class for transport types."""
    
    @abstractmethod
    def move(self, distance: float) -> str:
        """Move the transport for a given distance.
        
        Args:
            distance: Distance to travel in kilometers.
        
        Returns:
            String describing the movement.
        """
        pass
    
    @abstractmethod
    def get_capacity(self) -> int:
        """Get passenger capacity.
        
        Returns:
            Number of passengers the transport can carry.
        """
        pass
    
    @abstractmethod
    def get_fuel_cost(self, distance: float) -> float:
        """Calculate fuel cost for a distance.
        
        Args:
            distance: Distance to travel in kilometers.
        
        Returns:
            Fuel cost in dollars.
        """
        pass


class Car(Transport):
    """Car transport implementation.
    
    Attributes:
        model: Car model name.
        fuel_efficiency: km per liter.
        capacity: Passenger capacity.
    """
    
    def __init__(self, model: str, fuel_efficiency: float, capacity: int = 5) -> None:
        """Initialize car.
        
        Args:
            model: Car model name.
            fuel_efficiency: km per liter.
            capacity: Passenger capacity (default 5).
        """
        self.model = model
        self.fuel_efficiency = fuel_efficiency
        self._capacity = capacity
    
    def move(self, distance: float) -> str:
        """Drive the car.
        
        Args:
            distance: Distance to travel.
        
        Returns:
            String describing the movement.
        """
        return f"{self.model} drove {distance}km"
    
    def get_capacity(self) -> int:
        """Return passenger capacity."""
        return self._capacity
    
    def get_fuel_cost(self, distance: float) -> float:
        """Calculate fuel cost.
        
        Args:
            distance: Distance to travel.
        
        Returns:
            Fuel cost in dollars.
        """
        liters_needed = distance / self.fuel_efficiency
        return liters_needed * 1.50


class Bike(Transport):
    """Bike transport implementation.
    
    Attributes:
        model: Bike model name.
        capacity: Passenger capacity.
    """
    
    def __init__(self, model: str, capacity: int = 1) -> None:
        """Initialize bike.
        
        Args:
            model: Bike model name.
            capacity: Passenger capacity (default 1).
        """
        self.model = model
        self._capacity = capacity
    
    def move(self, distance: float) -> str:
        """Cycle the bike.
        
        Args:
            distance: Distance to travel.
        
        Returns:
            String describing the movement.
        """
        return f"{self.model} cycled {distance}km"
    
    def get_capacity(self) -> int:
        """Return passenger capacity."""
        return self._capacity
    
    def get_fuel_cost(self, distance: float) -> float:
        """Calculate fuel cost (always 0).
        
        Returns:
            0.0 since bikes don't use fuel.
        """
        return 0.0


class Bus(Transport):
    """Bus transport implementation.
    
    Attributes:
        route: Bus route identifier.
        fuel_efficiency: km per liter.
        capacity: Passenger capacity.
    """
    
    def __init__(self, route: str, fuel_efficiency: float, capacity: int = 50) -> None:
        """Initialize bus.
        
        Args:
            route: Bus route identifier.
            fuel_efficiency: km per liter.
            capacity: Passenger capacity (default 50).
        """
        self.route = route
        self.fuel_efficiency = fuel_efficiency
        self._capacity = capacity
    
    def move(self, distance: float) -> str:
        """Drive the bus.
        
        Args:
            distance: Distance to travel.
        
        Returns:
            String describing the movement.
        """
        return f"Bus {self.route} traveled {distance}km"
    
    def get_capacity(self) -> int:
        """Return passenger capacity."""
        return self._capacity
    
    def get_fuel_cost(self, distance: float) -> float:
        """Calculate fuel cost (cheaper diesel).
        
        Args:
            distance: Distance to travel.
        
        Returns:
            Fuel cost in dollars.
        """
        liters_needed = distance / self.fuel_efficiency
        return liters_needed * 1.20


def simulate_transport(transports: list[Transport], distance: float) -> dict:
    """Simulate all transports moving a given distance.
    
    This function demonstrates polymorphism - it works with any
    Transport subclass without knowing the specific type.
    
    Args:
        transports: List of Transport instances.
        distance: Distance to travel in kilometers.
    
    Returns:
        Dictionary with simulation results.
    """
    movements = []
    total_capacity = 0
    total_fuel_cost = 0.0
    
    for transport in transports:
        movements.append(transport.move(distance))
        total_capacity += transport.get_capacity()
        total_fuel_cost += transport.get_fuel_cost(distance)
    
    return {
        "movements": movements,
        "total_capacity": total_capacity,
        "total_fuel_cost": round(total_fuel_cost, 2),
    }
