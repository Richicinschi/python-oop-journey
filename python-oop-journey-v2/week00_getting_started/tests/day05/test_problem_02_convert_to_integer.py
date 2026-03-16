"""Tests for Problem 02."""

from __future__ import annotations

from week00_getting_started.solutions.day05.problem_02_convert_to_integer import convert_to_integer


def test_convert_string() -> None:
    """Test case 1."""
    assert convert_to_integer('42') == 42
    assert convert_to_integer('0') == 0
    assert convert_to_integer('-5') == -5


def test_convert_float() -> None:
    """Test case 2."""
    assert convert_to_integer(3.7) == 3
    assert convert_to_integer(3.2) == 3
    assert convert_to_integer(-2.9) == -2


def test_convert_bool() -> None:
    """Test case 3."""
    assert convert_to_integer(True) == 1
    assert convert_to_integer(False) == 0
