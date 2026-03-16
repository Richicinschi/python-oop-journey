"""Tests for Problem 02."""

from __future__ import annotations

from week00_getting_started.solutions.day07.problem_02_compare_numbers import compare_numbers


def test_compare_greater() -> None:
    """Test case 1."""
    result = compare_numbers(5, 3)
    assert result['greater'] is True
    assert result['equal'] is False
    assert result['less'] is False


def test_compare_less() -> None:
    """Test case 2."""
    result = compare_numbers(2, 7)
    assert result['greater'] is False
    assert result['equal'] is False
    assert result['less'] is True


def test_compare_equal() -> None:
    """Test case 3."""
    result = compare_numbers(4, 4)
    assert result['greater'] is False
    assert result['equal'] is True
    assert result['less'] is False
