"""Tests for Problem 01: Count Items."""

from __future__ import annotations

from week00_getting_started.solutions.day19.problem_01_count_items import (
    count_items,
    is_empty,
    compare_lengths,
)


def test_count_items_list() -> None:
    """Test counting items in a list."""
    assert count_items(["a", "b", "c"]) == 3
    assert count_items([]) == 0
    assert count_items(["single"]) == 1


def test_count_items_string() -> None:
    """Test counting characters in a string."""
    assert count_items("hello") == 5
    assert count_items("") == 0
    assert count_items("a") == 1


def test_count_items_dict() -> None:
    """Test counting items in a dictionary."""
    assert count_items({"a": 1, "b": 2}) == 2
    assert count_items({}) == 0
    assert count_items({"only": "one"}) == 1


def test_is_empty() -> None:
    """Test checking if collections are empty."""
    assert is_empty([]) is True
    assert is_empty("") is True
    assert is_empty({}) is True
    assert is_empty(["a"]) is False
    assert is_empty("hello") is False
    assert is_empty({"a": 1}) is False


def test_compare_lengths() -> None:
    """Test comparing lengths of collections."""
    assert compare_lengths([1, 2, 3], [1, 2]) == "first"
    assert compare_lengths([1], [1, 2, 3]) == "second"
    assert compare_lengths("abc", "def") == "equal"
    assert compare_lengths([1, 2], "ab") == "equal"
