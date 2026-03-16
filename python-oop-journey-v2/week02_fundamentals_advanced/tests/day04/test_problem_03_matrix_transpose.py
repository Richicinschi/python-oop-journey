"""Tests for Problem 03: Matrix Transpose."""

from __future__ import annotations

from week02_fundamentals_advanced.solutions.day04.problem_03_matrix_transpose import (
    matrix_transpose,
)


def test_basic_transpose() -> None:
    """Test basic 2x3 matrix transpose."""
    matrix = [[1, 2, 3], [4, 5, 6]]
    assert matrix_transpose(matrix) == [[1, 4], [2, 5], [3, 6]]


def test_transpose_back_to_original() -> None:
    """Test that transpose is reversible."""
    matrix = [[1, 2, 3], [4, 5, 6]]
    transposed = matrix_transpose(matrix)
    assert matrix_transpose(transposed) == matrix


def test_square_matrix() -> None:
    """Test with square matrix."""
    matrix = [[1, 2], [3, 4]]
    assert matrix_transpose(matrix) == [[1, 3], [2, 4]]


def test_single_row() -> None:
    """Test with single row matrix."""
    matrix = [[1, 2, 3]]
    assert matrix_transpose(matrix) == [[1], [2], [3]]


def test_single_column() -> None:
    """Test with single column matrix."""
    matrix = [[1], [2], [3]]
    assert matrix_transpose(matrix) == [[1, 2, 3]]


def test_1x1_matrix() -> None:
    """Test with 1x1 matrix."""
    matrix = [[42]]
    assert matrix_transpose(matrix) == [[42]]


def test_empty_matrix() -> None:
    """Test with empty matrix."""
    assert matrix_transpose([]) == []


def test_negative_numbers() -> None:
    """Test with negative numbers."""
    matrix = [[-1, -2], [-3, -4]]
    assert matrix_transpose(matrix) == [[-1, -3], [-2, -4]]


def test_mixed_numbers() -> None:
    """Test with mixed positive and negative numbers."""
    matrix = [[1, -2, 3], [-4, 5, -6]]
    assert matrix_transpose(matrix) == [[1, -4], [-2, 5], [3, -6]]


def test_rectangular_matrix() -> None:
    """Test with 3x2 matrix."""
    matrix = [[1, 2], [3, 4], [5, 6]]
    assert matrix_transpose(matrix) == [[1, 3, 5], [2, 4, 6]]
