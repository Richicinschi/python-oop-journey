"""Reference solution for Problem 05: Slot Optimized Point."""

from __future__ import annotations
from typing import Iterator
import sys


class SlotPoint2D:
    """Memory-efficient 2D point using __slots__."""
    
    __slots__ = ["x", "y"]
    
    def __init__(self, x: float, y: float) -> None:
        """Initialize a 2D point."""
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        """String representation."""
        return f"SlotPoint2D(x={self.x}, y={self.y})"
    
    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, SlotPoint2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        """Hash support for use in sets/dicts."""
        return hash((self.x, self.y))
    
    def distance_squared(self, other: SlotPoint2D) -> float:
        """Calculate squared distance to another point."""
        dx = self.x - other.x
        dy = self.y - other.y
        return dx * dx + dy * dy
    
    def translate(self, dx: float, dy: float) -> SlotPoint2D:
        """Return a new point translated by (dx, dy)."""
        return SlotPoint2D(self.x + dx, self.y + dy)


class SlotPoint3D:
    """Memory-efficient 3D point using __slots__."""
    
    __slots__ = ["x", "y", "z"]
    
    def __init__(self, x: float, y: float, z: float) -> None:
        """Initialize a 3D point."""
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self) -> str:
        """String representation."""
        return f"SlotPoint3D(x={self.x}, y={self.y}, z={self.z})"
    
    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, SlotPoint3D):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __hash__(self) -> int:
        """Hash support."""
        return hash((self.x, self.y, self.z))
    
    def distance_squared(self, other: SlotPoint3D) -> float:
        """Calculate squared distance to another 3D point."""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return dx * dx + dy * dy + dz * dz
    
    def translate(self, dx: float, dy: float, dz: float) -> SlotPoint3D:
        """Return a new point translated by (dx, dy, dz)."""
        return SlotPoint3D(self.x + dx, self.y + dy, self.z + dz)


class RegularPoint2D:
    """Regular 2D point without __slots__ (for comparison)."""
    
    def __init__(self, x: float, y: float) -> None:
        """Initialize a 2D point."""
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        """String representation."""
        return f"RegularPoint2D(x={self.x}, y={self.y})"
    
    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, RegularPoint2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        """Hash support."""
        return hash((self.x, self.y))


def compare_memory_usage(count: int = 10000) -> dict[str, int]:
    """Compare memory usage between slotted and regular classes.
    
    Note: This is a simplified comparison. Actual memory savings depend
    on the Python implementation and platform.
    """
    # Create instances
    slot_points = [SlotPoint2D(i, i) for i in range(count)]
    regular_points = [RegularPoint2D(i, i) for i in range(count)]
    
    # Get sizes
    slot_size = sys.getsizeof(slot_points[0])
    regular_size = sys.getsizeof(regular_points[0])
    
    # Check if __dict__ exists (it adds overhead)
    has_dict = hasattr(regular_points[0], "__dict__")
    dict_size = sys.getsizeof(regular_points[0].__dict__) if has_dict else 0
    
    return {
        "slotted_instance": slot_size,
        "regular_instance": regular_size,
        "regular_dict_overhead": dict_size,
        "approximate_savings_per_instance": regular_size + dict_size - slot_size,
        "total_count": count
    }


def create_point_grid(
    width: int,
    height: int,
    use_slots: bool = True
) -> Iterator[SlotPoint2D | RegularPoint2D]:
    """Create a grid of points."""
    point_class = SlotPoint2D if use_slots else RegularPoint2D
    
    for y in range(height):
        for x in range(width):
            yield point_class(float(x), float(y))
