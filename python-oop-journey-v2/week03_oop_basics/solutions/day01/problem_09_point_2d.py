"""Reference solution for Problem 09: Point2D."""

from __future__ import annotations

import math


class Point2D:
    """A class representing a point in 2D Cartesian space."""

    def __init__(self, x: float, y: float) -> None:
        """Initialize a point with x and y coordinates.
        
        Args:
            x: The x-coordinate
            y: The y-coordinate
        """
        self.x = float(x)
        self.y = float(y)

    def distance_from_origin(self) -> float:
        """Calculate Euclidean distance from the origin (0, 0)."""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def distance_to(self, other: Point2D) -> float:
        """Calculate Euclidean distance to another point."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def midpoint_to(self, other: Point2D) -> Point2D:
        """Calculate the midpoint between this point and another."""
        mid_x = (self.x + other.x) / 2
        mid_y = (self.y + other.y) / 2
        return Point2D(mid_x, mid_y)

    def translate(self, dx: float, dy: float) -> None:
        """Translate (move) the point by (dx, dy)."""
        self.x += dx
        self.y += dy

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        return f"Point2D({self.x}, {self.y})"

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"Point2D(x={self.x}, y={self.y})"
