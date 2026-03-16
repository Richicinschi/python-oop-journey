"""Solution for Problem 02: Shape ABC.

Demonstrates abstract properties with geometric shapes.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import math


class Shape(ABC):
    """Abstract base class for geometric shapes.
    
    All shapes must implement area and perimeter as properties.
    
    Example:
        >>> rect = Rectangle(5.0, 3.0)
        >>> rect.area
        15.0
        >>> rect.perimeter
        16.0
    """
    
    @property
    @abstractmethod
    def area(self) -> float:
        """Calculate and return the area of the shape."""
        pass
    
    @property
    @abstractmethod
    def perimeter(self) -> float:
        """Calculate and return the perimeter of the shape."""
        pass


class Rectangle(Shape):
    """A rectangle with width and height.
    
    Attributes:
        _width: The rectangle width.
        _height: The rectangle height.
    """
    
    def __init__(self, width: float, height: float) -> None:
        """Initialize rectangle.
        
        Args:
            width: The rectangle width (must be positive).
            height: The rectangle height (must be positive).
        
        Raises:
            ValueError: If width or height is not positive.
        """
        if width <= 0:
            raise ValueError("Width must be positive")
        if height <= 0:
            raise ValueError("Height must be positive")
        self._width = float(width)
        self._height = float(height)
    
    @property
    def area(self) -> float:
        """Calculate rectangle area."""
        return self._width * self._height
    
    @property
    def perimeter(self) -> float:
        """Calculate rectangle perimeter."""
        return 2 * (self._width + self._height)


class Circle(Shape):
    """A circle with radius.
    
    Attributes:
        _radius: The circle radius.
    """
    
    def __init__(self, radius: float) -> None:
        """Initialize circle.
        
        Args:
            radius: The circle radius (must be positive).
        
        Raises:
            ValueError: If radius is not positive.
        """
        if radius <= 0:
            raise ValueError("Radius must be positive")
        self._radius = float(radius)
    
    @property
    def area(self) -> float:
        """Calculate circle area using πr²."""
        return math.pi * self._radius ** 2
    
    @property
    def perimeter(self) -> float:
        """Calculate circle circumference using 2πr."""
        return 2 * math.pi * self._radius


class Triangle(Shape):
    """A triangle with three sides.
    
    Attributes:
        _side_a: First side length.
        _side_b: Second side length.
        _side_c: Third side length.
    """
    
    def __init__(self, side_a: float, side_b: float, side_c: float) -> None:
        """Initialize triangle.
        
        Args:
            side_a: Length of first side (must be positive).
            side_b: Length of second side (must be positive).
            side_c: Length of third side (must be positive).
        
        Raises:
            ValueError: If sides don't form a valid triangle
                       (sum of any two sides must exceed the third).
        """
        if side_a <= 0 or side_b <= 0 or side_c <= 0:
            raise ValueError("All sides must be positive")
        
        # Check triangle inequality
        if (side_a + side_b <= side_c or
            side_a + side_c <= side_b or
            side_b + side_c <= side_a):
            raise ValueError("Sides do not form a valid triangle")
        
        self._side_a = float(side_a)
        self._side_b = float(side_b)
        self._side_c = float(side_c)
    
    @property
    def area(self) -> float:
        """Calculate triangle area using Heron's formula."""
        s = (self._side_a + self._side_b + self._side_c) / 2
        return math.sqrt(s * (s - self._side_a) * (s - self._side_b) * (s - self._side_c))
    
    @property
    def perimeter(self) -> float:
        """Calculate triangle perimeter."""
        return self._side_a + self._side_b + self._side_c
