"""Tests for Problem 08: Rotate Image."""

from __future__ import annotations

from week01_fundamentals.solutions.day05.problem_08_rotate_image import rotate_image


def test_rotate_image_3x3() -> None:
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    expected = [
        [7, 4, 1],
        [8, 5, 2],
        [9, 6, 3]
    ]
    rotate_image(matrix)
    assert matrix == expected


def test_rotate_image_1x1() -> None:
    matrix = [[1]]
    rotate_image(matrix)
    assert matrix == [[1]]


def test_rotate_image_2x2() -> None:
    matrix = [
        [1, 2],
        [3, 4]
    ]
    expected = [
        [3, 1],
        [4, 2]
    ]
    rotate_image(matrix)
    assert matrix == expected


def test_rotate_image_4x4() -> None:
    matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]
    expected = [
        [13, 9, 5, 1],
        [14, 10, 6, 2],
        [15, 11, 7, 3],
        [16, 12, 8, 4]
    ]
    rotate_image(matrix)
    assert matrix == expected


def test_rotate_image_empty() -> None:
    matrix: list[list[int]] = []
    rotate_image(matrix)
    assert matrix == []


def test_rotate_image_single_row() -> None:
    matrix: list[list[int]] = [[]]
    rotate_image(matrix)
    assert matrix == [[]]
