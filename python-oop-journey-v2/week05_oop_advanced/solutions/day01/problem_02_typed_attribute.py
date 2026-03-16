"""Reference solution for Problem 02: Typed Attribute."""

from __future__ import annotations

from typing import Any, Type, Union, get_args, get_origin


class TypedAttribute:
    """A descriptor that enforces type checking."""
    
    def __init__(self, expected_type: Type[Any], default: Any = None) -> None:
        self.expected_type = expected_type
        self.default = default
        self.name = ""
        self.storage_name = ""
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.storage_name = f"_{name}"
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.storage_name, self.default)
    
    def __set__(self, instance: object, value: Any) -> None:
        if not self._check_type(value):
            raise TypeError(
                f"'{self.name}' must be of type {self.expected_type}, "
                f"got {type(value).__name__}"
            )
        setattr(instance, self.storage_name, value)
    
    def _check_type(self, value: Any) -> bool:
        if value is None:
            return True
        
        origin = get_origin(self.expected_type)
        if origin is Union:
            args = get_args(self.expected_type)
            return isinstance(value, args)
        
        # Allow int for float type
        if self.expected_type is float and isinstance(value, int):
            return True
        
        return isinstance(value, self.expected_type)


class Student:
    """A student with type-checked attributes."""
    
    name = TypedAttribute(str)
    age = TypedAttribute(int)
    gpa = TypedAttribute(float)
    grades = TypedAttribute(list, default=[])
    
    def __init__(self, name: str, age: int, gpa: float = 0.0) -> None:
        self.name = name
        self.age = age
        self.gpa = gpa


class Config:
    """Configuration with typed attributes."""
    
    debug = TypedAttribute(bool, default=False)
    port = TypedAttribute(int, default=8080)
    host = TypedAttribute(str, default="localhost")
    
    def __init__(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
