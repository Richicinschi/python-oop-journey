"""Problem 01: Greeting Module

Topic: Creating and using modules
Difficulty: Easy

Create a simple greeting module with functions to generate different
types of greeting messages.

Your module should expose these functions:
- hello(name): Return a simple hello message
- goodbye(name): Return a goodbye message
- welcome(name, occasion): Return a welcome message for an occasion

Example usage when imported:
    >>> from greeting_module import hello
    >>> hello("Alice")
    'Hello, Alice!'
    >>> goodbye("Bob")
    'Goodbye, Bob!'
    >>> welcome("Charlie", "party")
    'Welcome to the party, Charlie!'
"""

from __future__ import annotations


def hello(name: str) -> str:
    """Return a simple hello greeting.

    Args:
        name: The name of the person to greet

    Returns:
        A greeting string like "Hello, {name}!"
    """
    raise NotImplementedError("Implement hello")


def goodbye(name: str) -> str:
    """Return a goodbye message.

    Args:
        name: The name of the person to bid farewell

    Returns:
        A farewell string like "Goodbye, {name}!"
    """
    raise NotImplementedError("Implement goodbye")


def welcome(name: str, occasion: str) -> str:
    """Return a welcome message for an occasion.

    Args:
        name: The name of the guest
        occasion: The type of event (party, meeting, etc.)

    Returns:
        A welcome string like "Welcome to the {occasion}, {name}!"
    """
    raise NotImplementedError("Implement welcome")


if __name__ == "__main__":
    # This block runs when the file is executed directly
    # Add code here to test your functions
    pass
