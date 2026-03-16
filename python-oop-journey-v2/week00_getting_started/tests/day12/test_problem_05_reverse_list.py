"""Tests for Problem 05: Reverse List."""

from __future__ import annotations

from week00_getting_started.solutions.day12.problem_05_reverse_list import reverse_list


def test_reverse_multiple_elements() -> None:
    """Test reversing a list with multiple elements."""
    assert reverse_list(["a", "b", "c"]) == ["c", "b", "a"]
    assert reverse_list(["one", "two", "three", "four"]) == ["four", "three", "two", "one"]


def test_reverse_empty_list() -> None:
    """Test reversing an empty list."""
    assert reverse_list([]) == []


def test_reverse_single_element() -> None:
    """Test reversing a single element list."""
    assert reverse_list(["solo"]) == ["solo"]


def test_reverse_does_not_modify_original() -> None:
    """Test that original list is not modified."""
    original = ["x", "y", "z"]
    reversed_list = reverse_list(original)
    assert original == ["x", "y", "z"]
    assert reversed_list == ["z", "y", "x"]
