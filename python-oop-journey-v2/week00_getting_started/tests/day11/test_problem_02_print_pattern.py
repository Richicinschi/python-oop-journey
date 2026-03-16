"""Tests for Problem 02: Print Pattern."""

from __future__ import annotations

from week00_getting_started.solutions.day11.problem_02_print_pattern import print_pattern


def test_print_pattern_small() -> None:
    """Test small patterns."""
    assert print_pattern(1) == ["*"]
    assert print_pattern(2) == ["*", "**"]
    assert print_pattern(3) == ["*", "**", "***"]


def test_print_pattern_larger() -> None:
    """Test larger patterns."""
    result = print_pattern(5)
    assert len(result) == 5
    assert result[0] == "*"
    assert result[1] == "**"
    assert result[2] == "***"
    assert result[3] == "****"
    assert result[4] == "*****"


def test_print_pattern_zero() -> None:
    """Test with zero rows."""
    assert print_pattern(0) == []


def test_print_pattern_asterisk_count() -> None:
    """Verify correct number of asterisks in each row."""
    result = print_pattern(4)
    for i, row in enumerate(result, start=1):
        assert len(row) == i
        assert row == "*" * i
