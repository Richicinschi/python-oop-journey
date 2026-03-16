"""Tests for Problem 01: Vehicle Hierarchy."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day01.problem_01_vehicle_hierarchy import (
    Vehicle, Car, Truck, Motorcycle
)


class TestVehicle:
    """Tests for the base Vehicle class."""
    
    def test_vehicle_init(self) -> None:
        vehicle = Vehicle("Generic", "Model", 2020)
        assert vehicle.brand == "Generic"
        assert vehicle.model == "Model"
        assert vehicle.year == 2020
    
    def test_vehicle_description(self) -> None:
        vehicle = Vehicle("Toyota", "Camry", 2023)
        assert vehicle.description() == "2023 Toyota Camry"
    
    def test_vehicle_start_engine(self) -> None:
        vehicle = Vehicle("Test", "Test", 2020)
        assert vehicle.start_engine() == "Engine starting..."
    
    def test_vehicle_honk(self) -> None:
        vehicle = Vehicle("Test", "Test", 2020)
        assert vehicle.honk() == "Beep!"


class TestCar:
    """Tests for the Car class."""
    
    def test_car_inheritance(self) -> None:
        car = Car("Toyota", "Camry", 2023, 4, 15.5)
        assert isinstance(car, Vehicle)
    
    def test_car_init(self) -> None:
        car = Car("Toyota", "Camry", 2023, 4, 15.5)
        assert car.brand == "Toyota"
        assert car.model == "Camry"
        assert car.year == 2023
        assert car.doors == 4
        assert car.trunk_capacity == 15.5
    
    def test_car_description_inherits(self) -> None:
        car = Car("Honda", "Civic", 2022, 2, 12.0)
        assert car.description() == "2022 Honda Civic"
    
    def test_car_start_engine_override(self) -> None:
        car = Car("Test", "Test", 2020, 4, 15.0)
        assert car.start_engine() == "Vroom! Car engine purring..."
    
    def test_car_honk_inherits(self) -> None:
        car = Car("Test", "Test", 2020, 4, 15.0)
        assert car.honk() == "Beep!"
    
    def test_car_open_trunk(self) -> None:
        car = Car("Toyota", "Camry", 2023, 4, 15.5)
        assert car.open_trunk() == "Trunk opened. Capacity: 15.5 cu ft"


class TestTruck:
    """Tests for the Truck class."""
    
    def test_truck_inheritance(self) -> None:
        truck = Truck("Ford", "F-150", 2023, 2000.0, True)
        assert isinstance(truck, Vehicle)
    
    def test_truck_init(self) -> None:
        truck = Truck("Ford", "F-150", 2023, 2000.0, True)
        assert truck.brand == "Ford"
        assert truck.bed_capacity == 2000.0
        assert truck.has_four_wheel_drive is True
    
    def test_truck_start_engine_override(self) -> None:
        truck = Truck("Ford", "F-150", 2023, 2000.0, False)
        assert truck.start_engine() == "Rumble! Truck engine roaring..."
    
    def test_truck_honk_override(self) -> None:
        truck = Truck("Ford", "F-150", 2023, 2000.0, False)
        assert truck.honk() == "HONK HONK!"
    
    def test_truck_tow_success(self) -> None:
        truck = Truck("Ford", "F-150", 2023, 2000.0, True)
        assert truck.tow(1500.0) == "Successfully towing 1500.0 lbs"
    
    def test_truck_tow_failure(self) -> None:
        truck = Truck("Ford", "F-150", 2023, 2000.0, True)
        assert truck.tow(2500.0) == "Cannot tow 2500.0 lbs. Max capacity: 2000.0 lbs"


class TestMotorcycle:
    """Tests for the Motorcycle class."""
    
    def test_motorcycle_inheritance(self) -> None:
        motorcycle = Motorcycle("Harley", "Sportster", 2023, 1200, False)
        assert isinstance(motorcycle, Vehicle)
    
    def test_motorcycle_init(self) -> None:
        motorcycle = Motorcycle("Harley", "Sportster", 2023, 1200, True)
        assert motorcycle.brand == "Harley"
        assert motorcycle.engine_cc == 1200
        assert motorcycle.has_sidecar is True
    
    def test_motorcycle_init_default_sidecar(self) -> None:
        motorcycle = Motorcycle("Honda", "CBR", 2023, 600)
        assert motorcycle.has_sidecar is False
    
    def test_motorcycle_start_engine_override(self) -> None:
        motorcycle = Motorcycle("Harley", "Sportster", 2023, 1200)
        assert motorcycle.start_engine() == "Rev! Motorcycle engine revving..."
    
    def test_motorcycle_wheelie_success(self) -> None:
        motorcycle = Motorcycle("Harley", "Sportster", 2023, 1200, False)
        assert motorcycle.wheelie() == "Doing a wheelie!"
    
    def test_motorcycle_wheelie_failure(self) -> None:
        motorcycle = Motorcycle("Harley", "Sportster", 2023, 1200, True)
        assert motorcycle.wheelie() == "Cannot do wheelie with sidecar attached"


class TestPolymorphism:
    """Tests demonstrating polymorphic behavior."""
    
    def test_polymorphic_start_engine(self) -> None:
        vehicles: list[Vehicle] = [
            Car("Toyota", "Camry", 2023, 4, 15.0),
            Truck("Ford", "F-150", 2023, 2000.0, True),
            Motorcycle("Harley", "Sportster", 2023, 1200)
        ]
        
        results = [v.start_engine() for v in vehicles]
        assert "Vroom!" in results[0]
        assert "Rumble!" in results[1]
        assert "Rev!" in results[2]
    
    def test_isinstance_checks(self) -> None:
        car = Car("Toyota", "Camry", 2023, 4, 15.0)
        assert isinstance(car, Car)
        assert isinstance(car, Vehicle)
        
        truck = Truck("Ford", "F-150", 2023, 2000.0, True)
        assert isinstance(truck, Truck)
        assert isinstance(truck, Vehicle)


class TestIssubclass:
    """Tests for class inheritance relationships."""
    
    def test_car_is_subclass_of_vehicle(self) -> None:
        assert issubclass(Car, Vehicle)
    
    def test_truck_is_subclass_of_vehicle(self) -> None:
        assert issubclass(Truck, Vehicle)
    
    def test_motorcycle_is_subclass_of_vehicle(self) -> None:
        assert issubclass(Motorcycle, Vehicle)
