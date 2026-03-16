"""Tests for Problem 03: String Utilities Module."""

from __future__ import annotations

from week00_getting_started.solutions.day28.problem_03_string_utilities import (
    count_words,
    is_palindrome,
    reverse,
    to_snake_case,
    truncate,
)


def test_reverse_simple() -> None:
    """Test reverse with simple strings."""
    assert reverse("hello") == "olleh"
    assert reverse("abc") == "cba"
    assert reverse("") == ""


def test_reverse_single_char() -> None:
    """Test reverse with single character."""
    assert reverse("a") == "a"


def test_is_palindrome_simple() -> None:
    """Test is_palindrome with simple cases."""
    assert is_palindrome("racecar") is True
    assert is_palindrome("level") is True
    assert is_palindrome("hello") is False


def test_is_palindrome_case_insensitive() -> None:
    """Test is_palindrome is case-insensitive."""
    assert is_palindrome("Racecar") is True
    assert is_palindrome("Level") is True


def test_is_palindrome_with_punctuation() -> None:
    """Test is_palindrome ignores non-alphanumeric chars."""
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("Was it a car or a cat I saw?") is True
    assert is_palindrome("hello, world!") is False


def test_count_words_simple() -> None:
    """Test count_words with simple text."""
    assert count_words("hello world") == 2
    assert count_words("one two three four") == 4


def test_count_words_single() -> None:
    """Test count_words with single word."""
    assert count_words("hello") == 1


def test_count_words_empty() -> None:
    """Test count_words with empty string."""
    assert count_words("") == 0


def test_count_words_multiple_spaces() -> None:
    """Test count_words handles multiple spaces."""
    assert count_words("hello   world") == 2
    assert count_words("  a  b  c  ") == 3


def test_to_snake_case_camel_case() -> None:
    """Test to_snake_case with CamelCase."""
    assert to_snake_case("HelloWorld") == "hello_world"
    assert to_snake_case("SomeVariableName") == "some_variable_name"


def test_to_snake_case_space_separated() -> None:
    """Test to_snake_case with space-separated text."""
    assert to_snake_case("hello world") == "hello_world"
    assert to_snake_case("foo bar baz") == "foo_bar_baz"


def test_to_snake_case_already_snake() -> None:
    """Test to_snake_case with already snake_case text."""
    assert to_snake_case("hello_world") == "hello_world"


def test_to_snake_case_mixed() -> None:
    """Test to_snake_case with mixed input."""
    assert to_snake_case("XMLParser") == "xml_parser"


def test_truncate_no_truncation() -> None:
    """Test truncate when text fits within limit."""
    assert truncate("hello", 10) == "hello"
    assert truncate("hello world", 20) == "hello world"


def test_truncate_with_truncation() -> None:
    """Test truncate adds ellipsis when needed."""
    assert truncate("hello world", 8) == "hello..."
    assert truncate("very long text here", 10) == "very lo..."


def test_truncate_short_limit() -> None:
    """Test truncate with short limit."""
    assert truncate("hello", 3) == "hel"
    assert truncate("hello", 2) == "he"


def test_truncate_exact_length() -> None:
    """Test truncate when text equals max_length."""
    assert truncate("hello", 5) == "hello"
