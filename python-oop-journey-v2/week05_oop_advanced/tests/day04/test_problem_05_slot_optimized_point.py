"""Tests for Problem 05: Slot Optimized Point."""

from __future__ import annotations

import sys

import pytest

from week05_oop_advanced.solutions.day04.problem_05_slot_optimized_point import (
    RegularPoint2D, SlotPoint2D, SlotPoint3D, compare_memory_usage, create_point_grid
)


class TestSlotPoint2D:
    """Tests for SlotPoint2D class."""
    
    def test_slot_point_creation(self) -> None:
        """Test creating a 2D slot point."""
        point = SlotPoint2D(1.0, 2.0)
        
        assert point.x == 1.0
        assert point.y == 2.0
    
    def test_slot_point_repr(self) -> None:
        """Test string representation."""
        point = SlotPoint2D(3.5, 4.5)
        
        assert "SlotPoint2D" in repr(point)
        assert "3.5" in repr(point)
        assert "4.5" in repr(point)
    
    def test_slot_point_equality(self) -> None:
        """Test equality comparison."""
        p1 = SlotPoint2D(1.0, 2.0)
        p2 = SlotPoint2D(1.0, 2.0)
        p3 = SlotPoint2D(2.0, 1.0)
        
        assert p1 == p2
        assert p1 != p3
    
    def test_slot_point_not_equal_other_types(self) -> None:
        """Test that comparison with non-SlotPoint2D returns NotImplemented."""
        point = SlotPoint2D(1.0, 2.0)
        
        assert point != "not a point"
        assert point != 123
        assert point != None
    
    def test_slot_point_hash(self) -> None:
        """Test that points can be hashed."""
        point = SlotPoint2D(1.0, 2.0)
        
        # Should be usable in a set
        point_set = {point}
        assert point in point_set
        
        # Should be usable as dict key
        point_dict = {point: "value"}
        assert point_dict[point] == "value"
    
    def test_slot_point_distance_squared(self) -> None:
        """Test squared distance calculation."""
        p1 = SlotPoint2D(0.0, 0.0)
        p2 = SlotPoint2D(3.0, 4.0)
        
        # Distance is 5, squared is 25
        assert p1.distance_squared(p2) == 25.0
    
    def test_slot_point_distance_squared_same_point(self) -> None:
        """Test distance from point to itself."""
        p = SlotPoint2D(5.0, 5.0)
        
        assert p.distance_squared(p) == 0.0
    
    def test_slot_point_translate(self) -> None:
        """Test point translation."""
        point = SlotPoint2D(1.0, 2.0)
        translated = point.translate(3.0, 4.0)
        
        assert translated.x == 4.0
        assert translated.y == 6.0
        # Original unchanged
        assert point.x == 1.0
        assert point.y == 2.0
    
    def test_slot_point_no_dict(self) -> None:
        """Test that slotted class doesn't have __dict__."""
        point = SlotPoint2D(1.0, 2.0)
        
        with pytest.raises(AttributeError):
            _ = point.__dict__
    
    def test_slot_point_cannot_add_attributes(self) -> None:
        """Test that new attributes cannot be added to slotted class."""
        point = SlotPoint2D(1.0, 2.0)
        
        with pytest.raises(AttributeError):
            point.z = 3.0
    
    def test_slot_point_has_slots(self) -> None:
        """Test that __slots__ is defined."""
        assert hasattr(SlotPoint2D, "__slots__")
        assert "x" in SlotPoint2D.__slots__
        assert "y" in SlotPoint2D.__slots__


class TestSlotPoint3D:
    """Tests for SlotPoint3D class."""
    
    def test_slot_point_3d_creation(self) -> None:
        """Test creating a 3D slot point."""
        point = SlotPoint3D(1.0, 2.0, 3.0)
        
        assert point.x == 1.0
        assert point.y == 2.0
        assert point.z == 3.0
    
    def test_slot_point_3d_repr(self) -> None:
        """Test string representation."""
        point = SlotPoint3D(1.0, 2.0, 3.0)
        
        assert "SlotPoint3D" in repr(point)
        assert "z=" in repr(point)
    
    def test_slot_point_3d_equality(self) -> None:
        """Test equality comparison."""
        p1 = SlotPoint3D(1.0, 2.0, 3.0)
        p2 = SlotPoint3D(1.0, 2.0, 3.0)
        p3 = SlotPoint3D(3.0, 2.0, 1.0)
        
        assert p1 == p2
        assert p1 != p3
    
    def test_slot_point_3d_distance_squared(self) -> None:
        """Test squared distance calculation in 3D."""
        p1 = SlotPoint3D(0.0, 0.0, 0.0)
        p2 = SlotPoint3D(1.0, 2.0, 2.0)
        
        # 1^2 + 2^2 + 2^2 = 1 + 4 + 4 = 9
        assert p1.distance_squared(p2) == 9.0
    
    def test_slot_point_3d_translate(self) -> None:
        """Test 3D point translation."""
        point = SlotPoint3D(1.0, 2.0, 3.0)
        translated = point.translate(1.0, 1.0, 1.0)
        
        assert translated.x == 2.0
        assert translated.y == 3.0
        assert translated.z == 4.0
    
    def test_slot_point_3d_slots(self) -> None:
        """Test that 3D point has correct slots."""
        assert hasattr(SlotPoint3D, "__slots__")
        assert "x" in SlotPoint3D.__slots__
        assert "y" in SlotPoint3D.__slots__
        assert "z" in SlotPoint3D.__slots__
    
    def test_slot_point_3d_cannot_add_attributes(self) -> None:
        """Test that new attributes cannot be added."""
        point = SlotPoint3D(1.0, 2.0, 3.0)
        
        with pytest.raises(AttributeError):
            point.w = 4.0


class TestRegularPoint2D:
    """Tests for RegularPoint2D class (for comparison)."""
    
    def test_regular_point_creation(self) -> None:
        """Test creating a regular point."""
        point = RegularPoint2D(1.0, 2.0)
        
        assert point.x == 1.0
        assert point.y == 2.0
    
    def test_regular_point_has_dict(self) -> None:
        """Test that regular class has __dict__."""
        point = RegularPoint2D(1.0, 2.0)
        
        assert hasattr(point, "__dict__")
        assert point.__dict__["x"] == 1.0
        assert point.__dict__["y"] == 2.0
    
    def test_regular_point_can_add_attributes(self) -> None:
        """Test that new attributes can be added to regular class."""
        point = RegularPoint2D(1.0, 2.0)
        
        # This should work for regular class
        point.z = 3.0
        assert point.z == 3.0
    
    def test_regular_point_equality(self) -> None:
        """Test equality comparison."""
        p1 = RegularPoint2D(1.0, 2.0)
        p2 = RegularPoint2D(1.0, 2.0)
        
        assert p1 == p2


class TestMemoryComparison:
    """Tests for memory usage comparison."""
    
    def test_compare_memory_usage_returns_dict(self) -> None:
        """Test that compare_memory_usage returns expected structure."""
        result = compare_memory_usage(count=100)
        
        assert "slotted_instance" in result
        assert "regular_instance" in result
        assert "approximate_savings_per_instance" in result
    
    def test_compare_memory_usage_savings_positive(self) -> None:
        """Test that slotted instances use less memory."""
        result = compare_memory_usage(count=100)
        
        # Slotted should generally use less memory
        assert result["slotted_instance"] <= result["regular_instance"]


class TestPointGrid:
    """Tests for point grid creation."""
    
    def test_create_point_grid_with_slots(self) -> None:
        """Test creating a grid with slotted points."""
        points = list(create_point_grid(3, 2, use_slots=True))
        
        assert len(points) == 6  # 3 * 2
        assert all(isinstance(p, SlotPoint2D) for p in points)
    
    def test_create_point_grid_without_slots(self) -> None:
        """Test creating a grid with regular points."""
        points = list(create_point_grid(3, 2, use_slots=False))
        
        assert len(points) == 6
        assert all(isinstance(p, RegularPoint2D) for p in points)
    
    def test_create_point_grid_coordinates(self) -> None:
        """Test that grid has correct coordinates."""
        points = list(create_point_grid(2, 2, use_slots=True))
        
        # Points should be: (0,0), (1,0), (0,1), (1,1)
        coords = [(p.x, p.y) for p in points]
        
        assert (0.0, 0.0) in coords
        assert (1.0, 0.0) in coords
        assert (0.0, 1.0) in coords
        assert (1.0, 1.0) in coords
    
    def test_create_point_grid_empty(self) -> None:
        """Test creating an empty grid."""
        points = list(create_point_grid(0, 0, use_slots=True))
        
        assert len(points) == 0
    
    def test_create_point_grid_generator(self) -> None:
        """Test that create_point_grid returns a generator."""
        result = create_point_grid(3, 3, use_slots=True)
        
        # Should be a generator/iterator
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")
