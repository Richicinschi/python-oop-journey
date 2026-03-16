"""Tests for Problem 02: Append and Get Length."""

from __future__ import annotations

from week00_getting_started.solutions.day12.problem_02_append_and_length import append_and_count


def test_append_to_empty_list() -> None:
    """Test appending to an empty list."""
    items: list[str] = []
    result, length = append_and_count(items, "first")
    assert result == ["first"]
    assert length == 1


def test_append_to_existing_list() -> None:
    """Test appending to a list with existing items."""
    items = ["a", "b", "c"]
    result, length = append_and_count(items, "d")
    assert result == ["a", "b", "c", "d"]
    assert length == 4


def test_append_multiple() -> None:
    """Test that multiple appends work correctly."""
    items: list[str] = []
    items, _ = append_and_count(items, "one")
    items, _ = append_and_count(items, "two")
    result, length = append_and_count(items, "three")
    assert result == ["one", "two", "three"]
    assert length == 3
