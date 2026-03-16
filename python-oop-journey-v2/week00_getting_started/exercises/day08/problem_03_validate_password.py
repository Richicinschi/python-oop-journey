"""Problem 03: Validate Password

Topic: Boolean Logic, Logical Operators
Difficulty: Easy

Write a function that validates a password based on basic criteria.
A valid password must:
- Be at least 8 characters long
- Contain at least one uppercase letter
- Contain at least one lowercase letter
- Contain at least one digit

Examples:
    >>> validate_password("Hello1")
    False  # Too short
    >>> validate_password("HELLO123")
    False  # No lowercase
    >>> validate_password("hello123")
    False  # No uppercase
    >>> validate_password("HelloWorld")
    False  # No digit
    >>> validate_password("HelloWorld1")
    True   # Valid

Requirements:
    - Use string methods like isupper(), islower(), isdigit()
    - Combine conditions with logical operators
    - Return a boolean value
"""

from __future__ import annotations


def validate_password(password: str) -> bool:
    """Validate password meets complexity requirements.

    Args:
        password: The password string to validate

    Returns:
        True if password meets all criteria, False otherwise
    """
    raise NotImplementedError("Implement validate_password")
