"""Reference solution for Problem 01: Person Class."""

from __future__ import annotations


class Person:
    """A class representing a person with name and age."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize a Person with name and age.
        
        Args:
            name: The person's name
            age: The person's age
        """
        self.name = name
        self.age = age

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        return f"Person(name={self.name}, age={self.age})"

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"Person(name='{self.name}', age={self.age})"
