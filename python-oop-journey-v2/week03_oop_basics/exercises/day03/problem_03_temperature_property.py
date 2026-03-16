"""Exercise: Temperature Property.

Implement a Temperature class with automatic Celsius/Fahrenheit conversion.

TODO:
1. Store temperature internally as _celsius
2. Implement @property getter for celsius
3. Implement @celsius.setter with validation (above absolute zero)
4. Implement @property for fahrenheit with getter and setter
5. Implement read-only kelvin property
"""

from __future__ import annotations


class Temperature:
    """A temperature class with automatic unit conversion.
    
    Stores temperature internally in Celsius but provides
    properties for both Celsius and Fahrenheit.
    """
    
    def __init__(self, celsius: float = 0.0) -> None:
        """Initialize temperature in Celsius."""
        self._celsius = float(celsius)
    
    @property
    def celsius(self) -> float:
        """Get the temperature in Celsius."""
        # TODO: Return the internal _celsius value
        raise NotImplementedError("Return celsius")
    
    @celsius.setter
    def celsius(self, value: float) -> None:
        """Set the temperature in Celsius."""
        # TODO: Validate value is a number
        # TODO: Validate value is >= -273.15 (absolute zero)
        # TODO: Set _celsius
        raise NotImplementedError("Validate and set celsius")
    
    @property
    def fahrenheit(self) -> float:
        """Get the temperature in Fahrenheit."""
        # TODO: Convert celsius to fahrenheit
        # Formula: (celsius * 9/5) + 32
        raise NotImplementedError("Convert to fahrenheit")
    
    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        """Set the temperature in Fahrenheit."""
        # TODO: Validate value is a number
        # TODO: Validate value is >= -459.67 (absolute zero in F)
        # TODO: Convert fahrenheit to celsius and store
        # Formula: (value - 32) * 5/9
        raise NotImplementedError("Convert and store fahrenheit")
    
    @property
    def kelvin(self) -> float:
        """Get the temperature in Kelvin (read-only)."""
        # TODO: Return celsius + 273.15
        raise NotImplementedError("Return kelvin")
    
    def is_freezing(self) -> bool:
        """Check if temperature is at or below freezing (0°C)."""
        # TODO: Return True if celsius <= 0
        raise NotImplementedError("Check freezing")
    
    def is_boiling(self) -> bool:
        """Check if temperature is at or above boiling (100°C)."""
        # TODO: Return True if celsius >= 100
        raise NotImplementedError("Check boiling")
