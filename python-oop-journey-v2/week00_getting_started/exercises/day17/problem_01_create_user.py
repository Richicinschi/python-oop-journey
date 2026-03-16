"""Problem 01: Create User Profile

Topic: Function Parameters - Default Values
Difficulty: Easy

Write a function that creates a user profile dictionary.

Function Signature:
    def create_user(name: str, age: int = 0, city: str = "Unknown") -> dict[str, str | int]

Requirements:
    - Return a dictionary with keys: 'name', 'age', 'city'
    - name is required
    - age defaults to 0
    - city defaults to "Unknown"

Behavior Notes:
    - Use default parameter values
    - name has no default (required argument)
    - age and city have defaults (optional arguments)

Examples:
    >>> create_user("Alice", 30, "NYC")
    {'name': 'Alice', 'age': 30, 'city': 'NYC'}
    
    With defaults:
    >>> create_user("Bob")
    {'name': 'Bob', 'age': 0, 'city': 'Unknown'}
    
    Partial defaults:
    >>> create_user("Charlie", 25)
    {'name': 'Charlie', 'age': 25, 'city': 'Unknown'}
    
    >>> create_user("Diana", city="LA")
    {'name': 'Diana', 'age': 0, 'city': 'LA'}

Input Validation:
    - You may assume name is a string
    - age is an integer
    - city is a string

"""

from __future__ import annotations


def create_user(name: str, age: int = 0, city: str = "Unknown") -> dict[str, str | int]:
    """Create a user profile dictionary.

    Args:
        name: The user's name (required).
        age: The user's age (default 0).
        city: The user's city (default "Unknown").

    Returns:
        A dictionary with user information.
    """
    raise NotImplementedError("Implement create_user")
