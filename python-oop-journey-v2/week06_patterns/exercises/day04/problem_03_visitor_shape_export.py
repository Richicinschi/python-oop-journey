"""Problem 03: Visitor Shape Export

Topic: Visitor Pattern
Difficulty: Hard

Implement a shape export system using the Visitor pattern.
Different export formats (XML, JSON) are implemented as visitors that operate
on a hierarchy of shapes without modifying the shape classes.

HINTS:
- Hint 1 (Conceptual): Double dispatch is key. Shape.accept(visitor) calls 
  visitor.visit_shape(self). The shape decides WHICH visit method is called.
- Hint 2 (Structural): Each visitor needs visit_circle(), visit_rectangle(), 
  visit_triangle(). Each shape's accept() calls the corresponding visit method. 
  AreaCalculatorVisitor accumulates state across visits.
- Hint 3 (Edge Case): Heron's formula for triangle area: sqrt(s*(s-a)*(s-b)*(s-c)) 
  where s = (a+b+c)/2. Return 0 for invalid triangles (violating triangle inequality).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import override


class ShapeVisitor(ABC):
    """Abstract visitor defining operations for each shape type.
    
    Each concrete visitor implements export logic for all shape types.
    """
    
    @abstractmethod
    def visit_circle(self, circle: Circle) -> str:
        """Visit a Circle shape.
        
        Args:
            circle: Circle instance to visit
            
        Returns:
            Exported representation of the circle
        """
        raise NotImplementedError("Implement visit_circle")
    
    @abstractmethod
    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Visit a Rectangle shape.
        
        Args:
            rectangle: Rectangle instance to visit
            
        Returns:
            Exported representation of the rectangle
        """
        raise NotImplementedError("Implement visit_rectangle")
    
    @abstractmethod
    def visit_triangle(self, triangle: Triangle) -> str:
        """Visit a Triangle shape.
        
        Args:
            triangle: Triangle instance to visit
            
        Returns:
            Exported representation of the triangle
        """
        raise NotImplementedError("Implement visit_triangle")


class Shape(ABC):
    """Abstract base class for shapes.
    
    The accept() method enables the visitor pattern through double dispatch.
    """
    
    @abstractmethod
    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept a visitor and dispatch to appropriate visit method.
        
        Args:
            visitor: The visitor to accept
            
        Returns:
            Result of the visitor operation
        """
        raise NotImplementedError("Implement accept")
    
    @abstractmethod
    def get_area(self) -> float:
        """Calculate and return the area of the shape."""
        raise NotImplementedError("Implement get_area")


class Circle(Shape):
    """Circle shape with radius."""
    
    def __init__(self, radius: float, x: float = 0, y: float = 0) -> None:
        """Initialize a circle.
        
        Args:
            radius: Circle radius
            x: X-coordinate of center
            y: Y-coordinate of center
        """
        raise NotImplementedError("Implement Circle.__init__")
    
    @override
    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept visitor - calls visitor.visit_circle(self)."""
        raise NotImplementedError("Implement Circle.accept")
    
    @override
    def get_area(self) -> float:
        """Calculate circle area: πr²"""
        raise NotImplementedError("Implement Circle.get_area")


class Rectangle(Shape):
    """Rectangle shape with width and height."""
    
    def __init__(self, width: float, height: float, x: float = 0, y: float = 0) -> None:
        """Initialize a rectangle.
        
        Args:
            width: Rectangle width
            height: Rectangle height
            x: X-coordinate of top-left corner
            y: Y-coordinate of top-left corner
        """
        raise NotImplementedError("Implement Rectangle.__init__")
    
    @override
    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept visitor - calls visitor.visit_rectangle(self)."""
        raise NotImplementedError("Implement Rectangle.accept")
    
    @override
    def get_area(self) -> float:
        """Calculate rectangle area: width × height"""
        raise NotImplementedError("Implement Rectangle.get_area")


class Triangle(Shape):
    """Triangle shape defined by three sides."""
    
    def __init__(self, a: float, b: float, c: float, x: float = 0, y: float = 0) -> None:
        """Initialize a triangle.
        
        Args:
            a: Length of side a
            b: Length of side b
            c: Length of side c
            x: X-coordinate reference point
            y: Y-coordinate reference point
        """
        raise NotImplementedError("Implement Triangle.__init__")
    
    @override
    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept visitor - calls visitor.visit_triangle(self)."""
        raise NotImplementedError("Implement Triangle.accept")
    
    @override
    def get_area(self) -> float:
        """Calculate triangle area using Heron's formula."""
        raise NotImplementedError("Implement Triangle.get_area")


class XMLExportVisitor(ShapeVisitor):
    """Visitor that exports shapes to XML format.
    
    XML format example:
    <circle radius="5.0" x="0" y="0" area="78.54"/>
    """
    
    @override
    def visit_circle(self, circle: Circle) -> str:
        """Export circle as XML element."""
        raise NotImplementedError("Implement XMLExportVisitor.visit_circle")
    
    @override
    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Export rectangle as XML element."""
        raise NotImplementedError("Implement XMLExportVisitor.visit_rectangle")
    
    @override
    def visit_triangle(self, triangle: Triangle) -> str:
        """Export triangle as XML element."""
        raise NotImplementedError("Implement XMLExportVisitor.visit_triangle")


class JSONExportVisitor(ShapeVisitor):
    """Visitor that exports shapes to JSON format.
    
    JSON format example:
    {"type": "circle", "radius": 5.0, "x": 0, "y": 0, "area": 78.54}
    """
    
    @override
    def visit_circle(self, circle: Circle) -> str:
        """Export circle as JSON object."""
        raise NotImplementedError("Implement JSONExportVisitor.visit_circle")
    
    @override
    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Export rectangle as JSON object."""
        raise NotImplementedError("Implement JSONExportVisitor.visit_rectangle")
    
    @override
    def visit_triangle(self, triangle: Triangle) -> str:
        """Export triangle as JSON object."""
        raise NotImplementedError("Implement JSONExportVisitor.visit_triangle")


class AreaCalculatorVisitor(ShapeVisitor):
    """Visitor that calculates total area of visited shapes.
    
    Accumulates area across multiple shape visits.
    """
    
    def __init__(self) -> None:
        """Initialize area calculator with zero total."""
        raise NotImplementedError("Implement AreaCalculatorVisitor.__init__")
    
    @override
    def visit_circle(self, circle: Circle) -> str:
        """Add circle area to total. Returns running total as string."""
        raise NotImplementedError("Implement AreaCalculatorVisitor.visit_circle")
    
    @override
    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Add rectangle area to total. Returns running total as string."""
        raise NotImplementedError("Implement AreaCalculatorVisitor.visit_rectangle")
    
    @override
    def visit_triangle(self, triangle: Triangle) -> str:
        """Add triangle area to total. Returns running total as string."""
        raise NotImplementedError("Implement AreaCalculatorVisitor.visit_triangle")
    
    def get_total_area(self) -> float:
        """Return the accumulated total area."""
        raise NotImplementedError("Implement AreaCalculatorVisitor.get_total_area")
    
    def reset(self) -> None:
        """Reset the total area to zero."""
        raise NotImplementedError("Implement AreaCalculatorVisitor.reset")


class ShapeCollection:
    """A collection of shapes that can be visited."""
    
    def __init__(self) -> None:
        """Initialize empty shape collection."""
        raise NotImplementedError("Implement ShapeCollection.__init__")
    
    def add(self, shape: Shape) -> None:
        """Add a shape to the collection."""
        raise NotImplementedError("Implement ShapeCollection.add")
    
    def accept(self, visitor: ShapeVisitor) -> list[str]:
        """Apply visitor to all shapes and return results.
        
        Args:
            visitor: Visitor to apply to each shape
            
        Returns:
            List of results from visiting each shape
        """
        raise NotImplementedError("Implement ShapeCollection.accept")
