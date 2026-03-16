"""Reference solution for Problem 02: Is Syntax Error."""

from __future__ import annotations


def is_syntax_error(error_type: str) -> bool:
    """Determine if an error type is a syntax error.

    Args:
        error_type: The name of the error type

    Returns:
        True if it's a syntax error, False otherwise
    """
    syntax_errors = {"SyntaxError", "IndentationError"}
    return error_type in syntax_errors
