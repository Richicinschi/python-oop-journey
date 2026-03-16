"""Reference solution for Problem 03: Visitor Shape Export.

WHY VISITOR?
The Visitor pattern separates algorithms from the objects they operate on.
This is useful when:
- You have many distinct operations on a class hierarchy
- Adding new operations should be easy without modifying existing classes
- You need to perform operations across a set of unrelated classes

KEY BENEFIT: We can add new export formats (YAML, CSV) by creating new visitors
without modifying Circle, Rectangle, or Triangle classes. This follows the
Open/Closed Principle.

DOUBLE DISPATCH:
The accept() method in shapes calls visitor.visit_XXX(self), which allows
the visitor to access the specific shape type without casting. This is
"double dispatch" - the operation depends on both the visitor type AND
the shape type.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from math import sqrt
from typing import override


class ShapeVisitor(ABC):
    """Abstract visitor defining operations for each shape type."""
    
    @abstractmethod
    def visit_circle(self, circle: Circle) -> str:
        pass
    
    @abstractmethod
    def visit_rectangle(self, rectangle: Rectangle) -> str:
        pass
    
    @abstractmethod
    def visit_triangle(self, triangle: Triangle) -> str:
        pass


class Shape(ABC):
    """Abstract base class for shapes."""
    
    @abstractmethod
    def accept(self, visitor: ShapeVisitor) -> str:
        pass
    
    @abstractmethod
    def get_area(self) -> float:
        pass


class Circle(Shape):
    """Circle shape with radius."""
    
    def __init__(self, radius: float, x: float = 0, y: float = 0) -> None:
        self.radius = radius
        self.x = x
        self.y = y
    
    @override
    def accept(self, visitor: ShapeVisitor) -> str:
        return visitor.visit_circle(self)
    
    @override
    def get_area(self) -> float:
        import math
        return math.pi * self.radius ** 2


class Rectangle(Shape):
    """Rectangle shape with width and height."""
    
    def __init__(self, width: float, height: float, x: float = 0, y: float = 0) -> None:
        self.width = width
        self.height = height
        self.x = x
        self.y = y
    
    @override
    def accept(self, visitor: ShapeVisitor) -> str:
        return visitor.visit_rectangle(self)
    
    @override
    def get_area(self) -> float:
        return self.width * self.height


class Triangle(Shape):
    """Triangle shape defined by three sides."""
    
    def __init__(self, a: float, b: float, c: float, x: float = 0, y: float = 0) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.x = x
        self.y = y
    
    @override
    def accept(self, visitor: ShapeVisitor) -> str:
        return visitor.visit_triangle(self)
    
    @override
    def get_area(self) -> float:
        s = (self.a + self.b + self.c) / 2
        area_sq = s * (s - self.a) * (s - self.b) * (s - self.c)
        if area_sq <= 0:
            return 0.0
        return sqrt(area_sq)


class XMLExportVisitor(ShapeVisitor):
    """Visitor that exports shapes to XML format."""
    
    @override
    def visit_circle(self, circle: Circle) -> str:
        area = circle.get_area()
        return (
            f'<circle radius="{circle.radius:.2f}" '
            f'x="{circle.x:.2f}" y="{circle.y:.2f}" '
            f'area="{area:.2f}"/>'
        )
    
    @override
    def visit_rectangle(self, rectangle: Rectangle) -> str:
        area = rectangle.get_area()
        return (
            f'<rectangle width="{rectangle.width:.2f}" '
            f'height="{rectangle.height:.2f}" '
            f'x="{rectangle.x:.2f}" y="{rectangle.y:.2f}" '
            f'area="{area:.2f}"/>'
        )
    
    @override
    def visit_triangle(self, triangle: Triangle) -> str:
        area = triangle.get_area()
        return (
            f'<triangle a="{triangle.a:.2f}" b="{triangle.b:.2f}" '
            f'c="{triangle.c:.2f}" x="{triangle.x:.2f}" '
            f'y="{triangle.y:.2f}" area="{area:.2f}"/>'
        )


class JSONExportVisitor(ShapeVisitor):
    """Visitor that exports shapes to JSON format."""
    
    @override
    def visit_circle(self, circle: Circle) -> str:
        area = circle.get_area()
        return (
            f'{{"type": "circle", "radius": {circle.radius:.2f}, '
            f'"x": {circle.x:.2f}, "y": {circle.y:.2f}, '
            f'"area": {area:.2f}}}'
        )
    
    @override
    def visit_rectangle(self, rectangle: Rectangle) -> str:
        area = rectangle.get_area()
        return (
            f'{{"type": "rectangle", "width": {rectangle.width:.2f}, '
            f'"height": {rectangle.height:.2f}, "x": {rectangle.x:.2f}, '
            f'"y": {rectangle.y:.2f}, "area": {area:.2f}}}'
        )
    
    @override
    def visit_triangle(self, triangle: Triangle) -> str:
        area = triangle.get_area()
        return (
            f'{{"type": "triangle", "a": {triangle.a:.2f}, '
            f'"b": {triangle.b:.2f}, "c": {triangle.c:.2f}, '
            f'"x": {triangle.x:.2f}, "y": {triangle.y:.2f}, '
            f'"area": {area:.2f}}}'
        )


class AreaCalculatorVisitor(ShapeVisitor):
    """Visitor that calculates total area of visited shapes."""
    
    def __init__(self) -> None:
        self._total_area = 0.0
    
    @override
    def visit_circle(self, circle: Circle) -> str:
        self._total_area += circle.get_area()
        return f"Total: {self._total_area:.2f}"
    
    @override
    def visit_rectangle(self, rectangle: Rectangle) -> str:
        self._total_area += rectangle.get_area()
        return f"Total: {self._total_area:.2f}"
    
    @override
    def visit_triangle(self, triangle: Triangle) -> str:
        self._total_area += triangle.get_area()
        return f"Total: {self._total_area:.2f}"
    
    def get_total_area(self) -> float:
        return self._total_area
    
    def reset(self) -> None:
        self._total_area = 0.0


class ShapeCollection:
    """A collection of shapes that can be visited."""
    
    def __init__(self) -> None:
        self._shapes: list[Shape] = []
    
    def add(self, shape: Shape) -> None:
        self._shapes.append(shape)
    
    def accept(self, visitor: ShapeVisitor) -> list[str]:
        return [shape.accept(visitor) for shape in self._shapes]
