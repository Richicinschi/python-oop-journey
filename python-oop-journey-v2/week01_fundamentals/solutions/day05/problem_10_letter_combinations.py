"""Reference solution for Problem 10: Letter Combinations of a Phone Number."""

from __future__ import annotations


def letter_combinations(digits: str) -> list[str]:
    """Return all letter combinations for the given digits.

    Args:
        digits: A string of digits from '2' to '9'.

    Returns:
        A list of all possible letter combinations.
    """
    if not digits:
        return []

    # Phone digit to letters mapping
    phone_map: dict[str, str] = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz"
    }

    result: list[str] = []

    def backtrack(index: int, current: str) -> None:
        """Build combinations using backtracking.

        Args:
            index: Current position in digits string.
            current: The current combination being built.
        """
        # Base case: we've processed all digits
        if index == len(digits):
            result.append(current)
            return

        # Get the letters for current digit
        digit = digits[index]
        for letter in phone_map[digit]:
            backtrack(index + 1, current + letter)

    backtrack(0, "")
    return result
