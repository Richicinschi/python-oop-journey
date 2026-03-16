"""Tests for Problem 03: Rectangle."""

from __future__ import annotations

from week03_oop_basics.solutions.day01.problem_03_rectangle import Rectangle


def test_rectangle_creation() -> None:
    """Test creating a rectangle."""
    rect = Rectangle(5.0, 3.0)
    assert rect.width == 5.0
    assert rect.height == 3.0


def test_rectangle_area() -> None:
    """Test area calculation."""
    rect = Rectangle(5.0, 3.0)
    assert rect.area() == 15.0


def test_rectangle_perimeter() -> None:
    """Test perimeter calculation."""
    rect = Rectangle(5.0, 3.0)
    assert rect.perimeter() == 16.0


def test_rectangle_is_square_true() -> None:
    """Test is_square returns True for square."""
    rect = Rectangle(5.0, 5.0)
    assert rect.is_square() is True


def test_rectangle_is_square_false() -> None:
    """Test is_square returns False for non-square."""
    rect = Rectangle(5.0, 3.0)
    assert rect.is_square() is False


def test_rectangle_with_integers() -> None:
    """Test rectangle with integer dimensions."""
    rect = Rectangle(4, 6)
    assert rect.area() == 24.0
    assert rect.perimeter() == 20.0


def test_rectangle_square_area() -> None:
    """Test area of a square."""
    rect = Rectangle(4.0, 4.0)
    assert rect.area() == 16.0
    assert rect.is_square() is True


def test_rectangle_str() -> None:
    """Test string representation."""
    rect = Rectangle(5.0, 3.0)
    result = str(rect)
    assert "5.0" in result or "5" in result
    assert "3.0" in result or "3" in result


def test_rectangle_repr() -> None:
    """Test repr representation."""
    rect = Rectangle(5.0, 3.0)
    result = repr(rect)
    assert "Rectangle" in result
