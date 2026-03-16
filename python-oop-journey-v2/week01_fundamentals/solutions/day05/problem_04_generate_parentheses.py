"""Reference solution for Problem 04: Generate Parentheses."""

from __future__ import annotations


def generate_parentheses(n: int) -> list[str]:
    """Generate all combinations of well-formed parentheses.

    Args:
        n: Number of pairs of parentheses.

    Returns:
        A list of all valid combinations of n pairs of parentheses.
    """
    if n < 0:
        return []

    result: list[str] = []

    def backtrack(current: str, open_count: int, close_count: int) -> None:
        """Helper function to build parentheses combinations.

        Args:
            current: The current string being built.
            open_count: Number of opening brackets used so far.
            close_count: Number of closing brackets used so far.
        """
        # Base case: we've used all n pairs
        if len(current) == 2 * n:
            result.append(current)
            return

        # We can add an opening bracket if we haven't used all n
        if open_count < n:
            backtrack(current + "(", open_count + 1, close_count)

        # We can add a closing bracket if it won't exceed opening brackets
        if close_count < open_count:
            backtrack(current + ")", open_count, close_count + 1)

    backtrack("", 0, 0)
    return result
