"""Problem 05: Student Registry

Topic: @classmethod registry pattern
Difficulty: Medium

Create a Student class that tracks all registered students using
the registry pattern with class methods.

Example:
    >>> s1 = Student("Alice", 101)
    >>> s2 = Student("Bob", 102)
    >>> 
    >>> Student.get_count()
    2
    >>> 
    >>> Student.list_all()
    ['Alice (101)', 'Bob (102)']
    >>> 
    >>> Student.find_by_id(101)
    'Alice (101)'
    >>> Student.find_by_id(999)
    None
    >>> 
    >>> s1.unregister()
    >>> Student.get_count()
    1

Requirements:
    - __init__ takes name (str) and student_id (int)
    - _registry: class-level dict to store students by id
    - get_count(cls) -> int: classmethod, returns number of registered students
    - list_all(cls) -> list[str]: classmethod, returns list of "Name (ID)" strings
    - find_by_id(cls, student_id: int) -> str | None: classmethod
    - unregister(self): instance method to remove student from registry
"""

from __future__ import annotations


class Student:
    """Student class with registry pattern for tracking all instances."""
    
    _registry: dict[int, Student] = {}
    
    def __init__(self, name: str, student_id: int) -> None:
        """Initialize a student and register in the class registry.
        
        Args:
            name: Student name
            student_id: Unique student ID
        """
        raise NotImplementedError("Implement __init__")
    
    def __repr__(self) -> str:
        """Return string representation."""
        return f"{self.name} ({self.student_id})"
    
    @classmethod
    def get_count(cls) -> int:
        """Get the number of registered students.
        
        Returns:
            Count of registered students
        """
        raise NotImplementedError("Implement get_count")
    
    @classmethod
    def list_all(cls) -> list[str]:
        """List all registered students.
        
        Returns:
            List of student representations
        """
        raise NotImplementedError("Implement list_all")
    
    @classmethod
    def find_by_id(cls, student_id: int) -> str | None:
        """Find a student by their ID.
        
        Args:
            student_id: The student ID to search for
            
        Returns:
            Student representation if found, None otherwise
        """
        raise NotImplementedError("Implement find_by_id")
    
    def unregister(self) -> None:
        """Remove this student from the registry."""
        raise NotImplementedError("Implement unregister")
