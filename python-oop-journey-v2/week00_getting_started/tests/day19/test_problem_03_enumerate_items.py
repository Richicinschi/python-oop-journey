"""Tests for Problem 03: Enumerate Items."""

from __future__ import annotations

from week00_getting_started.solutions.day19.problem_03_enumerate_items import (
    add_indices,
    add_numbered_labels,
    find_item_index,
    create_numbered_string,
)


def test_add_indices() -> None:
    """Test adding zero-based indices."""
    assert add_indices(["a", "b", "c"]) == [(0, "a"), (1, "b"), (2, "c")]
    assert add_indices([]) == []
    assert add_indices(["single"]) == [(0, "single")]


def test_add_numbered_labels_default() -> None:
    """Test adding numbered labels with default start (1)."""
    assert add_numbered_labels(["a", "b", "c"]) == [(1, "a"), (2, "b"), (3, "c")]


def test_add_numbered_labels_custom_start() -> None:
    """Test adding numbered labels with custom start."""
    assert add_numbered_labels(["a", "b"], start=5) == [(5, "a"), (6, "b")]
    assert add_numbered_labels(["x", "y"], start=0) == [(0, "x"), (1, "y")]


def test_find_item_index_found() -> None:
    """Test finding an item that exists."""
    assert find_item_index(["a", "b", "c"], "b") == 1
    assert find_item_index(["a", "b", "c"], "a") == 0
    assert find_item_index(["a", "b", "c"], "c") == 2


def test_find_item_index_not_found() -> None:
    """Test finding an item that doesn't exist."""
    assert find_item_index(["a", "b", "c"], "z") == -1
    assert find_item_index([], "a") == -1


def test_create_numbered_string() -> None:
    """Test creating numbered string."""
    assert create_numbered_string(["apple", "banana"]) == "1. apple, 2. banana"
    assert create_numbered_string(["single"]) == "1. single"


def test_create_numbered_string_empty() -> None:
    """Test creating numbered string from empty list."""
    assert create_numbered_string([]) == ""
