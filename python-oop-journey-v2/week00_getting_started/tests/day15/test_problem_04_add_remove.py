"""Tests for Problem 04: Add and Remove."""

from __future__ import annotations

from week00_getting_started.solutions.day15.problem_04_add_remove import add_and_remove


def test_add_and_remove_different() -> None:
    """Test adding and removing different elements."""
    data = {1, 2, 3}
    result = add_and_remove(data, 4, 2)
    assert result == {1, 3, 4}


def test_add_existing_remove_existing() -> None:
    """Test adding existing element and removing existing element."""
    data = {1, 2, 3}
    result = add_and_remove(data, 2, 1)
    assert result == {2, 3}


def test_add_new_remove_nonexistent() -> None:
    """Test adding new element and removing non-existent element."""
    data = {1, 2, 3}
    result = add_and_remove(data, 4, 99)
    assert result == {1, 2, 3, 4}


def test_add_and_remove_same() -> None:
    """Test adding and removing the same element."""
    data = {1, 2, 3}
    result = add_and_remove(data, 5, 5)
    # Add 5, then remove 5 - net effect: original set
    assert result == {1, 2, 3}


def test_empty_set() -> None:
    """Test operations on empty set."""
    data = set()
    result = add_and_remove(data, 1, 99)
    assert result == {1}
