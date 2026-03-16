"""Tests for Problem 02: Lookup Value."""

from __future__ import annotations

from week00_getting_started.solutions.day14.problem_02_lookup_value import lookup_value


def test_lookup_existing_key() -> None:
    """Test looking up an existing key."""
    data = {"a": 1, "b": 2, "c": 3}
    assert lookup_value(data, "b", 0) == 2
    assert lookup_value(data, "a", 999) == 1


def test_lookup_missing_key() -> None:
    """Test looking up a missing key returns default."""
    data = {"a": 1, "b": 2}
    assert lookup_value(data, "z", 0) == 0
    assert lookup_value(data, "missing", -1) == -1


def test_lookup_empty_dict() -> None:
    """Test looking up in empty dictionary."""
    assert lookup_value({}, "any", 100) == 100


def test_default_zero() -> None:
    """Test with default value of zero."""
    data = {"x": 10}
    assert lookup_value(data, "y", 0) == 0
