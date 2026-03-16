"""Tests for Problem 01: Car with Engine Component."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day06.problem_01_car_with_engine_component import (
    Car,
    ElectricMotor,
    Engine,
    PowerSource,
)


class TestPowerSource:
    """Tests for the PowerSource abstract base class."""
    
    def test_power_source_is_abstract(self) -> None:
        """Test that PowerSource cannot be instantiated."""
        with pytest.raises(TypeError):
            PowerSource()


class TestEngine:
    """Tests for the Engine class."""
    
    def test_engine_init(self) -> None:
        """Test Engine initialization."""
        engine = Engine(200, "gasoline")
        assert engine.horsepower == 200
        assert engine.fuel_type == "gasoline"
    
    def test_engine_start(self) -> None:
        """Test Engine start method."""
        engine = Engine(200, "gasoline")
        result = engine.start()
        assert "200 HP" in result
        assert "gasoline" in result
        assert "roars" in result.lower()
    
    def test_engine_get_specs(self) -> None:
        """Test Engine get_specs method."""
        engine = Engine(200, "gasoline")
        assert engine.get_specs() == "200 HP gasoline engine"
    
    def test_engine_is_power_source(self) -> None:
        """Test that Engine is a PowerSource."""
        engine = Engine(150, "diesel")
        assert isinstance(engine, PowerSource)


class TestElectricMotor:
    """Tests for the ElectricMotor class."""
    
    def test_electric_motor_init(self) -> None:
        """Test ElectricMotor initialization."""
        motor = ElectricMotor(150)
        assert motor.kilowatts == 150
    
    def test_electric_motor_start(self) -> None:
        """Test ElectricMotor start method."""
        motor = ElectricMotor(150)
        result = motor.start()
        assert "150 kW" in result
        assert "hums" in result.lower()
    
    def test_electric_motor_get_specs(self) -> None:
        """Test ElectricMotor get_specs method."""
        motor = ElectricMotor(150)
        assert motor.get_specs() == "150 kW electric motor"
    
    def test_electric_motor_is_power_source(self) -> None:
        """Test that ElectricMotor is a PowerSource."""
        motor = ElectricMotor(100)
        assert isinstance(motor, PowerSource)


class TestCar:
    """Tests for the Car class."""
    
    def test_car_init_with_engine(self) -> None:
        """Test Car initialization with Engine."""
        engine = Engine(200, "gasoline")
        car = Car("Toyota", "Camry", engine)
        assert car.make == "Toyota"
        assert car.model == "Camry"
        assert car.power_source == engine
        assert not car.is_running()
    
    def test_car_init_with_electric_motor(self) -> None:
        """Test Car initialization with ElectricMotor."""
        motor = ElectricMotor(150)
        car = Car("Tesla", "Model 3", motor)
        assert car.make == "Tesla"
        assert car.model == "Model 3"
        assert isinstance(car.power_source, ElectricMotor)
    
    def test_car_start_with_engine(self) -> None:
        """Test starting a car with an engine."""
        engine = Engine(200, "gasoline")
        car = Car("Toyota", "Camry", engine)
        result = car.start()
        assert "Toyota Camry starting:" in result
        assert "roars" in result.lower()
        assert car.is_running()
    
    def test_car_start_with_electric_motor(self) -> None:
        """Test starting a car with an electric motor."""
        motor = ElectricMotor(150)
        car = Car("Tesla", "Model 3", motor)
        result = car.start()
        assert "Tesla Model 3 starting:" in result
        assert "hums" in result.lower()
        assert car.is_running()
    
    def test_car_stop(self) -> None:
        """Test stopping a car."""
        engine = Engine(200, "gasoline")
        car = Car("Toyota", "Camry", engine)
        car.start()
        result = car.stop()
        assert "Toyota Camry stopped" in result
        assert not car.is_running()
    
    def test_car_swap_power_source(self) -> None:
        """Test swapping the car's power source."""
        engine = Engine(200, "gasoline")
        car = Car("Toyota", "Camry", engine)
        
        motor = ElectricMotor(150)
        result = car.swap_power_source(motor)
        
        assert car.power_source == motor
        assert "Swapped" in result
        assert "gasoline engine" in result
        assert "electric motor" in result
    
    def test_car_get_specs(self) -> None:
        """Test getting car specifications."""
        engine = Engine(200, "gasoline")
        car = Car("Toyota", "Camry", engine)
        specs = car.get_specs()
        assert "Toyota Camry" in specs
        assert "200 HP gasoline engine" in specs
    
    def test_car_str_running(self) -> None:
        """Test string representation when running."""
        engine = Engine(200, "gasoline")
        car = Car("Toyota", "Camry", engine)
        car.start()
        result = str(car)
        assert "Toyota Camry" in result
        assert "running" in result
    
    def test_car_str_stopped(self) -> None:
        """Test string representation when stopped."""
        engine = Engine(200, "gasoline")
        car = Car("Toyota", "Camry", engine)
        result = str(car)
        assert "Toyota Camry" in result
        assert "stopped" in result
    
    def test_car_uses_composition(self) -> None:
        """Test that Car uses composition, not inheritance."""
        assert not issubclass(Car, PowerSource)
        assert not issubclass(Car, Engine)
        assert not issubclass(Car, ElectricMotor)
