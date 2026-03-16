"""Solution for Problem 09: Circle Radius Validation.

Demonstrates @property with type checking and validation.
"""

from __future__ import annotations

import math
from typing import Union


class Circle:
    """A circle with validated radius and computed properties.
    
    This class demonstrates strict type checking in property setters
    along with computed geometric properties.
    
    Example:
        >>> c = Circle(5)
        >>> c.radius
        5.0
        >>> c.area
        78.53981633974483
        >>> c.diameter
        10.0
    """
    
    def __init__(self, radius: Union[int, float]) -> None:
        """Initialize a circle with radius.
        
        Args:
            radius: The circle's radius (must be positive number).
        
        Raises:
            TypeError: If radius is not a number.
            ValueError: If radius is negative or zero.
        """
        self._radius: float = 0.0
        self.radius = radius  # Use setter for validation
    
    @property
    def radius(self) -> float:
        """Get the radius.
        
        Returns:
            The circle's radius.
        """
        return self._radius
    
    @radius.setter
    def radius(self, value: Union[int, float]) -> None:
        """Set the radius with strict type and value checking.
        
        Args:
            value: The new radius.
        
        Raises:
            TypeError: If value is not an int or float.
            ValueError: If value is negative or zero.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Radius must be a number, got {type(value).__name__}")
        if isinstance(value, bool):  # bool is subclass of int
            raise TypeError("Radius must be a number, got bool")
        if value <= 0:
            raise ValueError(f"Radius must be positive, got {value}")
        self._radius = float(value)
    
    @property
    def diameter(self) -> float:
        """Get the diameter (read-only).
        
        Returns:
            The circle's diameter (2 * radius).
        """
        return self._radius * 2
    
    @diameter.setter
    def diameter(self, value: Union[int, float]) -> None:
        """Set the diameter (updates radius).
        
        Args:
            value: The new diameter.
        
        Raises:
            TypeError: If value is not a number.
            ValueError: If value is negative or zero.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Diameter must be a number, got {type(value).__name__}")
        if isinstance(value, bool):
            raise TypeError("Diameter must be a number, got bool")
        if value <= 0:
            raise ValueError(f"Diameter must be positive, got {value}")
        self._radius = float(value) / 2
    
    @property
    def area(self) -> float:
        """Get the area (read-only).
        
        Returns:
            The circle's area (π * r²).
        """
        return math.pi * self._radius ** 2
    
    @property
    def circumference(self) -> float:
        """Get the circumference (read-only).
        
        Returns:
            The circle's circumference (2 * π * r).
        """
        return 2 * math.pi * self._radius
    
    @property
    def is_unit_circle(self) -> bool:
        """Check if this is a unit circle (read-only).
        
        Returns:
            True if radius is 1, False otherwise.
        """
        return math.isclose(self._radius, 1.0)
    
    def scale(self, factor: Union[int, float]) -> None:
        """Scale the circle by a factor.
        
        Args:
            factor: The scaling factor.
        
        Raises:
            TypeError: If factor is not a number.
            ValueError: If factor is not positive.
        """
        if not isinstance(factor, (int, float)):
            raise TypeError("Scale factor must be a number")
        if factor <= 0:
            raise ValueError("Scale factor must be positive")
        self._radius *= factor
    
    def contains_point(self, x: float, y: float) -> bool:
        """Check if a point is inside the circle.
        
        The circle is assumed to be centered at origin (0, 0).
        
        Args:
            x: The x-coordinate of the point.
            y: The y-coordinate of the point.
        
        Returns:
            True if point is inside or on the circle, False otherwise.
        """
        distance = math.sqrt(x ** 2 + y ** 2)
        return distance <= self._radius
