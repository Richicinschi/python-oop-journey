"""Tests for Problem 02."""

from __future__ import annotations

from week00_getting_started.solutions.day06.problem_02_format_sum_output import format_sum_output


def test_format_sum() -> None:
    """Test case 1."""
    assert format_sum_output(5, 3) == 'The sum of 5 and 3 is 8'
    assert format_sum_output(10, 20) == 'The sum of 10 and 20 is 30'


def test_format_zero() -> None:
    """Test case 2."""
    assert format_sum_output(0, 0) == 'The sum of 0 and 0 is 0'


def test_format_negative() -> None:
    """Test case 3."""
    assert format_sum_output(-5, 3) == 'The sum of -5 and 3 is -2'
