"""Reference solution for Problem 01: Vector 2D."""

from __future__ import annotations

import math


class Vector2D:
    """A 2D vector supporting addition, subtraction, and scalar multiplication.
    
    Attributes:
        x: The x-component of the vector.
        y: The y-component of the vector.
    """
    
    def __init__(self, x: float, y: float) -> None:
        """Initialize a 2D vector.
        
        Args:
            x: The x-component.
            y: The y-component.
        """
        self.x = x
        self.y = y
    
    def __add__(self, other: Vector2D) -> Vector2D:
        """Add two vectors component-wise.
        
        Args:
            other: The vector to add.
        
        Returns:
            A new Vector2D with summed components.
        
        Raises:
            TypeError: If other is not a Vector2D.
        """
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Vector2D) -> Vector2D:
        """Subtract another vector component-wise.
        
        Args:
            other: The vector to subtract.
        
        Returns:
            A new Vector2D with subtracted components.
        
        Raises:
            TypeError: If other is not a Vector2D.
        """
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> Vector2D:
        """Multiply the vector by a scalar.
        
        Args:
            scalar: The scalar value.
        
        Returns:
            A new Vector2D with scaled components.
        
        Raises:
            TypeError: If scalar is not a number.
        """
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: float) -> Vector2D:
        """Support scalar * vector (reverse multiplication).
        
        Args:
            scalar: The scalar value.
        
        Returns:
            A new Vector2D with scaled components.
        """
        return self.__mul__(scalar)
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        return f"Vector2D({self.x}, {self.y})"
    
    def magnitude(self) -> float:
        """Calculate the magnitude (length) of the vector.
        
        Returns:
            The Euclidean magnitude sqrt(x² + y²).
        """
        return math.sqrt(self.x**2 + self.y**2)
