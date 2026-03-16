"""Problem 05: Slot Optimized Point

Topic: __slots__ for memory efficiency
Difficulty: Medium

Implement 2D and 3D point classes using __slots__ for memory optimization.
Compare behavior with regular classes.
"""

from __future__ import annotations
from typing import Iterator


class SlotPoint2D:
    """Memory-efficient 2D point using __slots__.
    
    Attributes:
        x: X coordinate
        y: Y coordinate
    
    Uses __slots__ to reduce memory overhead compared to regular classes.
    """
    
    __slots__ = ["x", "y"]
    
    def __init__(self, x: float, y: float) -> None:
        """Initialize a 2D point.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        raise NotImplementedError("Implement SlotPoint2D.__init__")
    
    def __repr__(self) -> str:
        """String representation."""
        raise NotImplementedError("Implement SlotPoint2D.__repr__")
    
    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        raise NotImplementedError("Implement SlotPoint2D.__eq__")
    
    def __hash__(self) -> int:
        """Hash support for use in sets/dicts."""
        raise NotImplementedError("Implement SlotPoint2D.__hash__")
    
    def distance_squared(self, other: SlotPoint2D) -> float:
        """Calculate squared distance to another point.
        
        Args:
            other: Another 2D point
            
        Returns:
            Squared Euclidean distance
        """
        raise NotImplementedError("Implement SlotPoint2D.distance_squared")
    
    def translate(self, dx: float, dy: float) -> SlotPoint2D:
        """Return a new point translated by (dx, dy).
        
        Args:
            dx: X offset
            dy: Y offset
            
        Returns:
            New SlotPoint2D at translated position
        """
        raise NotImplementedError("Implement SlotPoint2D.translate")


class SlotPoint3D:
    """Memory-efficient 3D point using __slots__.
    
    Attributes:
        x: X coordinate
        y: Y coordinate
        z: Z coordinate
    
    Inherits from SlotPoint2D conceptually but uses its own __slots__.
    """
    
    __slots__ = ["x", "y", "z"]
    
    def __init__(self, x: float, y: float, z: float) -> None:
        """Initialize a 3D point.
        
        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate
        """
        raise NotImplementedError("Implement SlotPoint3D.__init__")
    
    def __repr__(self) -> str:
        """String representation."""
        raise NotImplementedError("Implement SlotPoint3D.__repr__")
    
    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        raise NotImplementedError("Implement SlotPoint3D.__eq__")
    
    def __hash__(self) -> int:
        """Hash support."""
        raise NotImplementedError("Implement SlotPoint3D.__hash__")
    
    def distance_squared(self, other: SlotPoint3D) -> float:
        """Calculate squared distance to another 3D point.
        
        Args:
            other: Another 3D point
            
        Returns:
            Squared Euclidean distance
        """
        raise NotImplementedError("Implement SlotPoint3D.distance_squared")
    
    def translate(self, dx: float, dy: float, dz: float) -> SlotPoint3D:
        """Return a new point translated by (dx, dy, dz).
        
        Args:
            dx: X offset
            dy: Y offset
            dz: Z offset
            
        Returns:
            New SlotPoint3D at translated position
        """
        raise NotImplementedError("Implement SlotPoint3D.translate")


class RegularPoint2D:
    """Regular 2D point without __slots__ (for comparison).
    
    This is exactly the same as SlotPoint2D but uses a regular __dict__
    to demonstrate the memory difference.
    """
    
    def __init__(self, x: float, y: float) -> None:
        """Initialize a 2D point."""
        raise NotImplementedError("Implement RegularPoint2D.__init__")
    
    def __repr__(self) -> str:
        """String representation."""
        raise NotImplementedError("Implement RegularPoint2D.__repr__")
    
    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        raise NotImplementedError("Implement RegularPoint2D.__eq__")
    
    def __hash__(self) -> int:
        """Hash support."""
        raise NotImplementedError("Implement RegularPoint2D.__hash__")


def compare_memory_usage(count: int = 10000) -> dict[str, int]:
    """Compare memory usage between slotted and regular classes.
    
    This is a simplified comparison for demonstration.
    In practice, use sys.getsizeof() and tracemalloc for accurate measurements.
    
    Args:
        count: Number of instances to create
        
    Returns:
        Dictionary with approximate sizes
    """
    raise NotImplementedError("Implement compare_memory_usage")


def create_point_grid(
    width: int,
    height: int,
    use_slots: bool = True
) -> Iterator[SlotPoint2D | RegularPoint2D]:
    """Create a grid of points.
    
    Args:
        width: Grid width
        height: Grid height
        use_slots: If True, use SlotPoint2D; otherwise RegularPoint2D
        
    Yields:
        Points in the grid from (0,0) to (width-1, height-1)
    """
    raise NotImplementedError("Implement create_point_grid")
