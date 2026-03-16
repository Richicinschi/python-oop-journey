"""Tests for Problem 02: Calculate Rectangle Area."""

from __future__ import annotations

import pytest

from week00_getting_started.solutions.day16.problem_02_calculate_rectangle_area import calculate_rectangle_area


def test_rectangle_with_positive_dimensions() -> None:
    """Test area calculation with positive dimensions."""
    assert calculate_rectangle_area(5.0, 3.0) == 15.0
    assert calculate_rectangle_area(10.0, 4.0) == 40.0


def test_rectangle_with_zero_dimensions() -> None:
    """Test area calculation with zero dimensions."""
    assert calculate_rectangle_area(0.0, 5.0) == 0.0
    assert calculate_rectangle_area(5.0, 0.0) == 0.0
    assert calculate_rectangle_area(0.0, 0.0) == 0.0


def test_rectangle_with_decimal_dimensions() -> None:
    """Test area calculation with decimal dimensions."""
    assert calculate_rectangle_area(2.5, 4.0) == 10.0
    assert calculate_rectangle_area(3.3, 3.3) == pytest.approx(10.89)


def test_square() -> None:
    """Test area calculation with equal length and width (square)."""
    assert calculate_rectangle_area(4.0, 4.0) == 16.0
    assert calculate_rectangle_area(1.0, 1.0) == 1.0
