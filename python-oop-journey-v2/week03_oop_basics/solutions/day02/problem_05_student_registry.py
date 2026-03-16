"""Solution for Problem 05: Student Registry."""

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
        self.name = name
        self.student_id = student_id
        self._registry[student_id] = self
    
    def __repr__(self) -> str:
        """Return string representation."""
        return f"{self.name} ({self.student_id})"
    
    @classmethod
    def get_count(cls) -> int:
        """Get the number of registered students.
        
        Returns:
            Count of registered students
        """
        return len(cls._registry)
    
    @classmethod
    def list_all(cls) -> list[str]:
        """List all registered students.
        
        Returns:
            List of student representations
        """
        return [str(student) for student in cls._registry.values()]
    
    @classmethod
    def find_by_id(cls, student_id: int) -> str | None:
        """Find a student by their ID.
        
        Args:
            student_id: The student ID to search for
            
        Returns:
            Student representation if found, None otherwise
        """
        student = cls._registry.get(student_id)
        if student:
            return str(student)
        return None
    
    def unregister(self) -> None:
        """Remove this student from the registry."""
        if self.student_id in self._registry:
            del self._registry[self.student_id]
