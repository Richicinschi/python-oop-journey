"""Reference solution for Problem 06: Temperature Converter."""

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
        scale_upper = scale.upper()
        if scale_upper not in ('C', 'F'):
            raise ValueError("Scale must be 'C' or 'F'")
        
        value_float = float(value)
        
        # Validate against absolute zero
        if scale_upper == 'C' and value_float < self.ABSOLUTE_ZERO_C:
            raise ValueError("Temperature below absolute zero")
        if scale_upper == 'F' and value_float < self.ABSOLUTE_ZERO_F:
            raise ValueError("Temperature below absolute zero")
        
        self._value = value_float
        self._scale = scale_upper

    @property
    def value(self) -> float:
        """Return the temperature value."""
        return self._value

    @property
    def scale(self) -> str:
        """Return the temperature scale ('C' or 'F')."""
        return self._scale

    def to_celsius(self) -> float:
        """Return the temperature in Celsius."""
        if self._scale == 'C':
            return self._value
        # Convert F to C
        return (self._value - 32) * 5 / 9

    def to_fahrenheit(self) -> float:
        """Return the temperature in Fahrenheit."""
        if self._scale == 'F':
            return self._value
        # Convert C to F
        return (self._value * 9 / 5) + 32

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        return f"{self._value}°{self._scale}"

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"Temperature(value={self._value}, scale='{self._scale}')"
