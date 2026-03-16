"""Tests for Problem 01: Create Dictionary."""

from __future__ import annotations

from week00_getting_started.solutions.day14.problem_01_create_dictionary import create_dictionary


def test_create_equal_length() -> None:
    """Test creating dictionary from equal length lists."""
    keys = ["a", "b", "c"]
    values = [1, 2, 3]
    assert create_dictionary(keys, values) == {"a": 1, "b": 2, "c": 3}


def test_more_keys_than_values() -> None:
    """Test when keys list is longer."""
    keys = ["a", "b", "c", "d"]
    values = [1, 2]
    assert create_dictionary(keys, values) == {"a": 1, "b": 2}


def test_more_values_than_keys() -> None:
    """Test when values list is longer."""
    keys = ["a", "b"]
    values = [1, 2, 3, 4]
    assert create_dictionary(keys, values) == {"a": 1, "b": 2}


def test_empty_lists() -> None:
    """Test with empty lists."""
    assert create_dictionary([], []) == {}


def test_single_pair() -> None:
    """Test with single key-value pair."""
    assert create_dictionary(["x"], [100]) == {"x": 100}
