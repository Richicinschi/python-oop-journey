"""Reference solution for Problem 01: Slots Memory Comparison."""

from __future__ import annotations

import sys


class RegularPoint:
    """Standard class using __dict__ for attributes."""
    
    def __init__(self, x: float, y: float, z: float) -> None:
        """Initialize a 3D point.
        
        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate
        """
        self.x = x
        self.y = y
        self.z = z
    
    def to_tuple(self) -> tuple[float, float, float]:
        """Return coordinates as a tuple."""
        return (self.x, self.y, self.z)


class SlottedPoint:
    """Memory-optimized class using __slots__."""
    
    __slots__ = ('x', 'y', 'z')
    
    def __init__(self, x: float, y: float, z: float) -> None:
        """Initialize a 3D point.
        
        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate
        """
        self.x = x
        self.y = y
        self.z = z
    
    def to_tuple(self) -> tuple[float, float, float]:
        """Return coordinates as a tuple."""
        return (self.x, self.y, self.z)


def create_point_instances(
    point_class: type[RegularPoint] | type[SlottedPoint],
    count: int
) -> list[RegularPoint | SlottedPoint]:
    """Create multiple point instances using the given class.
    
    Args:
        point_class: The class to instantiate (RegularPoint or SlottedPoint)
        count: Number of instances to create
        
    Returns:
        List of point instances
    """
    return [point_class(float(i), float(i + 1), float(i + 2)) for i in range(count)]


def compare_memory_usage(count: int = 10000) -> dict[str, int]:
    """Compare memory usage between RegularPoint and SlottedPoint.
    
    Args:
        count: Number of instances to create for comparison
        
    Returns:
        Dictionary with memory sizes in bytes for both classes
        
    Note:
        Returns approximate memory usage based on sys.getsizeof
    """
    regular_points = create_point_instances(RegularPoint, count)
    slotted_points = create_point_instances(SlottedPoint, count)
    
    regular_size = sum(sys.getsizeof(p) for p in regular_points)
    slotted_size = sum(sys.getsizeof(p) for p in slotted_points)
    
    return {
        'regular_total': regular_size,
        'slotted_total': slotted_size,
        'count': count,
    }
