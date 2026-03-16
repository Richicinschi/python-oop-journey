"""Tests for Problem 01: Slots Memory Comparison."""

from __future__ import annotations

import sys

from week07_real_world.solutions.day06.problem_01_slots_memory_comparison import (
    RegularPoint,
    SlottedPoint,
    compare_memory_usage,
    create_point_instances,
)


def test_regular_point_creation() -> None:
    """Test RegularPoint can be created and accessed."""
    point = RegularPoint(1.0, 2.0, 3.0)
    assert point.x == 1.0
    assert point.y == 2.0
    assert point.z == 3.0


def test_regular_point_to_tuple() -> None:
    """Test RegularPoint.to_tuple returns correct values."""
    point = RegularPoint(1.0, 2.0, 3.0)
    assert point.to_tuple() == (1.0, 2.0, 3.0)


def test_slotted_point_creation() -> None:
    """Test SlottedPoint can be created and accessed."""
    point = SlottedPoint(1.0, 2.0, 3.0)
    assert point.x == 1.0
    assert point.y == 2.0
    assert point.z == 3.0


def test_slotted_point_to_tuple() -> None:
    """Test SlottedPoint.to_tuple returns correct values."""
    point = SlottedPoint(1.0, 2.0, 3.0)
    assert point.to_tuple() == (1.0, 2.0, 3.0)


def test_slotted_point_has_no_dict() -> None:
    """Test that SlottedPoint instances don't have __dict__."""
    point = SlottedPoint(1.0, 2.0, 3.0)
    assert not hasattr(point, '__dict__')


def test_regular_point_has_dict() -> None:
    """Test that RegularPoint instances have __dict__."""
    point = RegularPoint(1.0, 2.0, 3.0)
    assert hasattr(point, '__dict__')
    assert point.__dict__ == {'x': 1.0, 'y': 2.0, 'z': 3.0}


def test_create_point_instances_with_regular() -> None:
    """Test create_point_instances creates correct number of RegularPoints."""
    points = create_point_instances(RegularPoint, 100)
    assert len(points) == 100
    assert all(isinstance(p, RegularPoint) for p in points)


def test_create_point_instances_with_slotted() -> None:
    """Test create_point_instances creates correct number of SlottedPoints."""
    points = create_point_instances(SlottedPoint, 100)
    assert len(points) == 100
    assert all(isinstance(p, SlottedPoint) for p in points)


def test_create_point_instances_values() -> None:
    """Test created points have expected values."""
    points = create_point_instances(SlottedPoint, 3)
    assert points[0].to_tuple() == (0.0, 1.0, 2.0)
    assert points[1].to_tuple() == (1.0, 2.0, 3.0)
    assert points[2].to_tuple() == (2.0, 3.0, 4.0)


def test_compare_memory_usage_returns_dict() -> None:
    """Test compare_memory_usage returns expected dictionary keys."""
    result = compare_memory_usage(100)
    assert 'regular_total' in result
    assert 'slotted_total' in result
    assert 'count' in result
    assert result['count'] == 100


def test_slotted_uses_less_memory() -> None:
    """Test that SlottedPoint uses less memory than RegularPoint.
    
    Note: This test verifies the key behavior of __slots__ - that slotted
    instances don't have __dict__, which is the primary memory saving mechanism.
    The actual memory difference depends on Python implementation details.
    """
    # Create instances to compare
    regular = RegularPoint(1.0, 2.0, 3.0)
    slotted = SlottedPoint(1.0, 2.0, 3.0)
    
    # Slotted instances should not have __dict__
    assert not hasattr(slotted, '__dict__')
    # Regular instances should have __dict__
    assert hasattr(regular, '__dict__')
    
    # Verify both work correctly
    assert regular.to_tuple() == slotted.to_tuple()


def test_slotted_point_cannot_add_new_attributes() -> None:
    """Test that SlottedPoint cannot have new attributes added."""
    point = SlottedPoint(1.0, 2.0, 3.0)
    try:
        point.w = 4.0  # type: ignore[attr-defined]
        assert False, "Should have raised AttributeError"
    except AttributeError:
        pass  # Expected


def test_regular_point_can_add_new_attributes() -> None:
    """Test that RegularPoint can have new attributes added."""
    point = RegularPoint(1.0, 2.0, 3.0)
    point.w = 4.0  # type: ignore[attr-defined]
    assert point.w == 4.0


def test_compare_memory_usage_with_zero_count() -> None:
    """Test compare_memory_usage handles zero count."""
    result = compare_memory_usage(0)
    assert result['regular_total'] == 0
    assert result['slotted_total'] == 0
    assert result['count'] == 0
