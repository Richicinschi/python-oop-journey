"""Problem 04: Student

Topic: Collections as attributes, aggregations
Difficulty: Medium

Create a Student class that manages courses and grades.

Examples:
    >>> student = Student("Alice", "S001")
    >>> student.add_course("Math", 90)
    >>> student.add_course("Science", 85)
    >>> student.get_courses()
    ['Math', 'Science']
    >>> student.get_grade("Math")
    90
    >>> student.average_grade()
    87.5
    >>> student.get_grade("History")  # Not enrolled
    >>> student.add_course("Math", 95)  # Update grade
    >>> student.get_grade("Math")
    95

Requirements:
    - __init__ takes name (str) and student_id (str)
    - add_course(course_name, grade) adds or updates a course grade
    - get_courses() returns list of course names
    - get_grade(course_name) returns grade or None if not found
    - average_grade() returns the average of all grades
    - Grades should be integers between 0 and 100
"""

from __future__ import annotations


class Student:
    """A class representing a student with courses and grades."""

    def __init__(self, name: str, student_id: str) -> None:
        """Initialize a student with name and ID."""
        raise NotImplementedError("Initialize name, student_id, and grades storage")

    def add_course(self, course_name: str, grade: int) -> None:
        """Add or update a course grade.
        
        Args:
            course_name: Name of the course
            grade: Grade for the course (0-100)
        """
        raise NotImplementedError("Implement add_course method")

    def get_courses(self) -> list[str]:
        """Return a list of all course names."""
        raise NotImplementedError("Implement get_courses method")

    def get_grade(self, course_name: str) -> int | None:
        """Return the grade for a specific course, or None if not found."""
        raise NotImplementedError("Implement get_grade method")

    def average_grade(self) -> float | None:
        """Return the average grade across all courses, or None if no courses."""
        raise NotImplementedError("Implement average_grade method")

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        raise NotImplementedError("Implement __str__ method")

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        raise NotImplementedError("Implement __repr__ method")
