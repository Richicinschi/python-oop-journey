"""Tests for Problem 03."""

from __future__ import annotations

from week00_getting_started.solutions.day05.problem_03_convert_to_string import convert_to_string


def test_convert_positive() -> None:
    """Test case 1."""
    assert convert_to_string(42) == 'Value: 42'
    assert convert_to_string(0) == 'Value: 0'


def test_convert_negative() -> None:
    """Test case 2."""
    assert convert_to_string(-5) == 'Value: -5'
    assert convert_to_string(-100) == 'Value: -100'
