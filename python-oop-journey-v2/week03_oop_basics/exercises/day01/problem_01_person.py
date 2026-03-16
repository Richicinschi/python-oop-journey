"""Problem 01: Person Class

Topic: Basic class definition, __init__, attributes
Difficulty: Easy

Create a Person class with name and age attributes.

Examples:
    >>> person = Person("Alice", 30)
    >>> person.name
    'Alice'
    >>> person.age
    30
    >>> str(person)
    'Person(name=Alice, age=30)'

Requirements:
    - __init__ takes name (str) and age (int) parameters
    - Store name and age as instance attributes
    - Implement __str__ for readable string representation
    - Implement __repr__ for debugging representation
"""

from __future__ import annotations


class Person:
    """A class representing a person with name and age."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize a Person with name and age."""
        raise NotImplementedError("Initialize name and age attributes")

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        raise NotImplementedError("Implement __str__ method")

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        raise NotImplementedError("Implement __repr__ method")
