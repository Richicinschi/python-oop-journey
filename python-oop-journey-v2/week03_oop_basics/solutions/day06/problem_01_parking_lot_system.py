"""Solution for Problem 01: Parking Lot System.

Demonstrates class design principles:
- Single Responsibility: Each class has one clear purpose
- Cohesion: Related attributes and methods grouped together
- Loose Coupling: Classes interact through well-defined interfaces
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
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
    
    def can_fit_in_spot(self, spot_size: SpotSize) -> bool:
        """Check if vehicle can fit in given spot size.
        
        Args:
            spot_size: Size of the parking spot
            
        Returns:
            True if vehicle fits, False otherwise
        """
        # Each vehicle type knows what spots it fits in
        raise NotImplementedError("Subclasses must implement")


class Motorcycle(Vehicle):
    """Motorcycle vehicle type - fits in any spot."""
    
    def __init__(self, license_plate: str) -> None:
        super().__init__(license_plate, VehicleType.MOTORCYCLE)
    
    def can_fit_in_spot(self, spot_size: SpotSize) -> bool:
        """Motorcycles fit in all spot sizes."""
        return True


class Car(Vehicle):
    """Car vehicle type - fits in medium or large spots."""
    
    def __init__(self, license_plate: str) -> None:
        super().__init__(license_plate, VehicleType.CAR)
    
    def can_fit_in_spot(self, spot_size: SpotSize) -> bool:
        """Cars fit in medium or large spots."""
        return spot_size in (SpotSize.MEDIUM, SpotSize.LARGE)


class Truck(Vehicle):
    """Truck vehicle type - only fits in large spots."""
    
    def __init__(self, license_plate: str) -> None:
        super().__init__(license_plate, VehicleType.TRUCK)
    
    def can_fit_in_spot(self, spot_size: SpotSize) -> bool:
        """Trucks only fit in large spots."""
        return spot_size == SpotSize.LARGE


class ParkingSpot:
    """A single parking spot.
    
    Attributes:
        spot_id: Unique identifier for the spot
        size: Size category of the spot
        is_occupied: Whether the spot is currently taken
    """
    
    def __init__(self, spot_id: str, size: SpotSize) -> None:
        self.spot_id = spot_id
        self.size = size
        self._vehicle: Vehicle | None = None
    
    @property
    def is_occupied(self) -> bool:
        """True if spot has a vehicle."""
        return self._vehicle is not None
    
    def park(self, vehicle: Vehicle) -> bool:
        """Park a vehicle in this spot.
        
        Args:
            vehicle: Vehicle to park
            
        Returns:
            True if parking successful, False otherwise
        """
        if self.is_occupied:
            return False
        if not vehicle.can_fit_in_spot(self.size):
            return False
        self._vehicle = vehicle
        return True
    
    def remove_vehicle(self) -> Vehicle | None:
        """Remove vehicle from this spot.
        
        Returns:
            The removed vehicle, or None if spot was empty
        """
        vehicle = self._vehicle
        self._vehicle = None
        return vehicle


class ParkingTicket:
    """Ticket issued when vehicle enters parking lot.
    
    Attributes:
        ticket_id: Unique ticket identifier
        license_plate: Vehicle's license plate
        entry_time: When vehicle entered
        spot_id: ID of assigned parking spot
    """
    
    def __init__(self, ticket_id: str, license_plate: str, spot_id: str) -> None:
        self.ticket_id = ticket_id
        self.license_plate = license_plate
        self.entry_time = datetime.now()
        self.spot_id = spot_id
    
    def calculate_fee(self, hourly_rate: float) -> float:
        """Calculate parking fee based on time elapsed.
        
        Args:
            hourly_rate: Cost per hour
            
        Returns:
            Total fee (rounded up to nearest hour)
        """
        elapsed = datetime.now() - self.entry_time
        hours = elapsed.total_seconds() / 3600
        # Round up to nearest hour, minimum 1 hour
        charged_hours = max(1, int(hours) + (1 if hours % 1 > 0 else 0))
        return charged_hours * hourly_rate


class ParkingLot:
    """Manages the parking lot operations.
    
    Coordinates spots, tickets, and fee calculation.
    Single Responsibility: Parking lot management only.
    
    Attributes:
        name: Name of the parking lot
        hourly_rate: Rate charged per hour
    """
    
    def __init__(self, name: str, hourly_rate: float) -> None:
        self.name = name
        self.hourly_rate = hourly_rate
        self._spots: dict[str, ParkingSpot] = {}
        self._ticket_counter = 0
    
    def add_spot(self, spot_id: str, size: SpotSize) -> None:
        """Add a parking spot to the lot.
        
        Args:
            spot_id: Unique identifier for the spot
            size: Size of the spot
        """
        self._spots[spot_id] = ParkingSpot(spot_id, size)
    
    def get_available_spots(self, size: SpotSize | None = None) -> list[ParkingSpot]:
        """Get list of available spots.
        
        Args:
            size: Optional size filter
            
        Returns:
            List of available parking spots
        """
        available = [spot for spot in self._spots.values() if not spot.is_occupied]
        if size is not None:
            available = [spot for spot in available if spot.size == size]
        return available
    
    def enter(self, vehicle: Vehicle) -> ParkingTicket | None:
        """Process vehicle entry.
        
        Finds suitable spot and issues ticket.
        
        Args:
            vehicle: Vehicle entering the lot
            
        Returns:
            ParkingTicket if spot available, None otherwise
        """
        # Find first available spot that fits
        for spot in self._spots.values():
            if not spot.is_occupied and vehicle.can_fit_in_spot(spot.size):
                if spot.park(vehicle):
                    self._ticket_counter += 1
                    return ParkingTicket(
                        f"T{self._ticket_counter:04d}",
                        vehicle.license_plate,
                        spot.spot_id
                    )
        return None
    
    def exit(self, ticket: ParkingTicket) -> tuple[Vehicle, float] | None:
        """Process vehicle exit.
        
        Calculates fee and frees up the spot.
        
        Args:
            ticket: Parking ticket to process
            
        Returns:
            Tuple of (vehicle, fee) or None if invalid ticket
        """
        if ticket.spot_id not in self._spots:
            return None
        
        spot = self._spots[ticket.spot_id]
        vehicle = spot.remove_vehicle()
        
        if vehicle is None:
            return None
        
        fee = ticket.calculate_fee(self.hourly_rate)
        return (vehicle, fee)
