"""Problem 02: Celsius to Fahrenheit

Topic: Temperature conversion, arithmetic formulas
Difficulty: Easy

Write a function that converts a temperature from Celsius to Fahrenheit.

Formula: F = (C × 9/5) + 32

Examples:
    >>> celsius_to_fahrenheit(0)
    32.0
    >>> celsius_to_fahrenheit(100)
    212.0
    >>> celsius_to_fahrenheit(-40)
    -40.0

Requirements:
    - The function must accept a float or int for Celsius
    - The function must return a float
    - Handle negative temperatures correctly
"""

from __future__ import annotations


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert temperature from Celsius to Fahrenheit.

    Args:
        celsius: Temperature in Celsius

    Returns:
        Temperature in Fahrenheit
    """
    raise NotImplementedError("Implement celsius_to_fahrenheit")
