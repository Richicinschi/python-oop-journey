"""Tests for Problem 01."""

from __future__ import annotations

from week00_getting_started.solutions.day05.problem_01_get_type_info import get_type_info


def test_type_int() -> None:
    """Test case 1."""
    assert get_type_info(42) == 'int'
    assert get_type_info(0) == 'int'
    assert get_type_info(-5) == 'int'


def test_type_str() -> None:
    """Test case 2."""
    assert get_type_info('hello') == 'str'
    assert get_type_info('') == 'str'


def test_type_float() -> None:
    """Test case 3."""
    assert get_type_info(3.14) == 'float'
    assert get_type_info(0.0) == 'float'


def test_type_bool() -> None:
    """Test case 4."""
    assert get_type_info(True) == 'bool'
    assert get_type_info(False) == 'bool'
