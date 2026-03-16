"""Tests for Problem 01: Create and Access List."""

from __future__ import annotations

from week00_getting_started.solutions.day12.problem_01_create_and_access import create_and_access


def test_access_valid_index() -> None:
    """Test accessing valid indices."""
    numbers = [10, 20, 30, 40, 50]
    assert create_and_access(numbers, 0) == 10
    assert create_and_access(numbers, 2) == 30
    assert create_and_access(numbers, 4) == 50


def test_access_invalid_index() -> None:
    """Test accessing invalid indices returns None."""
    numbers = [10, 20, 30]
    assert create_and_access(numbers, -1) is None
    assert create_and_access(numbers, 3) is None
    assert create_and_access(numbers, 100) is None


def test_empty_list() -> None:
    """Test accessing any index in empty list returns None."""
    numbers: list[int] = []
    assert create_and_access(numbers, 0) is None
    assert create_and_access(numbers, -1) is None
