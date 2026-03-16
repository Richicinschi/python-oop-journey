"""Tests for Problem 05: Invert Dictionary."""

from __future__ import annotations

from week00_getting_started.solutions.day14.problem_05_invert_dictionary import invert_dictionary


def test_invert_basic() -> None:
    """Test basic dictionary inversion."""
    original = {"a": 1, "b": 2, "c": 3}
    assert invert_dictionary(original) == {1: "a", 2: "b", 3: "c"}


def test_invert_empty() -> None:
    """Test inverting empty dictionary."""
    assert invert_dictionary({}) == {}


def test_invert_single_pair() -> None:
    """Test inverting single key-value pair."""
    assert invert_dictionary({"x": 100}) == {100: "x"}


def test_invert_duplicate_values() -> None:
    """Test inversion with duplicate values - last key should win."""
    original = {"a": 1, "b": 2, "c": 1}
    result = invert_dictionary(original)
    assert result == {1: "c", 2: "b"}
