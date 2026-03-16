"""Tests for Problem 07: Spiral Matrix."""

from __future__ import annotations

from week01_fundamentals.solutions.day05.problem_07_spiral_matrix import spiral_matrix


def test_spiral_matrix_3x3() -> None:
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    expected = [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert spiral_matrix(matrix) == expected


def test_spiral_matrix_3x4() -> None:
    matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ]
    expected = [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    assert spiral_matrix(matrix) == expected


def test_spiral_matrix_1x1() -> None:
    matrix = [[1]]
    assert spiral_matrix(matrix) == [1]


def test_spiral_matrix_1xn() -> None:
    matrix = [[1, 2, 3, 4, 5]]
    assert spiral_matrix(matrix) == [1, 2, 3, 4, 5]


def test_spiral_matrix_mx1() -> None:
    matrix = [[1], [2], [3], [4]]
    assert spiral_matrix(matrix) == [1, 2, 3, 4]


def test_spiral_matrix_2x2() -> None:
    matrix = [
        [1, 2],
        [3, 4]
    ]
    expected = [1, 2, 4, 3]
    assert spiral_matrix(matrix) == expected


def test_spiral_matrix_empty() -> None:
    assert spiral_matrix([]) == []
    assert spiral_matrix([[]]) == []


def test_spiral_matrix_2x3() -> None:
    matrix = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    expected = [1, 2, 3, 6, 5, 4]
    assert spiral_matrix(matrix) == expected
