"""Tests for Problem 07: Longest Substring Without Repeating Characters."""

from __future__ import annotations

from week01_fundamentals.solutions.day02.problem_07_longest_substring_without_repeating import longest_substring_without_repeating


def test_abcabcbb() -> None:
    """Test classic example abcabcbb -> abc = 3."""
    assert longest_substring_without_repeating("abcabcbb") == 3


def test_bbbbb() -> None:
    """Test all same characters -> 1."""
    assert longest_substring_without_repeating("bbbbb") == 1


def test_pwwkew() -> None:
    """Test pwwkew -> wke = 3."""
    assert longest_substring_without_repeating("pwwkew") == 3


def test_empty_string() -> None:
    """Test empty string -> 0."""
    assert longest_substring_without_repeating("") == 0


def test_single_character() -> None:
    """Test single character -> 1."""
    assert longest_substring_without_repeating("a") == 1


def test_single_space() -> None:
    """Test single space -> 1."""
    assert longest_substring_without_repeating(" ") == 1


def test_no_repeating() -> None:
    """Test all unique characters -> length of string."""
    assert longest_substring_without_repeating("abcdef") == 6


def test_two_unique() -> None:
    """Test two unique characters."""
    assert longest_substring_without_repeating("au") == 2


def test_repeating_at_end() -> None:
    """Test repeating characters at end."""
    assert longest_substring_without_repeating("dvdf") == 3


def test_long_repeating() -> None:
    """Test longer string with repeating."""
    assert longest_substring_without_repeating("anviaj") == 5


def test_mixed_case() -> None:
    """Test case sensitivity (a != A)."""
    assert longest_substring_without_repeating("aA") == 2
