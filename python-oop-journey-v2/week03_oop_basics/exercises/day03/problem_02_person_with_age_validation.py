"""Exercise: Person with Age Validation.

Implement a Person class with @property for age validation.

TODO:
1. Create a private _age attribute
2. Implement @property getter for age
3. Implement @age.setter with validation (0-150 range)
4. Implement is_adult() and celebrate_birthday() methods
"""

from __future__ import annotations


class Person:
    """A person with validated age using @property.
    
    Attributes:
        name: The person's name (read-only after creation).
    """
    
    def __init__(self, name: str, age: int) -> None:
        """Initialize a person."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = name.strip()
        self._age: int = 0
        self.age = age  # Use setter for validation
    
    @property
    def name(self) -> str:
        """Get the person's name."""
        return self._name
    
    @property
    def age(self) -> int:
        """Get the person's age."""
        # TODO: Return the private _age attribute
        raise NotImplementedError("Return the age")
    
    @age.setter
    def age(self, value: int) -> None:
        """Set the person's age with validation."""
        # TODO: Validate value is an integer
        # TODO: Validate value is between 0 and 150
        # TODO: Set self._age
        raise NotImplementedError("Validate and set the age")
    
    def is_adult(self) -> bool:
        """Check if the person is an adult (age >= 18)."""
        # TODO: Return True if age >= 18
        raise NotImplementedError("Check if adult")
    
    def celebrate_birthday(self) -> None:
        """Increment the person's age by one year."""
        # TODO: Increment age by 1
        raise NotImplementedError("Increment age")
