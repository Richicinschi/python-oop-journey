"""Problem 04: Validation Metaclass - Solution.

Validates class attributes at class creation time, catching configuration
errors early when the class is defined rather than when instantiated.
"""

from __future__ import annotations

from typing import Any


class ValidationMeta(type):
    """Metaclass that validates class attributes at creation time.
    
    Classes using this metaclass can define _validation_rules to specify:
    - Required attributes that must be present
    - Type constraints for attributes
    - Value constraints (min, max, length, etc.)
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
        # Get validation rules from the namespace
        rules = namespace.get('_validation_rules', {})
        
        if rules:
            mcs._validate_rules(name, namespace, rules)
        
        return super().__new__(mcs, name, bases, namespace)
    
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
        for attr_name, constraints in rules.items():
            # Check attribute exists
            if attr_name not in namespace:
                raise TypeError(
                    f"{class_name} is missing required attribute '{attr_name}'"
                )
            
            value = namespace[attr_name]
            
            # Check type constraint
            if 'type' in constraints:
                expected_types = constraints['type']
                if isinstance(expected_types, tuple):
                    if not isinstance(value, expected_types):
                        raise TypeError(
                            f"{class_name}.{attr_name} must be one of "
                            f"{[t.__name__ for t in expected_types]}, "
                            f"got {type(value).__name__}"
                        )
                elif not isinstance(value, expected_types):
                    raise TypeError(
                        f"{class_name}.{attr_name} must be {expected_types.__name__}, "
                        f"got {type(value).__name__}"
                    )
            
            # Check min value constraint (for numbers)
            if 'min' in constraints and isinstance(value, (int, float)):
                if value < constraints['min']:
                    raise TypeError(
                        f"{class_name}.{attr_name} must be >= {constraints['min']}, "
                        f"got {value}"
                    )
            
            # Check max value constraint (for numbers)
            if 'max' in constraints and isinstance(value, (int, float)):
                if value > constraints['max']:
                    raise TypeError(
                        f"{class_name}.{attr_name} must be <= {constraints['max']}, "
                        f"got {value}"
                    )
            
            # Check min length constraint (for strings)
            if 'min_length' in constraints and isinstance(value, str):
                if len(value) < constraints['min_length']:
                    raise TypeError(
                        f"{class_name}.{attr_name} must have length >= "
                        f"{constraints['min_length']}, got {len(value)}"
                    )


class ValidatedModel(metaclass=ValidationMeta):
    """Base model class with validation support.
    
    Subclasses should define _validation_rules to enable validation.
    """
    
    _validation_rules: dict[str, Any] = {}
    
    def __init__(self, **kwargs: Any) -> None:
        """Initialize model with validated attributes."""
        for key, value in kwargs.items():
            setattr(self, key, value)


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
        super().__init__()
        self.username = username
    
    def validate_username(self, username: str) -> bool:
        """Validate username meets minimum length.
        
        Args:
            username: Username to validate
            
        Returns:
            True if valid, False otherwise
        """
        return len(username) >= self.USERNAME_MIN_LENGTH


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
        super().__init__()
        self.name = name
        self.price = price
    
    def is_valid_price(self) -> bool:
        """Check if current price is valid.
        
        Returns:
            True if price is valid (0 < price <= MAX_PRICE)
        """
        return 0 < self.price <= self.MAX_PRICE
