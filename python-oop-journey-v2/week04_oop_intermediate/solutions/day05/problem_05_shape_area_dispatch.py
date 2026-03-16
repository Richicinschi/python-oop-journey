"""Solution for Problem 05: Shape Area Dispatch.

Demonstrates polymorphic area calculation for mixed shapes.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract base class for shapes."""
    
    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape.
        
        Returns:
            Area as a float.
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the shape name.
        
        Returns:
            String name of the shape.
        """
        pass


class Rectangle(Shape):
    """Rectangle shape implementation.
    
    Attributes:
        width: Rectangle width.
        height: Rectangle height.
    """
    
    def __init__(self, width: float, height: float) -> None:
        """Initialize rectangle.
        
        Args:
            width: Rectangle width.
            height: Rectangle height.
        """
        self.width = width
        self.height = height
    
    def area(self) -> float:
        """Calculate rectangle area."""
        return self.width * self.height
    
    def get_name(self) -> str:
        """Return shape name."""
        return "Rectangle"


class Circle(Shape):
    """Circle shape implementation.
    
    Attributes:
        radius: Circle radius.
    """
    
    def __init__(self, radius: float) -> None:
        """Initialize circle.
        
        Args:
            radius: Circle radius.
        """
        self.radius = radius
    
    def area(self) -> float:
        """Calculate circle area."""
        return math.pi * self.radius ** 2
    
    def get_name(self) -> str:
        """Return shape name."""
        return "Circle"


class Triangle(Shape):
    """Triangle shape implementation.
    
    Attributes:
        base: Triangle base length.
        height: Triangle height.
    """
    
    def __init__(self, base: float, height: float) -> None:
        """Initialize triangle.
        
        Args:
            base: Triangle base length.
            height: Triangle height.
        """
        self.base = base
        self.height = height
    
    def area(self) -> float:
        """Calculate triangle area."""
        return 0.5 * self.base * self.height
    
    def get_name(self) -> str:
        """Return shape name."""
        return "Triangle"


class Square(Rectangle):
    """Square shape - inherits from Rectangle.
    
    A square is a special case of rectangle where width = height.
    """
    
    def __init__(self, side: float) -> None:
        """Initialize square.
        
        Args:
            side: Square side length.
        """
        super().__init__(side, side)
        self.side = side
    
    def get_name(self) -> str:
        """Return shape name."""
        return "Square"


def calculate_total_area(shapes: list[Shape]) -> float:
    """Calculate total area of all shapes.
    
    This function demonstrates polymorphism - it works with any
    Shape subclass without knowing the specific type.
    
    Args:
        shapes: List of Shape instances.
    
    Returns:
        Total area of all shapes.
    """
    return sum(shape.area() for shape in shapes)


def get_shape_summary(shapes: list[Shape]) -> dict:
    """Get summary statistics for shapes.
    
    Args:
        shapes: List of Shape instances.
    
    Returns:
        Dictionary with summary statistics.
    """
    total_area = 0.0
    by_type: dict[str, int] = {}
    
    for shape in shapes:
        total_area += shape.area()
        name = shape.get_name()
        by_type[name] = by_type.get(name, 0) + 1
    
    return {
        "total_area": round(total_area, 2),
        "count": len(shapes),
        "by_type": by_type,
    }
