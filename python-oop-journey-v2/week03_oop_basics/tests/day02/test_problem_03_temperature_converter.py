"""Tests for Problem 03: Temperature Converter."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day02.problem_03_temperature_converter import (
    TemperatureConverter,
)


class TestCelsiusToFahrenheit:
    """Test suite for celsius_to_fahrenheit."""
    
    def test_freezing_point(self) -> None:
        """Test 0°C = 32°F."""
        assert TemperatureConverter.celsius_to_fahrenheit(0) == 32.0
    
    def test_boiling_point(self) -> None:
        """Test 100°C = 212°F."""
        assert TemperatureConverter.celsius_to_fahrenheit(100) == 212.0
    
    def test_negative(self) -> None:
        """Test negative Celsius."""
        assert TemperatureConverter.celsius_to_fahrenheit(-40) == -40.0
        assert TemperatureConverter.celsius_to_fahrenheit(-17.78) == pytest.approx(-0.004, abs=0.01)
    
    def test_room_temperature(self) -> None:
        """Test typical room temperature."""
        assert TemperatureConverter.celsius_to_fahrenheit(20) == 68.0
        assert TemperatureConverter.celsius_to_fahrenheit(25) == 77.0


class TestFahrenheitToCelsius:
    """Test suite for fahrenheit_to_celsius."""
    
    def test_freezing_point(self) -> None:
        """Test 32°F = 0°C."""
        assert TemperatureConverter.fahrenheit_to_celsius(32) == 0.0
    
    def test_boiling_point(self) -> None:
        """Test 212°F = 100°C."""
        assert TemperatureConverter.fahrenheit_to_celsius(212) == 100.0
    
    def test_negative(self) -> None:
        """Test negative Fahrenheit."""
        assert TemperatureConverter.fahrenheit_to_celsius(-40) == -40.0
    
    def test_room_temperature(self) -> None:
        """Test typical room temperature."""
        assert TemperatureConverter.fahrenheit_to_celsius(68) == 20.0


class TestCelsiusToKelvin:
    """Test suite for celsius_to_kelvin."""
    
    def test_absolute_zero(self) -> None:
        """Test -273.15°C = 0K."""
        assert TemperatureConverter.celsius_to_kelvin(-273.15) == 0.0
    
    def test_freezing_point(self) -> None:
        """Test 0°C = 273.15K."""
        assert TemperatureConverter.celsius_to_kelvin(0) == 273.15
    
    def test_boiling_point(self) -> None:
        """Test 100°C = 373.15K."""
        assert TemperatureConverter.celsius_to_kelvin(100) == 373.15


class TestKelvinToCelsius:
    """Test suite for kelvin_to_celsius."""
    
    def test_absolute_zero(self) -> None:
        """Test 0K = -273.15°C."""
        assert TemperatureConverter.kelvin_to_celsius(0) == -273.15
    
    def test_freezing_point(self) -> None:
        """Test 273.15K = 0°C."""
        assert TemperatureConverter.kelvin_to_celsius(273.15) == 0.0
    
    def test_boiling_point(self) -> None:
        """Test 373.15K = 100°C."""
        assert TemperatureConverter.kelvin_to_celsius(373.15) == 100.0


class TestRoundTrip:
    """Test that conversions are reversible."""
    
    def test_celsius_fahrenheit_roundtrip(self) -> None:
        """Test C -> F -> C returns original."""
        original = 25.0
        fahrenheit = TemperatureConverter.celsius_to_fahrenheit(original)
        back = TemperatureConverter.fahrenheit_to_celsius(fahrenheit)
        assert back == pytest.approx(original, abs=0.0001)
    
    def test_celsius_kelvin_roundtrip(self) -> None:
        """Test C -> K -> C returns original."""
        original = 50.0
        kelvin = TemperatureConverter.celsius_to_kelvin(original)
        back = TemperatureConverter.kelvin_to_celsius(kelvin)
        assert back == pytest.approx(original, abs=0.0001)
