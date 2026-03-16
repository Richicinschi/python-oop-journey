"""Tests for Problem 04: First Unique Character in a String."""

from __future__ import annotations

from week01_fundamentals.solutions.day02.problem_04_first_unique_character import first_unique_character


def test_first_unique_at_beginning() -> None:
    """Test first unique character at beginning."""
    assert first_unique_character("leetcode") == 0


def test_first_unique_in_middle() -> None:
    """Test first unique character in middle."""
    assert first_unique_character("loveleetcode") == 2


def test_no_unique_character() -> None:
    """Test string with no unique characters."""
    assert first_unique_character("aabb") == -1


def test_empty_string() -> None:
    """Test empty string."""
    assert first_unique_character("") == -1


def test_single_character() -> None:
    """Test single character."""
    assert first_unique_character("a") == 0


def test_all_same_characters() -> None:
    """Test all same characters."""
    assert first_unique_character("aaaa") == -1


def test_unique_at_end() -> None:
    """Test unique character at end."""
    assert first_unique_character("aabbccd") == 6


def test_multiple_unique() -> None:
    """Test multiple unique characters - return first one."""
    assert first_unique_character("abc") == 0


def test_case_sensitive() -> None:
    """Test case sensitivity."""
    assert first_unique_character("aAbB") == 0


def test_with_spaces() -> None:
    """Test string with spaces."""
    assert first_unique_character("a a b") == 4
