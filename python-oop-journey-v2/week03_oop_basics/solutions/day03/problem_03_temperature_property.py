"""Solution for Problem 03: Temperature Property.

Demonstrates @property for automatic unit conversion between
Celsius and Fahrenheit.
"""

from __future__ import annotations


class Temperature:
    """A temperature class with automatic Celsius/Fahrenheit conversion.
    
    This class stores temperature internally in Celsius but provides
    properties for both Celsius and Fahrenheit access.
    
    Example:
        >>> temp = Temperature(0)  # 0 degrees Celsius
        >>> temp.celsius
        0.0
        >>> temp.fahrenheit
        32.0
        >>> temp.fahrenheit = 212  # Set to boiling point
        >>> temp.celsius
        100.0
    """
    
    def __init__(self, celsius: float = 0.0) -> None:
        """Initialize temperature in Celsius.
        
        Args:
            celsius: The initial temperature in Celsius (default 0.0).
        """
        self._celsius = float(celsius)
    
    @property
    def celsius(self) -> float:
        """Get the temperature in Celsius.
        
        Returns:
            The temperature in Celsius.
        """
        return self._celsius
    
    @celsius.setter
    def celsius(self, value: float) -> None:
        """Set the temperature in Celsius.
        
        Args:
            value: The new temperature in Celsius.
        
        Raises:
            TypeError: If value is not a number.
            ValueError: If temperature is below absolute zero (-273.15°C).
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Temperature must be a number")
        if value < -273.15:
            raise ValueError("Temperature cannot be below absolute zero (-273.15°C)")
        self._celsius = float(value)
    
    @property
    def fahrenheit(self) -> float:
        """Get the temperature in Fahrenheit.
        
        Returns:
            The temperature in Fahrenheit.
        """
        return (self._celsius * 9 / 5) + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        """Set the temperature in Fahrenheit.
        
        Args:
            value: The new temperature in Fahrenheit.
        
        Raises:
            TypeError: If value is not a number.
            ValueError: If temperature is below absolute zero (-459.67°F).
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Temperature must be a number")
        if value < -459.67:
            raise ValueError("Temperature cannot be below absolute zero (-459.67°F)")
        self._celsius = (value - 32) * 5 / 9
    
    @property
    def kelvin(self) -> float:
        """Get the temperature in Kelvin (read-only property).
        
        Returns:
            The temperature in Kelvin.
        """
        return self._celsius + 273.15
    
    def is_freezing(self) -> bool:
        """Check if temperature is at or below freezing (0°C).
        
        Returns:
            True if temperature is at or below 0°C, False otherwise.
        """
        return self._celsius <= 0
    
    def is_boiling(self) -> bool:
        """Check if temperature is at or above boiling (100°C).
        
        Returns:
            True if temperature is at or above 100°C, False otherwise.
        """
        return self._celsius >= 100
