"""Tests for Problem 05: Shape Hierarchy."""

from __future__ import annotations

import math
import pytest

from week04_oop_intermediate.solutions.day01.problem_05_shape_hierarchy import (
    Shape, Circle, Rectangle, Triangle
)


class TestShape:
    """Tests for the base Shape class (abstract)."""
    
    def test_shape_area_not_implemented(self) -> None:
        shape = Shape()
        with pytest.raises(NotImplementedError):
            shape.area()
    
    def test_shape_perimeter_not_implemented(self) -> None:
        shape = Shape()
        with pytest.raises(NotImplementedError):
            shape.perimeter()
    
    def test_shape_scale_not_implemented(self) -> None:
        shape = Shape()
        with pytest.raises(NotImplementedError):
            shape.scale(2.0)


class TestCircle:
    """Tests for the Circle class."""
    
    def test_circle_inheritance(self) -> None:
        circle = Circle(5.0)
        assert isinstance(circle, Shape)
    
    def test_circle_init(self) -> None:
        circle = Circle(5.0)
        assert circle.radius == 5.0
    
    def test_circle_init_negative_radius(self) -> None:
        with pytest.raises(ValueError, match="negative"):
            Circle(-5.0)
    
    def test_circle_area(self) -> None:
        circle = Circle(5.0)
        expected = math.pi * 25.0
        assert circle.area() == pytest.approx(expected)
    
    def test_circle_perimeter(self) -> None:
        circle = Circle(5.0)
        expected = 2 * math.pi * 5.0
        assert circle.perimeter() == pytest.approx(expected)
    
    def test_circle_describe(self) -> None:
        circle = Circle(5.0)
        desc = circle.describe()
        assert "Circle" in desc
        assert "radius=5.00" in desc
    
    def test_circle_scale(self) -> None:
        circle = Circle(5.0)
        circle.scale(2.0)
        assert circle.radius == 10.0
    
    def test_circle_get_diameter(self) -> None:
        circle = Circle(5.0)
        assert circle.get_diameter() == 10.0


class TestRectangle:
    """Tests for the Rectangle class."""
    
    def test_rectangle_inheritance(self) -> None:
        rect = Rectangle(4.0, 5.0)
        assert isinstance(rect, Shape)
    
    def test_rectangle_init(self) -> None:
        rect = Rectangle(4.0, 5.0)
        assert rect.width == 4.0
        assert rect.height == 5.0
    
    def test_rectangle_init_negative(self) -> None:
        with pytest.raises(ValueError, match="negative"):
            Rectangle(-4.0, 5.0)
    
    def test_rectangle_area(self) -> None:
        rect = Rectangle(4.0, 5.0)
        assert rect.area() == 20.0
    
    def test_rectangle_perimeter(self) -> None:
        rect = Rectangle(4.0, 5.0)
        assert rect.perimeter() == 18.0
    
    def test_rectangle_describe(self) -> None:
        rect = Rectangle(4.0, 5.0)
        desc = rect.describe()
        assert "Rectangle" in desc
        assert "4.00x5.00" in desc
    
    def test_rectangle_scale(self) -> None:
        rect = Rectangle(4.0, 5.0)
        rect.scale(2.0)
        assert rect.width == 8.0
        assert rect.height == 10.0
    
    def test_rectangle_is_square_true(self) -> None:
        rect = Rectangle(5.0, 5.0)
        assert rect.is_square() is True
    
    def test_rectangle_is_square_false(self) -> None:
        rect = Rectangle(4.0, 5.0)
        assert rect.is_square() is False


class TestTriangle:
    """Tests for the Triangle class."""
    
    def test_triangle_inheritance(self) -> None:
        triangle = Triangle(3.0, 4.0, 5.0)
        assert isinstance(triangle, Shape)
    
    def test_triangle_init(self) -> None:
        triangle = Triangle(3.0, 4.0, 5.0)
        assert triangle.a == 3.0
        assert triangle.b == 4.0
        assert triangle.c == 5.0
    
    def test_triangle_init_negative(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            Triangle(-3.0, 4.0, 5.0)
    
    def test_triangle_init_invalid(self) -> None:
        with pytest.raises(ValueError, match="triangle inequality"):
            Triangle(1.0, 1.0, 10.0)
    
    def test_triangle_area(self) -> None:
        triangle = Triangle(3.0, 4.0, 5.0)
        expected = 6.0  # Right triangle with area = 6
        assert triangle.area() == pytest.approx(expected)
    
    def test_triangle_perimeter(self) -> None:
        triangle = Triangle(3.0, 4.0, 5.0)
        assert triangle.perimeter() == 12.0
    
    def test_triangle_describe(self) -> None:
        triangle = Triangle(3.0, 4.0, 5.0)
        desc = triangle.describe()
        assert "Triangle" in desc
        assert "3.00,4.00,5.00" in desc
    
    def test_triangle_scale(self) -> None:
        triangle = Triangle(3.0, 4.0, 5.0)
        triangle.scale(2.0)
        assert triangle.a == 6.0
        assert triangle.b == 8.0
        assert triangle.c == 10.0
    
    def test_triangle_equilateral(self) -> None:
        triangle = Triangle(5.0, 5.0, 5.0)
        assert triangle.get_triangle_type() == "equilateral"
    
    def test_triangle_isosceles(self) -> None:
        triangle = Triangle(5.0, 5.0, 6.0)
        assert triangle.get_triangle_type() == "isosceles"
    
    def test_triangle_scalene(self) -> None:
        triangle = Triangle(3.0, 4.0, 5.0)
        assert triangle.get_triangle_type() == "scalene"


class TestPolymorphism:
    """Tests demonstrating polymorphic behavior."""
    
    def test_polymorphic_area(self) -> None:
        shapes: list[Shape] = [
            Circle(5.0),  # area = ~78.5
            Rectangle(4.0, 5.0),  # area = 20
            Triangle(3.0, 4.0, 5.0)  # area = 6
        ]
        
        areas = [s.area() for s in shapes]
        assert areas[0] == pytest.approx(math.pi * 25.0)
        assert areas[1] == 20.0
        assert areas[2] == pytest.approx(6.0)
    
    def test_polymorphic_perimeter(self) -> None:
        shapes: list[Shape] = [
            Circle(5.0),
            Rectangle(4.0, 5.0),
            Triangle(3.0, 4.0, 5.0)
        ]
        
        perimeters = [s.perimeter() for s in shapes]
        assert perimeters[0] == pytest.approx(2 * math.pi * 5.0)
        assert perimeters[1] == 18.0
        assert perimeters[2] == 12.0
    
    def test_polymorphic_scale(self) -> None:
        shapes: list[Shape] = [
            Circle(5.0),
            Rectangle(4.0, 5.0),
            Triangle(3.0, 4.0, 5.0)
        ]
        
        for shape in shapes:
            before_area = shape.area()
            shape.scale(2.0)
            after_area = shape.area()
            assert after_area == pytest.approx(before_area * 4.0)  # Area scales by square


class TestShapeCollection:
    """Tests for working with collections of shapes."""
    
    def test_total_area(self) -> None:
        shapes: list[Shape] = [
            Circle(1.0),  # pi
            Rectangle(2.0, 2.0),  # 4
            Triangle(3.0, 4.0, 5.0)  # 6
        ]
        
        total = sum(s.area() for s in shapes)
        expected = math.pi + 4.0 + 6.0
        assert total == pytest.approx(expected)
    
    def test_total_perimeter(self) -> None:
        shapes: list[Shape] = [
            Circle(1.0),  # 2*pi
            Rectangle(2.0, 2.0),  # 8
            Triangle(3.0, 4.0, 5.0)  # 12
        ]
        
        total = sum(s.perimeter() for s in shapes)
        expected = 2 * math.pi + 8.0 + 12.0
        assert total == pytest.approx(expected)
