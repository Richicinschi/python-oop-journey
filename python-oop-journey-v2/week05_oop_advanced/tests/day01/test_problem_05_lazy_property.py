"""Tests for Problem 05: Lazy Property."""

from __future__ import annotations

import math
import pytest

from week05_oop_advanced.solutions.day01.problem_05_lazy_property import (
    LazyProperty, Circle, DatabaseConnection, Matrix
)


class TestLazyProperty:
    """Tests for the LazyProperty descriptor."""
    
    def test_property_computed_on_first_access(self) -> None:
        call_count = 0
        
        class TestClass:
            @LazyProperty
            def value(self) -> int:
                nonlocal call_count
                call_count += 1
                return 42
        
        obj = TestClass()
        assert call_count == 0
        
        v = obj.value
        assert call_count == 1
        assert v == 42
    
    def test_property_cached_after_first_access(self) -> None:
        call_count = 0
        
        class TestClass:
            @LazyProperty
            def value(self) -> int:
                nonlocal call_count
                call_count += 1
                return 42
        
        obj = TestClass()
        _ = obj.value
        _ = obj.value
        _ = obj.value
        
        assert call_count == 1


class TestCircle:
    """Tests for the Circle class."""
    
    def test_circle_creation(self) -> None:
        circle = Circle(5.0)
        assert circle.radius == 5.0
    
    def test_circle_negative_radius_raises(self) -> None:
        with pytest.raises(ValueError):
            _ = Circle(-5.0)
    
    def test_circle_area(self) -> None:
        circle = Circle(5.0)
        expected_area = math.pi * 25.0
        assert circle.area == expected_area
    
    def test_circle_circumference(self) -> None:
        circle = Circle(5.0)
        expected_circumference = 2 * math.pi * 5.0
        assert circle.circumference == expected_circumference
    
    def test_circle_diameter(self) -> None:
        circle = Circle(5.0)
        assert circle.diameter == 10.0
    
    def test_circle_properties_cached(self) -> None:
        circle = Circle(5.0)
        
        # Access multiple times
        a1 = circle.area
        a2 = circle.area
        assert a1 is a2


class TestDatabaseConnection:
    """Tests for the DatabaseConnection class."""
    
    def test_connection_creation(self) -> None:
        conn = DatabaseConnection("postgresql://localhost/db")
        assert conn.connection_string == "postgresql://localhost/db"
    
    def test_connection_lazy_initialization(self) -> None:
        conn = DatabaseConnection("postgresql://localhost/db")
        assert not conn.is_connected()
        
        _ = conn.connection
        assert conn.is_connected()
    
    def test_connection_string_in_connection(self) -> None:
        conn = DatabaseConnection("postgresql://localhost/db")
        connection = conn.connection
        assert "postgresql://localhost/db" in connection
    
    def test_schema_lazy_loaded(self) -> None:
        conn = DatabaseConnection("postgresql://localhost/db")
        schema = conn.schema
        
        assert "users" in schema
        assert "posts" in schema


class TestMatrix:
    """Tests for the Matrix class."""
    
    def test_matrix_creation(self) -> None:
        matrix = Matrix([[1, 2], [3, 4]])
        assert matrix.data == [[1, 2], [3, 4]]
    
    def test_matrix_transpose(self) -> None:
        matrix = Matrix([[1, 2, 3], [4, 5, 6]])
        transposed = matrix.transpose
        
        expected = [[1, 4], [2, 5], [3, 6]]
        assert transposed.data == expected
    
    def test_matrix_transpose_cached(self) -> None:
        matrix = Matrix([[1, 2], [3, 4]])
        t1 = matrix.transpose
        t2 = matrix.transpose
        assert t1 is t2
    
    def test_matrix_determinant_2x2(self) -> None:
        matrix = Matrix([[1, 2], [3, 4]])
        # det = 1*4 - 2*3 = -2
        assert matrix.determinant == -2
    
    def test_matrix_determinant_3x3(self) -> None:
        matrix = Matrix([[1, 2, 3], [0, 1, 4], [5, 6, 0]])
        # Determinant calculation
        det = matrix.determinant
        assert isinstance(det, float)
    
    def test_matrix_determinant_non_square_raises(self) -> None:
        matrix = Matrix([[1, 2, 3], [4, 5, 6]])
        with pytest.raises(ValueError, match="square"):
            _ = matrix.determinant
