"""Tests for Problem 02: Is In Range."""

from __future__ import annotations

from week00_getting_started.solutions.day08.problem_02_is_in_range import is_in_range


def test_is_in_range_middle() -> None:
    """Test values in the middle of the range."""
    assert is_in_range(5, 1, 10) is True
    assert is_in_range(50, 0, 100) is True
    assert is_in_range(0, -10, 10) is True


def test_is_in_range_at_boundaries() -> None:
    """Test values at the boundaries (inclusive)."""
    assert is_in_range(1, 1, 10) is True  # At min
    assert is_in_range(10, 1, 10) is True  # At max
    assert is_in_range(0, 0, 0) is True  # Single point


def test_is_in_range_below() -> None:
    """Test values below the range."""
    assert is_in_range(0, 1, 10) is False
    assert is_in_range(-5, 0, 10) is False
    assert is_in_range(9, 10, 20) is False


def test_is_in_range_above() -> None:
    """Test values above the range."""
    assert is_in_range(11, 1, 10) is False
    assert is_in_range(100, 0, 50) is False
    assert is_in_range(21, 10, 20) is False


def test_is_in_range_negative() -> None:
    """Test with negative ranges."""
    assert is_in_range(-5, -10, -1) is True
    assert is_in_range(-10, -10, -1) is True
    assert is_in_range(-1, -10, -1) is True
    assert is_in_range(0, -10, -1) is False
