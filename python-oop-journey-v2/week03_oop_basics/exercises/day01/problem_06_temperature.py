"""Problem 06: Temperature Converter

Topic: Unit conversion, validation
Difficulty: Easy

Create a Temperature class that handles Celsius/Fahrenheit conversion.

Examples:
    >>> temp = Temperature(100, "C")
    >>> temp.value
    100.0
    >>> temp.scale
    'C'
    >>> temp.to_fahrenheit()
    212.0
    >>> temp2 = Temperature(32, "F")
    >>> temp2.to_celsius()
    0.0
    >>> temp3 = Temperature(-300, "C")  # Invalid, too low
    Traceback (most recent call last):
        ...
    ValueError: Temperature below absolute zero

Requirements:
    - __init__ takes value (float) and scale (str, either 'C' or 'F')
    - to_celsius() returns temperature in Celsius
    - to_fahrenheit() returns temperature in Fahrenheit
    - Validate scale is 'C' or 'F' (case-insensitive)
    - Validate temperature is not below absolute zero (-273.15 C, -459.67 F)
    - Store value as float internally
"""

from __future__ import annotations


class Temperature:
    """A class representing temperature with Celsius/Fahrenheit conversion."""

    ABSOLUTE_ZERO_C = -273.15
    ABSOLUTE_ZERO_F = -459.67

    def __init__(self, value: float, scale: str) -> None:
        """Initialize temperature with value and scale.
        
        Args:
            value: The temperature value
            scale: Either 'C' for Celsius or 'F' for Fahrenheit
            
        Raises:
            ValueError: If scale is invalid or below absolute zero
        """
        raise NotImplementedError("Initialize and validate temperature")

    def to_celsius(self) -> float:
        """Return the temperature in Celsius."""
        raise NotImplementedError("Implement to_celsius method")

    def to_fahrenheit(self) -> float:
        """Return the temperature in Fahrenheit."""
        raise NotImplementedError("Implement to_fahrenheit method")

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        raise NotImplementedError("Implement __str__ method")

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        raise NotImplementedError("Implement __repr__ method")
