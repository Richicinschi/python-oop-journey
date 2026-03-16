"""Tests for Problem 05: Longest Common Prefix."""

from __future__ import annotations

from week01_fundamentals.solutions.day02.problem_05_longest_common_prefix import longest_common_prefix


def test_multiple_strings_with_common_prefix() -> None:
    """Test multiple strings with common prefix."""
    assert longest_common_prefix(["flower", "flow", "flight"]) == "fl"


def test_no_common_prefix() -> None:
    """Test strings with no common prefix."""
    assert longest_common_prefix(["dog", "racecar", "car"]) == ""


def test_longer_common_prefix() -> None:
    """Test with longer common prefix."""
    assert longest_common_prefix(["interspecies", "interstellar", "interstate"]) == "inters"


def test_single_string() -> None:
    """Test single string - returns the whole string."""
    assert longest_common_prefix(["a"]) == "a"


def test_empty_list() -> None:
    """Test empty list."""
    assert longest_common_prefix([]) == ""


def test_identical_strings() -> None:
    """Test identical strings."""
    assert longest_common_prefix(["abc", "abc", "abc"]) == "abc"


def test_one_string_is_prefix() -> None:
    """Test where one string is a prefix of others."""
    assert longest_common_prefix(["ab", "abc", "abcd"]) == "ab"


def test_empty_string_in_list() -> None:
    """Test with empty string in list."""
    assert longest_common_prefix(["", "abc"]) == ""


def test_all_empty_strings() -> None:
    """Test all empty strings."""
    assert longest_common_prefix(["", "", ""]) == ""


def test_two_strings() -> None:
    """Test with just two strings."""
    assert longest_common_prefix(["hello", "help"]) == "hel"
