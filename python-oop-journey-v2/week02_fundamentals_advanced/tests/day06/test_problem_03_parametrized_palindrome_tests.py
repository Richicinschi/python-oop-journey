"""Tests for Problem 03: Parametrized Palindrome Tests."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day06.problem_03_parametrized_palindrome_tests import (
    is_palindrome,
    is_strict_palindrome,
)


class TestIsPalindrome:
    """Tests for the flexible palindrome checker."""

    @pytest.mark.parametrize("text,expected", [
        # Simple palindromes
        ("radar", True),
        ("level", True),
        ("madam", True),
        ("civic", True),
        ("rotor", True),
        ("kayak", True),
        # Single character
        ("a", True),
        ("X", True),
        # Empty string
        ("", True),
        # Phrases with punctuation and spaces
        ("A man, a plan, a canal: Panama", True),
        ("Was it a car or a cat I saw?", True),
        ("No 'x' in Nixon", True),
        ("Madam, I'm Adam", True),
        # Numbers
        ("12321", True),
        ("123321", True),
        # Mixed case palindromes
        ("Radar", True),
        ("LeVel", True),
        # Non-palindromes
        ("hello", False),
        ("python", False),
        ("world", False),
        ("not a palindrome", False),
        # Numbers that aren't palindromes
        ("12345", False),
        ("123456", False),
    ])
    def test_is_palindrome_various_inputs(self, text: str, expected: bool) -> None:
        """Test palindrome detection with various inputs."""
        assert is_palindrome(text) == expected

    @pytest.mark.parametrize("text", [
        "radar",
        "A man, a plan, a canal: Panama",
        "Was it a car or a cat I saw",
    ])
    def test_palindromes_are_reversible(self, text: str) -> None:
        """Test that palindromes are detected regardless of order."""
        assert is_palindrome(text) is True
        # Reversed should also be palindrome
        assert is_palindrome(text[::-1]) is True

    def test_non_string_raises_type_error(self) -> None:
        """Test that non-string input raises TypeError."""
        with pytest.raises(TypeError):
            is_palindrome(12321)

    def test_unicode_palindromes(self) -> None:
        """Test palindromes with unicode characters - handled gracefully."""
        # Unicode non-ASCII chars are filtered out
        assert is_palindrome("ñoño") is True  # becomes "noo"
        assert is_palindrome("áéíéá") is True  # becomes ""


class TestIsStrictPalindrome:
    """Tests for the strict palindrome checker."""

    @pytest.mark.parametrize("text,expected", [
        # Strict palindromes (exact match)
        ("radar", True),
        ("level", True),
        ("madam", True),
        ("", True),
        ("a", True),
        # Not strict (case sensitive)
        ("Radar", False),
        ("LEvel", False),
        # Not strict (spaces/punctuation)
        ("a man a plan a canal panama", False),  # Spaces break strict palindrome
        ("a man, a plan, a canal: panama", False),  # With punctuation fails
        # Not strict (not palindromes)
        ("hello", False),
        ("python", False),
        ("world", False),
    ])
    def test_is_strict_palindrome_various_inputs(self, text: str, expected: bool) -> None:
        """Test strict palindrome detection."""
        assert is_strict_palindrome(text) == expected

    def test_strict_vs_flexible_difference(self) -> None:
        """Test that strict and flexible behave differently on same inputs."""
        # Flexible accepts these
        assert is_palindrome("Radar") is True
        assert is_palindrome("A man, a plan, a canal: Panama") is True

        # Strict rejects these
        assert is_strict_palindrome("Radar") is False
        assert is_strict_palindrome("A man, a plan, a canal: Panama") is False

    def test_non_string_raises_type_error_strict(self) -> None:
        """Test that non-string input raises TypeError in strict mode."""
        with pytest.raises(TypeError):
            is_strict_palindrome(12321)


class TestPalindromeEdgeCases:
    """Edge case tests for both palindrome functions."""

    @pytest.mark.parametrize("func", [is_palindrome, is_strict_palindrome])
    def test_whitespace_only_flexible_vs_strict(self, func) -> None:
        """Test whitespace handling."""
        # Both should handle empty string
        assert func("") is True

    def test_whitespace_variations(self) -> None:
        """Test various whitespace scenarios."""
        # Flexible ignores all non-alphanumeric
        assert is_palindrome("   ") is True  # Only whitespace -> empty string
        assert is_palindrome("  a  ") is True  # Whitespace around single char

        # Strict preserves everything - "  a  " reversed is "  a  " which IS a palindrome!
        # (spaces at both ends, 'a' in middle)
        assert is_strict_palindrome("   ") is True  # Only whitespace is palindrome
        assert is_strict_palindrome("  a  ") is True  # "  a  " is actually a palindrome!

    @pytest.mark.parametrize("text", [
        "a" * 1000,  # Very long palindrome
        "ab" * 500 + "a",  # Long palindrome pattern
    ])
    def test_long_palindromes(self, text: str) -> None:
        """Test performance with long palindromes."""
        assert is_palindrome(text) is True
        assert is_strict_palindrome(text) is True

    @pytest.mark.parametrize("text", [
        "a" * 1000 + "b",  # Very long non-palindrome
    ])
    def test_long_non_palindromes(self, text: str) -> None:
        """Test performance with long non-palindromes."""
        assert is_palindrome(text) is False
        assert is_strict_palindrome(text) is False
