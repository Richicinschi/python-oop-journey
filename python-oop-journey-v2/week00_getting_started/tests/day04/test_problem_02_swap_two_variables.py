"""Tests for Problem 02."""

from __future__ import annotations

from week00_getting_started.solutions.day04.problem_02_swap_two_variables import swap_two_variables


def test_swap_integers() -> None:
    """Test case 1."""
    assert swap_two_variables(3, 7) == (7, 3)
    assert swap_two_variables(0, 5) == (5, 0)
    assert swap_two_variables(-1, 1) == (1, -1)


def test_swap_strings() -> None:
    """Test case 2."""
    assert swap_two_variables('a', 'b') == ('b', 'a')
    assert swap_two_variables('hello', 'world') == ('world', 'hello')


def test_swap_same_value() -> None:
    """Test case 3."""
    assert swap_two_variables(5, 5) == (5, 5)
    assert swap_two_variables('x', 'x') == ('x', 'x')
