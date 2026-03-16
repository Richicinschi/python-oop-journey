"""Tests for Problem 09: Pascal's Triangle."""

from __future__ import annotations

from week01_fundamentals.solutions.day05.problem_09_pascals_triangle import pascals_triangle


def test_pascals_triangle_5_rows() -> None:
    result = pascals_triangle(5)
    expected = [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1]
    ]
    assert result == expected


def test_pascals_triangle_1_row() -> None:
    assert pascals_triangle(1) == [[1]]


def test_pascals_triangle_2_rows() -> None:
    assert pascals_triangle(2) == [[1], [1, 1]]


def test_pascals_triangle_3_rows() -> None:
    assert pascals_triangle(3) == [[1], [1, 1], [1, 2, 1]]


def test_pascals_triangle_0_rows() -> None:
    assert pascals_triangle(0) == []


def test_pascals_triangle_negative() -> None:
    assert pascals_triangle(-1) == []


def test_pascals_triangle_6_rows() -> None:
    result = pascals_triangle(6)
    expected = [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1],
        [1, 5, 10, 10, 5, 1]
    ]
    assert result == expected
