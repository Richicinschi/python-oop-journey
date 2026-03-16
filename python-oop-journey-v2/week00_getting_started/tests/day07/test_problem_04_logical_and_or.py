"""Tests for Problem 04."""

from __future__ import annotations

from week00_getting_started.solutions.day07.problem_04_logical_and_or import logical_and_or


def test_and_or() -> None:
    """Test case 1."""
    result = logical_and_or(True, False)
    assert result['and'] is False
    assert result['or'] is True


def test_both_true() -> None:
    """Test case 2."""
    result = logical_and_or(True, True)
    assert result['and'] is True
    assert result['or'] is True


def test_both_false() -> None:
    """Test case 3."""
    result = logical_and_or(False, False)
    assert result['and'] is False
    assert result['or'] is False
