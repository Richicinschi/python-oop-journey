"""Reference solution for Problem 04: Validate Data."""

from __future__ import annotations


def validate_data(data: dict) -> list:
    """Validate user data and return list of errors.

    Args:
        data: Dictionary containing user data

    Returns:
        List of error message strings (empty if valid)
    """
    errors = []
    
    # Check name
    if "name" not in data:
        errors.append("name is required")
    elif not isinstance(data["name"], str):
        errors.append("name must be a string")
    elif not data["name"].strip():
        errors.append("name cannot be empty")
    
    # Check age
    if "age" not in data:
        errors.append("age is required")
    else:
        try:
            age = int(data["age"])
            if age < 0:
                errors.append("age must be non-negative")
        except (ValueError, TypeError):
            errors.append("age must be a valid integer")
    
    # Check email
    if "email" not in data:
        errors.append("email is required")
    elif not isinstance(data["email"], str):
        errors.append("email must be a string")
    elif "@" not in data["email"]:
        errors.append("email must contain @")
    
    return errors
