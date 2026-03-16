"""Exercise: Circle Radius Validation.

Implement a Circle class with strict type checking.

TODO:
1. Implement @property for radius with strict type checking
2. Implement @property for diameter with getter and setter
3. Implement read-only computed properties: area, circumference
4. Implement contains_point method

Hints:
    - Hint 1: Type check: isinstance(value, (int, float)) and not isinstance(value, bool)
    - Hint 2: diameter getter returns 2 * radius, setter sets radius = value / 2
    - Hint 3: contains_point: distance = sqrt(x² + y²), return distance <= radius
"""

from __future__ import annotations

import math
from typing import Union


class Circle:
    """A circle with validated radius and computed properties.
    
    Example:
        >>> c = Circle(5)
        >>> c.radius  # Should be 5.0
        >>> c.area  # Should be ~78.54
    """
    
    def __init__(self, radius: Union[int, float]) -> None:
        """Initialize a circle with radius."""
        self._radius: float = 0.0
        self.radius = radius  # Use setter for validation
    
    @property
    def radius(self) -> float:
        """Get the radius."""
        # TODO: Return _radius
        raise NotImplementedError("Return radius")
    
    @radius.setter
    def radius(self, value: Union[int, float]) -> None:
        """Set the radius with strict type checking."""
        # TODO: Validate value is int or float (not bool!)
        # Hint: bool is subclass of int, so check type(value) is bool
        # TODO: Validate value is positive
        raise NotImplementedError("Validate and set radius")
    
    @property
    def diameter(self) -> float:
        """Get the diameter."""
        # TODO: Return 2 * radius
        raise NotImplementedError("Return diameter")
    
    @diameter.setter
    def diameter(self, value: Union[int, float]) -> None:
        """Set the diameter (updates radius)."""
        # TODO: Validate value is positive number
        # TODO: Set radius to value / 2
        raise NotImplementedError("Set diameter")
    
    @property
    def area(self) -> float:
        """Get the area (read-only)."""
        # TODO: Return π * r² (use math.pi)
        raise NotImplementedError("Calculate area")
    
    @property
    def circumference(self) -> float:
        """Get the circumference (read-only)."""
        # TODO: Return 2 * π * r
        raise NotImplementedError("Calculate circumference")
    
    @property
    def is_unit_circle(self) -> bool:
        """Check if this is a unit circle (read-only)."""
        # TODO: Return True if radius == 1.0
        raise NotImplementedError("Check unit circle")
    
    def scale(self, factor: Union[int, float]) -> None:
        """Scale the circle by a factor."""
        # TODO: Validate factor is positive
        # TODO: Multiply radius by factor
        raise NotImplementedError("Scale circle")
    
    def contains_point(self, x: float, y: float) -> bool:
        """Check if a point is inside the circle.
        
        Assumes circle is centered at origin (0, 0).
        
        Args:
            x: The x-coordinate of the point.
            y: The y-coordinate of the point.
        
        Returns:
            True if point is inside or on the circle.
        """
        # TODO: Calculate distance from origin: sqrt(x² + y²)
        # TODO: Return True if distance <= radius
        raise NotImplementedError("Check point containment")
