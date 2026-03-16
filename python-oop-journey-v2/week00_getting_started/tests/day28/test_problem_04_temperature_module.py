"""Tests for Problem 04: Temperature Conversion Module."""

from __future__ import annotations

import pytest

from week00_getting_started.solutions.day28.problem_04_temperature_module import (
    ABSOLUTE_ZERO_C,
    celsius_to_fahrenheit,
    celsius_to_kelvin,
    convert_temperature,
    fahrenheit_to_celsius,
    fahrenheit_to_kelvin,
    kelvin_to_celsius,
    kelvin_to_fahrenheit,
)


def test_absolute_zero_constant() -> None:
    """Test ABSOLUTE_ZERO_C constant."""
    assert ABSOLUTE_ZERO_C == -273.15


def test_celsius_to_fahrenheit() -> None:
    """Test Celsius to Fahrenheit conversion."""
    assert celsius_to_fahrenheit(0) == 32.0
    assert celsius_to_fahrenheit(100) == 212.0
    assert celsius_to_fahrenheit(-40) == -40.0


def test_fahrenheit_to_celsius() -> None:
    """Test Fahrenheit to Celsius conversion."""
    assert fahrenheit_to_celsius(32) == 0.0
    assert fahrenheit_to_celsius(212) == 100.0
    assert fahrenheit_to_celsius(-40) == -40.0


def test_celsius_to_kelvin() -> None:
    """Test Celsius to Kelvin conversion."""
    assert celsius_to_kelvin(0) == 273.15
    assert celsius_to_kelvin(100) == 373.15
    assert celsius_to_kelvin(-273.15) == 0.0


def test_kelvin_to_celsius() -> None:
    """Test Kelvin to Celsius conversion."""
    assert kelvin_to_celsius(273.15) == 0.0
    assert kelvin_to_celsius(373.15) == 100.0
    assert kelvin_to_celsius(0) == -273.15


def test_fahrenheit_to_kelvin() -> None:
    """Test Fahrenheit to Kelvin conversion."""
    assert round(fahrenheit_to_kelvin(32), 2) == 273.15
    assert round(fahrenheit_to_kelvin(212), 2) == 373.15


def test_kelvin_to_fahrenheit() -> None:
    """Test Kelvin to Fahrenheit conversion."""
    assert round(kelvin_to_fahrenheit(273.15), 2) == 32.0
    assert round(kelvin_to_fahrenheit(373.15), 2) == 212.0


def test_convert_temperature_same_scale() -> None:
    """Test conversion to same scale returns same value."""
    assert convert_temperature(100, "celsius", "celsius") == 100
    assert convert_temperature(50, "fahrenheit", "fahrenheit") == 50
    assert convert_temperature(300, "kelvin", "kelvin") == 300


def test_convert_temperature_celsius_to_fahrenheit() -> None:
    """Test convert_temperature celsius to fahrenheit."""
    assert convert_temperature(0, "celsius", "fahrenheit") == 32.0
    assert convert_temperature(100, "celsius", "fahrenheit") == 212.0


def test_convert_temperature_celsius_to_kelvin() -> None:
    """Test convert_temperature celsius to kelvin."""
    assert convert_temperature(0, "celsius", "kelvin") == 273.15


def test_convert_temperature_fahrenheit_to_celsius() -> None:
    """Test convert_temperature fahrenheit to celsius."""
    assert convert_temperature(32, "fahrenheit", "celsius") == 0.0


def test_convert_temperature_kelvin_to_celsius() -> None:
    """Test convert_temperature kelvin to celsius."""
    assert convert_temperature(273.15, "kelvin", "celsius") == 0.0


def test_convert_temperature_case_insensitive() -> None:
    """Test convert_temperature is case-insensitive."""
    assert convert_temperature(0, "Celsius", "Fahrenheit") == 32.0
    assert convert_temperature(0, "CELSIUS", "KELVIN") == 273.15


def test_convert_temperature_invalid_from_scale() -> None:
    """Test convert_temperature raises error for invalid from_scale."""
    with pytest.raises(ValueError, match="Invalid from_scale"):
        convert_temperature(100, "invalid", "celsius")


def test_convert_temperature_invalid_to_scale() -> None:
    """Test convert_temperature raises error for invalid to_scale."""
    with pytest.raises(ValueError, match="Invalid to_scale"):
        convert_temperature(100, "celsius", "invalid")
