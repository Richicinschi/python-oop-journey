"""Tests for Problem 06: Temperature Converter."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day01.problem_06_temperature import Temperature


def test_temperature_creation_celsius() -> None:
    """Test creating temperature in Celsius."""
    temp = Temperature(100, "C")
    assert temp.value == 100.0
    assert temp.scale == "C"


def test_temperature_creation_fahrenheit() -> None:
    """Test creating temperature in Fahrenheit."""
    temp = Temperature(212, "F")
    assert temp.value == 212.0
    assert temp.scale == "F"


def test_celsius_to_fahrenheit() -> None:
    """Test converting Celsius to Fahrenheit."""
    temp = Temperature(100, "C")
    assert temp.to_fahrenheit() == 212.0


def test_fahrenheit_to_celsius() -> None:
    """Test converting Fahrenheit to Celsius."""
    temp = Temperature(212, "F")
    assert temp.to_celsius() == 100.0


def test_celsius_to_celsius() -> None:
    """Test Celsius to Celsius returns same value."""
    temp = Temperature(50, "C")
    assert temp.to_celsius() == 50.0


def test_fahrenheit_to_fahrenheit() -> None:
    """Test Fahrenheit to Fahrenheit returns same value."""
    temp = Temperature(100, "F")
    assert temp.to_fahrenheit() == 100.0


def test_freezing_point_celsius() -> None:
    """Test 0°C equals 32°F."""
    temp = Temperature(0, "C")
    assert temp.to_fahrenheit() == 32.0


def test_freezing_point_fahrenheit() -> None:
    """Test 32°F equals 0°C."""
    temp = Temperature(32, "F")
    assert temp.to_celsius() == 0.0


def test_body_temperature() -> None:
    """Test body temperature conversion."""
    temp = Temperature(37, "C")
    # 37°C = 98.6°F
    assert abs(temp.to_fahrenheit() - 98.6) < 0.1


def test_case_insensitive_scale() -> None:
    """Test that scale is case-insensitive."""
    temp1 = Temperature(100, "c")
    temp2 = Temperature(212, "f")
    assert temp1.scale == "C"
    assert temp2.scale == "F"


def test_invalid_scale() -> None:
    """Test that invalid scale raises ValueError."""
    with pytest.raises(ValueError):
        Temperature(100, "K")


def test_below_absolute_zero_celsius() -> None:
    """Test that temperature below absolute zero in Celsius raises ValueError."""
    with pytest.raises(ValueError):
        Temperature(-300, "C")


def test_below_absolute_zero_fahrenheit() -> None:
    """Test that temperature below absolute zero in Fahrenheit raises ValueError."""
    with pytest.raises(ValueError):
        Temperature(-500, "F")


def test_exact_absolute_zero_celsius() -> None:
    """Test that absolute zero in Celsius is valid."""
    temp = Temperature(-273.15, "C")
    assert temp.value == -273.15


def test_str_representation() -> None:
    """Test the __str__ method."""
    temp = Temperature(100, "C")
    result = str(temp)
    assert "100" in result
    assert "C" in result


def test_repr_representation() -> None:
    """Test the __repr__ method."""
    temp = Temperature(100, "C")
    result = repr(temp)
    assert "Temperature" in result
    assert "100" in result
