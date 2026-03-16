"""Reference solution for Problem 01: Vehicle Hierarchy."""

from __future__ import annotations


class Vehicle:
    """Base class for all vehicles."""
    
    def __init__(self, brand: str, model: str, year: int) -> None:
        self.brand = brand
        self.model = model
        self.year = year
    
    def description(self) -> str:
        return f"{self.year} {self.brand} {self.model}"
    
    def start_engine(self) -> str:
        return "Engine starting..."
    
    def honk(self) -> str:
        return "Beep!"


class Car(Vehicle):
    """A car inherits from Vehicle."""
    
    def __init__(self, brand: str, model: str, year: int, doors: int, trunk_capacity: float) -> None:
        super().__init__(brand, model, year)
        self.doors = doors
        self.trunk_capacity = trunk_capacity
    
    def start_engine(self) -> str:
        return "Vroom! Car engine purring..."
    
    def open_trunk(self) -> str:
        return f"Trunk opened. Capacity: {self.trunk_capacity} cu ft"


class Truck(Vehicle):
    """A truck inherits from Vehicle."""
    
    def __init__(self, brand: str, model: str, year: int, bed_capacity: float, has_four_wheel_drive: bool) -> None:
        super().__init__(brand, model, year)
        self.bed_capacity = bed_capacity
        self.has_four_wheel_drive = has_four_wheel_drive
    
    def start_engine(self) -> str:
        return "Rumble! Truck engine roaring..."
    
    def honk(self) -> str:
        return "HONK HONK!"
    
    def tow(self, weight: float) -> str:
        if weight <= self.bed_capacity:
            return f"Successfully towing {weight} lbs"
        return f"Cannot tow {weight} lbs. Max capacity: {self.bed_capacity} lbs"


class Motorcycle(Vehicle):
    """A motorcycle inherits from Vehicle."""
    
    def __init__(self, brand: str, model: str, year: int, engine_cc: int, has_sidecar: bool = False) -> None:
        super().__init__(brand, model, year)
        self.engine_cc = engine_cc
        self.has_sidecar = has_sidecar
    
    def start_engine(self) -> str:
        return "Rev! Motorcycle engine revving..."
    
    def wheelie(self) -> str:
        if not self.has_sidecar:
            return "Doing a wheelie!"
        return "Cannot do wheelie with sidecar attached"
