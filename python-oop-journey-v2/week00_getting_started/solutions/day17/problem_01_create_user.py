"""Problem 01: Create User - Solution."""

from __future__ import annotations


def create_user(name: str, age: int, city: str = "Unknown") -> dict[str, str | int]:
    """Create a user profile dictionary.

    Args:
        name: The user's name (required).
        age: The user's age in years (required).
        city: The user's city (optional, defaults to "Unknown").

    Returns:
        A dictionary with keys 'name', 'age', and 'city'.
    """
    return {"name": name, "age": age, "city": city}
