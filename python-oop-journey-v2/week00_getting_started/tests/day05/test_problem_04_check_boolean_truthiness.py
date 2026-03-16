"""Tests for Problem 04."""

from __future__ import annotations

from week00_getting_started.solutions.day05.problem_04_check_boolean_truthiness import check_boolean_truthiness


def test_truthy_values() -> None:
    """Test case 1."""
    assert check_boolean_truthiness(1) is True
    assert check_boolean_truthiness(-5) is True
    assert check_boolean_truthiness('hello') is True


def test_falsy_values() -> None:
    """Test case 2."""
    assert check_boolean_truthiness(0) is False
    assert check_boolean_truthiness('') is False
    assert check_boolean_truthiness(None) is False
