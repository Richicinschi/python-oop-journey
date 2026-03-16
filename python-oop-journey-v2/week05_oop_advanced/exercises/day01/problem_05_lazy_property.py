"""Problem 05: Lazy Property

Topic: Property computed once on first access
Difficulty: Medium

Create a lazy property descriptor that defers computation until first access.
"""

from __future__ import annotations

from typing import Any, Callable


class LazyProperty:
    """A non-data descriptor for lazy property evaluation.
    
    This is similar to @property but the value is computed only on first
    access and then cached. This is useful for expensive computations.
    
    The descriptor should:
    - Accept a function that computes the value
    - Compute value only on first access
    - Cache the result in instance __dict__
    - Replace itself with the cached value
    
    This is a NON-DATA descriptor (only __get__).
    """
    
    def __init__(self, func: Callable[[Any], Any]) -> None:
        """Initialize with a compute function.
        
        Args:
            func: Function that computes the property value.
                  Takes instance as argument.
        """
        raise NotImplementedError("Implement LazyProperty.__init__")
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Called when descriptor is assigned to class.
        
        Args:
            owner: The class
            name: The attribute name
        """
        raise NotImplementedError("Implement LazyProperty.__set_name__")
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        """Get the value, computing if necessary.
        
        On first access:
        1. Call the compute function
        2. Store result in instance.__dict__
        3. Return the value
        
        On subsequent accesses, instance.__dict__ will be checked first
        (since this is a non-data descriptor) and this method won't be called.
        
        Args:
            instance: The instance, or None for class access
            owner: The owner class
            
        Returns:
            The computed/cached value, or self if class access
        """
        raise NotImplementedError("Implement LazyProperty.__get__")


class Circle:
    """A circle with lazy-computed properties.
    
    Attributes:
        radius: The circle radius
        
    Lazy Properties:
        area: Area of the circle (πr²)
        circumference: Circumference of the circle (2πr)
        diameter: Diameter of the circle (2r)
    """
    
    def __init__(self, radius: float) -> None:
        """Initialize circle with radius.
        
        Args:
            radius: The circle radius (must be positive)
        """
        raise NotImplementedError("Implement Circle.__init__")
    
    @LazyProperty
    def area(self) -> float:
        """Calculate area (expensive computation).
        
        Returns:
            π * radius²
        """
        raise NotImplementedError("Implement Circle.area")
    
    @LazyProperty
    def circumference(self) -> float:
        """Calculate circumference.
        
        Returns:
            2 * π * radius
        """
        raise NotImplementedError("Implement Circle.circumference")
    
    @LazyProperty
    def diameter(self) -> float:
        """Calculate diameter.
        
        Returns:
            2 * radius
        """
        raise NotImplementedError("Implement Circle.diameter")


class DatabaseConnection:
    """A database connection with lazy initialization.
    
    Attributes:
        connection_string: Database connection string
        
    Lazy Properties:
        connection: The actual database connection (expensive to create)
        schema: Database schema information
    """
    
    def __init__(self, connection_string: str) -> None:
        """Initialize with connection string.
        
        Args:
            connection_string: Connection string
        """
        raise NotImplementedError("Implement DatabaseConnection.__init__")
    
    @LazyProperty
    def connection(self) -> str:
        """Establish database connection (simulated).
        
        Returns:
            Connection object (simulated as string)
        """
        raise NotImplementedError("Implement DatabaseConnection.connection")
    
    @LazyProperty
    def schema(self) -> dict[str, list[str]]:
        """Get database schema (requires connection).
        
        Returns:
            Dictionary mapping table names to column lists
        """
        raise NotImplementedError("Implement DatabaseConnection.schema")
    
    def is_connected(self) -> bool:
        """Check if connection has been established.
        
        Returns:
            True if connection property has been accessed
        """
        raise NotImplementedError("Implement DatabaseConnection.is_connected")


class Matrix:
    """A matrix with lazy computed properties.
    
    Attributes:
        data: 2D list of matrix values
        
    Lazy Properties:
        transpose: Transpose of the matrix
        determinant: Determinant of the matrix
    """
    
    def __init__(self, data: list[list[float]]) -> None:
        """Initialize with matrix data.
        
        Args:
            data: 2D list of floats
        """
        raise NotImplementedError("Implement Matrix.__init__")
    
    @LazyProperty
    def transpose(self) -> Matrix:
        """Compute matrix transpose.
        
        Returns:
            New Matrix that is the transpose
        """
        raise NotImplementedError("Implement Matrix.transpose")
    
    @LazyProperty
    def determinant(self) -> float:
        """Compute determinant (for 2x2 or 3x3 matrices).
        
        Returns:
            The determinant value
            
        Raises:
            ValueError: If matrix is not 2x2 or 3x3
        """
        raise NotImplementedError("Implement Matrix.determinant")


# Hints for Lazy Property (Medium):
# 
# Hint 1 - Conceptual nudge:
# You need to store the computed value somewhere so you don't recompute it on each access.
# Consider where to store it (instance dict? descriptor storage?) and how to track if
# the value has been computed yet.
#
# Hint 2 - Structural plan:
# - In __init__, store the compute function and initialize a cache dict (WeakKeyDictionary)
# - In __get__, check if instance has a cached value
# - If not cached, call the compute function and store the result
# - Return the cached value on subsequent calls
# - Provide an invalidate() method to clear the cache
#
# Hint 3 - Edge-case warning:
# What if the compute function raises an exception? You might want to cache that result
# or let it propagate each time. Also, make sure to handle class access (instance is None)
# by returning self.
