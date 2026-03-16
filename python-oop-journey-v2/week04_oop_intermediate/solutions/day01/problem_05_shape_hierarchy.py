"""Reference solution for Problem 05: Shape Hierarchy."""

from __future__ import annotations

import math


class Shape:
    """Base class for geometric shapes."""
    
    def area(self) -> float:
        raise NotImplementedError("Subclasses must implement area()")
    
    def perimeter(self) -> float:
        raise NotImplementedError("Subclasses must implement perimeter()")
    
    def describe(self) -> str:
        return f"Shape(area={self.area():.2f}, perimeter={self.perimeter():.2f})"
    
    def scale(self, factor: float) -> None:
        raise NotImplementedError("Subclasses must implement scale()")


class Circle(Shape):
    """A circle shape."""
    
    def __init__(self, radius: float) -> None:
        if radius < 0:
            raise ValueError("Radius cannot be negative")
        self.radius = radius
    
    def area(self) -> float:
        return math.pi * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * math.pi * self.radius
    
    def describe(self) -> str:
        return (f"Circle(radius={self.radius:.2f}, area={self.area():.2f}, "
                f"perimeter={self.perimeter():.2f})")
    
    def scale(self, factor: float) -> None:
        self.radius *= factor
    
    def get_diameter(self) -> float:
        return 2 * self.radius


class Rectangle(Shape):
    """A rectangle shape."""
    
    def __init__(self, width: float, height: float) -> None:
        if width < 0 or height < 0:
            raise ValueError("Dimensions cannot be negative")
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
    
    def describe(self) -> str:
        return (f"Rectangle(WxH={self.width:.2f}x{self.height:.2f}, "
                f"area={self.area():.2f}, perimeter={self.perimeter():.2f})")
    
    def scale(self, factor: float) -> None:
        self.width *= factor
        self.height *= factor
    
    def is_square(self) -> bool:
        return self.width == self.height


class Triangle(Shape):
    """A triangle shape using three sides."""
    
    def __init__(self, a: float, b: float, c: float) -> None:
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Side lengths must be positive")
        if not (a + b > c and a + c > b and b + c > a):
            raise ValueError("Invalid triangle: triangle inequality violated")
        self.a = a
        self.b = b
        self.c = c
    
    def area(self) -> float:
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    
    def perimeter(self) -> float:
        return self.a + self.b + self.c
    
    def describe(self) -> str:
        return (f"Triangle(sides={self.a:.2f},{self.b:.2f},{self.c:.2f}, "
                f"area={self.area():.2f}, perimeter={self.perimeter():.2f})")
    
    def scale(self, factor: float) -> None:
        self.a *= factor
        self.b *= factor
        self.c *= factor
    
    def get_triangle_type(self) -> str:
        if self.a == self.b == self.c:
            return "equilateral"
        if self.a == self.b or self.b == self.c or self.a == self.c:
            return "isosceles"
        return "scalene"
