"""Tests for Problem 03."""

from __future__ import annotations

from week00_getting_started.solutions.day06.problem_03_format_person_info import format_person_info


def test_person_info() -> None:
    """Test case 1."""
    assert format_person_info('Alice', 25) == 'Name: Alice\nAge: 25'


def test_person_info_zero() -> None:
    """Test case 2."""
    assert format_person_info('Baby', 0) == 'Name: Baby\nAge: 0'
