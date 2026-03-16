"""Tests for Problem 01: Tuple Unpacking."""

from __future__ import annotations

from week00_getting_started.solutions.day13.problem_01_tuple_unpacking import unpack_coordinates


def test_unpack_positive_coordinates() -> None:
    """Test unpacking positive coordinates."""
    result = unpack_coordinates((3, 4))
    assert result == {"x": 3, "y": 4}


def test_unpack_negative_coordinates() -> None:
    """Test unpacking negative coordinates."""
    result = unpack_coordinates((-10, -20))
    assert result == {"x": -10, "y": -20}


def test_unpack_zero_coordinates() -> None:
    """Test unpacking zero coordinates."""
    result = unpack_coordinates((0, 0))
    assert result == {"x": 0, "y": 0}


def test_unpack_mixed_coordinates() -> None:
    """Test unpacking mixed positive/negative coordinates."""
    result = unpack_coordinates((5, -3))
    assert result == {"x": 5, "y": -3}
