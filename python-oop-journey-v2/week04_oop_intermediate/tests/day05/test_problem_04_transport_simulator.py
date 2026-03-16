"""Tests for Problem 04: Transport Simulator."""

from __future__ import annotations

import pytest
from abc import ABC

from week04_oop_intermediate.solutions.day05.problem_04_transport_simulator import (
    Transport,
    Car,
    Bike,
    Bus,
    simulate_transport,
)


class TestTransportABC:
    """Test suite for Transport abstract base class."""
    
    def test_transport_is_abstract(self) -> None:
        """Test that Transport cannot be instantiated."""
        assert issubclass(Transport, ABC)
        with pytest.raises(TypeError, match="abstract"):
            Transport()


class TestCar:
    """Test suite for Car."""
    
    def test_initialization(self) -> None:
        """Test car initialization."""
        car = Car("Toyota Camry", 15.0, 5)
        assert car.model == "Toyota Camry"
        assert car.fuel_efficiency == 15.0
        assert car.get_capacity() == 5
    
    def test_initialization_default_capacity(self) -> None:
        """Test car with default capacity."""
        car = Car("Honda Civic", 18.0)
        assert car.get_capacity() == 5
    
    def test_move(self) -> None:
        """Test move method."""
        car = Car("Toyota Camry", 15.0, 5)
        result = car.move(100.0)
        assert result == "Toyota Camry drove 100.0km"
    
    def test_get_fuel_cost(self) -> None:
        """Test fuel cost calculation."""
        car = Car("Toyota Camry", 15.0, 5)  # 15 km/l
        # 100 km / 15 km/l = 6.67 liters * $1.50 = $10.00
        result = car.get_fuel_cost(100.0)
        assert result == 10.0
    
    def test_get_fuel_cost_zero_distance(self) -> None:
        """Test fuel cost for zero distance."""
        car = Car("Toyota Camry", 15.0, 5)
        result = car.get_fuel_cost(0.0)
        assert result == 0.0


class TestBike:
    """Test suite for Bike."""
    
    def test_initialization(self) -> None:
        """Test bike initialization."""
        bike = Bike("Trek Mountain", 1)
        assert bike.model == "Trek Mountain"
        assert bike.get_capacity() == 1
    
    def test_initialization_default_capacity(self) -> None:
        """Test bike with default capacity."""
        bike = Bike("Giant Road")
        assert bike.get_capacity() == 1
    
    def test_move(self) -> None:
        """Test move method."""
        bike = Bike("Trek Mountain", 1)
        result = bike.move(50.0)
        assert result == "Trek Mountain cycled 50.0km"
    
    def test_get_fuel_cost(self) -> None:
        """Test fuel cost is always 0."""
        bike = Bike("Trek Mountain", 1)
        result = bike.get_fuel_cost(100.0)
        assert result == 0.0


class TestBus:
    """Test suite for Bus."""
    
    def test_initialization(self) -> None:
        """Test bus initialization."""
        bus = Bus("Route 42", 8.0, 50)
        assert bus.route == "Route 42"
        assert bus.fuel_efficiency == 8.0
        assert bus.get_capacity() == 50
    
    def test_initialization_default_capacity(self) -> None:
        """Test bus with default capacity."""
        bus = Bus("Route 1", 8.0)
        assert bus.get_capacity() == 50
    
    def test_move(self) -> None:
        """Test move method."""
        bus = Bus("Route 42", 8.0, 50)
        result = bus.move(25.0)
        assert result == "Bus Route 42 traveled 25.0km"
    
    def test_get_fuel_cost(self) -> None:
        """Test fuel cost calculation (cheaper diesel)."""
        bus = Bus("Route 42", 8.0, 50)  # 8 km/l
        # 100 km / 8 km/l = 12.5 liters * $1.20 = $15.00
        result = bus.get_fuel_cost(100.0)
        assert result == 15.0


class TestSimulateTransport:
    """Test suite for simulate_transport function."""
    
    def test_empty_list(self) -> None:
        """Test with empty list."""
        result = simulate_transport([], 100.0)
        
        assert result["movements"] == []
        assert result["total_capacity"] == 0
        assert result["total_fuel_cost"] == 0.0
    
    def test_single_transport(self) -> None:
        """Test with single transport."""
        transports = [Car("Toyota Camry", 15.0, 5)]
        result = simulate_transport(transports, 100.0)
        
        assert len(result["movements"]) == 1
        assert "Toyota Camry drove 100.0km" in result["movements"]
        assert result["total_capacity"] == 5
        assert result["total_fuel_cost"] == 10.0
    
    def test_mixed_transports(self) -> None:
        """Test polymorphic simulation with mixed transports."""
        transports = [
            Car("Toyota Camry", 15.0, 5),
            Bike("Trek Mountain", 1),
            Bus("Route 42", 8.0, 50),
        ]
        result = simulate_transport(transports, 100.0)
        
        assert len(result["movements"]) == 3
        assert "Toyota Camry drove 100.0km" in result["movements"]
        assert "Trek Mountain cycled 100.0km" in result["movements"]
        assert "Bus Route 42 traveled 100.0km" in result["movements"]
        
        assert result["total_capacity"] == 56  # 5 + 1 + 50
        assert result["total_fuel_cost"] == 25.0  # 10.0 + 0.0 + 15.0
    
    def test_preserves_order(self) -> None:
        """Test that movements are in same order as input."""
        transports = [
            Bus("Route 1", 8.0, 50),
            Car("Honda", 18.0, 5),
            Bike("Trek", 1),
        ]
        result = simulate_transport(transports, 50.0)
        
        assert result["movements"][0] == "Bus Route 1 traveled 50.0km"
        assert result["movements"][1] == "Honda drove 50.0km"
        assert result["movements"][2] == "Trek cycled 50.0km"
    
    def test_zero_distance(self) -> None:
        """Test simulation with zero distance."""
        transports = [
            Car("Toyota", 15.0, 5),
            Bike("Trek", 1),
        ]
        result = simulate_transport(transports, 0.0)
        
        assert result["movements"][0] == "Toyota drove 0.0km"
        assert result["total_fuel_cost"] == 0.0
