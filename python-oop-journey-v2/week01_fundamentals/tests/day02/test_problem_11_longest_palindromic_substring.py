"""Tests for Problem 11: Longest Palindromic Substring."""

from __future__ import annotations

from week01_fundamentals.solutions.day02.problem_11_longest_palindromic_substring import longest_palindromic_substring


def test_babad() -> None:
    """Test babad - can return 'bab' or 'aba'."""
    result = longest_palindromic_substring("babad")
    assert result in ["bab", "aba"]


def test_cbbd() -> None:
    """Test cbbd - should return 'bb'."""
    assert longest_palindromic_substring("cbbd") == "bb"


def test_single_character() -> None:
    """Test single character."""
    assert longest_palindromic_substring("a") == "a"


def test_empty_string() -> None:
    """Test empty string."""
    assert longest_palindromic_substring("") == ""


def test_two_different_characters() -> None:
    """Test two different characters - return either one."""
    result = longest_palindromic_substring("ac")
    assert result in ["a", "c"]


def test_two_same_characters() -> None:
    """Test two same characters."""
    assert longest_palindromic_substring("aa") == "aa"


def test_all_same_characters() -> None:
    """Test all same characters."""
    assert longest_palindromic_substring("aaaa") == "aaaa"


def test_no_palindrome_longer_than_1() -> None:
    """Test string with no palindrome longer than 1 char."""
    result = longest_palindromic_substring("abc")
    assert result in ["a", "b", "c"]


def test_palindrome_at_end() -> None:
    """Test palindrome at end of string."""
    assert longest_palindromic_substring("abbb") == "bbb"


def test_palindrome_at_beginning() -> None:
    """Test palindrome at beginning of string."""
    assert longest_palindromic_substring("aaab") == "aaa"


def test_full_string_palindrome() -> None:
    """Test full string is palindrome."""
    assert longest_palindromic_substring("racecar") == "racecar"


def test_long_string() -> None:
    """Test longer string."""
    result = longest_palindromic_substring("bananas")
    assert result == "anana"
