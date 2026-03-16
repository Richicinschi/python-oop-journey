"""Problem 03: Format Name

Topic: Function Parameters - Multiple Arguments
Difficulty: Easy

Write a function that formats a person's full name.

Function Signature:
    def format_name(first: str, last: str, middle: str = "") -> str

Requirements:
    - Return formatted full name
    - If middle name provided: "First Middle Last"
    - If no middle name: "First Last"
    - Handle extra whitespace

Behavior Notes:
    - Check if middle is provided (non-empty)
    - Strip whitespace from all parts
    - Join with spaces appropriately

Examples:
    >>> format_name("John", "Doe")
    'John Doe'
    
    With middle name:
    >>> format_name("John", "Doe", "Quincy")
    'John Quincy Doe'
    
    Empty middle name:
    >>> format_name("Jane", "Smith", "")
    'Jane Smith'
    
    Extra whitespace:
    >>> format_name("  John  ", "  Doe  ")
    'John Doe'

Input Validation:
    - You may assume first and last are non-empty strings
    - middle may be empty string

"""

from __future__ import annotations


def format_name(first: str, last: str, middle: str = "") -> str:
    """Format a person's full name.

    Args:
        first: First name.
        last: Last name.
        middle: Middle name (optional).

    Returns:
        Formatted full name.
    """
    raise NotImplementedError("Implement format_name")
