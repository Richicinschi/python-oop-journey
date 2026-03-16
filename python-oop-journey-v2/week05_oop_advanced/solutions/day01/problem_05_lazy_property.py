"""Reference solution for Problem 05: Lazy Property."""

from __future__ import annotations

import math
from typing import Any, Callable


class LazyProperty:
    """A non-data descriptor for lazy property evaluation."""
    
    def __init__(self, func: Callable[[Any], Any]) -> None:
        self.func = func
        self.name = func.__name__
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        
        value = self.func(instance)
        setattr(instance, self.name, value)
        return value


class Circle:
    """A circle with lazy-computed properties."""
    
    def __init__(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("Radius must be positive")
        self.radius = radius
    
    @LazyProperty
    def area(self) -> float:
        return math.pi * self.radius ** 2
    
    @LazyProperty
    def circumference(self) -> float:
        return 2 * math.pi * self.radius
    
    @LazyProperty
    def diameter(self) -> float:
        return 2 * self.radius


class DatabaseConnection:
    """A database connection with lazy initialization."""
    
    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string
    
    @LazyProperty
    def connection(self) -> str:
        return f"Connection({self.connection_string})"
    
    @LazyProperty
    def schema(self) -> dict[str, list[str]]:
        return {
            "users": ["id", "name", "email"],
            "posts": ["id", "user_id", "title", "content"]
        }
    
    def is_connected(self) -> bool:
        return 'connection' in self.__dict__


class Matrix:
    """A matrix with lazy computed properties."""
    
    def __init__(self, data: list[list[float]]) -> None:
        self.data = data
    
    @LazyProperty
    def transpose(self) -> Matrix:
        transposed = [[self.data[j][i] for j in range(len(self.data))] 
                      for i in range(len(self.data[0]))]
        return Matrix(transposed)
    
    @LazyProperty
    def determinant(self) -> float:
        if len(self.data) != len(self.data[0]):
            raise ValueError("Matrix must be square")
        
        n = len(self.data)
        if n == 2:
            return float(self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0])
        elif n == 3:
            a, b, c = self.data[0]
            d, e, f = self.data[1]
            g, h, i = self.data[2]
            return float(a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g))
        else:
            raise ValueError("Only 2x2 or 3x3 matrices supported")
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return False
        return self.data == other.data
