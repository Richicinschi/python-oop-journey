"""Problem 03: Rectangle

Topic: Computed properties, geometry
Difficulty: Easy

Create a Rectangle class with width and height attributes.

Examples:
    >>> rect = Rectangle(5.0, 3.0)
    >>> rect.width
    5.0
    >>> rect.height
    3.0
    >>> rect.area()
    15.0
    >>> rect.perimeter()
    16.0
    >>> rect.is_square()
    False

Requirements:
    - __init__ takes width and height (both positive floats)
    - area() returns the rectangle's area
    - perimeter() returns the rectangle's perimeter
    - is_square() returns True if width equals height
    - __str__ and __repr__ for string representation
"""

from __future__ import annotations


class Rectangle:
    """A class representing a rectangle with width and height."""

    def __init__(self, width: float, height: float) -> None:
        """Initialize a rectangle with width and height.
        
        Args:
            width: The width of the rectangle (must be positive)
            height: The height of the rectangle (must be positive)
        """
        raise NotImplementedError("Initialize width and height attributes")

    def area(self) -> float:
        """Calculate and return the area of the rectangle."""
        raise NotImplementedError("Implement area method")

    def perimeter(self) -> float:
        """Calculate and return the perimeter of the rectangle."""
        raise NotImplementedError("Implement perimeter method")

    def is_square(self) -> bool:
        """Return True if the rectangle is a square (width == height)."""
        raise NotImplementedError("Implement is_square method")

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        raise NotImplementedError("Implement __str__ method")

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        raise NotImplementedError("Implement __repr__ method")
