"""Solution for Problem 10: Gradebook.

Demonstrates private grades with calculated GPA using properties.
"""

from __future__ import annotations

from typing import Optional


class Student:
    """A student with private grades and calculated GPA.
    
    This class demonstrates encapsulation of sensitive data (grades)
    with computed statistics accessible through properties.
    
    Attributes:
        student_id: The unique student identifier (read-only).
        name: The student's name.
    
    Example:
        >>> student = Student("S001", "Alice")
        >>> student.add_grade("Math", 90)
        >>> student.add_grade("Science", 85)
        >>> student.gpa
        3.75
    """
    
    # Grade point mapping
    GRADE_POINTS = {
        'A+': 4.0, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'D-': 0.7,
        'F': 0.0,
    }
    
    def __init__(self, student_id: str, name: str) -> None:
        """Initialize a student.
        
        Args:
            student_id: The unique student identifier.
            name: The student's name.
        
        Raises:
            TypeError: If types are incorrect.
            ValueError: If student_id or name is empty.
        """
        if not isinstance(student_id, str):
            raise TypeError("Student ID must be a string")
        if not student_id.strip():
            raise ValueError("Student ID cannot be empty")
        self._student_id = student_id.strip()
        
        self.name = name  # Use setter
        self.__grades: dict[str, float] = {}  # Private: course -> numeric grade
    
    @property
    def student_id(self) -> str:
        """Get the student ID.
        
        Returns:
            The unique student identifier.
        """
        return self._student_id
    
    @property
    def name(self) -> str:
        """Get the student's name.
        
        Returns:
            The student's name.
        """
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the student's name.
        
        Args:
            value: The new name.
        
        Raises:
            TypeError: If value is not a string.
            ValueError: If name is empty.
        """
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @property
    def num_courses(self) -> int:
        """Get the number of courses (read-only).
        
        Returns:
            The number of courses with grades.
        """
        return len(self.__grades)
    
    @property
    def courses(self) -> list[str]:
        """Get list of courses (read-only).
        
        Returns:
            A list of course names.
        """
        return list(self.__grades.keys())
    
    @property
    def average(self) -> Optional[float]:
        """Calculate the average numeric grade (read-only).
        
        Returns:
            The average grade as a percentage, or None if no grades.
        """
        if not self.__grades:
            return None
        return sum(self.__grades.values()) / len(self.__grades)
    
    @property
    def gpa(self) -> Optional[float]:
        """Calculate the Grade Point Average (read-only).
        
        Returns:
            The GPA on a 4.0 scale, or None if no grades.
        """
        if not self.__grades:
            return None
        
        total_points = 0.0
        for grade in self.__grades.values():
            total_points += self._numeric_to_gpa(grade)
        
        return total_points / len(self.__grades)
    
    @property
    def highest_grade(self) -> Optional[tuple[str, float]]:
        """Get the highest grade (read-only).
        
        Returns:
            Tuple of (course, grade) for the highest grade,
            or None if no grades.
        """
        if not self.__grades:
            return None
        course = max(self.__grades, key=self.__grades.get)
        return (course, self.__grades[course])
    
    @property
    def lowest_grade(self) -> Optional[tuple[str, float]]:
        """Get the lowest grade (read-only).
        
        Returns:
            Tuple of (course, grade) for the lowest grade,
            or None if no grades.
        """
        if not self.__grades:
            return None
        course = min(self.__grades, key=self.__grades.get)
        return (course, self.__grades[course])
    
    def add_grade(self, course: str, grade: float) -> None:
        """Add or update a grade for a course.
        
        Args:
            course: The course name.
            grade: The numeric grade (0-100).
        
        Raises:
            TypeError: If types are incorrect.
            ValueError: If grade is outside 0-100 range.
        """
        if not isinstance(course, str):
            raise TypeError("Course must be a string")
        if not isinstance(grade, (int, float)):
            raise TypeError("Grade must be a number")
        if grade < 0 or grade > 100:
            raise ValueError("Grade must be between 0 and 100")
        self.__grades[course.strip()] = float(grade)
    
    def get_grade(self, course: str) -> Optional[float]:
        """Get the grade for a specific course.
        
        Args:
            course: The course name.
        
        Returns:
            The grade for the course, or None if not found.
        """
        return self.__grades.get(course.strip())
    
    def remove_grade(self, course: str) -> bool:
        """Remove a grade for a course.
        
        Args:
            course: The course name.
        
        Returns:
            True if grade was removed, False if course didn't exist.
        """
        course = course.strip()
        if course in self.__grades:
            del self.__grades[course]
            return True
        return False
    
    def _numeric_to_gpa(self, numeric_grade: float) -> float:
        """Convert a numeric grade to GPA points.
        
        Args:
            numeric_grade: Grade as percentage (0-100).
        
        Returns:
            GPA points on a 4.0 scale.
        """
        if numeric_grade >= 93:
            return 4.0
        elif numeric_grade >= 90:
            return 3.7
        elif numeric_grade >= 87:
            return 3.3
        elif numeric_grade >= 83:
            return 3.0
        elif numeric_grade >= 80:
            return 2.7
        elif numeric_grade >= 77:
            return 2.3
        elif numeric_grade >= 73:
            return 2.0
        elif numeric_grade >= 70:
            return 1.7
        elif numeric_grade >= 67:
            return 1.3
        elif numeric_grade >= 65:
            return 1.0
        else:
            return 0.0
    
    def get_letter_grade(self, course: str) -> Optional[str]:
        """Get the letter grade for a course.
        
        Args:
            course: The course name.
        
        Returns:
            The letter grade (A, B, C, etc.), or None if course not found.
        """
        numeric = self.get_grade(course)
        if numeric is None:
            return None
        
        if numeric >= 93:
            return "A"
        elif numeric >= 90:
            return "A-"
        elif numeric >= 87:
            return "B+"
        elif numeric >= 83:
            return "B"
        elif numeric >= 80:
            return "B-"
        elif numeric >= 77:
            return "C+"
        elif numeric >= 73:
            return "C"
        elif numeric >= 70:
            return "C-"
        elif numeric >= 67:
            return "D+"
        elif numeric >= 65:
            return "D"
        else:
            return "F"
