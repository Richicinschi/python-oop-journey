"""Tests for Problem 03: Visitor Shape Export."""

from __future__ import annotations

import pytest
import math

from week06_patterns.solutions.day04.problem_03_visitor_shape_export import (
    Shape,
    Circle,
    Rectangle,
    Triangle,
    ShapeVisitor,
    XMLExportVisitor,
    JSONExportVisitor,
    AreaCalculatorVisitor,
    ShapeCollection,
)


class TestShapeClasses:
    """Tests for shape implementations."""
    
    def test_circle_creation(self) -> None:
        """Circle can be created with radius and position."""
        circle = Circle(5.0, 1.0, 2.0)
        assert circle.radius == 5.0
        assert circle.x == 1.0
        assert circle.y == 2.0
    
    def test_circle_area(self) -> None:
        """Circle calculates correct area."""
        circle = Circle(5.0)
        expected = math.pi * 25.0
        assert abs(circle.get_area() - expected) < 0.001
    
    def test_rectangle_creation(self) -> None:
        """Rectangle can be created with dimensions."""
        rect = Rectangle(10.0, 5.0, 0, 0)
        assert rect.width == 10.0
        assert rect.height == 5.0
    
    def test_rectangle_area(self) -> None:
        """Rectangle calculates correct area."""
        rect = Rectangle(10.0, 5.0)
        assert rect.get_area() == 50.0
    
    def test_triangle_creation(self) -> None:
        """Triangle can be created with three sides."""
        tri = Triangle(3.0, 4.0, 5.0)
        assert tri.a == 3.0
        assert tri.b == 4.0
        assert tri.c == 5.0
    
    def test_triangle_area(self) -> None:
        """Triangle calculates correct area using Heron's formula."""
        tri = Triangle(3.0, 4.0, 5.0)  # Right triangle
        expected = 6.0  # (3*4)/2
        assert abs(tri.get_area() - expected) < 0.001
    
    def test_triangle_invalid_sides(self) -> None:
        """Triangle with invalid sides returns 0 area."""
        tri = Triangle(1.0, 1.0, 10.0)  # Invalid triangle
        assert tri.get_area() == 0.0


class TestXMLExportVisitor:
    """Tests for XML export visitor."""
    
    def test_visit_circle_xml_format(self) -> None:
        """Circle exported to XML format."""
        visitor = XMLExportVisitor()
        circle = Circle(5.0, 1.0, 2.0)
        result = visitor.visit_circle(circle)
        
        assert result.startswith("<circle")
        assert 'radius="5.00"' in result
        assert 'x="1.00"' in result
        assert 'y="2.00"' in result
        assert "area=" in result
        assert result.endswith("/>")
    
    def test_visit_rectangle_xml_format(self) -> None:
        """Rectangle exported to XML format."""
        visitor = XMLExportVisitor()
        rect = Rectangle(10.0, 5.0, 0, 0)
        result = visitor.visit_rectangle(rect)
        
        assert result.startswith("<rectangle")
        assert 'width="10.00"' in result
        assert 'height="5.00"' in result
        assert result.endswith("/>")
    
    def test_visit_triangle_xml_format(self) -> None:
        """Triangle exported to XML format."""
        visitor = XMLExportVisitor()
        tri = Triangle(3.0, 4.0, 5.0)
        result = visitor.visit_triangle(tri)
        
        assert result.startswith("<triangle")
        assert 'a="3.00"' in result
        assert 'b="4.00"' in result
        assert 'c="5.00"' in result
        assert result.endswith("/>")


class TestJSONExportVisitor:
    """Tests for JSON export visitor."""
    
    def test_visit_circle_json_format(self) -> None:
        """Circle exported to JSON format."""
        visitor = JSONExportVisitor()
        circle = Circle(5.0, 1.0, 2.0)
        result = visitor.visit_circle(circle)
        
        assert result.startswith("{")
        assert '"type": "circle"' in result
        assert '"radius": 5.00' in result
        assert '"x": 1.00' in result
        assert '"y": 2.00' in result
        assert result.endswith("}")
    
    def test_visit_rectangle_json_format(self) -> None:
        """Rectangle exported to JSON format."""
        visitor = JSONExportVisitor()
        rect = Rectangle(10.0, 5.0)
        result = visitor.visit_rectangle(rect)
        
        assert '"type": "rectangle"' in result
        assert '"width": 10.00' in result
        assert '"height": 5.00' in result
    
    def test_visit_triangle_json_format(self) -> None:
        """Triangle exported to JSON format."""
        visitor = JSONExportVisitor()
        tri = Triangle(3.0, 4.0, 5.0)
        result = visitor.visit_triangle(tri)
        
        assert '"type": "triangle"' in result
        assert '"a": 3.00' in result
        assert '"b": 4.00' in result
        assert '"c": 5.00' in result


class TestAreaCalculatorVisitor:
    """Tests for area calculator visitor."""
    
    def test_initial_total_is_zero(self) -> None:
        """Calculator starts with zero total."""
        calc = AreaCalculatorVisitor()
        assert calc.get_total_area() == 0.0
    
    def test_visit_circle_adds_area(self) -> None:
        """Visiting circle adds its area to total."""
        calc = AreaCalculatorVisitor()
        circle = Circle(5.0)  # Area = ~78.54
        calc.visit_circle(circle)
        
        assert calc.get_total_area() > 0
        assert abs(calc.get_total_area() - circle.get_area()) < 0.001
    
    def test_visit_multiple_shapes_accumulates(self) -> None:
        """Visiting multiple shapes accumulates total."""
        calc = AreaCalculatorVisitor()
        rect = Rectangle(10.0, 5.0)  # Area = 50
        tri = Triangle(3.0, 4.0, 5.0)  # Area = 6
        
        calc.visit_rectangle(rect)
        calc.visit_triangle(tri)
        
        assert abs(calc.get_total_area() - 56.0) < 0.001
    
    def test_reset_clears_total(self) -> None:
        """Reset clears accumulated area."""
        calc = AreaCalculatorVisitor()
        calc.visit_rectangle(Rectangle(10.0, 10.0))
        assert calc.get_total_area() > 0
        
        calc.reset()
        assert calc.get_total_area() == 0.0


class TestShapeAccept:
    """Tests for shape accept method (double dispatch)."""
    
    def test_circle_accept_calls_visitor(self) -> None:
        """Circle accept dispatches to visitor method."""
        circle = Circle(5.0)
        visitor = XMLExportVisitor()
        result = circle.accept(visitor)
        
        assert "<circle" in result
    
    def test_rectangle_accept_calls_visitor(self) -> None:
        """Rectangle accept dispatches to visitor method."""
        rect = Rectangle(10.0, 5.0)
        visitor = JSONExportVisitor()
        result = rect.accept(visitor)
        
        assert '"type": "rectangle"' in result
    
    def test_triangle_accept_calls_visitor(self) -> None:
        """Triangle accept dispatches to visitor method."""
        tri = Triangle(3.0, 4.0, 5.0)
        visitor = XMLExportVisitor()
        result = tri.accept(visitor)
        
        assert "<triangle" in result


class TestShapeCollection:
    """Tests for ShapeCollection class."""
    
    def test_empty_collection(self) -> None:
        """Empty collection has no shapes."""
        collection = ShapeCollection()
        visitor = XMLExportVisitor()
        result = collection.accept(visitor)
        assert result == []
    
    def test_add_shape(self) -> None:
        """Shapes can be added to collection."""
        collection = ShapeCollection()
        collection.add(Circle(5.0))
        
        visitor = XMLExportVisitor()
        result = collection.accept(visitor)
        assert len(result) == 1
    
    def test_multiple_shapes(self) -> None:
        """Collection can hold multiple shapes."""
        collection = ShapeCollection()
        collection.add(Circle(5.0))
        collection.add(Rectangle(10.0, 5.0))
        collection.add(Triangle(3.0, 4.0, 5.0))
        
        visitor = JSONExportVisitor()
        result = collection.accept(visitor)
        assert len(result) == 3
    
    def test_visitor_applied_to_all(self) -> None:
        """Visitor is applied to all shapes in collection."""
        collection = ShapeCollection()
        collection.add(Circle(5.0))
        collection.add(Rectangle(10.0, 5.0))
        
        calc = AreaCalculatorVisitor()
        collection.accept(calc)
        
        expected = (math.pi * 25.0) + 50.0
        assert abs(calc.get_total_area() - expected) < 0.01


class TestVisitorPattern:
    """Tests verifying the Visitor pattern structure."""
    
    def test_shape_is_abstract(self) -> None:
        """Shape cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Shape()  # type: ignore[abstract]
    
    def test_visitor_is_abstract(self) -> None:
        """ShapeVisitor cannot be instantiated directly."""
        with pytest.raises(TypeError):
            ShapeVisitor()  # type: ignore[abstract]
    
    def test_all_shapes_inherit_shape(self) -> None:
        """All concrete shapes inherit from Shape."""
        assert issubclass(Circle, Shape)
        assert issubclass(Rectangle, Shape)
        assert issubclass(Triangle, Shape)
    
    def test_all_visitors_inherit_visitor(self) -> None:
        """All concrete visitors implement visitor protocol."""
        assert hasattr(XMLExportVisitor, 'visit_circle')
        assert hasattr(XMLExportVisitor, 'visit_rectangle')
        assert hasattr(XMLExportVisitor, 'visit_triangle')
