"""Solution for Problem 02: Person with Age Validation.

Demonstrates using @property for age validation.
"""

from __future__ import annotations


class Person:
    """A person with validated age using @property.
    
    This class demonstrates property-based encapsulation where
    age is validated whenever it's set.
    
    Attributes:
        name: The person's name (read-only after creation).
    
    Example:
        >>> person = Person("Alice", 25)
        >>> person.age
        25
        >>> person.age = 30
        >>> person.age
        30
        >>> person.age = -5  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
            ...
        ValueError: Age must be between 0 and 150
    """
    
    def __init__(self, name: str, age: int) -> None:
        """Initialize a person.
        
        Args:
            name: The person's name.
            age: The person's age (must be 0-150).
        
        Raises:
            TypeError: If name is not a string.
            ValueError: If age is not between 0 and 150.
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not name.strip():
            raise ValueError("Name cannot be empty")
        self._name = name.strip()
        self._age: int = 0
        self.age = age  # Use setter for validation
    
    @property
    def name(self) -> str:
        """Get the person's name.
        
        Returns:
            The person's name.
        """
        return self._name
    
    @property
    def age(self) -> int:
        """Get the person's age.
        
        Returns:
            The person's age as an integer.
        """
        return self._age
    
    @age.setter
    def age(self, value: int) -> None:
        """Set the person's age with validation.
        
        Args:
            value: The new age value.
        
        Raises:
            TypeError: If value is not an integer.
            ValueError: If value is not between 0 and 150.
        """
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value < 0 or value > 150:
            raise ValueError("Age must be between 0 and 150")
        self._age = value
    
    def is_adult(self) -> bool:
        """Check if the person is an adult (age >= 18).
        
        Returns:
            True if age is 18 or older, False otherwise.
        """
        return self._age >= 18
    
    def celebrate_birthday(self) -> None:
        """Increment the person's age by one year."""
        self._age += 1
