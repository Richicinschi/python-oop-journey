"""Tests for Problem 04: Transport Interface."""

from __future__ import annotations

import math
import pytest
from abc import ABC

from week04_oop_intermediate.solutions.day03.problem_04_transport_interface import (
    Transport,
    Car,
    Bicycle,
    ElectricScooter,
)


class TestTransportABC:
    """Test suite for Transport abstract base class."""
    
    def test_transport_is_abstract(self) -> None:
        """Test that Transport cannot be instantiated."""
        assert issubclass(Transport, ABC)
        with pytest.raises(TypeError, match="abstract"):
            Transport("test")
    
    def test_transport_has_abstract_max_speed(self) -> None:
        """Test that Transport defines abstract max_speed property."""
        assert hasattr(Transport, 'max_speed')
    
    def test_transport_has_abstract_move(self) -> None:
        """Test that Transport defines abstract move method."""
        assert hasattr(Transport, 'move')
    
    def test_transport_has_abstract_get_location(self) -> None:
        """Test that Transport defines abstract get_location method."""
        assert hasattr(Transport, 'get_location')
    
    def test_transport_has_concrete_distance_from_origin(self) -> None:
        """Test that Transport provides concrete distance_from_origin."""
        car = Car("test", 50.0)
        car._x = 3.0
        car._y = 4.0
        assert car.distance_from_origin() == 5.0


class TestCar:
    """Test suite for Car."""
    
    def test_initialization(self) -> None:
        """Test car initialization."""
        car = Car("Honda", 50.0)
        assert car.name == "Honda"
        assert car.fuel_capacity == 50.0
        assert car.current_fuel == 50.0
        assert car._x == 0.0
        assert car._y == 0.0
    
    def test_max_speed(self) -> None:
        """Test max_speed property."""
        car = Car("Honda", 50.0)
        assert car.max_speed == 120.0
    
    def test_get_location_initial(self) -> None:
        """Test initial location."""
        car = Car("Honda", 50.0)
        assert car.get_location() == (0.0, 0.0)
    
    def test_move_north(self) -> None:
        """Test moving north (0 degrees)."""
        car = Car("Honda", 50.0)
        car.move(10.0, 0.0)
        x, y = car.get_location()
        assert x == pytest.approx(0.0, abs=0.001)
        assert y == pytest.approx(10.0, abs=0.001)
    
    def test_move_east(self) -> None:
        """Test moving east (90 degrees)."""
        car = Car("Honda", 50.0)
        car.move(10.0, 90.0)
        x, y = car.get_location()
        assert x == pytest.approx(10.0, abs=0.001)
        assert y == pytest.approx(0.0, abs=0.001)
    
    def test_move_consumes_fuel(self) -> None:
        """Test that movement consumes fuel."""
        car = Car("Honda", 50.0)
        initial_fuel = car.current_fuel
        car.move(10.0, 0.0)
        # 10 km * 0.1 L/km = 1 L consumed
        assert car.current_fuel == initial_fuel - 1.0
    
    def test_move_insufficient_fuel_raises(self) -> None:
        """Test that moving with insufficient fuel raises ValueError."""
        car = Car("Honda", 1.0)  # Only 1 liter
        with pytest.raises(ValueError, match="fuel"):
            car.move(20.0, 0.0)  # Needs 2 liters
    
    def test_refuel(self) -> None:
        """Test refueling."""
        car = Car("Honda", 50.0)
        car.move(30.0, 0.0)  # Consumes 3 liters
        assert car.current_fuel == 47.0
        car.refuel(3.0)
        assert car.current_fuel == 50.0
    
    def test_refuel_does_not_exceed_capacity(self) -> None:
        """Test that refueling doesn't exceed capacity."""
        car = Car("Honda", 50.0)
        car.move(10.0, 0.0)  # Consumes 1 liter
        car.refuel(100.0)  # Try to add too much
        assert car.current_fuel == 50.0


class TestBicycle:
    """Test suite for Bicycle."""
    
    def test_initialization(self) -> None:
        """Test bicycle initialization."""
        bike = Bicycle("Trek", 10.0)
        assert bike.name == "Trek"
        assert bike.rider_fatigue == 10.0
    
    def test_initialization_default_fatigue(self) -> None:
        """Test bicycle initialization with default fatigue."""
        bike = Bicycle("Trek")
        assert bike.rider_fatigue == 0.0
    
    def test_max_speed(self) -> None:
        """Test max_speed property."""
        bike = Bicycle("Trek")
        assert bike.max_speed == 25.0
    
    def test_move_increases_fatigue(self) -> None:
        """Test that movement increases fatigue."""
        bike = Bicycle("Trek")
        assert bike.rider_fatigue == 0.0
        bike.move(10.0, 0.0)
        assert bike.rider_fatigue == 10.0
    
    def test_move_changes_location(self) -> None:
        """Test that movement changes location."""
        bike = Bicycle("Trek")
        bike.move(10.0, 90.0)
        x, y = bike.get_location()
        assert x == pytest.approx(10.0, abs=0.001)
    
    def test_rest_resets_fatigue(self) -> None:
        """Test resting resets fatigue."""
        bike = Bicycle("Trek")
        bike.move(20.0, 0.0)
        assert bike.rider_fatigue == 20.0
        bike.rest()
        assert bike.rider_fatigue == 0.0
    
    def test_fatigue_accumulates(self) -> None:
        """Test that fatigue accumulates over multiple moves."""
        bike = Bicycle("Trek")
        bike.move(5.0, 0.0)
        bike.move(10.0, 90.0)
        bike.move(5.0, 180.0)
        assert bike.rider_fatigue == 20.0


class TestElectricScooter:
    """Test suite for ElectricScooter."""
    
    def test_initialization(self) -> None:
        """Test scooter initialization."""
        scooter = ElectricScooter("Xiaomi")
        assert scooter.name == "Xiaomi"
        assert scooter.battery == 100.0
    
    def test_max_speed(self) -> None:
        """Test max_speed property."""
        scooter = ElectricScooter("Xiaomi")
        assert scooter.max_speed == 20.0
    
    def test_move_consumes_battery(self) -> None:
        """Test that movement consumes battery."""
        scooter = ElectricScooter("Xiaomi")
        initial_battery = scooter.battery
        scooter.move(10.0, 0.0)
        # 10 km * 0.5 %/km = 5% consumed
        assert scooter.battery == initial_battery - 5.0
    
    def test_move_insufficient_battery_raises(self) -> None:
        """Test that moving with insufficient battery raises ValueError."""
        scooter = ElectricScooter("Xiaomi")
        scooter.battery = 10.0  # Only 10%
        with pytest.raises(ValueError, match="battery"):
            scooter.move(30.0, 0.0)  # Needs 15%
    
    def test_charge(self) -> None:
        """Test charging."""
        scooter = ElectricScooter("Xiaomi")
        scooter.move(50.0, 0.0)  # Consumes 25%
        assert scooter.battery == 75.0
        scooter.charge()
        assert scooter.battery == 100.0
    
    def test_charge_from_zero(self) -> None:
        """Test charging from empty."""
        scooter = ElectricScooter("Xiaomi")
        scooter.battery = 0.0
        scooter.charge()
        assert scooter.battery == 100.0
