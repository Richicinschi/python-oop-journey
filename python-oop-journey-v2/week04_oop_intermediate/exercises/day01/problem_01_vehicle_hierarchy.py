"""Problem 01: Vehicle Hierarchy

Topic: Basic Inheritance
Difficulty: Easy

Create a Vehicle base class and three derived classes (Car, Truck, Motorcycle).
Demonstrate proper inheritance with method overriding.
"""

from __future__ import annotations


class Vehicle:
    """Base class for all vehicles.
    
    Attributes:
        brand: The manufacturer of the vehicle
        model: The model name
        year: The manufacturing year
    """
    
    def __init__(self, brand: str, model: str, year: int) -> None:
        """Initialize a Vehicle.
        
        Args:
            brand: Vehicle manufacturer
            model: Vehicle model name
            year: Manufacturing year
        """
        raise NotImplementedError("Implement Vehicle.__init__")
    
    def description(self) -> str:
        """Return a description of the vehicle.
        
        Returns:
            String in format: "YYYY Brand Model"
        """
        raise NotImplementedError("Implement Vehicle.description")
    
    def start_engine(self) -> str:
        """Return engine start message.
        
        Returns:
            Base message: "Engine starting..."
        """
        raise NotImplementedError("Implement Vehicle.start_engine")
    
    def honk(self) -> str:
        """Return the vehicle's honk sound.
        
        Returns:
            Default sound: "Beep!"
        """
        raise NotImplementedError("Implement Vehicle.honk")


class Car(Vehicle):
    """A car inherits from Vehicle.
    
    Additional Attributes:
        doors: Number of doors (2 or 4)
        trunk_capacity: Trunk capacity in cubic feet
    """
    
    def __init__(self, brand: str, model: str, year: int, doors: int, trunk_capacity: float) -> None:
        """Initialize a Car.
        
        Args:
            brand: Car manufacturer
            model: Car model name
            year: Manufacturing year
            doors: Number of doors (should be 2 or 4)
            trunk_capacity: Trunk capacity in cubic feet
        """
        raise NotImplementedError("Implement Car.__init__")
    
    def start_engine(self) -> str:
        """Override: Car-specific engine start sound.
        
        Returns:
            "Vroom! Car engine purring..."
        """
        raise NotImplementedError("Implement Car.start_engine")
    
    def open_trunk(self) -> str:
        """Car-specific method to open trunk.
        
        Returns:
            "Trunk opened. Capacity: X cu ft"
        """
        raise NotImplementedError("Implement Car.open_trunk")


class Truck(Vehicle):
    """A truck inherits from Vehicle.
    
    Additional Attributes:
        bed_capacity: Maximum bed capacity in pounds
        has_four_wheel_drive: Whether truck has 4WD
    """
    
    def __init__(self, brand: str, model: str, year: int, bed_capacity: float, has_four_wheel_drive: bool) -> None:
        """Initialize a Truck.
        
        Args:
            brand: Truck manufacturer
            model: Truck model name
            year: Manufacturing year
            bed_capacity: Maximum bed capacity in pounds
            has_four_wheel_drive: Whether truck has 4WD
        """
        raise NotImplementedError("Implement Truck.__init__")
    
    def start_engine(self) -> str:
        """Override: Truck-specific engine start sound.
        
        Returns:
            "Rumble! Truck engine roaring..."
        """
        raise NotImplementedError("Implement Truck.start_engine")
    
    def honk(self) -> str:
        """Override: Truck-specific horn sound.
        
        Returns:
            "HONK HONK!"
        """
        raise NotImplementedError("Implement Truck.honk")
    
    def tow(self, weight: float) -> str:
        """Truck-specific method to attempt towing.
        
        Args:
            weight: Weight to tow in pounds
            
        Returns:
            Success message if weight <= bed_capacity
            Failure message if weight > bed_capacity
        """
        raise NotImplementedError("Implement Truck.tow")


class Motorcycle(Vehicle):
    """A motorcycle inherits from Vehicle.
    
    Additional Attributes:
        engine_cc: Engine displacement in cubic centimeters
        has_sidecar: Whether motorcycle has a sidecar
    """
    
    def __init__(self, brand: str, model: str, year: int, engine_cc: int, has_sidecar: bool = False) -> None:
        """Initialize a Motorcycle.
        
        Args:
            brand: Motorcycle manufacturer
            model: Motorcycle model name
            year: Manufacturing year
            engine_cc: Engine displacement in CC
            has_sidecar: Whether motorcycle has a sidecar
        """
        raise NotImplementedError("Implement Motorcycle.__init__")
    
    def start_engine(self) -> str:
        """Override: Motorcycle-specific engine start sound.
        
        Returns:
            "Rev! Motorcycle engine revving..."
        """
        raise NotImplementedError("Implement Motorcycle.start_engine")
    
    def wheelie(self) -> str:
        """Motorcycle-specific method (only if no sidecar).
        
        Returns:
            Success message if no sidecar
            Failure message if has sidecar
        """
        raise NotImplementedError("Implement Motorcycle.wheelie")
