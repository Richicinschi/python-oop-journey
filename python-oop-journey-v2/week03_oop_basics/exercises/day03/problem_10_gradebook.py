"""Exercise: Gradebook.

Implement a Student class with private grades and calculated GPA.

TODO:
1. Implement add_grade method to store grades privately
2. Implement read-only properties: num_courses, courses, average, gpa
3. Implement highest_grade and lowest_grade read-only properties
4. Implement helper methods: get_grade, remove_grade, get_letter_grade

Hints:
    - Hint 1: Store grades in a private dict: self._grades = {} mapping course -> grade
    - Hint 2: highest_grade uses max() with key=lambda item: item[1] on dict items
    - Hint 3: GPA conversion: A=4.0, B=3.0, C=2.0, D=1.0, F=0.0; average the points
"""

from __future__ import annotations

from typing import Optional


class Student:
    """A student with private grades and calculated GPA.
    
    Attributes:
        student_id: The unique student identifier (read-only).
        name: The student's name.
    """
    
    def __init__(self, student_id: str, name: str) -> None:
        """Initialize a student."""
        self._student_id = student_id.strip()
        self._name = name.strip()
        # TODO: Create private dict to store grades: course -> numeric grade
        raise NotImplementedError("Initialize grades storage")
    
    @property
    def student_id(self) -> str:
        """Get the student ID."""
        return self._student_id
    
    @property
    def name(self) -> str:
        """Get the student's name."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the student's name."""
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @property
    def num_courses(self) -> int:
        """Get the number of courses (read-only)."""
        # TODO: Return number of courses with grades
        raise NotImplementedError("Return course count")
    
    @property
    def courses(self) -> list[str]:
        """Get list of courses (read-only)."""
        # TODO: Return list of course names
        raise NotImplementedError("Return courses")
    
    @property
    def average(self) -> Optional[float]:
        """Calculate the average numeric grade (read-only)."""
        # TODO: Return None if no grades
        # TODO: Calculate and return average of all grades
        raise NotImplementedError("Calculate average")
    
    @property
    def gpa(self) -> Optional[float]:
        """Calculate the Grade Point Average (read-only).
        
        Use 4.0 scale:
        A (90-100) = 4.0, B (80-89) = 3.0, C (70-79) = 2.0,
        D (60-69) = 1.0, F (<60) = 0.0
        """
        # TODO: Return None if no grades
        # TODO: Convert each grade to GPA points and average
        raise NotImplementedError("Calculate GPA")
    
    @property
    def highest_grade(self) -> Optional[tuple[str, float]]:
        """Get the highest grade (read-only).
        
        Returns:
            Tuple of (course, grade) or None if no grades.
        """
        # TODO: Return None if no grades
        # TODO: Find and return course with highest grade
        raise NotImplementedError("Find highest grade")
    
    @property
    def lowest_grade(self) -> Optional[tuple[str, float]]:
        """Get the lowest grade (read-only).
        
        Returns:
            Tuple of (course, grade) or None if no grades.
        """
        # TODO: Return None if no grades
        # TODO: Find and return course with lowest grade
        raise NotImplementedError("Find lowest grade")
    
    def add_grade(self, course: str, grade: float) -> None:
        """Add or update a grade for a course."""
        # TODO: Validate grade is between 0 and 100
        # TODO: Store grade in the private dict
        raise NotImplementedError("Add grade")
    
    def get_grade(self, course: str) -> Optional[float]:
        """Get the grade for a specific course."""
        # TODO: Return grade for course or None if not found
        raise NotImplementedError("Get grade")
    
    def remove_grade(self, course: str) -> bool:
        """Remove a grade for a course.
        
        Returns:
            True if grade was removed, False if course didn't exist.
        """
        # TODO: Remove grade if it exists
        # TODO: Return True if removed, False otherwise
        raise NotImplementedError("Remove grade")
    
    def get_letter_grade(self, course: str) -> Optional[str]:
        """Get the letter grade for a course."""
        # TODO: Get numeric grade for course
        # TODO: Convert to letter: A(90+), B(80+), C(70+), D(60+), F(<60)
        raise NotImplementedError("Get letter grade")
