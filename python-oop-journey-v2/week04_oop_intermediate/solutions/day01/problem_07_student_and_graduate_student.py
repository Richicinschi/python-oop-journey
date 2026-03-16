"""Reference solution for Problem 07: Student and Graduate Student."""

from __future__ import annotations


class Student:
    """Base class for all students."""
    
    def __init__(self, student_id: str, name: str, email: str, major: str) -> None:
        self.student_id = student_id
        self.name = name
        self.email = email
        self.major = major
        self._enrolled_courses: list[str] = []
        self._completed_courses: dict[str, float] = {}
    
    def enroll(self, course: str) -> bool:
        if course in self._enrolled_courses:
            return False
        self._enrolled_courses.append(course)
        return True
    
    def drop_course(self, course: str) -> bool:
        if course in self._enrolled_courses:
            self._enrolled_courses.remove(course)
            return True
        return False
    
    def complete_course(self, course: str, grade: float) -> bool:
        if course not in self._enrolled_courses:
            return False
        self._enrolled_courses.remove(course)
        self._completed_courses[course] = grade
        return True
    
    def calculate_gpa(self) -> float:
        if not self._completed_courses:
            return 0.0
        return sum(self._completed_courses.values()) / len(self._completed_courses)
    
    def get_academic_status(self) -> str:
        gpa = self.calculate_gpa()
        if gpa >= 3.5:
            return "Honors"
        if gpa >= 2.0:
            return "Good Standing"
        return "Probation"
    
    def get_student_info(self) -> str:
        gpa = self.calculate_gpa()
        return (f"Student ID: {self.student_id}\n"
                f"Name: {self.name}\n"
                f"Email: {self.email}\n"
                f"Major: {self.major}\n"
                f"GPA: {gpa:.2f}")
    
    def get_credits_completed(self) -> int:
        return len(self._completed_courses) * 3


class GraduateStudent(Student):
    """A graduate student with thesis requirements."""
    
    def __init__(self, student_id: str, name: str, email: str, major: str,
                 advisor: str, is_ta: bool = False, stipend: float = 2000.0) -> None:
        super().__init__(student_id, name, email, major)
        self.advisor = advisor
        self.is_ta = is_ta
        self.stipend = stipend
        self.thesis_title: str | None = None
        self.thesis_status = "not_started"
        self._publications: list[dict] = []
    
    def get_student_info(self) -> str:
        base = super().get_student_info()
        thesis = self.thesis_title if self.thesis_title else "Not set"
        return (f"{base}\n"
                f"Advisor: {self.advisor}\n"
                f"Thesis: {thesis}\n"
                f"Status: {self.thesis_status}")
    
    def set_thesis_title(self, title: str) -> None:
        self.thesis_title = title
        if self.thesis_status == "not_started":
            self.thesis_status = "in_progress"
    
    def update_thesis_status(self, status: str) -> bool:
        valid_transitions = {
            "not_started": ["in_progress"],
            "in_progress": ["defended"],
            "defended": ["approved"],
            "approved": []
        }
        if status in valid_transitions.get(self.thesis_status, []):
            self.thesis_status = status
            return True
        return False
    
    def add_publication(self, title: str, journal: str, year: int) -> None:
        self._publications.append({"title": title, "journal": journal, "year": year})
    
    def get_publication_count(self) -> int:
        return len(self._publications)
    
    def can_graduate(self) -> bool:
        return (len(self._completed_courses) >= 10 and
                self.calculate_gpa() >= 3.0 and
                self.thesis_status == "approved")
    
    def toggle_ta_status(self) -> bool:
        self.is_ta = not self.is_ta
        return self.is_ta
