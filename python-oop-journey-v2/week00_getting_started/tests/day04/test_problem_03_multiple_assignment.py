"""Tests for Problem 03."""

from __future__ import annotations

from week00_getting_started.solutions.day04.problem_03_multiple_assignment import multiple_assignment


def test_multiple_integers() -> None:
    """Test case 1."""
    assert multiple_assignment(1, 2, 3) == (1, 2, 3)
    assert multiple_assignment(0, 0, 0) == (0, 0, 0)


def test_multiple_strings() -> None:
    """Test case 2."""
    assert multiple_assignment('a', 'b', 'c') == ('a', 'b', 'c')


def test_multiple_mixed() -> None:
    """Test case 3."""
    assert multiple_assignment(1, 'two', 3) == (1, 'two', 3)
