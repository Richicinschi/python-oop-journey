"""Tests for Problem 09: Circle Radius Validation."""

from __future__ import annotations

import math

import pytest

from week03_oop_basics.solutions.day03.problem_09_circle_radius_validation import (
    Circle,
)


class TestCircle:
    """Test suite for Circle class."""
    
    def test_initialization_int(self) -> None:
        """Test circle initialization with int."""
        circle = Circle(5)
        assert circle.radius == 5.0
    
    def test_initialization_float(self) -> None:
        """Test circle initialization with float."""
        circle = Circle(5.5)
        assert circle.radius == 5.5
    
    def test_initialization_negative_raises(self) -> None:
        """Test initialization with negative radius raises."""
        with pytest.raises(ValueError, match="positive"):
            Circle(-5.0)
    
    def test_initialization_zero_raises(self) -> None:
        """Test initialization with zero radius raises."""
        with pytest.raises(ValueError, match="positive"):
            Circle(0.0)
    
    def test_initialization_bool_raises(self) -> None:
        """Test initialization with bool raises TypeError."""
        with pytest.raises(TypeError, match="bool"):
            Circle(True)  # type: ignore
        with pytest.raises(TypeError, match="bool"):
            Circle(False)  # type: ignore
    
    def test_initialization_non_number_raises(self) -> None:
        """Test initialization with non-number raises TypeError."""
        with pytest.raises(TypeError, match="number"):
            Circle("five")  # type: ignore
    
    def test_radius_getter(self) -> None:
        """Test radius getter."""
        circle = Circle(5.0)
        assert circle.radius == 5.0
    
    def test_radius_setter_valid(self) -> None:
        """Test radius setter with valid value."""
        circle = Circle(5.0)
        circle.radius = 10.0
        assert circle.radius == 10.0
    
    def test_radius_setter_negative_raises(self) -> None:
        """Test radius setter with negative raises ValueError."""
        circle = Circle(5.0)
        with pytest.raises(ValueError, match="positive"):
            circle.radius = -5.0
    
    def test_radius_setter_bool_raises(self) -> None:
        """Test radius setter with bool raises TypeError."""
        circle = Circle(5.0)
        with pytest.raises(TypeError, match="bool"):
            circle.radius = True  # type: ignore
    
    def test_diameter_getter(self) -> None:
        """Test diameter getter."""
        circle = Circle(5.0)
        assert circle.diameter == 10.0
    
    def test_diameter_setter(self) -> None:
        """Test diameter setter."""
        circle = Circle(5.0)
        circle.diameter = 20.0
        assert circle.radius == 10.0
        assert circle.diameter == 20.0
    
    def test_diameter_setter_negative_raises(self) -> None:
        """Test diameter setter with negative raises ValueError."""
        circle = Circle(5.0)
        with pytest.raises(ValueError, match="positive"):
            circle.diameter = -10.0
    
    def test_area(self) -> None:
        """Test area calculation."""
        circle = Circle(5.0)
        expected = math.pi * 25.0
        assert abs(circle.area - expected) < 0.0001
    
    def test_area_read_only(self) -> None:
        """Test that area is read-only."""
        circle = Circle(5.0)
        with pytest.raises(AttributeError):
            circle.area = 100  # type: ignore
    
    def test_circumference(self) -> None:
        """Test circumference calculation."""
        circle = Circle(5.0)
        expected = 2 * math.pi * 5.0
        assert abs(circle.circumference - expected) < 0.0001
    
    def test_circumference_read_only(self) -> None:
        """Test that circumference is read-only."""
        circle = Circle(5.0)
        with pytest.raises(AttributeError):
            circle.circumference = 100  # type: ignore
    
    def test_is_unit_circle_true(self) -> None:
        """Test is_unit_circle returns True for radius 1."""
        circle = Circle(1.0)
        assert circle.is_unit_circle is True
    
    def test_is_unit_circle_false(self) -> None:
        """Test is_unit_circle returns False for other radii."""
        circle = Circle(5.0)
        assert circle.is_unit_circle is False
    
    def test_is_unit_circle_approximate(self) -> None:
        """Test is_unit_circle with floating point comparison."""
        circle = Circle(1.0)
        # After scaling and back
        circle.radius = 2.0
        circle.radius = 1.0
        assert circle.is_unit_circle is True
    
    def test_scale(self) -> None:
        """Test scale method."""
        circle = Circle(5.0)
        circle.scale(2.0)
        assert circle.radius == 10.0
    
    def test_scale_non_positive_raises(self) -> None:
        """Test scale with non-positive factor raises."""
        circle = Circle(5.0)
        with pytest.raises(ValueError, match="positive"):
            circle.scale(0.0)
        with pytest.raises(ValueError, match="positive"):
            circle.scale(-1.0)
    
    def test_scale_non_number_raises(self) -> None:
        """Test scale with non-number raises TypeError."""
        circle = Circle(5.0)
        with pytest.raises(TypeError, match="number"):
            circle.scale("two")  # type: ignore
    
    def test_contains_point_center(self) -> None:
        """Test contains_point for center."""
        circle = Circle(5.0)
        assert circle.contains_point(0.0, 0.0) is True
    
    def test_contains_point_inside(self) -> None:
        """Test contains_point for point inside."""
        circle = Circle(5.0)
        assert circle.contains_point(3.0, 3.0) is True
    
    def test_contains_point_on_edge(self) -> None:
        """Test contains_point for point on edge."""
        circle = Circle(5.0)
        assert circle.contains_point(5.0, 0.0) is True
    
    def test_contains_point_outside(self) -> None:
        """Test contains_point for point outside."""
        circle = Circle(5.0)
        assert circle.contains_point(4.0, 4.0) is False  # dist ~5.66 > 5
    
    def test_contains_point_negative_coords(self) -> None:
        """Test contains_point with negative coordinates."""
        circle = Circle(5.0)
        assert circle.contains_point(-3.0, -3.0) is True
