"""Tests for Problem 04: Is Leap Year."""

from __future__ import annotations

from week00_getting_started.solutions.day09.problem_04_is_leap_year import is_leap_year


def test_is_leap_year_divisible_by_400() -> None:
    """Test years divisible by 400 are leap years."""
    assert is_leap_year(2000) is True
    assert is_leap_year(1600) is True
    assert is_leap_year(2400) is True


def test_is_leap_year_divisible_by_100_not_400() -> None:
    """Test years divisible by 100 but not 400 are not leap years."""
    assert is_leap_year(1900) is False
    assert is_leap_year(1700) is False
    assert is_leap_year(2100) is False


def test_is_leap_year_divisible_by_4_not_100() -> None:
    """Test years divisible by 4 but not 100 are leap years."""
    assert is_leap_year(2020) is True
    assert is_leap_year(2016) is True
    assert is_leap_year(2024) is True


def test_is_leap_year_not_divisible_by_4() -> None:
    """Test years not divisible by 4 are not leap years."""
    assert is_leap_year(2021) is False
    assert is_leap_year(2019) is False
    assert is_leap_year(2023) is False


def test_is_leap_year_edge_cases() -> None:
    """Test edge cases."""
    assert is_leap_year(4) is True
    assert is_leap_year(100) is False
    assert is_leap_year(400) is True
