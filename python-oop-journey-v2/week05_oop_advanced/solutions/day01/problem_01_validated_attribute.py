"""Reference solution for Problem 01: Validated Attribute."""

from __future__ import annotations

from typing import Any, Callable


class ValidatedAttribute:
    """A descriptor that validates values using custom validator functions."""
    
    def __init__(
        self, 
        validator: Callable[[Any], bool] | None = None,
        default: Any = None
    ) -> None:
        self.validator = validator
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
        if self.validator is not None and not self.validator(value):
            raise ValueError(f"Invalid value for '{self.name}': {value}")
        setattr(instance, self.storage_name, value)


class Person:
    """A person with validated attributes."""
    
    age = ValidatedAttribute(validator=lambda x: isinstance(x, int) and 0 <= x <= 150)
    name = ValidatedAttribute(validator=lambda x: isinstance(x, str) and len(x) > 0)
    
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age


class Product:
    """A product with validated price."""
    
    price = ValidatedAttribute(validator=lambda x: isinstance(x, (int, float)) and x > 0)
    
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price
