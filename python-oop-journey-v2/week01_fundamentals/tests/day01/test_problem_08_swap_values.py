"""Tests for Problem 08: Swap Values."""

from __future__ import annotations

from week01_fundamentals.solutions.day01.problem_08_swap_values import swap_values


def test_swap_integers() -> None:
    """Test swapping integers."""
    assert swap_values(5, 10) == (10, 5)
    assert swap_values(-5, 5) == (5, -5)
    assert swap_values(0, 0) == (0, 0)


def test_swap_strings() -> None:
    """Test swapping strings."""
    assert swap_values('a', 'b') == ('b', 'a')
    assert swap_values('hello', 'world') == ('world', 'hello')


def test_swap_mixed_types() -> None:
    """Test swapping values of same type but different values."""
    result = swap_values(1, 2)
    assert result == (2, 1)
    assert isinstance(result[0], int)
    assert isinstance(result[1], int)


def test_swap_floats() -> None:
    """Test swapping floats."""
    assert swap_values(1.5, 2.5) == (2.5, 1.5)
    assert swap_values(-3.14, 3.14) == (3.14, -3.14)


def test_swap_same_values() -> None:
    """Test swapping identical values."""
    assert swap_values(5, 5) == (5, 5)
    assert swap_values('x', 'x') == ('x', 'x')


def test_unpacking_usage() -> None:
    """Test that the result can be unpacked."""
    a, b = swap_values(1, 2)
    assert a == 2
    assert b == 1

    x, y = swap_values('first', 'second')
    assert x == 'second'
    assert y == 'first'
