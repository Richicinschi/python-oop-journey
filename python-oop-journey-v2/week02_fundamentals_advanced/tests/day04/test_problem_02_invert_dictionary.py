"""Tests for Problem 02: Invert Dictionary."""

from __future__ import annotations

from week02_fundamentals_advanced.solutions.day04.problem_02_invert_dictionary import (
    invert_dictionary,
)


def test_basic_inversion() -> None:
    """Test basic dictionary inversion."""
    original = {"a": 1, "b": 2, "c": 3}
    assert invert_dictionary(original) == {1: "a", 2: "b", 3: "c"}


def test_single_entry() -> None:
    """Test with single entry."""
    original = {"x": 10}
    assert invert_dictionary(original) == {10: "x"}


def test_empty_dictionary() -> None:
    """Test with empty dictionary."""
    assert invert_dictionary({}) == {}


def test_negative_values() -> None:
    """Test with negative integer values."""
    original = {"a": -1, "b": -2, "c": -3}
    assert invert_dictionary(original) == {-1: "a", -2: "b", -3: "c"}


def test_zero_value() -> None:
    """Test with zero as a value."""
    original = {"zero": 0, "one": 1}
    assert invert_dictionary(original) == {0: "zero", 1: "one"}


def test_large_values() -> None:
    """Test with large integer values."""
    original = {"big": 1000000, "bigger": 2000000}
    assert invert_dictionary(original) == {1000000: "big", 2000000: "bigger"}


def test_does_not_modify_original() -> None:
    """Test that original dictionary is not modified."""
    original = {"a": 1, "b": 2}
    original_copy = original.copy()
    invert_dictionary(original)
    assert original == original_copy
