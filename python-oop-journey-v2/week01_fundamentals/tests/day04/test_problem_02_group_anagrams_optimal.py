"""Tests for Problem 02: Group Anagrams Optimal."""

from __future__ import annotations

from week01_fundamentals.solutions.day04.problem_02_group_anagrams_optimal import (
    group_anagrams_optimal,
)


def test_basic_case() -> None:
    """Test basic grouping of anagrams."""
    input_strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    result = group_anagrams_optimal(input_strs)

    # Normalize result for comparison (order of groups doesn't matter)
    normalized = sorted([sorted(group) for group in result])
    expected = sorted([["bat"], ["ate", "eat", "tea"], ["nat", "tan"]])

    assert normalized == expected


def test_empty_strings() -> None:
    """Test with empty strings."""
    result = group_anagrams_optimal(["", ""])
    assert len(result) == 1
    assert sorted(result[0]) == ["", ""]


def test_single_string() -> None:
    """Test with single string."""
    result = group_anagrams_optimal(["hello"])
    assert result == [["hello"]]


def test_no_anagrams() -> None:
    """Test when no strings are anagrams."""
    result = group_anagrams_optimal(["abc", "def", "ghi"])
    assert len(result) == 3
    assert sorted([sorted(group) for group in result]) == [
        ["abc"],
        ["def"],
        ["ghi"],
    ]


def test_empty_list() -> None:
    """Test with empty list."""
    result = group_anagrams_optimal([])
    assert result == []


def test_all_same_anagrams() -> None:
    """Test when all strings are anagrams."""
    result = group_anagrams_optimal(["abc", "bca", "cab", "cba"])
    assert len(result) == 1
    assert sorted(result[0]) == ["abc", "bca", "cab", "cba"]


def test_single_character_strings() -> None:
    """Test with single character strings."""
    result = group_anagrams_optimal(["a", "b", "a", "c", "b"])
    normalized = sorted([sorted(group) for group in result])
    assert normalized == [["a", "a"], ["b", "b"], ["c"]]


def test_longer_anagrams() -> None:
    """Test with longer anagram strings."""
    result = group_anagrams_optimal(["listen", "silent", "enlist", "inlets"])
    assert len(result) == 1
    assert sorted(result[0]) == ["enlist", "inlets", "listen", "silent"]
