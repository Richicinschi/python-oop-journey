"""Tests for Problem 09: Group Anagrams."""

from __future__ import annotations

from week01_fundamentals.solutions.day02.problem_09_group_anagrams import group_anagrams


def test_multiple_groups() -> None:
    """Test with multiple anagram groups."""
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    # Sort each group and the overall result for comparison
    result = [sorted(group) for group in result]
    result.sort(key=lambda x: x[0] if x else "")
    expected = [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
    assert result == expected


def test_empty_string() -> None:
    """Test with single empty string."""
    result = group_anagrams([""])
    assert result == [[""]]


def test_single_string() -> None:
    """Test with single string."""
    result = group_anagrams(["a"])
    assert result == [["a"]]


def test_no_anagrams() -> None:
    """Test with no anagrams - each in its own group."""
    result = group_anagrams(["abc", "def", "ghi"])
    # Sort for comparison
    result = [sorted(group) for group in result]
    result.sort()
    expected = [["abc"], ["def"], ["ghi"]]
    assert result == expected


def test_all_same_anagram() -> None:
    """Test with all strings being anagrams."""
    result = group_anagrams(["abc", "bca", "cab"])
    # Sort for comparison
    result = [sorted(group) for group in result]
    assert result == [["abc", "bca", "cab"]]


def test_empty_list() -> None:
    """Test with empty list."""
    result = group_anagrams([])
    assert result == []


def test_case_sensitive() -> None:
    """Test case sensitivity."""
    result = group_anagrams(["A", "a"])
    # 'A' and 'a' are NOT anagrams (different ASCII values)
    assert len(result) == 2


def test_multiple_same_word() -> None:
    """Test with multiple instances of same word."""
    result = group_anagrams(["abc", "abc", "abc"])
    result = [sorted(group) for group in result]
    assert result == [["abc", "abc", "abc"]]


def test_different_length_words() -> None:
    """Test words of different lengths."""
    result = group_anagrams(["a", "ab", "ba", "abc", "cba"])
    result = [sorted(group) for group in result]
    result.sort()
    expected = [["a"], ["ab", "ba"], ["abc", "cba"]]
    assert result == expected
