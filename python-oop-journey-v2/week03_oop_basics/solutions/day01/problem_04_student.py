"""Reference solution for Problem 04: Student."""

from __future__ import annotations


class Student:
    """A class representing a student with courses and grades."""

    def __init__(self, name: str, student_id: str) -> None:
        """Initialize a student with name and ID.
        
        Args:
            name: The student's name
            student_id: The student's unique identifier
        """
        self.name = name
        self.student_id = student_id
        self._grades: dict[str, int] = {}

    def add_course(self, course_name: str, grade: int) -> None:
        """Add or update a course grade.
        
        Args:
            course_name: Name of the course
            grade: Grade for the course (0-100)
        """
        self._grades[course_name] = grade

    def get_courses(self) -> list[str]:
        """Return a list of all course names."""
        return list(self._grades.keys())

    def get_grade(self, course_name: str) -> int | None:
        """Return the grade for a specific course, or None if not found."""
        return self._grades.get(course_name)

    def average_grade(self) -> float | None:
        """Return the average grade across all courses, or None if no courses."""
        if not self._grades:
            return None
        return sum(self._grades.values()) / len(self._grades)

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        avg = self.average_grade()
        avg_str = f"{avg:.1f}" if avg is not None else "N/A"
        return f"Student({self.name}, ID={self.student_id}, avg={avg_str})"

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"Student(name='{self.name}', student_id='{self.student_id}')"
