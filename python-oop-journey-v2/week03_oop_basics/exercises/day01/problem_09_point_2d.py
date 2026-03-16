"""Problem 09: Point2D

Topic: Mathematical operations, distance
Difficulty: Medium

Create a Point2D class representing a point in 2D space.

Examples:
    >>> p1 = Point2D(3.0, 4.0)
    >>> p1.x
    3.0
    >>> p1.y
    4.0
    >>> p1.distance_from_origin()
    5.0
    >>> p2 = Point2D(0.0, 0.0)
    >>> p1.distance_to(p2)
    5.0
    >>> p3 = Point2D(1.0, 1.0)
    >>> p1.midpoint_to(p3)
    Point2D(x=2.0, y=2.5)

Requirements:
    - __init__ takes x and y coordinates (floats)
    - distance_from_origin() returns Euclidean distance from (0,0)
    - distance_to(other) returns Euclidean distance to another Point2D
    - midpoint_to(other) returns Point2D at midpoint between self and other
    - translate(dx, dy) moves the point by (dx, dy)
    - __str__ and __repr__ for string representation

Hints:
    - Hint 1: Euclidean distance uses math.sqrt(dx*dx + dy*dy), import math
    - Hint 2: midpoint_to returns a NEW Point2D, doesn't modify self or other
    - Hint 3: translate modifies self.x and self.y in place (no return value)
"""

from __future__ import annotations


class Point2D:
    """A class representing a point in 2D Cartesian space."""

    def __init__(self, x: float, y: float) -> None:
        """Initialize a point with x and y coordinates."""
        raise NotImplementedError("Initialize x and y attributes")

    def distance_from_origin(self) -> float:
        """Calculate Euclidean distance from the origin (0, 0)."""
        raise NotImplementedError("Implement distance_from_origin method")

    def distance_to(self, other: Point2D) -> float:
        """Calculate Euclidean distance to another point."""
        raise NotImplementedError("Implement distance_to method")

    def midpoint_to(self, other: Point2D) -> Point2D:
        """Calculate the midpoint between this point and another."""
        raise NotImplementedError("Implement midpoint_to method")

    def translate(self, dx: float, dy: float) -> None:
        """Translate (move) the point by (dx, dy)."""
        raise NotImplementedError("Implement translate method")

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        raise NotImplementedError("Implement __str__ method")

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        raise NotImplementedError("Implement __repr__ method")
