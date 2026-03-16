"""Solution for Problem 03: Temperature Converter."""

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
        return celsius * 9 / 5 + 32
    
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Convert Fahrenheit to Celsius.
        
        Formula: C = (F - 32) * 5/9
        
        Args:
            fahrenheit: Temperature in Fahrenheit
            
        Returns:
            Temperature in Celsius
        """
        return (fahrenheit - 32) * 5 / 9
    
    @staticmethod
    def celsius_to_kelvin(celsius: float) -> float:
        """Convert Celsius to Kelvin.
        
        Formula: K = C + 273.15
        
        Args:
            celsius: Temperature in Celsius
            
        Returns:
            Temperature in Kelvin
        """
        return celsius + 273.15
    
    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        """Convert Kelvin to Celsius.
        
        Formula: C = K - 273.15
        
        Args:
            kelvin: Temperature in Kelvin
            
        Returns:
            Temperature in Celsius
        """
        return kelvin - 273.15
