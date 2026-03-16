"""Tests for Problem 03: Temperature Property."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day03.problem_03_temperature_property import (
    Temperature,
)


class TestTemperature:
    """Test suite for Temperature class."""
    
    def test_initialization_default(self) -> None:
        """Test temperature initialization with default value."""
        temp = Temperature()
        assert temp.celsius == 0.0
    
    def test_initialization_custom(self) -> None:
        """Test temperature initialization with custom value."""
        temp = Temperature(100.0)
        assert temp.celsius == 100.0
    
    def test_celsius_getter(self) -> None:
        """Test celsius getter."""
        temp = Temperature(25.0)
        assert temp.celsius == 25.0
    
    def test_celsius_setter(self) -> None:
        """Test celsius setter."""
        temp = Temperature()
        temp.celsius = 30.0
        assert temp.celsius == 30.0
    
    def test_celsius_setter_absolute_zero(self) -> None:
        """Test celsius setter allows absolute zero."""
        temp = Temperature()
        temp.celsius = -273.15
        assert temp.celsius == -273.15
    
    def test_celsius_setter_below_absolute_zero(self) -> None:
        """Test celsius setter rejects below absolute zero."""
        temp = Temperature()
        with pytest.raises(ValueError, match="absolute zero"):
            temp.celsius = -274.0
    
    def test_celsius_setter_non_number(self) -> None:
        """Test celsius setter rejects non-number."""
        temp = Temperature()
        with pytest.raises(TypeError, match="number"):
            temp.celsius = "hot"  # type: ignore
    
    def test_fahrenheit_getter_freezing(self) -> None:
        """Test fahrenheit getter at freezing point."""
        temp = Temperature(0.0)
        assert temp.fahrenheit == 32.0
    
    def test_fahrenheit_getter_boiling(self) -> None:
        """Test fahrenheit getter at boiling point."""
        temp = Temperature(100.0)
        assert temp.fahrenheit == 212.0
    
    def test_fahrenheit_getter_body_temp(self) -> None:
        """Test fahrenheit getter at body temperature."""
        temp = Temperature(37.0)
        assert abs(temp.fahrenheit - 98.6) < 0.1
    
    def test_fahrenheit_setter(self) -> None:
        """Test fahrenheit setter."""
        temp = Temperature()
        temp.fahrenheit = 212.0
        assert temp.celsius == 100.0
    
    def test_fahrenheit_setter_freezing(self) -> None:
        """Test fahrenheit setter at freezing point."""
        temp = Temperature()
        temp.fahrenheit = 32.0
        assert temp.celsius == 0.0
    
    def test_fahrenheit_setter_absolute_zero(self) -> None:
        """Test fahrenheit setter allows absolute zero."""
        temp = Temperature()
        temp.fahrenheit = -459.67
        assert abs(temp.celsius - (-273.15)) < 0.01
    
    def test_fahrenheit_setter_below_absolute_zero(self) -> None:
        """Test fahrenheit setter rejects below absolute zero."""
        temp = Temperature()
        with pytest.raises(ValueError, match="absolute zero"):
            temp.fahrenheit = -500.0
    
    def test_kelvin_getter(self) -> None:
        """Test kelvin getter."""
        temp = Temperature(0.0)
        assert temp.kelvin == 273.15
        temp.celsius = 100.0
        assert temp.kelvin == 373.15
    
    def test_kelvin_read_only(self) -> None:
        """Test that kelvin is read-only."""
        temp = Temperature()
        with pytest.raises(AttributeError):
            temp.kelvin = 300  # type: ignore
    
    def test_is_freezing_true(self) -> None:
        """Test is_freezing returns True at or below 0°C."""
        temp = Temperature(0.0)
        assert temp.is_freezing() is True
        temp.celsius = -10.0
        assert temp.is_freezing() is True
    
    def test_is_freezing_false(self) -> None:
        """Test is_freezing returns False above 0°C."""
        temp = Temperature(1.0)
        assert temp.is_freezing() is False
        temp.celsius = 25.0
        assert temp.is_freezing() is False
    
    def test_is_boiling_true(self) -> None:
        """Test is_boiling returns True at or above 100°C."""
        temp = Temperature(100.0)
        assert temp.is_boiling() is True
        temp.celsius = 110.0
        assert temp.is_boiling() is True
    
    def test_is_boiling_false(self) -> None:
        """Test is_boiling returns False below 100°C."""
        temp = Temperature(99.0)
        assert temp.is_boiling() is False
        temp.celsius = 25.0
        assert temp.is_boiling() is False
    
    def test_conversion_round_trip(self) -> None:
        """Test that conversions are consistent."""
        temp = Temperature(25.0)
        original_celsius = temp.celsius
        # Convert to fahrenheit and back
        temp.fahrenheit = temp.fahrenheit
        assert abs(temp.celsius - original_celsius) < 0.001
