"""Exercise: Rectangle Dimensions.

Implement a Rectangle class with computed properties.

TODO:
1. Implement @property for width and height with validation
2. Implement read-only computed properties: area, perimeter, diagonal
3. Implement read-only is_square property
4. Implement scale method
"""

from __future__ import annotations

import math


class Rectangle:
    """A rectangle with computed geometric properties.
    
    Example:
        >>> rect = Rectangle(5.0, 3.0)
        >>> rect.area  # Should be 15.0
    """
    
    def __init__(self, width: float, height: float) -> None:
        """Initialize a rectangle."""
        self._width: float = 0.0
        self._height: float = 0.0
        self.width = width  # Use setter
        self.height = height  # Use setter
    
    @property
    def width(self) -> float:
        """Get the width."""
        # TODO: Return _width
        raise NotImplementedError("Return width")
    
    @width.setter
    def width(self, value: float) -> None:
        """Set the width with validation."""
        # TODO: Validate value is positive
        # TODO: Set _width
        raise NotImplementedError("Validate and set width")
    
    @property
    def height(self) -> float:
        """Get the height."""
        # TODO: Return _height
        raise NotImplementedError("Return height")
    
    @height.setter
    def height(self, value: float) -> None:
        """Set the height with validation."""
        # TODO: Validate value is positive
        # TODO: Set _height
        raise NotImplementedError("Validate and set height")
    
    @property
    def area(self) -> float:
        """Calculate the area (read-only)."""
        # TODO: Return width * height
        raise NotImplementedError("Calculate area")
    
    @property
    def perimeter(self) -> float:
        """Calculate the perimeter (read-only)."""
        # TODO: Return 2 * (width + height)
        raise NotImplementedError("Calculate perimeter")
    
    @property
    def diagonal(self) -> float:
        """Calculate the diagonal length (read-only)."""
        # TODO: Use math.sqrt to calculate diagonal
        # Formula: sqrt(width² + height²)
        raise NotImplementedError("Calculate diagonal")
    
    @property
    def is_square(self) -> bool:
        """Check if the rectangle is a square (read-only)."""
        # TODO: Return True if width == height
        raise NotImplementedError("Check if square")
    
    def scale(self, factor: float) -> None:
        """Scale both dimensions by a factor."""
        # TODO: Validate factor is positive
        # TODO: Multiply both width and height by factor
        raise NotImplementedError("Scale dimensions")
