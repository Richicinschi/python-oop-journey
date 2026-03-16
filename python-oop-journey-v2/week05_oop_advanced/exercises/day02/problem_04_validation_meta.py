"""Problem 04: Validation Metaclass

Topic: Metaclasses
Difficulty: Medium

Implement a metaclass that validates class attributes at class creation time.
This allows catching configuration errors early, when the class is defined
rather than when it's instantiated.

Classes to implement:
- ValidationMeta: Metaclass that validates class definitions
- ValidatedModel: Base class for validated models
- User, Product: Example validated models

Requirements:
- Define validation rules as class attributes (_validation_rules)
- Validate that required attributes exist
- Validate attribute types match specifications
- Validate value constraints (min/max for numbers, length for strings)
- Raise TypeError at class creation time for invalid definitions
"""

from __future__ import annotations

from typing import Any


class ValidationMeta(type):
    """Metaclass that validates class attributes at creation time.
    
    Classes using this metaclass can define _validation_rules to specify:
    - Required attributes that must be present
    - Type constraints for attributes
    - Value constraints (min, max, length, etc.)
    
    Example:
        class MyClass(metaclass=ValidationMeta):
            _validation_rules = {
                'MIN_VALUE': {'type': int, 'min': 0},
                'name': {'type': str, 'min_length': 1},
            }
    """
    
    def __new__(
        mcs: type,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> type:
        """Create class after validating it meets all rules.
        
        Args:
            mcs: This metaclass
            name: Name of the class being created
            bases: Base classes
            namespace: Class namespace dictionary
            
        Returns:
            The newly created class
            
        Raises:
            TypeError: If validation rules are violated
        """
        raise NotImplementedError("Implement __new__")
    
    @staticmethod
    def _validate_rules(
        class_name: str,
        namespace: dict[str, Any],
        rules: dict[str, Any],
    ) -> None:
        """Validate namespace against the provided rules.
        
        Args:
            class_name: Name of class being validated
            namespace: Class namespace dictionary
            rules: Validation rules dictionary
            
        Raises:
            TypeError: If any validation fails
        """
        raise NotImplementedError("Implement _validate_rules")


class ValidatedModel(metaclass=ValidationMeta):
    """Base model class with validation support.
    
    Subclasses should define _validation_rules to enable validation.
    
    Attributes:
        _validation_rules: Dictionary of validation rules
    """
    
    _validation_rules: dict[str, Any] = {}
    
    def __init__(self, **kwargs: Any) -> None:
        """Initialize model with validated attributes."""
        raise NotImplementedError("Implement __init__")


class User(ValidatedModel):
    """User model with validation rules.
    
    Validation rules:
    - USERNAME_MIN_LENGTH: int >= 3
    - MAX_LOGIN_ATTEMPTS: int > 0
    - username field must exist (type: str)
    """
    
    _validation_rules = {
        'USERNAME_MIN_LENGTH': {'type': int, 'min': 3},
        'MAX_LOGIN_ATTEMPTS': {'type': int, 'min': 1},
        'username': {'type': str},
    }
    
    USERNAME_MIN_LENGTH: int = 3
    MAX_LOGIN_ATTEMPTS: int = 5
    username: str = ""
    
    def __init__(self, username: str = "") -> None:
        """Initialize user with username.
        
        Args:
            username: The user's username
        """
        raise NotImplementedError("Implement __init__")
    
    def validate_username(self, username: str) -> bool:
        """Validate username meets minimum length.
        
        Args:
            username: Username to validate
            
        Returns:
            True if valid, False otherwise
        """
        raise NotImplementedError("Implement validate_username")


class Product(ValidatedModel):
    """Product model with validation rules.
    
    Validation rules:
    - MAX_PRICE: float > 0
    - name field must exist (type: str)
    - price field must exist (type: float)
    """
    
    _validation_rules = {
        'MAX_PRICE': {'type': (int, float), 'min': 0.01},
        'name': {'type': str},
        'price': {'type': (int, float)},
    }
    
    MAX_PRICE: float = 10000.0
    name: str = ""
    price: float = 0.0
    
    def __init__(self, name: str = "", price: float = 0.0) -> None:
        """Initialize product with name and price.
        
        Args:
            name: Product name
            price: Product price
        """
        raise NotImplementedError("Implement __init__")
    
    def is_valid_price(self) -> bool:
        """Check if current price is valid.
        
        Returns:
            True if price is valid (0 < price <= MAX_PRICE)
        """
        raise NotImplementedError("Implement is_valid_price")


# Hints for Validation Metaclass (Hard):
# 
# Hint 1 - Conceptual nudge:
# You need to inspect type annotations and validate values against those types.
# Use the typing module and isinstance() checks.
#
# Hint 2 - Structural plan:
# - In __new__, look for __annotations__ in the namespace
# - For each annotated field, create a property with validation in the setter
# - The validator should check isinstance(value, annotation_type)
# - Raise TypeError if validation fails
# - Store validated values in instance.__dict__
#
# Hint 3 - Edge-case warning:
# What about Optional types (Union[X, None])? What about complex types like List[int]?
# You might need to use typing.get_origin() and typing.get_args() for complex type checking.
