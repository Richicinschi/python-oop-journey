"""Problem 07: Student and Graduate Student

Topic: Academic Hierarchy with Extended Functionality
Difficulty: Medium

Create a Student base class with a GraduateStudent subclass,
demonstrating academic progression with thesis handling.
"""

from __future__ import annotations


class Student:
    """Base class for all students.
    
    Attributes:
        student_id: Unique student identifier
        name: Student's full name
        email: Student email address
        major: Field of study
        gpa: Current GPA (0.0 - 4.0)
        enrolled_courses: List of currently enrolled courses
        completed_courses: List of completed courses with grades
    """
    
    def __init__(self, student_id: str, name: str, email: str, major: str) -> None:
        """Initialize a Student.
        
        Args:
            student_id: Unique identifier
            name: Full name
            email: Email address
            major: Field of study
        """
        raise NotImplementedError("Implement Student.__init__")
    
    def enroll(self, course: str) -> bool:
        """Enroll in a course.
        
        Args:
            course: Course name to enroll in
            
        Returns:
            True if successfully enrolled
            False if already enrolled
        """
        raise NotImplementedError("Implement Student.enroll")
    
    def drop_course(self, course: str) -> bool:
        """Drop an enrolled course.
        
        Args:
            course: Course name to drop
            
        Returns:
            True if successfully dropped
            False if not enrolled
        """
        raise NotImplementedError("Implement Student.drop_course")
    
    def complete_course(self, course: str, grade: float) -> bool:
        """Mark a course as completed with grade.
        
        Args:
            course: Course name
            grade: Grade received (0.0 - 4.0)
            
        Returns:
            True if course was enrolled and is now completed
        """
        raise NotImplementedError("Implement Student.complete_course")
    
    def calculate_gpa(self) -> float:
        """Calculate current GPA from completed courses.
        
        Returns:
            Current GPA (0.0 if no completed courses)
        """
        raise NotImplementedError("Implement Student.calculate_gpa")
    
    def get_academic_status(self) -> str:
        """Return academic status based on GPA.
        
        Returns:
            "Good Standing" if GPA >= 2.0
            "Probation" if GPA < 2.0
            "Honors" if GPA >= 3.5
        """
        raise NotImplementedError("Implement Student.get_academic_status")
    
    def get_student_info(self) -> str:
        """Return formatted student information.
        
        Returns:
            Multi-line string with student details
        """
        raise NotImplementedError("Implement Student.get_student_info")
    
    def get_credits_completed(self) -> int:
        """Return number of completed courses.
        
        Returns:
            Count of completed courses (3 credits each)
        """
        raise NotImplementedError("Implement Student.get_credits_completed")


class GraduateStudent(Student):
    """A graduate student with thesis requirements.
    
    Additional Attributes:
        advisor: Faculty advisor name
        thesis_title: Title of thesis/dissertation
        thesis_status: "not_started", "in_progress", "defended", "approved"
        publications: List of published papers
        is_ta: Whether student is a teaching assistant
        stipend: Monthly stipend amount
    """
    
    def __init__(self, student_id: str, name: str, email: str, major: str,
                 advisor: str, is_ta: bool = False, stipend: float = 2000.0) -> None:
        """Initialize a GraduateStudent.
        
        Args:
            student_id: Unique identifier
            name: Full name
            email: Email address
            major: Field of study (graduate level)
            advisor: Faculty advisor name
            is_ta: Whether TA (default False)
            stipend: Monthly stipend (default 2000.0)
        """
        raise NotImplementedError("Implement GraduateStudent.__init__")
    
    def get_student_info(self) -> str:
        """Override: Include graduate-specific info.
        
        Returns:
            Base info + "Advisor: X, Thesis: Y, Status: Z"
        """
        raise NotImplementedError("Implement GraduateStudent.get_student_info")
    
    def set_thesis_title(self, title: str) -> None:
        """GraduateStudent-specific: Set thesis title.
        
        Also sets thesis_status to "not_started" if it was empty.
        
        Args:
            title: Thesis title
        """
        raise NotImplementedError("Implement GraduateStudent.set_thesis_title")
    
    def update_thesis_status(self, status: str) -> bool:
        """GraduateStudent-specific: Update thesis status.
        
        Valid transitions:
        - not_started -> in_progress
        - in_progress -> defended
        - defended -> approved
        
        Args:
            status: New status
            
        Returns:
            True if transition is valid
            False if invalid transition
        """
        raise NotImplementedError("Implement GraduateStudent.update_thesis_status")
    
    def add_publication(self, title: str, journal: str, year: int) -> None:
        """GraduateStudent-specific: Add a publication.
        
        Args:
            title: Paper title
            journal: Journal name
            year: Publication year
        """
        raise NotImplementedError("Implement GraduateStudent.add_publication")
    
    def get_publication_count(self) -> int:
        """Return number of publications.
        
        Returns:
            Count of publications
        """
        raise NotImplementedError("Implement GraduateStudent.get_publication_count")
    
    def can_graduate(self) -> bool:
        """Check if student can graduate.
        
        Requirements:
        - At least 10 courses completed (30 credits)
        - GPA >= 3.0
        - Thesis status is "approved"
        
        Returns:
            True if all requirements met
        """
        raise NotImplementedError("Implement GraduateStudent.can_graduate")
    
    def toggle_ta_status(self) -> bool:
        """Toggle teaching assistant status.
        
        Returns:
            New TA status
        """
        raise NotImplementedError("Implement GraduateStudent.toggle_ta_status")
