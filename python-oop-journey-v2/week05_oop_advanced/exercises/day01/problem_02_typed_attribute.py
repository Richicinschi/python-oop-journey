"""Problem 02: Typed Attribute

Topic: Type-checking descriptor
Difficulty: Easy

Create a descriptor that enforces type checking on attribute assignment.
"""

from __future__ import annotations

from typing import Any, Type, Union, get_args, get_origin


class TypedAttribute:
    """A descriptor that enforces type checking.
    
    The descriptor should:
    - Accept an expected type in __init__
    - Support simple types (int, str, float) and complex types (list, dict)
    - Support Union types (e.g., Union[int, float])
    - Raise TypeError if value is not of expected type
    
    Attributes:
        expected_type: The type that values must match
        default: Optional default value
    """
    
    def __init__(self, expected_type: Type[Any], default: Any = None) -> None:
        """Initialize with an expected type.
        
        Args:
            expected_type: The type that values must match
            default: Default value if attribute not set
        """
        raise NotImplementedError("Implement TypedAttribute.__init__")
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Called when descriptor is assigned to class attribute.
        
        Args:
            owner: The class the descriptor is assigned to
            name: The attribute name
        """
        raise NotImplementedError("Implement TypedAttribute.__set_name__")
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        """Get the attribute value.
        
        Args:
            instance: The instance, or None if class access
            owner: The owner class
            
        Returns:
            Stored value, default, or self
        """
        raise NotImplementedError("Implement TypedAttribute.__get__")
    
    def __set__(self, instance: object, value: Any) -> None:
        """Set the attribute with type checking.
        
        Args:
            instance: The instance setting the attribute
            value: The value to set
            
        Raises:
            TypeError: If value doesn't match expected type
        """
        raise NotImplementedError("Implement TypedAttribute.__set__")
    
    def _check_type(self, value: Any) -> bool:
        """Check if value matches the expected type.
        
        Args:
            value: The value to check
            
        Returns:
            True if type matches, False otherwise
            
        Note:
            Must handle Union types using get_origin and get_args
        """
        raise NotImplementedError("Implement TypedAttribute._check_type")


class Student:
    """A student with type-checked attributes.
    
    Attributes:
        name: str
        age: int
        gpa: float
        grades: list
    """
    
    name = TypedAttribute(str)
    age = TypedAttribute(int)
    gpa = TypedAttribute(float)
    grades = TypedAttribute(list, default=[])
    
    def __init__(self, name: str, age: int, gpa: float = 0.0) -> None:
        """Initialize a Student.
        
        Args:
            name: Student's name (must be str)
            age: Student's age (must be int)
            gpa: Student's GPA (must be float)
        """
        raise NotImplementedError("Implement Student.__init__")


class Config:
    """Configuration with typed attributes.
    
    Attributes:
        debug: bool
        port: int
        host: str
    """
    
    debug = TypedAttribute(bool, default=False)
    port = TypedAttribute(int, default=8080)
    host = TypedAttribute(str, default="localhost")
    
    def __init__(self, **kwargs: Any) -> None:
        """Initialize config with keyword arguments.
        
        Args:
            **kwargs: Keyword arguments to set as attributes
        """
        raise NotImplementedError("Implement Config.__init__")
