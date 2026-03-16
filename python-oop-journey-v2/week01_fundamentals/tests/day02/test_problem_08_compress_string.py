"""Tests for Problem 08: String Compression."""

from __future__ import annotations

from week01_fundamentals.solutions.day02.problem_08_compress_string import compress_string


def test_aabccccaaa() -> None:
    """Test classic example."""
    assert compress_string("aabccccaaa") == "a2bc4a3"


def test_all_unique() -> None:
    """Test all unique characters (no compression)."""
    assert compress_string("abcd") == "abcd"


def test_single_character() -> None:
    """Test single character."""
    assert compress_string("a") == "a"


def test_two_same() -> None:
    """Test two same characters."""
    assert compress_string("aa") == "a2"


def test_two_different() -> None:
    """Test two different characters."""
    assert compress_string("ab") == "ab"


def test_aabbaa() -> None:
    """Test aabbaa pattern."""
    assert compress_string("aabbaa") == "a2b2a2"


def test_empty_string() -> None:
    """Test empty string."""
    assert compress_string("") == ""


def test_long_run() -> None:
    """Test long run of same character."""
    assert compress_string("aaaaaaaaaa") == "a10"


def test_multiple_runs() -> None:
    """Test multiple runs of different lengths."""
    assert compress_string("aaabbbccc") == "a3b3c3"


def test_alternating() -> None:
    """Test alternating characters."""
    assert compress_string("ababab") == "ababab"
