"""Tests for Problem 05: Shape Area Dispatch."""

from __future__ import annotations

import pytest
import math
from abc import ABC

from week04_oop_intermediate.solutions.day05.problem_05_shape_area_dispatch import (
    Shape,
    Rectangle,
    Circle,
    Triangle,
    Square,
    calculate_total_area,
    get_shape_summary,
)


class TestShapeABC:
    """Test suite for Shape abstract base class."""
    
    def test_shape_is_abstract(self) -> None:
        """Test that Shape cannot be instantiated."""
        assert issubclass(Shape, ABC)
        with pytest.raises(TypeError, match="abstract"):
            Shape()


class TestRectangle:
    """Test suite for Rectangle."""
    
    def test_initialization(self) -> None:
        """Test rectangle initialization."""
        rect = Rectangle(5.0, 3.0)
        assert rect.width == 5.0
        assert rect.height == 3.0
    
    def test_area(self) -> None:
        """Test area calculation."""
        rect = Rectangle(5.0, 3.0)
        assert rect.area() == 15.0
    
    def test_area_zero(self) -> None:
        """Test area with zero dimension."""
        rect = Rectangle(5.0, 0.0)
        assert rect.area() == 0.0
    
    def test_get_name(self) -> None:
        """Test get_name method."""
        rect = Rectangle(5.0, 3.0)
        assert rect.get_name() == "Rectangle"


class TestCircle:
    """Test suite for Circle."""
    
    def test_initialization(self) -> None:
        """Test circle initialization."""
        circle = Circle(5.0)
        assert circle.radius == 5.0
    
    def test_area(self) -> None:
        """Test area calculation."""
        circle = Circle(5.0)
        expected = math.pi * 25.0
        assert circle.area() == expected
    
    def test_area_zero_radius(self) -> None:
        """Test area with zero radius."""
        circle = Circle(0.0)
        assert circle.area() == 0.0
    
    def test_get_name(self) -> None:
        """Test get_name method."""
        circle = Circle(5.0)
        assert circle.get_name() == "Circle"


class TestTriangle:
    """Test suite for Triangle."""
    
    def test_initialization(self) -> None:
        """Test triangle initialization."""
        tri = Triangle(10.0, 5.0)
        assert tri.base == 10.0
        assert tri.height == 5.0
    
    def test_area(self) -> None:
        """Test area calculation."""
        tri = Triangle(10.0, 5.0)
        assert tri.area() == 25.0  # 0.5 * 10 * 5
    
    def test_get_name(self) -> None:
        """Test get_name method."""
        tri = Triangle(10.0, 5.0)
        assert tri.get_name() == "Triangle"


class TestSquare:
    """Test suite for Square."""
    
    def test_initialization(self) -> None:
        """Test square initialization."""
        square = Square(5.0)
        assert square.side == 5.0
        assert square.width == 5.0
        assert square.height == 5.0
    
    def test_area(self) -> None:
        """Test area calculation (inherited from Rectangle)."""
        square = Square(5.0)
        assert square.area() == 25.0
    
    def test_get_name(self) -> None:
        """Test get_name method (overridden)."""
        square = Square(5.0)
        assert square.get_name() == "Square"
    
    def test_is_instance_of_rectangle(self) -> None:
        """Test that Square is a Rectangle."""
        square = Square(5.0)
        assert isinstance(square, Rectangle)
        assert isinstance(square, Shape)


class TestCalculateTotalArea:
    """Test suite for calculate_total_area function."""
    
    def test_empty_list(self) -> None:
        """Test with empty list returns 0."""
        result = calculate_total_area([])
        assert result == 0.0
    
    def test_single_shape(self) -> None:
        """Test with single shape."""
        shapes = [Rectangle(5.0, 3.0)]
        result = calculate_total_area(shapes)
        assert result == 15.0
    
    def test_mixed_shapes(self) -> None:
        """Test polymorphic calculation with mixed shapes."""
        shapes = [
            Rectangle(5.0, 3.0),  # 15.0
            Circle(5.0),  # ~78.54
            Triangle(10.0, 5.0),  # 25.0
        ]
        result = calculate_total_area(shapes)
        expected = 15.0 + (math.pi * 25.0) + 25.0
        assert result == expected
    
    def test_with_square(self) -> None:
        """Test that squares work polymorphically."""
        shapes = [
            Rectangle(4.0, 4.0),  # 16.0
            Square(4.0),  # 16.0 (via Rectangle inheritance)
        ]
        result = calculate_total_area(shapes)
        assert result == 32.0


class TestGetShapeSummary:
    """Test suite for get_shape_summary function."""
    
    def test_empty_list(self) -> None:
        """Test with empty list."""
        result = get_shape_summary([])
        
        assert result["total_area"] == 0.0
        assert result["count"] == 0
        assert result["by_type"] == {}
    
    def test_single_shape(self) -> None:
        """Test with single shape."""
        shapes = [Rectangle(5.0, 3.0)]
        result = get_shape_summary(shapes)
        
        assert result["total_area"] == 15.0
        assert result["count"] == 1
        assert result["by_type"] == {"Rectangle": 1}
    
    def test_mixed_shapes(self) -> None:
        """Test summary with mixed shapes."""
        shapes = [
            Rectangle(5.0, 3.0),  # 15.0
            Rectangle(2.0, 2.0),  # 4.0
            Circle(5.0),  # ~78.54
            Triangle(10.0, 5.0),  # 25.0
        ]
        result = get_shape_summary(shapes)
        
        assert result["count"] == 4
        assert result["by_type"] == {
            "Rectangle": 2,
            "Circle": 1,
            "Triangle": 1,
        }
        # Check total area is calculated
        assert result["total_area"] > 0
    
    def test_with_square_inheritance(self) -> None:
        """Test that squares report as Square, not Rectangle."""
        shapes = [
            Rectangle(4.0, 4.0),
            Square(4.0),
        ]
        result = get_shape_summary(shapes)
        
        assert result["by_type"] == {
            "Rectangle": 1,
            "Square": 1,
        }
