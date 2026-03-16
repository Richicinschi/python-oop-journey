"""Tests for Problem 09: Point2D."""

from __future__ import annotations

import math

from week03_oop_basics.solutions.day01.problem_09_point_2d import Point2D


def test_point_creation() -> None:
    """Test creating a point."""
    point = Point2D(3.0, 4.0)
    assert point.x == 3.0
    assert point.y == 4.0


def test_distance_from_origin() -> None:
    """Test distance from origin."""
    point = Point2D(3.0, 4.0)
    assert point.distance_from_origin() == 5.0


def test_distance_from_origin_at_origin() -> None:
    """Test distance from origin for point at origin."""
    point = Point2D(0.0, 0.0)
    assert point.distance_from_origin() == 0.0


def test_distance_to() -> None:
    """Test distance between two points."""
    p1 = Point2D(3.0, 4.0)
    p2 = Point2D(0.0, 0.0)
    assert p1.distance_to(p2) == 5.0


def test_distance_to_same_point() -> None:
    """Test distance from point to itself."""
    p1 = Point2D(3.0, 4.0)
    assert p1.distance_to(p1) == 0.0


def test_midpoint_to() -> None:
    """Test calculating midpoint."""
    p1 = Point2D(0.0, 0.0)
    p2 = Point2D(4.0, 6.0)
    mid = p1.midpoint_to(p2)
    assert mid.x == 2.0
    assert mid.y == 3.0


def test_midpoint_returns_point2d() -> None:
    """Test that midpoint returns a Point2D instance."""
    p1 = Point2D(0.0, 0.0)
    p2 = Point2D(4.0, 6.0)
    mid = p1.midpoint_to(p2)
    assert isinstance(mid, Point2D)


def test_translate() -> None:
    """Test translating a point."""
    point = Point2D(1.0, 2.0)
    point.translate(3.0, 4.0)
    assert point.x == 4.0
    assert point.y == 6.0


def test_translate_negative() -> None:
    """Test translating with negative values."""
    point = Point2D(5.0, 5.0)
    point.translate(-2.0, -3.0)
    assert point.x == 3.0
    assert point.y == 2.0


def test_distance_with_integers() -> None:
    """Test distance calculation with integer coordinates."""
    p1 = Point2D(0, 0)
    p2 = Point2D(3, 4)
    assert p1.distance_to(p2) == 5.0


def test_pythagorean_triple() -> None:
    """Test with various Pythagorean triples."""
    p1 = Point2D(0, 0)
    p2 = Point2D(5, 12)  # 5-12-13 triangle
    assert p1.distance_to(p2) == 13.0


def test_str_representation() -> None:
    """Test the __str__ method."""
    point = Point2D(3.0, 4.0)
    result = str(point)
    assert "3.0" in result or "3" in result
    assert "4.0" in result or "4" in result


def test_repr_representation() -> None:
    """Test the __repr__ method."""
    point = Point2D(3.0, 4.0)
    result = repr(point)
    assert "Point2D" in result
