"""Problem 05: Shape Hierarchy

Topic: Abstract Base Behavior with Calculations
Difficulty: Medium

Create a Shape base class with Circle, Rectangle, and Triangle subclasses,
demonstrating polymorphic area calculations.
"""

from __future__ import annotations

import math


class Shape:
    """Base class for geometric shapes.
    
    This class defines the interface that all shapes must implement.
    """
    
    def area(self) -> float:
        """Calculate and return the area of the shape.
        
        Returns:
            Area as a float
            
        Raises:
            NotImplementedError: Base class doesn't implement this
        """
        raise NotImplementedError("Subclasses must implement area()")
    
    def perimeter(self) -> float:
        """Calculate and return the perimeter of the shape.
        
        Returns:
            Perimeter as a float
            
        Raises:
            NotImplementedError: Base class doesn't implement this
        """
        raise NotImplementedError("Subclasses must implement perimeter()")
    
    def describe(self) -> str:
        """Return a description of the shape.
        
        Returns:
            String with shape name, area, and perimeter
        """
        raise NotImplementedError("Implement Shape.describe")
    
    def scale(self, factor: float) -> None:
        """Scale the shape by the given factor.
        
        Args:
            factor: Scaling factor (must be positive)
        """
        raise NotImplementedError("Subclasses must implement scale()")


class Circle(Shape):
    """A circle shape.
    
    Attributes:
        radius: Radius of the circle
    """
    
    def __init__(self, radius: float) -> None:
        """Initialize a Circle.
        
        Args:
            radius: Circle radius (must be non-negative)
        """
        raise NotImplementedError("Implement Circle.__init__")
    
    def area(self) -> float:
        """Calculate circle area: π * r²
        
        Returns:
            Area of the circle
        """
        raise NotImplementedError("Implement Circle.area")
    
    def perimeter(self) -> float:
        """Calculate circle circumference: 2 * π * r
        
        Returns:
            Circumference of the circle
        """
        raise NotImplementedError("Implement Circle.perimeter")
    
    def describe(self) -> str:
        """Override: Return circle description.
        
        Returns:
            "Circle(radius=X, area=Y, perimeter=Z)"
        """
        raise NotImplementedError("Implement Circle.describe")
    
    def scale(self, factor: float) -> None:
        """Override: Scale the radius.
        
        Args:
            factor: Multiply radius by this factor
        """
        raise NotImplementedError("Implement Circle.scale")
    
    def get_diameter(self) -> float:
        """Return the diameter of the circle.
        
        Returns:
            Diameter (2 * radius)
        """
        raise NotImplementedError("Implement Circle.get_diameter")


class Rectangle(Shape):
    """A rectangle shape.
    
    Attributes:
        width: Width of the rectangle
        height: Height of the rectangle
    """
    
    def __init__(self, width: float, height: float) -> None:
        """Initialize a Rectangle.
        
        Args:
            width: Rectangle width (must be non-negative)
            height: Rectangle height (must be non-negative)
        """
        raise NotImplementedError("Implement Rectangle.__init__")
    
    def area(self) -> float:
        """Calculate rectangle area: width * height
        
        Returns:
            Area of the rectangle
        """
        raise NotImplementedError("Implement Rectangle.area")
    
    def perimeter(self) -> float:
        """Calculate rectangle perimeter: 2 * (width + height)
        
        Returns:
            Perimeter of the rectangle
        """
        raise NotImplementedError("Implement Rectangle.perimeter")
    
    def describe(self) -> str:
        """Override: Return rectangle description.
        
        Returns:
            "Rectangle(WxH=XxY, area=Z, perimeter=W)"
        """
        raise NotImplementedError("Implement Rectangle.describe")
    
    def scale(self, factor: float) -> None:
        """Override: Scale both dimensions.
        
        Args:
            factor: Multiply both width and height by this factor
        """
        raise NotImplementedError("Implement Rectangle.scale")
    
    def is_square(self) -> bool:
        """Check if this rectangle is a square.
        
        Returns:
            True if width == height
        """
        raise NotImplementedError("Implement Rectangle.is_square")


class Triangle(Shape):
    """A triangle shape using three sides.
    
    Attributes:
        a: Length of side a
        b: Length of side b
        c: Length of side c
    """
    
    def __init__(self, a: float, b: float, c: float) -> None:
        """Initialize a Triangle.
        
        Args:
            a: Length of side a
            b: Length of side b
            c: Length of side c
            
        Note:
            Triangle inequality must hold: a + b > c, a + c > b, b + c > a
            If invalid, raise ValueError
        """
        raise NotImplementedError("Implement Triangle.__init__")
    
    def area(self) -> float:
        """Calculate triangle area using Heron's formula.
        
        s = (a + b + c) / 2
        area = sqrt(s * (s-a) * (s-b) * (s-c))
        
        Returns:
            Area of the triangle
        """
        raise NotImplementedError("Implement Triangle.area")
    
    def perimeter(self) -> float:
        """Calculate triangle perimeter: a + b + c
        
        Returns:
            Perimeter of the triangle
        """
        raise NotImplementedError("Implement Triangle.perimeter")
    
    def describe(self) -> str:
        """Override: Return triangle description.
        
        Returns:
            "Triangle(sides=X,Y,Z, area=W, perimeter=V)"
        """
        raise NotImplementedError("Implement Triangle.describe")
    
    def scale(self, factor: float) -> None:
        """Override: Scale all sides.
        
        Args:
            factor: Multiply all sides by this factor
        """
        raise NotImplementedError("Implement Triangle.scale")
    
    def get_triangle_type(self) -> str:
        """Classify the triangle by its sides.
        
        Returns:
            "equilateral" if all sides equal
            "isosceles" if exactly two sides equal
            "scalene" if all sides different
        """
        raise NotImplementedError("Implement Triangle.get_triangle_type")
