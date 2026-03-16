"""Problem 05: Fix The Error

Topic: Debugging Basics
Difficulty: Medium

Write a function that analyzes code snippets and suggests fixes for common errors.

Given a problematic code snippet description, return the corrected version:
- "print(Hello)" → "print('Hello')" (missing quotes)
- "if x > 5 print(x)" → "if x > 5: print(x)" (missing colon)
- "10 / 0" → "Cannot fix - would raise ZeroDivisionError"
- "lst[5]" (for lst=[1,2,3]) → "lst[2]" or "Index check needed"
- "int('abc')" → "Cannot fix - would raise ValueError"

For fixable issues, return the corrected code.
For unfixable runtime errors, return an explanation message.

Examples:
    >>> suggest_fix("print(Hello)")
    "print('Hello')"
    >>> suggest_fix("10 / 0")
    'Cannot fix - would raise ZeroDivisionError'

Requirements:
    - Identify common syntax issues and suggest fixes
    - Identify runtime errors that cannot be automatically fixed
    - Return the corrected code or an explanation message
"""

from __future__ import annotations


def suggest_fix(code: str) -> str:
    """Analyze a code snippet and suggest a fix or identify the error.

    Args:
        code: A potentially problematic code snippet

    Returns:
        Either the corrected code or an error explanation
    """
    raise NotImplementedError("Implement suggest_fix")
