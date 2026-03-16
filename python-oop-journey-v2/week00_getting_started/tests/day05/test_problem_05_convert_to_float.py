"""Tests for Problem 05."""

from __future__ import annotations

from week00_getting_started.solutions.day05.problem_05_convert_to_float import convert_to_float


def test_convert_and_round() -> None:
    """Test case 1."""
    assert convert_to_float('3.14159') == 3.14
    assert convert_to_float('2.71828') == 2.72


def test_convert_exact() -> None:
    """Test case 2."""
    assert convert_to_float('2.5') == 2.5
    assert convert_to_float('10.00') == 10.0


def test_convert_whole() -> None:
    """Test case 3."""
    assert convert_to_float('5') == 5.0
