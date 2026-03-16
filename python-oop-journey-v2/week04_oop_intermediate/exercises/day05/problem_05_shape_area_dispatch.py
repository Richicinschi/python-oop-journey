"""Problem 05: Shape Area Dispatch.

Topic: Polymorphism
Difficulty: Medium

Create shape classes with area calculation.
Demonstrate polymorphic area calculation for mixed shape collections.

TODO:
1. Create Shape ABC with:
   - area(self) -> float (abstract)
   - get_name(self) -> str (abstract)

2. Create Rectangle class:
   - __init__(self, width: float, height: float)
   - area returns width * height
   - get_name returns "Rectangle"

3. Create Circle class:
   - __init__(self, radius: float)
   - area returns pi * radius^2
   - get_name returns "Circle"

4. Create Triangle class:
   - __init__(self, base: float, height: float)
   - area returns 0.5 * base * height
   - get_name returns "Triangle"

5. Create Square class (inherits from Rectangle):
   - __init__(self, side: float)
   - Call parent __init__ with side, side
   - get_name returns "Square"

6. Implement calculate_total_area(shapes: list) -> float
   that sums areas of all shapes polymorphically.

7. Implement get_shape_summary(shapes: list) -> dict
   that returns dict with 'total_area', 'count', and 'by_type' breakdown.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract base class for shapes."""
    
    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape.
        
        Returns:
            Area as a float.
        """
        raise NotImplementedError("area must be implemented")
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the shape name.
        
        Returns:
            String name of the shape.
        """
        raise NotImplementedError("get_name must be implemented")


class Rectangle(Shape):
    """Rectangle shape implementation."""
    
    def __init__(self, width: float, height: float) -> None:
        """Initialize rectangle.
        
        Args:
            width: Rectangle width.
            height: Rectangle height.
        """
        # TODO: Initialize attributes
        raise NotImplementedError("Initialize rectangle")
    
    def area(self) -> float:
        """Calculate rectangle area."""
        # TODO: Return width * height
        raise NotImplementedError("Implement area")
    
    def get_name(self) -> str:
        """Return shape name."""
        # TODO: Return "Rectangle"
        raise NotImplementedError("Implement get_name")


class Circle(Shape):
    """Circle shape implementation."""
    
    def __init__(self, radius: float) -> None:
        """Initialize circle.
        
        Args:
            radius: Circle radius.
        """
        # TODO: Initialize attributes
        raise NotImplementedError("Initialize circle")
    
    def area(self) -> float:
        """Calculate circle area."""
        # TODO: Return math.pi * radius ** 2
        raise NotImplementedError("Implement area")
    
    def get_name(self) -> str:
        """Return shape name."""
        # TODO: Return "Circle"
        raise NotImplementedError("Implement get_name")


class Triangle(Shape):
    """Triangle shape implementation."""
    
    def __init__(self, base: float, height: float) -> None:
        """Initialize triangle.
        
        Args:
            base: Triangle base length.
            height: Triangle height.
        """
        # TODO: Initialize attributes
        raise NotImplementedError("Initialize triangle")
    
    def area(self) -> float:
        """Calculate triangle area."""
        # TODO: Return 0.5 * base * height
        raise NotImplementedError("Implement area")
    
    def get_name(self) -> str:
        """Return shape name."""
        # TODO: Return "Triangle"
        raise NotImplementedError("Implement get_name")


class Square(Rectangle):
    """Square shape - inherits from Rectangle."""
    
    def __init__(self, side: float) -> None:
        """Initialize square.
        
        Args:
            side: Square side length.
        """
        # TODO: Call parent __init__ with side, side
        raise NotImplementedError("Initialize square")
    
    def get_name(self) -> str:
        """Return shape name."""
        # TODO: Return "Square"
        raise NotImplementedError("Implement get_name")


def calculate_total_area(shapes: list[Shape]) -> float:
    """Calculate total area of all shapes.
    
    Args:
        shapes: List of Shape instances.
    
    Returns:
        Total area of all shapes.
    """
    # TODO: Sum area() from all shapes
    raise NotImplementedError("Implement calculate_total_area")


def get_shape_summary(shapes: list[Shape]) -> dict:
    """Get summary statistics for shapes.
    
    Args:
        shapes: List of Shape instances.
    
    Returns:
        Dictionary with:
        - 'total_area': sum of all areas
        - 'count': number of shapes
        - 'by_type': dict mapping shape names to counts
    """
    # TODO: Build and return summary dict
    raise NotImplementedError("Implement get_shape_summary")
