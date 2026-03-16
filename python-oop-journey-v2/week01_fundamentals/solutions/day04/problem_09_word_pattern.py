"""Reference solution for Problem 09: Word Pattern."""

from __future__ import annotations


def word_pattern(pattern: str, s: str) -> bool:
    """Check if string follows pattern.

    Similar to isomorphic strings, but mapping pattern characters
    to words in the string.

    Time Complexity: O(n) where n is length of pattern
    Space Complexity: O(k) where k is unique characters/words

    Args:
        pattern: Pattern string containing letters
        s: String containing words separated by spaces

    Returns:
        True if s follows the pattern, False otherwise
    """
    words = s.split()

    if len(pattern) != len(words):
        return False

    pattern_to_word = {}
    word_to_pattern = {}

    for char, word in zip(pattern, words):
        # Check pattern -> word mapping
        if char in pattern_to_word:
            if pattern_to_word[char] != word:
                return False
        else:
            pattern_to_word[char] = word

        # Check word -> pattern mapping
        if word in word_to_pattern:
            if word_to_pattern[word] != char:
                return False
        else:
            word_to_pattern[word] = char

    return True
