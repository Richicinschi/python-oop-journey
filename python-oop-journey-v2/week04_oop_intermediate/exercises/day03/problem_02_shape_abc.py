"""Exercise: Shape ABC.

Create an abstract base class Shape with abstract properties for area
and perimeter, then implement concrete shape classes.

TODO:
1. Create Shape ABC with abstract property area -> float
2. Add abstract property perimeter -> float
3. Implement Rectangle class with width and height
4. Implement Circle class with radius
5. Implement Triangle class with three sides
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import math


class Shape(ABC):
    """Abstract base class for geometric shapes.
    
    All shapes must implement area and perimeter as properties.
    """
    
    @property
    @abstractmethod
    def area(self) -> float:
        """Calculate and return the area of the shape."""
        # TODO: Define abstract property
        raise NotImplementedError("area property must be implemented")
    
    @property
    @abstractmethod
    def perimeter(self) -> float:
        """Calculate and return the perimeter of the shape."""
        # TODO: Define abstract property
        raise NotImplementedError("perimeter property must be implemented")


class Rectangle(Shape):
    """A rectangle with width and height."""
    
    def __init__(self, width: float, height: float) -> None:
        """Initialize rectangle.
        
        Args:
            width: The rectangle width (must be positive).
            height: The rectangle height (must be positive).
        
        Raises:
            ValueError: If width or height is not positive.
        """
        # TODO: Validate and set width and height
        raise NotImplementedError("Initialize rectangle")
    
    @property
    def area(self) -> float:
        """Calculate rectangle area."""
        # TODO: Return width * height
        raise NotImplementedError("Calculate area")
    
    @property
    def perimeter(self) -> float:
        """Calculate rectangle perimeter."""
        # TODO: Return 2 * (width + height)
        raise NotImplementedError("Calculate perimeter")


class Circle(Shape):
    """A circle with radius."""
    
    def __init__(self, radius: float) -> None:
        """Initialize circle.
        
        Args:
            radius: The circle radius (must be positive).
        
        Raises:
            ValueError: If radius is not positive.
        """
        # TODO: Validate and set radius
        raise NotImplementedError("Initialize circle")
    
    @property
    def area(self) -> float:
        """Calculate circle area using πr²."""
        # TODO: Return math.pi * radius ** 2
        raise NotImplementedError("Calculate area")
    
    @property
    def perimeter(self) -> float:
        """Calculate circle circumference using 2πr."""
        # TODO: Return 2 * math.pi * radius
        raise NotImplementedError("Calculate perimeter")


class Triangle(Shape):
    """A triangle with three sides."""
    
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
        # TODO: Validate triangle inequality and set sides
        raise NotImplementedError("Initialize triangle")
    
    @property
    def area(self) -> float:
        """Calculate triangle area using Heron's formula."""
        # TODO: Use Heron's formula: sqrt(s * (s-a) * (s-b) * (s-c))
        # where s = (a + b + c) / 2
        raise NotImplementedError("Calculate area")
    
    @property
    def perimeter(self) -> float:
        """Calculate triangle perimeter."""
        # TODO: Return sum of all three sides
        raise NotImplementedError("Calculate perimeter")
