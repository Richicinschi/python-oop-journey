"""Tests for Problem 05."""

from __future__ import annotations

from week00_getting_started.solutions.day06.problem_05_format_calculation_table import format_calculation_table


def test_table() -> None:
    """Test case 1."""
    assert format_calculation_table(5) == '5 x 1 = 5\n5 x 2 = 10\n5 x 3 = 15'


def test_table_zero() -> None:
    """Test case 2."""
    assert format_calculation_table(0) == '0 x 1 = 0\n0 x 2 = 0\n0 x 3 = 0'


def test_table_one() -> None:
    """Test case 3."""
    assert format_calculation_table(1) == '1 x 1 = 1\n1 x 2 = 2\n1 x 3 = 3'
