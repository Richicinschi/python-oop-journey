"""Problem 02: Is Syntax Error

Topic: Syntax vs Runtime Errors
Difficulty: Easy

Write a function that determines if a given error type is a syntax error
or a runtime error.

Syntax errors are detected before the program runs:
- SyntaxError
- IndentationError

Runtime errors occur during execution:
- ZeroDivisionError, NameError, TypeError, ValueError
- IndexError, KeyError, AttributeError, etc.

Examples:
    >>> is_syntax_error("SyntaxError")
    True
    >>> is_syntax_error("ZeroDivisionError")
    False
    >>> is_syntax_error("IndentationError")
    True

Requirements:
    - Return True for syntax errors, False for runtime errors
    - Handle at least the common error types
"""

from __future__ import annotations


def is_syntax_error(error_type: str) -> bool:
    """Determine if an error type is a syntax error.

    Args:
        error_type: The name of the error type

    Returns:
        True if it's a syntax error, False otherwise
    """
    raise NotImplementedError("Implement is_syntax_error")
