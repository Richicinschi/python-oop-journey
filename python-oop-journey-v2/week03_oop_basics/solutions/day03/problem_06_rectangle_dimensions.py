"""Solution for Problem 06: Rectangle Dimensions.

Demonstrates @property for computed values like area and perimeter.
"""

from __future__ import annotations

import math


class Rectangle:
    """A rectangle with computed geometric properties.
    
    This class demonstrates read-only computed properties that are
    derived from the core dimensions (width and height).
    
    Example:
        >>> rect = Rectangle(5.0, 3.0)
        >>> rect.area
        15.0
        >>> rect.perimeter
        16.0
        >>> rect.is_square
        False
    """
    
    def __init__(self, width: float, height: float) -> None:
        """Initialize a rectangle.
        
        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
        
        Raises:
            TypeError: If width or height is not a number.
            ValueError: If width or height is negative or zero.
        """
        self.width = width  # Use setter for validation
        self.height = height  # Use setter for validation
    
    @property
    def width(self) -> float:
        """Get the width.
        
        Returns:
            The width of the rectangle.
        """
        return self._width
    
    @width.setter
    def width(self, value: float) -> None:
        """Set the width.
        
        Args:
            value: The new width.
        
        Raises:
            TypeError: If value is not a number.
            ValueError: If value is negative or zero.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Width must be a number")
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = float(value)
    
    @property
    def height(self) -> float:
        """Get the height.
        
        Returns:
            The height of the rectangle.
        """
        return self._height
    
    @height.setter
    def height(self, value: float) -> None:
        """Set the height.
        
        Args:
            value: The new height.
        
        Raises:
            TypeError: If value is not a number.
            ValueError: If value is negative or zero.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Height must be a number")
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = float(value)
    
    @property
    def area(self) -> float:
        """Calculate the area (read-only).
        
        Returns:
            The area of the rectangle (width * height).
        """
        return self._width * self._height
    
    @property
    def perimeter(self) -> float:
        """Calculate the perimeter (read-only).
        
        Returns:
            The perimeter of the rectangle (2 * (width + height)).
        """
        return 2 * (self._width + self._height)
    
    @property
    def diagonal(self) -> float:
        """Calculate the diagonal length (read-only).
        
        Returns:
            The length of the diagonal.
        """
        return math.sqrt(self._width ** 2 + self._height ** 2)
    
    @property
    def is_square(self) -> bool:
        """Check if the rectangle is a square (read-only).
        
        Returns:
            True if width equals height, False otherwise.
        """
        return self._width == self._height
    
    @property
    def aspect_ratio(self) -> float:
        """Calculate the aspect ratio (read-only).
        
        Returns:
            The ratio of width to height.
        """
        return self._width / self._height
    
    def scale(self, factor: float) -> None:
        """Scale both dimensions by a factor.
        
        Args:
            factor: The scaling factor.
        
        Raises:
            ValueError: If factor is not positive.
        """
        if factor <= 0:
            raise ValueError("Scale factor must be positive")
        self._width *= factor
        self._height *= factor
