"""Reference solution for Problem 01: Greeting Module."""

from __future__ import annotations


def hello(name: str) -> str:
    """Return a simple hello greeting.

    Args:
        name: The name of the person to greet

    Returns:
        A greeting string like "Hello, {name}!"
    """
    return f"Hello, {name}!"


def goodbye(name: str) -> str:
    """Return a goodbye message.

    Args:
        name: The name of the person to bid farewell

    Returns:
        A farewell string like "Goodbye, {name}!"
    """
    return f"Goodbye, {name}!"


def welcome(name: str, occasion: str) -> str:
    """Return a welcome message for an occasion.

    Args:
        name: The name of the guest
        occasion: The type of event (party, meeting, etc.)

    Returns:
        A welcome string like "Welcome to the {occasion}, {name}!"
    """
    return f"Welcome to the {occasion}, {name}!"


if __name__ == "__main__":
    print(hello("World"))
    print(goodbye("Alice"))
    print(welcome("Bob", "conference"))
