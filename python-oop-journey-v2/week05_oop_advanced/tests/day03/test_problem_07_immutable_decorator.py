"""Tests for Problem 07: Immutable Decorator."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day03.problem_07_immutable_decorator import (
    immutable, Point, Color
)


class TestImmutableDecorator:
    """Tests for the immutable decorator."""
    
    def test_immutable_allows_init(self) -> None:
        """Test that initialization works normally."""
        point = Point(1, 2)
        assert point.x == 1
        assert point.y == 2
    
    def test_immutable_blocks_setattr(self) -> None:
        """Test that setting attributes after init raises AttributeError."""
        point = Point(1, 2)
        
        with pytest.raises(AttributeError) as exc_info:
            point.x = 10
        
        assert "immutable" in str(exc_info.value).lower()
    
    def test_immutable_blocks_new_attr(self) -> None:
        """Test that adding new attributes raises AttributeError."""
        point = Point(1, 2)
        
        with pytest.raises(AttributeError):
            point.z = 3
    
    def test_immutable_blocks_delattr(self) -> None:
        """Test that deleting attributes raises AttributeError."""
        point = Point(1, 2)
        
        with pytest.raises(AttributeError) as exc_info:
            del point.x
        
        assert "immutable" in str(exc_info.value).lower()
    
    def test_immutable_color_class(self) -> None:
        """Test immutability with Color class."""
        color = Color(255, 128, 0)
        
        assert color.r == 255
        assert color.g == 128
        assert color.b == 0
        assert color.to_hex() == "#ff8000"
        
        with pytest.raises(AttributeError):
            color.r = 0


class TestImmutableEdgeCases:
    """Tests for immutable edge cases."""
    
    def test_immutable_multiple_instances(self) -> None:
        """Test that multiple immutable instances work independently."""
        point1 = Point(1, 2)
        point2 = Point(3, 4)
        
        assert point1.x == 1
        assert point2.x == 3
        
        # Both should be immutable
        with pytest.raises(AttributeError):
            point1.x = 10
        
        with pytest.raises(AttributeError):
            point2.x = 10
    
    def test_immutable_repr(self) -> None:
        """Test that repr works for immutable objects."""
        point = Point(5, 10)
        assert repr(point) == "Point(5, 10)"
        
        color = Color(0, 255, 0)
        assert repr(color) == "Color(0, 255, 0)"
