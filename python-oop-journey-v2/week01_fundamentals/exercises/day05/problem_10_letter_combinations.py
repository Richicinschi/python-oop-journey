"""Problem 10: Letter Combinations of a Phone Number

Topic: Cartesian product, multiple iterations, string building
Difficulty: Medium

Given a string containing digits from 2-9 inclusive, return all possible 
letter combinations that the number could represent.

A mapping of digits to letters (just like on the telephone buttons) is given.
Note that 1 does not map to any letters.

Mapping:
2: "abc"
3: "def"
4: "ghi"
5: "jkl"
6: "mno"
7: "pqrs"
8: "tuv"
9: "wxyz"

Example:
Input: "23"
Output: ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
"""

from __future__ import annotations


def letter_combinations(digits: str) -> list[str]:
    """Return all letter combinations for the given digits.

    Args:
        digits: A string of digits from '2' to '9'.

    Returns:
        A list of all possible letter combinations.

    Example:
        >>> letter_combinations("23")
        ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
        >>> letter_combinations("")
        []
    """
    raise NotImplementedError("Implement letter_combinations")
