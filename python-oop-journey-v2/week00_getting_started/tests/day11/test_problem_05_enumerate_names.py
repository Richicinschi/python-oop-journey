"""Tests for Problem 05: Enumerate Names."""

from __future__ import annotations

from week00_getting_started.solutions.day11.problem_05_enumerate_names import enumerate_names


def test_enumerate_names_multiple() -> None:
    """Test with multiple names."""
    assert enumerate_names(["Alice", "Bob", "Charlie"]) == [
        "1. Alice",
        "2. Bob",
        "3. Charlie",
    ]


def test_enumerate_names_single() -> None:
    """Test with single name."""
    assert enumerate_names(["Solo"]) == ["1. Solo"]


def test_enumerate_names_empty() -> None:
    """Test with empty list."""
    assert enumerate_names([]) == []


def test_enumerate_names_format() -> None:
    """Test correct formatting."""
    result = enumerate_names(["A", "B", "C"])
    for i, item in enumerate(result, start=1):
        assert item.startswith(f"{i}. ")


def test_enumerate_names_long_list() -> None:
    """Test with longer list."""
    names = ["One", "Two", "Three", "Four", "Five"]
    result = enumerate_names(names)
    assert len(result) == 5
    assert result[0] == "1. One"
    assert result[4] == "5. Five"
