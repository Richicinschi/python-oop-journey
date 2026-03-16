"""Problem 01: Vector 2D

Topic: Magic Methods - Arithmetic Operations
Difficulty: Easy

Implement a 2D vector class with arithmetic operations using magic methods.
"""

from __future__ import annotations


class Vector2D:
    """A 2D vector supporting addition, subtraction, and scalar multiplication.
    
    Attributes:
        x: The x-component of the vector.
        y: The y-component of the vector.
    
    Example:
        >>> v1 = Vector2D(1, 2)
        >>> v2 = Vector2D(3, 4)
        >>> v1 + v2
        Vector2D(4, 6)
        >>> v1 * 2
        Vector2D(2, 4)
    """
    
    def __init__(self, x: float, y: float) -> None:
        """Initialize a 2D vector.
        
        Args:
            x: The x-component.
            y: The y-component.
        """
        raise NotImplementedError("Implement __init__")
    
    def __add__(self, other: Vector2D) -> Vector2D:
        """Add two vectors component-wise.
        
        Args:
            other: The vector to add.
        
        Returns:
            A new Vector2D with summed components.
        
        Raises:
            TypeError: If other is not a Vector2D.
        """
        raise NotImplementedError("Implement __add__")
    
    def __sub__(self, other: Vector2D) -> Vector2D:
        """Subtract another vector component-wise.
        
        Args:
            other: The vector to subtract.
        
        Returns:
            A new Vector2D with subtracted components.
        
        Raises:
            TypeError: If other is not a Vector2D.
        """
        raise NotImplementedError("Implement __sub__")
    
    def __mul__(self, scalar: float) -> Vector2D:
        """Multiply the vector by a scalar.
        
        Args:
            scalar: The scalar value.
        
        Returns:
            A new Vector2D with scaled components.
        
        Raises:
            TypeError: If scalar is not a number.
        """
        raise NotImplementedError("Implement __mul__")
    
    def __rmul__(self, scalar: float) -> Vector2D:
        """Support scalar * vector (reverse multiplication).
        
        Args:
            scalar: The scalar value.
        
        Returns:
            A new Vector2D with scaled components.
        """
        raise NotImplementedError("Implement __rmul__")
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        raise NotImplementedError("Implement __repr__")
    
    def magnitude(self) -> float:
        """Calculate the magnitude (length) of the vector.
        
        Returns:
            The Euclidean magnitude sqrt(x² + y²).
        """
        raise NotImplementedError("Implement magnitude")
