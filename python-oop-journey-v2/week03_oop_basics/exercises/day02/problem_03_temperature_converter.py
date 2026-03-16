"""Problem 03: Temperature Converter

Topic: @staticmethod
Difficulty: Easy

Create a TemperatureConverter class with static methods for converting
between Celsius, Fahrenheit, and Kelvin.

Example:
    >>> TemperatureConverter.celsius_to_fahrenheit(0)
    32.0
    >>> TemperatureConverter.celsius_to_fahrenheit(100)
    212.0
    >>> TemperatureConverter.fahrenheit_to_celsius(32)
    0.0
    >>> TemperatureConverter.celsius_to_kelvin(0)
    273.15
    >>> TemperatureConverter.kelvin_to_celsius(273.15)
    0.0

Requirements:
    - celsius_to_fahrenheit(celsius: float) -> float
    - fahrenheit_to_celsius(fahrenheit: float) -> float
    - celsius_to_kelvin(celsius: float) -> float
    - kelvin_to_celsius(kelvin: float) -> float
    - All methods must be @staticmethod
    - Formulas:
      F = C * 9/5 + 32
      C = (F - 32) * 5/9
      K = C + 273.15
      C = K - 273.15
"""

from __future__ import annotations


class TemperatureConverter:
    """Utility class for temperature conversions."""
    
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Convert Celsius to Fahrenheit.
        
        Formula: F = C * 9/5 + 32
        
        Args:
            celsius: Temperature in Celsius
            
        Returns:
            Temperature in Fahrenheit
        """
        raise NotImplementedError("Implement celsius_to_fahrenheit")
    
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Convert Fahrenheit to Celsius.
        
        Formula: C = (F - 32) * 5/9
        
        Args:
            fahrenheit: Temperature in Fahrenheit
            
        Returns:
            Temperature in Celsius
        """
        raise NotImplementedError("Implement fahrenheit_to_celsius")
    
    @staticmethod
    def celsius_to_kelvin(celsius: float) -> float:
        """Convert Celsius to Kelvin.
        
        Formula: K = C + 273.15
        
        Args:
            celsius: Temperature in Celsius
            
        Returns:
            Temperature in Kelvin
        """
        raise NotImplementedError("Implement celsius_to_kelvin")
    
    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        """Convert Kelvin to Celsius.
        
        Formula: C = K - 273.15
        
        Args:
            kelvin: Temperature in Kelvin
            
        Returns:
            Temperature in Celsius
        """
        raise NotImplementedError("Implement kelvin_to_celsius")
