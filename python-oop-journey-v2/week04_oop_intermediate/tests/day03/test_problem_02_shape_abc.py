"""Tests for Problem 02: Shape ABC."""

from __future__ import annotations

import math
import pytest
from abc import ABC

from week04_oop_intermediate.solutions.day03.problem_02_shape_abc import (
    Shape,
    Rectangle,
    Circle,
    Triangle,
)


class TestShapeABC:
    """Test suite for Shape abstract base class."""
    
    def test_shape_is_abstract(self) -> None:
        """Test that Shape cannot be instantiated."""
        assert issubclass(Shape, ABC)
        with pytest.raises(TypeError, match="abstract"):
            Shape()
    
    def test_shape_has_abstract_properties(self) -> None:
        """Test that Shape defines abstract properties."""
        assert hasattr(Shape, 'area')
        assert hasattr(Shape, 'perimeter')


class TestRectangle:
    """Test suite for Rectangle."""
    
    def test_initialization(self) -> None:
        """Test rectangle initialization."""
        rect = Rectangle(5.0, 3.0)
        assert rect._width == 5.0
        assert rect._height == 3.0
    
    def test_initialization_negative_width_raises(self) -> None:
        """Test that negative width raises ValueError."""
        with pytest.raises(ValueError, match="Width"):
            Rectangle(-5.0, 3.0)
    
    def test_initialization_zero_width_raises(self) -> None:
        """Test that zero width raises ValueError."""
        with pytest.raises(ValueError, match="Width"):
            Rectangle(0.0, 3.0)
    
    def test_initialization_negative_height_raises(self) -> None:
        """Test that negative height raises ValueError."""
        with pytest.raises(ValueError, match="Height"):
            Rectangle(5.0, -3.0)
    
    def test_initialization_zero_height_raises(self) -> None:
        """Test that zero height raises ValueError."""
        with pytest.raises(ValueError, match="Height"):
            Rectangle(5.0, 0.0)
    
    def test_area(self) -> None:
        """Test area calculation."""
        rect = Rectangle(5.0, 3.0)
        assert rect.area == 15.0
    
    def test_area_square(self) -> None:
        """Test area of square."""
        square = Rectangle(4.0, 4.0)
        assert square.area == 16.0
    
    def test_perimeter(self) -> None:
        """Test perimeter calculation."""
        rect = Rectangle(5.0, 3.0)
        assert rect.perimeter == 16.0
    
    def test_perimeter_square(self) -> None:
        """Test perimeter of square."""
        square = Rectangle(4.0, 4.0)
        assert square.perimeter == 16.0


class TestCircle:
    """Test suite for Circle."""
    
    def test_initialization(self) -> None:
        """Test circle initialization."""
        circle = Circle(5.0)
        assert circle._radius == 5.0
    
    def test_initialization_negative_radius_raises(self) -> None:
        """Test that negative radius raises ValueError."""
        with pytest.raises(ValueError, match="Radius"):
            Circle(-5.0)
    
    def test_initialization_zero_radius_raises(self) -> None:
        """Test that zero radius raises ValueError."""
        with pytest.raises(ValueError, match="Radius"):
            Circle(0.0)
    
    def test_area(self) -> None:
        """Test area calculation."""
        circle = Circle(5.0)
        expected_area = math.pi * 25.0
        assert circle.area == pytest.approx(expected_area)
    
    def test_area_unit_circle(self) -> None:
        """Test area of unit circle."""
        circle = Circle(1.0)
        assert circle.area == pytest.approx(math.pi)
    
    def test_perimeter(self) -> None:
        """Test perimeter (circumference) calculation."""
        circle = Circle(5.0)
        expected_perimeter = 2 * math.pi * 5.0
        assert circle.perimeter == pytest.approx(expected_perimeter)


class TestTriangle:
    """Test suite for Triangle."""
    
    def test_initialization_equilateral(self) -> None:
        """Test equilateral triangle initialization."""
        triangle = Triangle(5.0, 5.0, 5.0)
        assert triangle._side_a == 5.0
        assert triangle._side_b == 5.0
        assert triangle._side_c == 5.0
    
    def test_initialization_right_triangle(self) -> None:
        """Test right triangle initialization (3-4-5)."""
        triangle = Triangle(3.0, 4.0, 5.0)
        assert triangle._side_a == 3.0
        assert triangle._side_b == 4.0
        assert triangle._side_c == 5.0
    
    def test_initialization_negative_side_raises(self) -> None:
        """Test that negative side raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            Triangle(-3.0, 4.0, 5.0)
    
    def test_initialization_zero_side_raises(self) -> None:
        """Test that zero side raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            Triangle(0.0, 4.0, 5.0)
    
    def test_initialization_invalid_triangle_raises(self) -> None:
        """Test that invalid triangle (violating inequality) raises ValueError."""
        with pytest.raises(ValueError, match="triangle"):
            Triangle(1.0, 2.0, 10.0)  # 1 + 2 < 10
    
    def test_perimeter_equilateral(self) -> None:
        """Test perimeter of equilateral triangle."""
        triangle = Triangle(5.0, 5.0, 5.0)
        assert triangle.perimeter == 15.0
    
    def test_perimeter_right_triangle(self) -> None:
        """Test perimeter of right triangle."""
        triangle = Triangle(3.0, 4.0, 5.0)
        assert triangle.perimeter == 12.0
    
    def test_area_equilateral(self) -> None:
        """Test area of equilateral triangle using Heron's formula."""
        triangle = Triangle(5.0, 5.0, 5.0)
        # s = 7.5, area = sqrt(7.5 * 2.5 * 2.5 * 2.5)
        expected_area = math.sqrt(7.5 * 2.5 * 2.5 * 2.5)
        assert triangle.area == pytest.approx(expected_area)
    
    def test_area_right_triangle(self) -> None:
        """Test area of right triangle (3-4-5)."""
        triangle = Triangle(3.0, 4.0, 5.0)
        # Area = (3 * 4) / 2 = 6
        assert triangle.area == 6.0
