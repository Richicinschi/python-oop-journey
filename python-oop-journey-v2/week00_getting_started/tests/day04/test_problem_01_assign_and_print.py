"""Tests for Problem 01."""

from __future__ import annotations

from week00_getting_started.solutions.day04.problem_01_assign_and_print import assign_and_print


def test_assign_integer() -> None:
    """Test case 1."""
    assert assign_and_print(42) == 42
    assert assign_and_print(0) == 0
    assert assign_and_print(-5) == -5


def test_assign_string() -> None:
    """Test case 2."""
    assert assign_and_print('hello') == 'hello'
    assert assign_and_print('') == ''
    assert assign_and_print('Python') == 'Python'
