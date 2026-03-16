"""Tests for Problem 08: Point Comparison."""

from __future__ import annotations

import math

import pytest

from week03_oop_basics.solutions.day04.problem_08_point_comparison import (
    PointComparison,
)


class TestPointComparisonInit:
    """Test PointComparison initialization."""
    
    def test_init_basic(self) -> None:
        p = PointComparison(3, 4)
        assert p.x == 3
        assert p.y == 4
    
    def test_init_with_floats(self) -> None:
        p = PointComparison(1.5, 2.5)
        assert p.x == 1.5
        assert p.y == 2.5
    
    def test_init_at_origin(self) -> None:
        p = PointComparison(0, 0)
        assert p.x == 0
        assert p.y == 0


class TestPointComparisonDistanceFromOrigin:
    """Test PointComparison distance calculation."""
    
    def test_distance_simple(self) -> None:
        p = PointComparison(3, 4)
        assert p.distance_from_origin() == 5.0
    
    def test_distance_at_origin(self) -> None:
        p = PointComparison(0, 0)
        assert p.distance_from_origin() == 0.0
    
    def test_distance_negative_coords(self) -> None:
        p = PointComparison(-3, -4)
        assert p.distance_from_origin() == 5.0


class TestPointComparisonDistanceTo:
    """Test PointComparison distance to another point."""
    
    def test_distance_to(self) -> None:
        p1 = PointComparison(0, 0)
        p2 = PointComparison(3, 4)
        assert p1.distance_to(p2) == 5.0
    
    def test_distance_to_same_point(self) -> None:
        p1 = PointComparison(3, 4)
        p2 = PointComparison(3, 4)
        assert p1.distance_to(p2) == 0.0


class TestPointComparisonEquality:
    """Test PointComparison equality."""
    
    def test_equal_same_distance(self) -> None:
        p1 = PointComparison(3, 4)  # distance = 5
        p2 = PointComparison(0, 5)  # distance = 5
        p3 = PointComparison(-3, -4)  # distance = 5
        assert p1 == p2
        assert p1 == p3
    
    def test_not_equal_different_distance(self) -> None:
        p1 = PointComparison(3, 4)  # distance = 5
        p2 = PointComparison(6, 8)  # distance = 10
        assert p1 != p2
    
    def test_not_equal_non_point(self) -> None:
        p = PointComparison(3, 4)
        assert p != (3, 4)
        assert p != 5.0


class TestPointComparisonHash:
    """Test PointComparison hashing."""
    
    def test_hash_same_for_equal_points(self) -> None:
        p1 = PointComparison(3, 4)
        p2 = PointComparison(0, 5)
        assert hash(p1) == hash(p2)
    
    def test_hash_can_be_used_in_set(self) -> None:
        p1 = PointComparison(3, 4)
        p2 = PointComparison(0, 5)  # Same distance
        p3 = PointComparison(6, 8)  # Different distance
        point_set = {p1, p2, p3}
        assert len(point_set) == 2
    
    def test_hash_can_be_used_as_dict_key(self) -> None:
        p1 = PointComparison(3, 4)
        d = {p1: "value"}
        p2 = PointComparison(0, 5)  # Same distance
        assert d[p2] == "value"


class TestPointComparisonLessThan:
    """Test PointComparison less than operator."""
    
    def test_less_than_true(self) -> None:
        p1 = PointComparison(3, 4)  # distance = 5
        p2 = PointComparison(6, 8)  # distance = 10
        assert p1 < p2
    
    def test_less_than_false(self) -> None:
        p1 = PointComparison(6, 8)  # distance = 10
        p2 = PointComparison(3, 4)  # distance = 5
        assert not (p1 < p2)


class TestPointComparisonLessThanOrEqual:
    """Test PointComparison less than or equal operator."""
    
    def test_less_than_or_equal_true(self) -> None:
        p1 = PointComparison(3, 4)
        p2 = PointComparison(6, 8)
        assert p1 <= p2
    
    def test_less_than_or_equal_equal(self) -> None:
        p1 = PointComparison(3, 4)
        p2 = PointComparison(0, 5)
        assert p1 <= p2


class TestPointComparisonGreaterThan:
    """Test PointComparison greater than operator."""
    
    def test_greater_than_true(self) -> None:
        p1 = PointComparison(6, 8)  # distance = 10
        p2 = PointComparison(3, 4)  # distance = 5
        assert p1 > p2


class TestPointComparisonGreaterThanOrEqual:
    """Test PointComparison greater than or equal operator."""
    
    def test_greater_than_or_equal_true(self) -> None:
        p1 = PointComparison(6, 8)
        p2 = PointComparison(3, 4)
        assert p1 >= p2
    
    def test_greater_than_or_equal_equal(self) -> None:
        p1 = PointComparison(3, 4)
        p2 = PointComparison(0, 5)
        assert p1 >= p2


class TestPointComparisonRepr:
    """Test PointComparison representation."""
    
    def test_repr(self) -> None:
        p = PointComparison(3, 4)
        assert repr(p) == "PointComparison(3, 4)"


class TestPointComparisonStr:
    """Test PointComparison string representation."""
    
    def test_str(self) -> None:
        p = PointComparison(3, 4)
        assert str(p) == "(3, 4)"


class TestPointComparisonSorting:
    """Test that PointComparison objects can be sorted."""
    
    def test_sort_by_distance(self) -> None:
        points = [
            PointComparison(6, 8),  # dist 10
            PointComparison(3, 4),  # dist 5
            PointComparison(0, 5),  # dist 5
            PointComparison(1, 1),  # dist sqrt(2)
        ]
        sorted_points = sorted(points)
        assert sorted_points[0].distance_from_origin() == pytest.approx(math.sqrt(2))
        assert sorted_points[1].distance_from_origin() == 5.0
        assert sorted_points[2].distance_from_origin() == 5.0
        assert sorted_points[3].distance_from_origin() == 10.0
