"""Reference solution for Problem 03: Validate Password.

This solution demonstrates a step-by-step validation approach:
1. Check each requirement independently
2. Return False as soon as any check fails
3. Only return True if all checks pass

The any() function is perfect here - it returns True if at least one
character satisfies the condition, and stops early (short-circuits).
"""

from __future__ import annotations


def validate_password(password: str) -> bool:
    """Validate password meets complexity requirements.

    Args:
        password: The password string to validate

    Returns:
        True if password meets all criteria, False otherwise
    """
    # Check 1: Minimum length requirement
    # Password must be at least 8 characters long
    if len(password) < 8:
        return False

    # Check 2: Must contain at least one uppercase letter
    # any() iterates through each character and checks isupper()
    has_upper = any(char.isupper() for char in password)
    if not has_upper:
        return False

    # Check 3: Must contain at least one lowercase letter
    has_lower = any(char.islower() for char in password)
    if not has_lower:
        return False

    # Check 4: Must contain at least one digit (0-9)
    has_digit = any(char.isdigit() for char in password)
    if not has_digit:
        return False

    # All checks passed - password is valid
    return True
