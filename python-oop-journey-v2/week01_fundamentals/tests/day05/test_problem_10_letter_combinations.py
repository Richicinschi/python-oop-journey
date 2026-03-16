"""Tests for Problem 10: Letter Combinations of a Phone Number."""

from __future__ import annotations

from week01_fundamentals.solutions.day05.problem_10_letter_combinations import letter_combinations


def test_letter_combinations_two_digits() -> None:
    result = letter_combinations("23")
    result.sort()
    expected = ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    expected.sort()
    assert result == expected


def test_letter_combinations_single_digit() -> None:
    result = letter_combinations("2")
    result.sort()
    expected = ["a", "b", "c"]
    expected.sort()
    assert result == expected


def test_letter_combinations_empty() -> None:
    assert letter_combinations("") == []


def test_letter_combinations_one_digit_four_letters() -> None:
    result = letter_combinations("7")
    result.sort()
    expected = ["p", "q", "r", "s"]
    expected.sort()
    assert result == expected


def test_letter_combinations_three_digits() -> None:
    result = letter_combinations("234")
    # 3 * 3 * 3 = 27 combinations
    assert len(result) == 27
    # Check a few specific combinations
    assert "adg" in result
    assert "cfi" in result
    assert "beh" in result
