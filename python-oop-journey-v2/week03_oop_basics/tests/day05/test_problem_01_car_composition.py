"""Tests for Problem 01: Car Composition."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day05.problem_01_car_composition import (
    Car,
    Engine,
    Transmission,
    Wheel,
)


class TestEngine:
    """Tests for Engine class."""
    
    def test_engine_init(self) -> None:
        """Test engine initialization."""
        engine = Engine(200)
        assert engine.horsepower == 200
        assert engine.is_running is False
    
    def test_engine_start(self) -> None:
        """Test starting the engine."""
        engine = Engine(200)
        result = engine.start()
        assert "started" in result.lower()
        assert engine.is_running is True
    
    def test_engine_start_already_running(self) -> None:
        """Test starting an already running engine."""
        engine = Engine(200)
        engine.start()
        result = engine.start()
        assert "already running" in result.lower()
    
    def test_engine_stop(self) -> None:
        """Test stopping the engine."""
        engine = Engine(200)
        engine.start()
        result = engine.stop()
        assert "stopped" in result.lower()
        assert engine.is_running is False
    
    def test_engine_stop_already_stopped(self) -> None:
        """Test stopping an already stopped engine."""
        engine = Engine(200)
        result = engine.stop()
        assert "already stopped" in result.lower()


class TestTransmission:
    """Tests for Transmission class."""
    
    def test_transmission_init(self) -> None:
        """Test transmission initialization."""
        trans = Transmission(5)
        assert trans.gear_count == 5
        assert trans.current_gear == 0
    
    def test_shift_up(self) -> None:
        """Test shifting up through gears."""
        trans = Transmission(3)
        assert trans.shift_up() is True  # To gear 1
        assert trans.current_gear == 1
        assert trans.shift_up() is True  # To gear 2
        assert trans.shift_up() is True  # To gear 3
        assert trans.shift_up() is False  # Can't go above max
        assert trans.current_gear == 3
    
    def test_shift_down(self) -> None:
        """Test shifting down through gears."""
        trans = Transmission(3)
        trans.shift_up()  # To gear 1
        trans.shift_up()  # To gear 2
        assert trans.shift_down() is True  # To gear 1
        assert trans.current_gear == 1
        assert trans.shift_down() is True  # To neutral
        assert trans.shift_down() is False  # Can't go below 0
        assert trans.current_gear == 0
    
    def test_is_in_gear(self) -> None:
        """Test checking if in gear."""
        trans = Transmission(3)
        assert trans.is_in_gear() is False
        trans.shift_up()
        assert trans.is_in_gear() is True


class TestWheel:
    """Tests for Wheel class."""
    
    def test_wheel_init(self) -> None:
        """Test wheel initialization."""
        wheel = Wheel(17, "front_left")
        assert wheel.size == 17
        assert wheel.position == "front_left"
    
    def test_wheel_repr(self) -> None:
        """Test wheel string representation."""
        wheel = Wheel(17, "front_left")
        assert "17" in repr(wheel)
        assert "front_left" in repr(wheel)


class TestCar:
    """Tests for Car class."""
    
    def test_car_init(self) -> None:
        """Test car initialization with components."""
        car = Car("Toyota", "Camry", 200, 5, 17)
        assert car.make == "Toyota"
        assert car.model == "Camry"
        assert isinstance(car.engine, Engine)
        assert isinstance(car.transmission, Transmission)
        assert len(car.wheels) == 4
        assert all(isinstance(w, Wheel) for w in car.wheels)
    
    def test_car_start(self) -> None:
        """Test starting the car."""
        car = Car("Toyota", "Camry", 200, 5, 17)
        result = car.start()
        assert "started" in result.lower()
        assert car.engine.is_running is True
    
    def test_car_drive_not_running(self) -> None:
        """Test driving when engine is not running."""
        car = Car("Toyota", "Camry", 200, 5, 17)
        result = car.drive()
        assert "cannot drive" in result.lower()
        assert "engine" in result.lower()
    
    def test_car_drive_neutral(self) -> None:
        """Test driving in neutral."""
        car = Car("Toyota", "Camry", 200, 5, 17)
        car.start()
        result = car.drive()
        assert "cannot drive" in result.lower()
        assert "neutral" in result.lower()
    
    def test_car_drive_success(self) -> None:
        """Test successful driving."""
        car = Car("Toyota", "Camry", 200, 5, 17)
        car.start()
        car.shift_up()
        result = car.drive()
        assert "driving" in result.lower()
        assert "gear 1" in result.lower()
    
    def test_car_stop(self) -> None:
        """Test stopping the car."""
        car = Car("Toyota", "Camry", 200, 5, 17)
        car.start()
        car.shift_up()
        result = car.stop()
        assert "stopped" in result.lower()
        assert car.engine.is_running is False
        assert car.transmission.current_gear == 0
    
    def test_car_shift_up(self) -> None:
        """Test shifting up through the car."""
        car = Car("Toyota", "Camry", 200, 5, 17)
        result = car.shift_up()
        assert "shifted up" in result.lower()
        assert "gear 1" in result.lower()
    
    def test_car_shift_up_max(self) -> None:
        """Test shifting up at max gear."""
        car = Car("Toyota", "Camry", 200, 3, 17)
        car.shift_up()
        car.shift_up()
        car.shift_up()
        result = car.shift_up()
        assert "highest gear" in result.lower()
    
    def test_car_shift_down(self) -> None:
        """Test shifting down through the car."""
        car = Car("Toyota", "Camry", 200, 5, 17)
        car.shift_up()
        result = car.shift_down()
        assert "shifted down" in result.lower()
        assert "gear 0" in result.lower()
    
    def test_car_wheel_count(self) -> None:
        """Test getting wheel count."""
        car = Car("Toyota", "Camry", 200, 5, 17)
        assert car.get_wheel_count() == 4
