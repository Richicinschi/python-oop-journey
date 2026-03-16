"""Problem 01: Slots Memory Comparison

Topic: __slots__ vs __dict__
Difficulty: Medium

Compare memory usage between classes using __dict__ and __slots__.
"""

from __future__ import annotations


class RegularPoint:
    """Standard class using __dict__ for attributes."""
    
    def __init__(self, x: float, y: float, z: float) -> None:
        """Initialize a 3D point.
        
        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate
        """
        raise NotImplementedError("Implement __init__")
    
    def to_tuple(self) -> tuple[float, float, float]:
        """Return coordinates as a tuple."""
        raise NotImplementedError("Implement to_tuple")


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
        raise NotImplementedError("Implement __init__")
    
    def to_tuple(self) -> tuple[float, float, float]:
        """Return coordinates as a tuple."""
        raise NotImplementedError("Implement to_tuple")


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
    raise NotImplementedError("Implement create_point_instances")


def compare_memory_usage(count: int = 10000) -> dict[str, int]:
    """Compare memory usage between RegularPoint and SlottedPoint.
    
    Args:
        count: Number of instances to create for comparison
        
    Returns:
        Dictionary with memory sizes in bytes for both classes
        
    Note:
        Returns approximate memory usage based on sys.getsizeof
    """
    raise NotImplementedError("Implement compare_memory_usage")
