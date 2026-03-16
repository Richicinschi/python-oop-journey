"""Problem 01: Parking Lot System.

Topic: Class Design Principles
Difficulty: Medium

Design a parking lot system with the following classes:
- Vehicle: Base class with license plate and vehicle type
- Car, Motorcycle: Vehicle subclasses
- ParkingSpot: Represents a parking spot with size and occupancy status
- ParkingTicket: Tracks entry time and calculates fees
- ParkingLot: Manages spots, issues tickets, and processes exits

Requirements:
- Different spot sizes (small, medium, large) for different vehicles
- Fee calculation based on time parked (hourly rate)
- Ticket generation on entry, fee calculation on exit
- Track available spots by size

Hints:
    - Hint 1: Vehicle.can_fit_in_spot: Motorcycle fits SMALL+, Car fits MEDIUM+, Truck fits LARGE only
    - Hint 2: ParkingLot stores spots in dict: self._spots = {spot_id: ParkingSpot}
    - Hint 3: Ticket.calculate_fee: hours = ceil((now - entry_time).total_seconds() / 3600), return hours * rate
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum, auto


class VehicleType(Enum):
    """Types of vehicles supported."""
    MOTORCYCLE = auto()
    CAR = auto()
    TRUCK = auto()


class SpotSize(Enum):
    """Sizes of parking spots."""
    SMALL = auto()    # Fits motorcycle
    MEDIUM = auto()   # Fits car
    LARGE = auto()    # Fits truck


class Vehicle:
    """Base class for vehicles.
    
    Attributes:
        license_plate: Unique identifier for the vehicle
        vehicle_type: Type of vehicle
    """
    
    def __init__(self, license_plate: str, vehicle_type: VehicleType) -> None:
        raise NotImplementedError("Implement Vehicle.__init__")
    
    def can_fit_in_spot(self, spot_size: SpotSize) -> bool:
        """Check if vehicle can fit in given spot size.
        
        Args:
            spot_size: Size of the parking spot
            
        Returns:
            True if vehicle fits, False otherwise
        """
        raise NotImplementedError("Implement Vehicle.can_fit_in_spot")


class Motorcycle(Vehicle):
    """Motorcycle vehicle type."""
    
    def __init__(self, license_plate: str) -> None:
        raise NotImplementedError("Implement Motorcycle.__init__")


class Car(Vehicle):
    """Car vehicle type."""
    
    def __init__(self, license_plate: str) -> None:
        raise NotImplementedError("Implement Car.__init__")


class Truck(Vehicle):
    """Truck vehicle type."""
    
    def __init__(self, license_plate: str) -> None:
        raise NotImplementedError("Implement Truck.__init__")


class ParkingSpot:
    """A single parking spot.
    
    Attributes:
        spot_id: Unique identifier for the spot
        size: Size category of the spot
        is_occupied: Whether the spot is currently taken
    """
    
    def __init__(self, spot_id: str, size: SpotSize) -> None:
        raise NotImplementedError("Implement ParkingSpot.__init__")
    
    def park(self, vehicle: Vehicle) -> bool:
        """Park a vehicle in this spot.
        
        Args:
            vehicle: Vehicle to park
            
        Returns:
            True if parking successful, False otherwise
        """
        raise NotImplementedError("Implement ParkingSpot.park")
    
    def remove_vehicle(self) -> Vehicle | None:
        """Remove vehicle from this spot.
        
        Returns:
            The removed vehicle, or None if spot was empty
        """
        raise NotImplementedError("Implement ParkingSpot.remove_vehicle")


class ParkingTicket:
    """Ticket issued when vehicle enters parking lot.
    
    Attributes:
        ticket_id: Unique ticket identifier
        license_plate: Vehicle's license plate
        entry_time: When vehicle entered
        spot_id: ID of assigned parking spot
    """
    
    def __init__(self, ticket_id: str, license_plate: str, spot_id: str) -> None:
        raise NotImplementedError("Implement ParkingTicket.__init__")
    
    def calculate_fee(self, hourly_rate: float) -> float:
        """Calculate parking fee based on time elapsed.
        
        Args:
            hourly_rate: Cost per hour
            
        Returns:
            Total fee (rounded up to nearest hour)
        """
        raise NotImplementedError("Implement ParkingTicket.calculate_fee")


class ParkingLot:
    """Manages the parking lot operations.
    
    Coordinates spots, tickets, and fee calculation.
    Single Responsibility: Parking lot management only.
    
    Attributes:
        name: Name of the parking lot
        hourly_rate: Rate charged per hour
    """
    
    def __init__(self, name: str, hourly_rate: float) -> None:
        raise NotImplementedError("Implement ParkingLot.__init__")
    
    def add_spot(self, spot_id: str, size: SpotSize) -> None:
        """Add a parking spot to the lot.
        
        Args:
            spot_id: Unique identifier for the spot
            size: Size of the spot
        """
        raise NotImplementedError("Implement ParkingLot.add_spot")
    
    def get_available_spots(self, size: SpotSize | None = None) -> list[ParkingSpot]:
        """Get list of available spots.
        
        Args:
            size: Optional size filter
            
        Returns:
            List of available parking spots
        """
        raise NotImplementedError("Implement ParkingLot.get_available_spots")
    
    def enter(self, vehicle: Vehicle) -> ParkingTicket | None:
        """Process vehicle entry.
        
        Finds suitable spot and issues ticket.
        
        Args:
            vehicle: Vehicle entering the lot
            
        Returns:
            ParkingTicket if spot available, None otherwise
        """
        raise NotImplementedError("Implement ParkingLot.enter")
    
    def exit(self, ticket: ParkingTicket) -> tuple[Vehicle, float] | None:
        """Process vehicle exit.
        
        Calculates fee and frees up the spot.
        
        Args:
            ticket: Parking ticket to process
            
        Returns:
            Tuple of (vehicle, fee) or None if invalid ticket
        """
        raise NotImplementedError("Implement ParkingLot.exit")
