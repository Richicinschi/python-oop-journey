"""Tests for Problem 01: Vector 2D."""

from __future__ import annotations

import math

import pytest

from week03_oop_basics.solutions.day04.problem_01_vector_2d import Vector2D


class TestVector2DInit:
    """Test Vector2D initialization."""
    
    def test_init_with_positive_values(self) -> None:
        v = Vector2D(3, 4)
        assert v.x == 3
        assert v.y == 4
    
    def test_init_with_negative_values(self) -> None:
        v = Vector2D(-3, -4)
        assert v.x == -3
        assert v.y == -4
    
    def test_init_with_zero(self) -> None:
        v = Vector2D(0, 0)
        assert v.x == 0
        assert v.y == 0
    
    def test_init_with_floats(self) -> None:
        v = Vector2D(1.5, 2.5)
        assert v.x == 1.5
        assert v.y == 2.5


class TestVector2DAddition:
    """Test Vector2D addition."""
    
    def test_add_two_vectors(self) -> None:
        v1 = Vector2D(1, 2)
        v2 = Vector2D(3, 4)
        result = v1 + v2
        assert result.x == 4
        assert result.y == 6
    
    def test_add_with_negative_components(self) -> None:
        v1 = Vector2D(1, -2)
        v2 = Vector2D(-3, 4)
        result = v1 + v2
        assert result.x == -2
        assert result.y == 2
    
    def test_add_returns_new_vector(self) -> None:
        v1 = Vector2D(1, 2)
        v2 = Vector2D(3, 4)
        result = v1 + v2
        assert result is not v1
        assert result is not v2
    
    def test_add_with_non_vector_returns_not_implemented(self) -> None:
        v = Vector2D(1, 2)
        result = v.__add__("not a vector")
        assert result is NotImplemented


class TestVector2DSubtraction:
    """Test Vector2D subtraction."""
    
    def test_subtract_two_vectors(self) -> None:
        v1 = Vector2D(5, 7)
        v2 = Vector2D(2, 3)
        result = v1 - v2
        assert result.x == 3
        assert result.y == 4
    
    def test_subtract_with_negative_result(self) -> None:
        v1 = Vector2D(1, 2)
        v2 = Vector2D(3, 4)
        result = v1 - v2
        assert result.x == -2
        assert result.y == -2
    
    def test_subtract_with_non_vector_returns_not_implemented(self) -> None:
        v = Vector2D(1, 2)
        result = v.__sub__("not a vector")
        assert result is NotImplemented


class TestVector2DMultiplication:
    """Test Vector2D scalar multiplication."""
    
    def test_multiply_by_positive_scalar(self) -> None:
        v = Vector2D(2, 3)
        result = v * 2
        assert result.x == 4
        assert result.y == 6
    
    def test_multiply_by_zero(self) -> None:
        v = Vector2D(2, 3)
        result = v * 0
        assert result.x == 0
        assert result.y == 0
    
    def test_multiply_by_negative_scalar(self) -> None:
        v = Vector2D(2, 3)
        result = v * -2
        assert result.x == -4
        assert result.y == -6
    
    def test_multiply_by_float(self) -> None:
        v = Vector2D(2, 4)
        result = v * 0.5
        assert result.x == 1.0
        assert result.y == 2.0
    
    def test_rmul_reversed_multiplication(self) -> None:
        v = Vector2D(2, 3)
        result = 3 * v
        assert result.x == 6
        assert result.y == 9
    
    def test_multiply_by_non_number_returns_not_implemented(self) -> None:
        v = Vector2D(1, 2)
        result = v.__mul__("not a number")
        assert result is NotImplemented


class TestVector2DRepr:
    """Test Vector2D representation."""
    
    def test_repr(self) -> None:
        v = Vector2D(3, 4)
        assert repr(v) == "Vector2D(3, 4)"
    
    def test_repr_with_floats(self) -> None:
        v = Vector2D(1.5, 2.5)
        assert repr(v) == "Vector2D(1.5, 2.5)"


class TestVector2DMagnitude:
    """Test Vector2D magnitude calculation."""
    
    def test_magnitude_simple(self) -> None:
        v = Vector2D(3, 4)
        assert v.magnitude() == 5.0
    
    def test_magnitude_zero_vector(self) -> None:
        v = Vector2D(0, 0)
        assert v.magnitude() == 0.0
    
    def test_magnitude_negative_components(self) -> None:
        v = Vector2D(-3, -4)
        assert v.magnitude() == 5.0
    
    def test_magnitude_with_floats(self) -> None:
        v = Vector2D(1, 1)
        assert math.isclose(v.magnitude(), math.sqrt(2))
