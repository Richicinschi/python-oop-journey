"""Problem 03: Student Record Model

Topic: Dataclasses with computed fields and post-init
Difficulty: Medium

Create a Student dataclass that automatically calculates GPA and academic
standing based on grades provided at initialization.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class CourseGrade:
    """A grade for a specific course.
    
    Attributes:
        course_code: Course identifier (e.g., "CS101")
        credits: Number of credit hours
        grade: Letter grade (A, B, C, D, F)
    """
    
    course_code: str
    credits: int
    grade: Literal["A", "B", "C", "D", "F", "A+", "B+", "C+", "D+", "A-", "B-", "C-", "D-"]
    
    def grade_points(self) -> float:
        """Convert letter grade to grade points.
        
        A/A+ = 4.0, A- = 3.7
        B+ = 3.3, B = 3.0, B- = 2.7
        C+ = 2.3, C = 2.0, C- = 1.7
        D+ = 1.3, D = 1.0, D- = 0.7
        F = 0.0
        
        Returns:
            Grade points for this course
        """
        raise NotImplementedError("Implement CourseGrade.grade_points")


@dataclass
class Student:
    """Student record with automatic GPA calculation.
    
    Attributes:
        student_id: Unique student identifier
        name: Student full name
        major: Field of study (default: "Undeclared")
        grades: List of course grades
    
    Computed Fields (set in __post_init__):
        gpa: Grade point average (0.0 - 4.0)
        total_credits: Total credit hours attempted
        academic_standing: "Good Standing", "Probation", or "Dean's List"
    """
    
    student_id: str
    name: str
    major: str = "Undeclared"
    grades: list[CourseGrade] = field(default_factory=list)
    
    # Computed fields - initialized in __post_init__
    gpa: float = field(init=False)
    total_credits: int = field(init=False)
    academic_standing: str = field(init=False)
    
    def __post_init__(self) -> None:
        """Calculate GPA, credits, and standing after initialization."""
        raise NotImplementedError("Implement Student.__post_init__")
    
    def _calculate_gpa(self) -> float:
        """Calculate GPA from grades.
        
        Returns:
            Weighted average of grade points, or 0.0 if no grades
        """
        raise NotImplementedError("Implement Student._calculate_gpa")
    
    def _calculate_standing(self) -> str:
        """Determine academic standing based on GPA.
        
        Dean's List: GPA >= 3.5 and at least 12 credits
        Good Standing: GPA >= 2.0
        Probation: GPA < 2.0
        
        Returns:
            Academic standing status
        """
        raise NotImplementedError("Implement Student._calculate_standing")
    
    def add_grade(self, grade: CourseGrade) -> None:
        """Add a new grade and recalculate statistics.
        
        Args:
            grade: New course grade to add
        """
        raise NotImplementedError("Implement Student.add_grade")
    
    def transcript(self) -> str:
        """Generate a formatted transcript.
        
        Returns:
            Multi-line string with student info and grades
        """
        raise NotImplementedError("Implement Student.transcript")
    
    def honors_eligible(self) -> bool:
        """Check if student is eligible for honors.
        
        Returns:
            True if GPA >= 3.5 and total_credits >= 60
        """
        raise NotImplementedError("Implement Student.honors_eligible")
