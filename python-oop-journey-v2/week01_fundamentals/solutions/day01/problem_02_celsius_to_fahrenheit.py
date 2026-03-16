"""Reference solution for Problem 02: Celsius to Fahrenheit."""

from __future__ import annotations


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert temperature from Celsius to Fahrenheit.

    Formula: F = (C × 9/5) + 32

    Args:
        celsius: Temperature in Celsius

    Returns:
        Temperature in Fahrenheit
    """
    return (celsius * 9 / 5) + 32
