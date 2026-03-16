"""Problem 04: Range Validator

Topic: Descriptor enforcing min/max
Difficulty: Easy

Create a descriptor that enforces numeric range constraints.
"""

from __future__ import annotations

from typing import TypeVar, Generic

T = TypeVar('T', int, float)


class RangeValidator:
    """A descriptor that validates numeric ranges.
    
    The descriptor should:
    - Accept min and max values
    - Accept an optional value type (int or float)
    - Validate that values are within the range [min, max]
    - Validate that values are of the correct type
    - Raise ValueError or TypeError for invalid values
    
    Attributes:
        min_value: Minimum allowed value (inclusive)
        max_value: Maximum allowed value (inclusive)
        value_type: Expected type (int or float)
    """
    
    def __init__(
        self,
        min_value: int | float,
        max_value: int | float,
        value_type: type[int] | type[float] = int
    ) -> None:
        """Initialize with range constraints.
        
        Args:
            min_value: Minimum allowed value (inclusive)
            max_value: Maximum allowed value (inclusive)
            value_type: Expected numeric type
        """
        raise NotImplementedError("Implement RangeValidator.__init__")
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Called when descriptor is assigned to class.
        
        Args:
            owner: The class
            name: The attribute name
        """
        raise NotImplementedError("Implement RangeValidator.__set_name__")
    
    def __get__(self, instance: object | None, owner: type) -> int | float | RangeValidator:
        """Get the attribute value.
        
        Args:
            instance: The instance, or None for class access
            owner: The owner class
            
        Returns:
            The stored value, or self if class access
        """
        raise NotImplementedError("Implement RangeValidator.__get__")
    
    def __set__(self, instance: object, value: int | float) -> None:
        """Set the attribute with range validation.
        
        Args:
            instance: The instance
            value: The value to set
            
        Raises:
            TypeError: If value is not of expected type
            ValueError: If value is outside valid range
        """
        raise NotImplementedError("Implement RangeValidator.__set__")


class Temperature:
    """Temperature reading with validated range.
    
    Attributes:
        celsius: Temperature in Celsius (-273.15 to 1000)
        fahrenheit: Temperature in Fahrenheit (-459.67 to 1832)
    """
    
    celsius = RangeValidator(-273.15, 1000.0, float)  # Absolute zero to reasonable max
    fahrenheit = RangeValidator(-459.67, 1832.0, float)
    
    def __init__(self, celsius: float = 0.0) -> None:
        """Initialize with Celsius temperature.
        
        Args:
            celsius: Temperature in Celsius
        """
        raise NotImplementedError("Implement Temperature.__init__")


class Score:
    """A game score with validated range.
    
    Attributes:
        value: The score value (0-100)
        level: The difficulty level (1-10)
    """
    
    value = RangeValidator(0, 100, int)
    level = RangeValidator(1, 10, int)
    
    def __init__(self, value: int = 0, level: int = 1) -> None:
        """Initialize score.
        
        Args:
            value: Score value (0-100)
            level: Difficulty level (1-10)
        """
        raise NotImplementedError("Implement Score.__init__")


class Percentage:
    """A percentage value (0-100).
    
    Attributes:
        value: The percentage (0-100)
    """
    
    value = RangeValidator(0, 100, int)
    
    def __init__(self, value: int = 0) -> None:
        """Initialize percentage.
        
        Args:
            value: Percentage value (0-100)
        """
        raise NotImplementedError("Implement Percentage.__init__")
    
    def __str__(self) -> str:
        """Return percentage as string.
        
        Returns:
            String like "50%"
        """
        raise NotImplementedError("Implement Percentage.__str__")
    
    def __repr__(self) -> str:
        """Return detailed representation.
        
        Returns:
            String like "Percentage(50)"
        """
        raise NotImplementedError("Implement Percentage.__repr__")
