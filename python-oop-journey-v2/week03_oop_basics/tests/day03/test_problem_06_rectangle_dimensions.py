"""Tests for Problem 06: Rectangle Dimensions."""

from __future__ import annotations

import math

import pytest

from week03_oop_basics.solutions.day03.problem_06_rectangle_dimensions import (
    Rectangle,
)


class TestRectangle:
    """Test suite for Rectangle class."""
    
    def test_initialization(self) -> None:
        """Test rectangle initialization."""
        rect = Rectangle(5.0, 3.0)
        assert rect.width == 5.0
        assert rect.height == 3.0
    
    def test_initialization_type_conversion(self) -> None:
        """Test that dimensions are converted to float."""
        rect = Rectangle(5, 3)
        assert isinstance(rect.width, float)
        assert isinstance(rect.height, float)
    
    def test_initialization_zero_width_raises(self) -> None:
        """Test initialization with zero width raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            Rectangle(0.0, 3.0)
    
    def test_initialization_negative_width_raises(self) -> None:
        """Test initialization with negative width raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            Rectangle(-5.0, 3.0)
    
    def test_initialization_zero_height_raises(self) -> None:
        """Test initialization with zero height raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            Rectangle(5.0, 0.0)
    
    def test_initialization_non_number_width_raises(self) -> None:
        """Test initialization with non-number width raises TypeError."""
        with pytest.raises(TypeError, match="number"):
            Rectangle("five", 3.0)  # type: ignore
    
    def test_width_setter_valid(self) -> None:
        """Test width setter with valid value."""
        rect = Rectangle(5.0, 3.0)
        rect.width = 10.0
        assert rect.width == 10.0
    
    def test_width_setter_negative_raises(self) -> None:
        """Test width setter with negative value raises ValueError."""
        rect = Rectangle(5.0, 3.0)
        with pytest.raises(ValueError, match="positive"):
            rect.width = -5.0
    
    def test_width_setter_non_number_raises(self) -> None:
        """Test width setter with non-number raises TypeError."""
        rect = Rectangle(5.0, 3.0)
        with pytest.raises(TypeError, match="number"):
            rect.width = "wide"  # type: ignore
    
    def test_height_setter_valid(self) -> None:
        """Test height setter with valid value."""
        rect = Rectangle(5.0, 3.0)
        rect.height = 6.0
        assert rect.height == 6.0
    
    def test_height_setter_negative_raises(self) -> None:
        """Test height setter with negative value raises ValueError."""
        rect = Rectangle(5.0, 3.0)
        with pytest.raises(ValueError, match="positive"):
            rect.height = -3.0
    
    def test_area(self) -> None:
        """Test area calculation."""
        rect = Rectangle(5.0, 3.0)
        assert rect.area == 15.0
    
    def test_area_after_resize(self) -> None:
        """Test area after changing dimensions."""
        rect = Rectangle(5.0, 3.0)
        rect.width = 10.0
        rect.height = 4.0
        assert rect.area == 40.0
    
    def test_area_read_only(self) -> None:
        """Test that area is read-only."""
        rect = Rectangle(5.0, 3.0)
        with pytest.raises(AttributeError):
            rect.area = 100  # type: ignore
    
    def test_perimeter(self) -> None:
        """Test perimeter calculation."""
        rect = Rectangle(5.0, 3.0)
        assert rect.perimeter == 16.0
    
    def test_perimeter_read_only(self) -> None:
        """Test that perimeter is read-only."""
        rect = Rectangle(5.0, 3.0)
        with pytest.raises(AttributeError):
            rect.perimeter = 20  # type: ignore
    
    def test_diagonal(self) -> None:
        """Test diagonal calculation."""
        rect = Rectangle(3.0, 4.0)
        assert rect.diagonal == 5.0
    
    def test_diagonal_square(self) -> None:
        """Test diagonal of a square."""
        rect = Rectangle(1.0, 1.0)
        assert abs(rect.diagonal - math.sqrt(2)) < 0.0001
    
    def test_diagonal_read_only(self) -> None:
        """Test that diagonal is read-only."""
        rect = Rectangle(5.0, 3.0)
        with pytest.raises(AttributeError):
            rect.diagonal = 10  # type: ignore
    
    def test_is_square_true(self) -> None:
        """Test is_square returns True for square."""
        rect = Rectangle(5.0, 5.0)
        assert rect.is_square is True
    
    def test_is_square_false(self) -> None:
        """Test is_square returns False for non-square."""
        rect = Rectangle(5.0, 3.0)
        assert rect.is_square is False
    
    def test_is_square_read_only(self) -> None:
        """Test that is_square is read-only."""
        rect = Rectangle(5.0, 3.0)
        with pytest.raises(AttributeError):
            rect.is_square = True  # type: ignore
    
    def test_aspect_ratio(self) -> None:
        """Test aspect_ratio calculation."""
        rect = Rectangle(6.0, 3.0)
        assert rect.aspect_ratio == 2.0
    
    def test_scale(self) -> None:
        """Test scale method."""
        rect = Rectangle(5.0, 3.0)
        rect.scale(2.0)
        assert rect.width == 10.0
        assert rect.height == 6.0
        assert rect.area == 60.0
    
    def test_scale_non_positive_raises(self) -> None:
        """Test scale with non-positive factor raises ValueError."""
        rect = Rectangle(5.0, 3.0)
        with pytest.raises(ValueError, match="positive"):
            rect.scale(0.0)
        with pytest.raises(ValueError, match="positive"):
            rect.scale(-1.0)
