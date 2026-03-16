"""Tests for Problem 05: Word Length Histogram."""

from __future__ import annotations

from week02_fundamentals_advanced.solutions.day04.problem_05_word_length_histogram import (
    word_length_histogram,
)


def test_basic_histogram() -> None:
    """Test basic histogram creation."""
    words = ["cat", "dog", "elephant", "bird"]
    result = word_length_histogram(words)
    assert result == {3: ["cat", "dog"], 4: ["bird"], 8: ["elephant"]}


def test_empty_list() -> None:
    """Test with empty list."""
    assert word_length_histogram([]) == {}


def test_single_word() -> None:
    """Test with single word."""
    assert word_length_histogram(["hello"]) == {5: ["hello"]}


def test_all_same_length() -> None:
    """Test with all words same length."""
    words = ["cat", "dog", "bat", "rat"]
    assert word_length_histogram(words) == {3: ["cat", "dog", "bat", "rat"]}


def test_all_different_lengths() -> None:
    """Test with all words different lengths."""
    words = ["a", "to", "cat", "bird", "eagle"]
    result = word_length_histogram(words)
    assert result == {
        1: ["a"],
        2: ["to"],
        3: ["cat"],
        4: ["bird"],
        5: ["eagle"],
    }


def test_preserves_input_order() -> None:
    """Test that words within each length group preserve input order."""
    words = ["dog", "cat", "bat", "elephant", "bird"]
    result = word_length_histogram(words)
    assert result[3] == ["dog", "cat", "bat"]


def test_duplicates() -> None:
    """Test with duplicate words."""
    words = ["cat", "cat", "dog", "dog"]
    result = word_length_histogram(words)
    assert result[3] == ["cat", "cat", "dog", "dog"]


def test_with_spaces() -> None:
    """Test words with internal spaces (counted as characters)."""
    words = ["a b", "cd", "e f g"]
    result = word_length_histogram(words)
    assert result == {2: ["cd"], 3: ["a b"], 5: ["e f g"]}
