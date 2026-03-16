"""Problem 04: Transport Simulator.

Topic: Polymorphism
Difficulty: Medium

Create transport types (Car, Bike, Bus) that share common methods.
Demonstrate polymorphic behavior in a simulation context.

TODO:
1. Create Transport ABC with:
   - move(self, distance: float) -> str (abstract)
   - get_capacity(self) -> int (abstract)
   - get_fuel_cost(self, distance: float) -> float (abstract)

2. Create Car class:
   - __init__(self, model: str, fuel_efficiency: float, capacity: int = 5)
   - move returns f"{model} drove {distance}km"
   - get_capacity returns capacity
   - get_fuel_cost returns (distance / fuel_efficiency) * 1.50

3. Create Bike class:
   - __init__(self, model: str, capacity: int = 1)
   - move returns f"{model} cycled {distance}km"
   - get_capacity returns capacity
   - get_fuel_cost returns 0.0 (no fuel)

4. Create Bus class:
   - __init__(self, route: str, fuel_efficiency: float, capacity: int = 50)
   - move returns f"Bus {route} traveled {distance}km"
   - get_capacity returns capacity
   - get_fuel_cost returns (distance / fuel_efficiency) * 1.20 (cheaper diesel)

5. Implement simulate_transport(transports: list, distance: float) -> dict
   that runs simulation and returns stats dict with:
   - 'movements': list of move results
   - 'total_capacity': sum of all capacities
   - 'total_fuel_cost': sum of all fuel costs

Hints:
    Hint 1: This exercise demonstrates polymorphism - all transport classes
    implement the same interface (move, get_capacity, get_fuel_cost) but with
    different behaviors. The Transport ABC enforces this interface.
    
    Hint 2: simulate_transport() should accept a list of Transport objects
    (the ABC, not specific types) and call their methods without knowing
    the concrete type. Use a loop: for transport in transports: transport.move(distance)
    
    Hint 3: When summing capacities and fuel costs, iterate through the list
    and accumulate results. Fuel cost calculations involve division - ensure
    you handle the math correctly: (distance / fuel_efficiency) * fuel_price.
    Round to 2 decimal places is acceptable.
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
        raise NotImplementedError("move must be implemented")
    
    @abstractmethod
    def get_capacity(self) -> int:
        """Get passenger capacity.
        
        Returns:
            Number of passengers the transport can carry.
        """
        raise NotImplementedError("get_capacity must be implemented")
    
    @abstractmethod
    def get_fuel_cost(self, distance: float) -> float:
        """Calculate fuel cost for a distance.
        
        Args:
            distance: Distance to travel in kilometers.
        
        Returns:
            Fuel cost in dollars.
        """
        raise NotImplementedError("get_fuel_cost must be implemented")


class Car(Transport):
    """Car transport implementation."""
    
    def __init__(self, model: str, fuel_efficiency: float, capacity: int = 5) -> None:
        """Initialize car.
        
        Args:
            model: Car model name.
            fuel_efficiency: km per liter.
            capacity: Passenger capacity (default 5).
        """
        # TODO: Initialize attributes
        raise NotImplementedError("Initialize car")
    
    def move(self, distance: float) -> str:
        """Drive the car."""
        # TODO: Return f"{self.model} drove {distance}km"
        raise NotImplementedError("Implement move")
    
    def get_capacity(self) -> int:
        """Return passenger capacity."""
        # TODO: Return capacity
        raise NotImplementedError("Implement get_capacity")
    
    def get_fuel_cost(self, distance: float) -> float:
        """Calculate fuel cost."""
        # TODO: Return (distance / fuel_efficiency) * 1.50
        raise NotImplementedError("Implement get_fuel_cost")


class Bike(Transport):
    """Bike transport implementation."""
    
    def __init__(self, model: str, capacity: int = 1) -> None:
        """Initialize bike.
        
        Args:
            model: Bike model name.
            capacity: Passenger capacity (default 1).
        """
        # TODO: Initialize attributes
        raise NotImplementedError("Initialize bike")
    
    def move(self, distance: float) -> str:
        """Cycle the bike."""
        # TODO: Return f"{self.model} cycled {distance}km"
        raise NotImplementedError("Implement move")
    
    def get_capacity(self) -> int:
        """Return passenger capacity."""
        # TODO: Return capacity
        raise NotImplementedError("Implement get_capacity")
    
    def get_fuel_cost(self, distance: float) -> float:
        """Calculate fuel cost (always 0)."""
        # TODO: Return 0.0
        raise NotImplementedError("Implement get_fuel_cost")


class Bus(Transport):
    """Bus transport implementation."""
    
    def __init__(self, route: str, fuel_efficiency: float, capacity: int = 50) -> None:
        """Initialize bus.
        
        Args:
            route: Bus route identifier.
            fuel_efficiency: km per liter.
            capacity: Passenger capacity (default 50).
        """
        # TODO: Initialize attributes
        raise NotImplementedError("Initialize bus")
    
    def move(self, distance: float) -> str:
        """Drive the bus."""
        # TODO: Return f"Bus {self.route} traveled {distance}km"
        raise NotImplementedError("Implement move")
    
    def get_capacity(self) -> int:
        """Return passenger capacity."""
        # TODO: Return capacity
        raise NotImplementedError("Implement get_capacity")
    
    def get_fuel_cost(self, distance: float) -> float:
        """Calculate fuel cost (cheaper diesel)."""
        # TODO: Return (distance / fuel_efficiency) * 1.20
        raise NotImplementedError("Implement get_fuel_cost")


def simulate_transport(transports: list[Transport], distance: float) -> dict:
    """Simulate all transports moving a given distance.
    
    Args:
        transports: List of Transport instances.
        distance: Distance to travel in kilometers.
    
    Returns:
        Dictionary with simulation results:
        - 'movements': list of move result strings
        - 'total_capacity': sum of all capacities
        - 'total_fuel_cost': sum of all fuel costs
    """
    # TODO: Implement simulation
    # 1. Call move() on each transport, collect results
    # 2. Sum get_capacity() from all transports
    # 3. Sum get_fuel_cost(distance) from all transports
    # 4. Return dict with all results
    raise NotImplementedError("Implement simulate_transport")
