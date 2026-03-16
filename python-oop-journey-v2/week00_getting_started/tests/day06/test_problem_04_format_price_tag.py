"""Tests for Problem 04."""

from __future__ import annotations

from week00_getting_started.solutions.day06.problem_04_format_price_tag import format_price_tag


def test_price_whole() -> None:
    """Test case 1."""
    assert format_price_tag(10) == '$10.00'
    assert format_price_tag(0) == '$0.00'


def test_price_decimal() -> None:
    """Test case 2."""
    assert format_price_tag(5.5) == '$5.50'
    assert format_price_tag(3.14159) == '$3.14'
