"""Problem 04: Generate Parentheses

Topic: Recursion simulation, backtracking, nested loops
Difficulty: Medium

Given n pairs of parentheses, write a function to generate all combinations 
of well-formed (balanced) parentheses.

A well-formed parentheses string has:
- Every opening '(' has a matching closing ')'
- At any point, the number of closing brackets never exceeds opening brackets
"""

from __future__ import annotations


def generate_parentheses(n: int) -> list[str]:
    """Generate all combinations of well-formed parentheses.

    Args:
        n: Number of pairs of parentheses.

    Returns:
        A list of all valid combinations of n pairs of parentheses.

    Example:
        >>> generate_parentheses(1)
        ['()']
        >>> generate_parentheses(2)
        ['(())', '()()']
        >>> generate_parentheses(3)
        ['((()))', '(()())', '(())()', '()(())', '()()()']
    """
    raise NotImplementedError("Implement generate_parentheses")
