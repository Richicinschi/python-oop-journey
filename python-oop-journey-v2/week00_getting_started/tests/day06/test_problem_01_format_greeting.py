"""Tests for Problem 01."""

from __future__ import annotations

from week00_getting_started.solutions.day06.problem_01_format_greeting import format_greeting


def test_greeting() -> None:
    """Test case 1."""
    assert format_greeting('Alice') == 'Hello, Alice!'
    assert format_greeting('Bob') == 'Hello, Bob!'


def test_greeting_empty() -> None:
    """Test case 2."""
    assert format_greeting('') == 'Hello, !'
