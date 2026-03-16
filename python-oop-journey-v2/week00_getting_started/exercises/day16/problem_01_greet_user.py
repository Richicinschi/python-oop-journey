"""Problem 01: Greet User

Topic: Functions - Defining and Calling
Difficulty: Easy

Write a function that takes a name and returns a greeting message.

Function Signature:
    def greet_user(name: str) -> str

Requirements:
    - Return a greeting message in the format "Hello, {name}!"
    - Handle empty string by returning "Hello, stranger!"

Behavior Notes:
    - Use f-strings for formatting: f"Hello, {name}!"
    - Empty name should use default greeting
    - Keep it simple - one parameter, one return

Examples:
    >>> greet_user("Alice")
    'Hello, Alice!'
    
    >>> greet_user("Bob")
    'Hello, Bob!'
    
    Empty string:
    >>> greet_user("")
    'Hello, stranger!'

Input Validation:
    - You may assume name is a string (could be empty)
    - No need to handle non-string inputs

"""

from __future__ import annotations


def greet_user(name: str) -> str:
    """Return a greeting message for the given name.

    Args:
        name: The name of the person to greet.

    Returns:
        A greeting message in the format "Hello, {name}!".
    """
    raise NotImplementedError("Implement greet_user")
