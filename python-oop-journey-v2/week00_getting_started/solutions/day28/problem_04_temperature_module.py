"""Reference solution for Problem 04: Temperature Conversion Module."""

from __future__ import annotations

ABSOLUTE_ZERO_C: float = -273.15


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit.

    Formula: (C × 9/5) + 32 = F
    """
    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius.

    Formula: (F - 32) × 5/9 = C
    """
    return (fahrenheit - 32) * 5 / 9


def celsius_to_kelvin(celsius: float) -> float:
    """Convert Celsius to Kelvin.

    Formula: C + 273.15 = K
    """
    return celsius + 273.15


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius.

    Formula: K - 273.15 = C
    """
    return kelvin - 273.15


def fahrenheit_to_kelvin(fahrenheit: float) -> float:
    """Convert Fahrenheit to Kelvin.

    Formula: (F - 32) × 5/9 + 273.15 = K
    """
    return (fahrenheit - 32) * 5 / 9 + 273.15


def kelvin_to_fahrenheit(kelvin: float) -> float:
    """Convert Kelvin to Fahrenheit.

    Formula: (K - 273.15) × 9/5 + 32 = F
    """
    return (kelvin - 273.15) * 9 / 5 + 32


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
    from_lower = from_scale.lower()
    to_lower = to_scale.lower()

    valid_scales = {"celsius", "fahrenheit", "kelvin"}
    if from_lower not in valid_scales:
        raise ValueError(f"Invalid from_scale: {from_scale}")
    if to_lower not in valid_scales:
        raise ValueError(f"Invalid to_scale: {to_scale}")

    if from_lower == to_lower:
        return value

    # Convert to celsius first, then to target
    if from_lower == "fahrenheit":
        celsius = fahrenheit_to_celsius(value)
    elif from_lower == "kelvin":
        celsius = kelvin_to_celsius(value)
    else:
        celsius = value

    # Convert from celsius to target
    if to_lower == "fahrenheit":
        return celsius_to_fahrenheit(celsius)
    elif to_lower == "kelvin":
        return celsius_to_kelvin(celsius)
    else:
        return celsius
