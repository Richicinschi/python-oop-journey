"""Tests for Problem 01: Parking Lot System."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day06.problem_01_parking_lot_system import (
    Car,
    Motorcycle,
    ParkingLot,
    ParkingSpot,
    ParkingTicket,
    SpotSize,
    Truck,
    VehicleType,
)


class TestVehicleTypes:
    """Tests for vehicle classes."""
    
    def test_motorcycle_creation(self) -> None:
        """Test motorcycle initialization."""
        bike = Motorcycle("M123")
        assert bike.license_plate == "M123"
        assert bike.vehicle_type == VehicleType.MOTORCYCLE
    
    def test_motorcycle_fits_all_spots(self) -> None:
        """Motorcycles fit in all spot sizes."""
        bike = Motorcycle("M123")
        assert bike.can_fit_in_spot(SpotSize.SMALL) is True
        assert bike.can_fit_in_spot(SpotSize.MEDIUM) is True
        assert bike.can_fit_in_spot(SpotSize.LARGE) is True
    
    def test_car_creation(self) -> None:
        """Test car initialization."""
        car = Car("C456")
        assert car.license_plate == "C456"
        assert car.vehicle_type == VehicleType.CAR
    
    def test_car_fits_medium_and_large(self) -> None:
        """Cars fit in medium and large spots only."""
        car = Car("C456")
        assert car.can_fit_in_spot(SpotSize.SMALL) is False
        assert car.can_fit_in_spot(SpotSize.MEDIUM) is True
        assert car.can_fit_in_spot(SpotSize.LARGE) is True
    
    def test_truck_creation(self) -> None:
        """Test truck initialization."""
        truck = Truck("T789")
        assert truck.license_plate == "T789"
        assert truck.vehicle_type == VehicleType.TRUCK
    
    def test_truck_fits_large_only(self) -> None:
        """Trucks only fit in large spots."""
        truck = Truck("T789")
        assert truck.can_fit_in_spot(SpotSize.SMALL) is False
        assert truck.can_fit_in_spot(SpotSize.MEDIUM) is False
        assert truck.can_fit_in_spot(SpotSize.LARGE) is True


class TestParkingSpot:
    """Tests for ParkingSpot class."""
    
    def test_spot_creation(self) -> None:
        """Test spot initialization."""
        spot = ParkingSpot("A1", SpotSize.MEDIUM)
        assert spot.spot_id == "A1"
        assert spot.size == SpotSize.MEDIUM
        assert spot.is_occupied is False
    
    def test_park_vehicle_success(self) -> None:
        """Test parking a compatible vehicle."""
        spot = ParkingSpot("A1", SpotSize.MEDIUM)
        car = Car("C123")
        assert spot.park(car) is True
        assert spot.is_occupied is True
    
    def test_park_vehicle_wrong_size(self) -> None:
        """Test parking incompatible vehicle size."""
        spot = ParkingSpot("A1", SpotSize.SMALL)
        car = Car("C123")
        assert spot.park(car) is False
        assert spot.is_occupied is False
    
    def test_park_when_occupied(self) -> None:
        """Test parking when spot already occupied."""
        spot = ParkingSpot("A1", SpotSize.MEDIUM)
        car1 = Car("C123")
        car2 = Car("C456")
        spot.park(car1)
        assert spot.park(car2) is False
    
    def test_remove_vehicle(self) -> None:
        """Test removing a vehicle."""
        spot = ParkingSpot("A1", SpotSize.MEDIUM)
        car = Car("C123")
        spot.park(car)
        removed = spot.remove_vehicle()
        assert removed == car
        assert spot.is_occupied is False
    
    def test_remove_from_empty_spot(self) -> None:
        """Test removing from empty spot returns None."""
        spot = ParkingSpot("A1", SpotSize.MEDIUM)
        assert spot.remove_vehicle() is None


class TestParkingTicket:
    """Tests for ParkingTicket class."""
    
    def test_ticket_creation(self) -> None:
        """Test ticket initialization."""
        ticket = ParkingTicket("T001", "ABC123", "A1")
        assert ticket.ticket_id == "T001"
        assert ticket.license_plate == "ABC123"
        assert ticket.spot_id == "A1"
        assert ticket.entry_time is not None
    
    def test_calculate_fee_one_hour(self) -> None:
        """Test fee calculation for short stay."""
        ticket = ParkingTicket("T001", "ABC123", "A1")
        # Since we can't wait, we just verify the calculation method exists
        # and returns a positive value for hourly rate
        fee = ticket.calculate_fee(5.0)
        assert fee >= 5.0  # At least 1 hour minimum


class TestParkingLot:
    """Tests for ParkingLot class."""
    
    def test_lot_creation(self) -> None:
        """Test parking lot initialization."""
        lot = ParkingLot("Downtown", 5.0)
        assert lot.name == "Downtown"
        assert lot.hourly_rate == 5.0
    
    def test_add_spot(self) -> None:
        """Test adding spots to lot."""
        lot = ParkingLot("Downtown", 5.0)
        lot.add_spot("A1", SpotSize.MEDIUM)
        spots = lot.get_available_spots()
        assert len(spots) == 1
    
    def test_get_available_spots_by_size(self) -> None:
        """Test filtering available spots by size."""
        lot = ParkingLot("Downtown", 5.0)
        lot.add_spot("A1", SpotSize.SMALL)
        lot.add_spot("A2", SpotSize.MEDIUM)
        lot.add_spot("A3", SpotSize.LARGE)
        
        medium_spots = lot.get_available_spots(SpotSize.MEDIUM)
        assert len(medium_spots) == 1
        assert medium_spots[0].spot_id == "A2"
    
    def test_enter_no_spots_available(self) -> None:
        """Test entry when no spots available."""
        lot = ParkingLot("Downtown", 5.0)
        car = Car("C123")
        assert lot.enter(car) is None
    
    def test_enter_success(self) -> None:
        """Test successful entry."""
        lot = ParkingLot("Downtown", 5.0)
        lot.add_spot("A1", SpotSize.MEDIUM)
        car = Car("C123")
        
        ticket = lot.enter(car)
        assert ticket is not None
        assert ticket.license_plate == "C123"
        assert ticket.spot_id == "A1"
    
    def test_enter_assigns_correct_size(self) -> None:
        """Test that correct spot size is assigned."""
        lot = ParkingLot("Downtown", 5.0)
        lot.add_spot("A1", SpotSize.SMALL)  # Small spot
        lot.add_spot("A2", SpotSize.MEDIUM)  # Medium spot
        
        car = Car("C123")  # Car needs medium
        ticket = lot.enter(car)
        assert ticket is not None
        assert ticket.spot_id == "A2"
    
    def test_exit_invalid_ticket(self) -> None:
        """Test exit with invalid ticket."""
        lot = ParkingLot("Downtown", 5.0)
        ticket = ParkingTicket("T001", "ABC123", "NONEXISTENT")
        assert lot.exit(ticket) is None
    
    def test_exit_success(self) -> None:
        """Test successful exit."""
        lot = ParkingLot("Downtown", 10.0)
        lot.add_spot("A1", SpotSize.MEDIUM)
        car = Car("C123")
        
        ticket = lot.enter(car)
        result = lot.exit(ticket)
        
        assert result is not None
        returned_car, fee = result
        assert returned_car == car
        assert isinstance(fee, float)
        
        # Spot should now be available again
        assert len(lot.get_available_spots()) == 1
    
    def test_multiple_vehicles(self) -> None:
        """Test parking multiple vehicles."""
        lot = ParkingLot("Downtown", 5.0)
        lot.add_spot("A1", SpotSize.MEDIUM)
        lot.add_spot("A2", SpotSize.MEDIUM)
        
        car1 = Car("C001")
        car2 = Car("C002")
        
        ticket1 = lot.enter(car1)
        ticket2 = lot.enter(car2)
        
        assert ticket1 is not None
        assert ticket2 is not None
        assert ticket1.spot_id != ticket2.spot_id
    
    def test_motorcycle_fits_small_spot(self) -> None:
        """Test motorcycle takes small spot when available."""
        lot = ParkingLot("Downtown", 5.0)
        lot.add_spot("A1", SpotSize.SMALL)
        
        bike = Motorcycle("M123")
        ticket = lot.enter(bike)
        
        assert ticket is not None
        assert ticket.spot_id == "A1"
