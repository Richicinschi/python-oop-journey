"""Reference solution for Problem 04: Range Validator."""

from __future__ import annotations

from typing import TypeVar, Generic

T = TypeVar('T', int, float)


class RangeValidator:
    """A descriptor that validates numeric ranges."""
    
    def __init__(
        self,
        min_value: int | float,
        max_value: int | float,
        value_type: type[int] | type[float] = int
    ) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.value_type = value_type
        self.name = ""
        self.storage_name = ""
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.storage_name = f"_{name}"
    
    def __get__(self, instance: object | None, owner: type) -> int | float | RangeValidator:
        if instance is None:
            return self
        return getattr(instance, self.storage_name, None)
    
    def __set__(self, instance: object, value: int | float) -> None:
        if not isinstance(value, self.value_type):
            raise TypeError(
                f"'{self.name}' must be {self.value_type.__name__}, "
                f"got {type(value).__name__}"
            )
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"'{self.name}' must be between {self.min_value} and {self.max_value}, "
                f"got {value}"
            )
        setattr(instance, self.storage_name, value)


class Temperature:
    """Temperature reading with validated range."""
    
    celsius = RangeValidator(-273.15, 1000.0, float)
    fahrenheit = RangeValidator(-459.67, 1832.0, float)
    
    def __init__(self, celsius: float = 0.0) -> None:
        self.celsius = celsius


class Score:
    """A game score with validated range."""
    
    value = RangeValidator(0, 100, int)
    level = RangeValidator(1, 10, int)
    
    def __init__(self, value: int = 0, level: int = 1) -> None:
        self.value = value
        self.level = level


class Percentage:
    """A percentage value (0-100)."""
    
    value = RangeValidator(0, 100, int)
    
    def __init__(self, value: int = 0) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return f"{self.value}%"
    
    def __repr__(self) -> str:
        return f"Percentage({self.value})"
