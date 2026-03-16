"""Reference solution for Problem 03: Rectangle."""

from __future__ import annotations


class Rectangle:
    """A class representing a rectangle with width and height."""

    def __init__(self, width: float, height: float) -> None:
        """Initialize a rectangle with width and height.
        
        Args:
            width: The width of the rectangle (must be positive)
            height: The height of the rectangle (must be positive)
        """
        self.width = float(width)
        self.height = float(height)

    def area(self) -> float:
        """Calculate and return the area of the rectangle."""
        return self.width * self.height

    def perimeter(self) -> float:
        """Calculate and return the perimeter of the rectangle."""
        return 2 * (self.width + self.height)

    def is_square(self) -> bool:
        """Return True if the rectangle is a square (width == height)."""
        return self.width == self.height

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        return f"Rectangle(width={self.width}, height={self.height})"

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"Rectangle(width={self.width}, height={self.height})"
