"""Problem 01: Validated Attribute

Topic: Descriptors with validation
Difficulty: Easy

Create a descriptor that validates values against custom rules.
"""

from __future__ import annotations

from typing import Any, Callable


class ValidatedAttribute:
    """A descriptor that validates values using custom validator functions.
    
    The descriptor should:
    - Accept a validator function in __init__
    - Validate values on __set__
    - Raise ValueError if validation fails
    - Store values using the descriptor protocol
    
    Attributes:
        validator: A function that takes a value and returns True if valid
        default: Optional default value
    """
    
    def __init__(
        self, 
        validator: Callable[[Any], bool] | None = None,
        default: Any = None
    ) -> None:
        """Initialize the descriptor with a validator function.
        
        Args:
            validator: Function that returns True if value is valid
            default: Default value if attribute is accessed before setting
        """
        raise NotImplementedError("Implement ValidatedAttribute.__init__")
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Called when descriptor is assigned to a class attribute.
        
        Args:
            owner: The class the descriptor is assigned to
            name: The attribute name
        """
        raise NotImplementedError("Implement ValidatedAttribute.__set_name__")
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        """Get the attribute value.
        
        Args:
            instance: The instance accessing the attribute, or None if class access
            owner: The class that owns this descriptor
            
        Returns:
            The stored value, or default if not set, or self if class access
        """
        raise NotImplementedError("Implement ValidatedAttribute.__get__")
    
    def __set__(self, instance: object, value: Any) -> None:
        """Set the attribute value with validation.
        
        Args:
            instance: The instance setting the attribute
            value: The value to set
            
        Raises:
            ValueError: If the value fails validation
        """
        raise NotImplementedError("Implement ValidatedAttribute.__set__")


class Person:
    """A person with validated attributes.
    
    Uses ValidatedAttribute for:
    - age: must be between 0 and 150
    - name: must be a non-empty string
    
    Attributes:
        name: The person's name (validated)
        age: The person's age (validated)
    """
    
    age = ValidatedAttribute(validator=lambda x: isinstance(x, int) and 0 <= x <= 150)
    name = ValidatedAttribute(validator=lambda x: isinstance(x, str) and len(x) > 0)
    
    def __init__(self, name: str, age: int) -> None:
        """Initialize a Person with validated attributes.
        
        Args:
            name: The person's name (must be non-empty string)
            age: The person's age (must be 0-150)
        """
        raise NotImplementedError("Implement Person.__init__")


class Product:
    """A product with validated price.
    
    Attributes:
        name: The product name
        price: The product price (must be positive)
    """
    
    price = ValidatedAttribute(validator=lambda x: isinstance(x, (int, float)) and x > 0)
    
    def __init__(self, name: str, price: float) -> None:
        """Initialize a Product.
        
        Args:
            name: The product name
            price: The product price (must be positive)
        """
        raise NotImplementedError("Implement Product.__init__")
