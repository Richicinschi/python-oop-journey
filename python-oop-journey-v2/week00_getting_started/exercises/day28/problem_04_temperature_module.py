"""Problem 04: Temperature Conversion Module

Topic: Specialized conversion module with aliases
Difficulty: Medium

Create a temperature conversion module that supports Celsius, Fahrenheit,
and Kelvin conversions. The module should be usable with different import
styles.

Required functions:
- celsius_to_fahrenheit(c): Convert C to F
- fahrenheit_to_celsius(f): Convert F to C
- celsius_to_kelvin(c): Convert C to K
- kelvin_to_celsius(k): Convert K to C
- fahrenheit_to_kelvin(f): Convert F to K
- kelvin_to_fahrenheit(k): Convert K to F
- convert_temperature(value, from_scale, to_scale): General converter

Scales: "celsius", "fahrenheit", "kelvin"

Example usage:
    >>> import temperature_module as temp
    >>> temp.celsius_to_fahrenheit(0)
    32.0
    >>> temp.convert_temperature(100, "celsius", "fahrenheit")
    212.0
    >>> from temperature_module import celsius_to_kelvin
    >>> celsius_to_kelvin(0)
    273.15
"""

from __future__ import annotations

ABSOLUTE_ZERO_C: float = -273.15


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit.

    Formula: (C × 9/5) + 32 = F
    """
    raise NotImplementedError("Implement celsius_to_fahrenheit")


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius.

    Formula: (F - 32) × 5/9 = C
    """
    raise NotImplementedError("Implement fahrenheit_to_celsius")


def celsius_to_kelvin(celsius: float) -> float:
    """Convert Celsius to Kelvin.

    Formula: C + 273.15 = K
    """
    raise NotImplementedError("Implement celsius_to_kelvin")


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius.

    Formula: K - 273.15 = C
    """
    raise NotImplementedError("Implement kelvin_to_celsius")


def fahrenheit_to_kelvin(fahrenheit: float) -> float:
    """Convert Fahrenheit to Kelvin.

    Formula: (F - 32) × 5/9 + 273.15 = K
    """
    raise NotImplementedError("Implement fahrenheit_to_kelvin")


def kelvin_to_fahrenheit(kelvin: float) -> float:
    """Convert Kelvin to Fahrenheit.

    Formula: (K - 273.15) × 9/5 + 32 = F
    """
    raise NotImplementedError("Implement kelvin_to_fahrenheit")


def convert_temperature(value: float, from_scale: str, to_scale: str) -> float:
    """Convert temperature between any two scales.

    Args:
        value: The temperature value to convert
        from_scale: Source scale ("celsius", "fahrenheit", "kelvin")
        to_scale: Target scale ("celsius", "fahrenheit", "kelvin")

    Returns:
        Converted temperature value

    Raises:
        ValueError: If invalid scale is provided
    """
    raise NotImplementedError("Implement convert_temperature")
