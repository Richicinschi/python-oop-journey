"""Tests for Problem 02: Word Frequency Analyzer."""

from __future__ import annotations

from week00_getting_started.solutions.day29.problem_02_word_frequency import (
    count_words,
    get_top_words,
    word_frequency_report,
)


def test_count_words_basic() -> None:
    """Test count_words with basic text."""
    result = count_words("hello world hello")
    assert result == {"hello": 2, "world": 1}


def test_count_words_case_insensitive() -> None:
    """Test count_words is case-insensitive."""
    result = count_words("Hello World hello")
    assert result == {"hello": 2, "world": 1}


def test_count_words_empty() -> None:
    """Test count_words with empty string."""
    assert count_words("") == {}


def test_count_words_whitespace_only() -> None:
    """Test count_words with whitespace only."""
    assert count_words("   \n\t  ") == {}


def test_count_words_removes_punctuation() -> None:
    """Test count_words removes punctuation."""
    result = count_words("Hello, world! How are you?")
    assert result == {"hello": 1, "world": 1, "how": 1, "are": 1, "you": 1}


def test_get_top_words_basic() -> None:
    """Test get_top_words returns correct top words."""
    result = get_top_words("hello world hello", 1)
    assert result == [("hello", 2)]


def test_get_top_words_multiple() -> None:
    """Test get_top_words returns multiple words."""
    result = get_top_words("a b c a b a", 2)
    assert result == [("a", 3), ("b", 2)]


def test_get_top_words_empty() -> None:
    """Test get_top_words with empty text."""
    assert get_top_words("", 5) == []


def test_word_frequency_report_basic() -> None:
    """Test word_frequency_report with basic text."""
    result = word_frequency_report("Hello world!")
    assert result["total_words"] == 2
    assert result["unique_words"] == 2
    assert len(result["most_common"]) <= 5


def test_word_frequency_report_empty() -> None:
    """Test word_frequency_report with empty text."""
    result = word_frequency_report("")
    assert result["total_words"] == 0
    assert result["unique_words"] == 0
    assert result["average_word_length"] == 0.0


def test_word_frequency_report_average_length() -> None:
    """Test word_frequency_report calculates average word length."""
    result = word_frequency_report("hi hello world")
    assert result["average_word_length"] == 4.0  # 2 + 5 + 5 / 3


def test_count_words_numbers() -> None:
    """Test count_words handles numbers in text."""
    result = count_words("test 123 test 456")
    assert result == {"test": 2, "123": 1, "456": 1}
