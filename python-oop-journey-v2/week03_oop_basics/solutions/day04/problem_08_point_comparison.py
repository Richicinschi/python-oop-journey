"""Reference solution for Problem 08: Point Comparison."""

from __future__ import annotations

import math


class PointComparison:
    """A 2D point with full comparison support and hashing.
    
    Points are compared by their Euclidean distance from the origin.
    Points with the same distance are considered equal.
    
    Attributes:
        x: The x-coordinate.
        y: The y-coordinate.
    """
    
    def __init__(self, x: float, y: float) -> None:
        """Initialize a point.
        
        Args:
            x: The x-coordinate.
            y: The y-coordinate.
        """
        self.x = x
        self.y = y
    
    def distance_from_origin(self) -> float:
        """Calculate the Euclidean distance from the origin.
        
        Returns:
            sqrt(x² + y²)
        """
        return math.sqrt(self.x**2 + self.y**2)
    
    def distance_to(self, other: PointComparison) -> float:
        """Calculate the Euclidean distance to another point.
        
        Args:
            other: The other point.
        
        Returns:
            The Euclidean distance between the two points.
        """
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __eq__(self, other: object) -> bool:
        """Check if two points have the same distance from origin.
        
        Args:
            other: The point to compare with.
        
        Returns:
            True if distances are equal, False otherwise.
        """
        if not isinstance(other, PointComparison):
            return NotImplemented
        # Compare squared distances to avoid sqrt precision issues
        return self.x**2 + self.y**2 == other.x**2 + other.y**2
    
    def __hash__(self) -> int:
        """Return a hash based on the distance from origin.
        
        Returns:
            Hash of the squared distance (avoids sqrt for performance).
        """
        # Use squared distance for hash (same for points at same distance)
        squared_dist = self.x**2 + self.y**2
        return hash(squared_dist)
    
    def __lt__(self, other: PointComparison) -> bool:
        """Check if this point is closer to origin than other.
        
        Args:
            other: The point to compare with.
        
        Returns:
            True if this distance < other distance.
        """
        if not isinstance(other, PointComparison):
            return NotImplemented
        return self.x**2 + self.y**2 < other.x**2 + other.y**2
    
    def __le__(self, other: PointComparison) -> bool:
        """Check if this point is closer or equal distance to origin."""
        if not isinstance(other, PointComparison):
            return NotImplemented
        return self.x**2 + self.y**2 <= other.x**2 + other.y**2
    
    def __gt__(self, other: PointComparison) -> bool:
        """Check if this point is farther from origin than other."""
        if not isinstance(other, PointComparison):
            return NotImplemented
        return self.x**2 + self.y**2 > other.x**2 + other.y**2
    
    def __ge__(self, other: PointComparison) -> bool:
        """Check if this point is farther or equal distance to origin."""
        if not isinstance(other, PointComparison):
            return NotImplemented
        return self.x**2 + self.y**2 >= other.x**2 + other.y**2
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        return f"PointComparison({self.x}, {self.y})"
    
    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"({self.x}, {self.y})"
