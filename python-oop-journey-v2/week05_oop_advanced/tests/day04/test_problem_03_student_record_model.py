"""Tests for Problem 03: Student Record Model."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day04.problem_03_student_record_model import (
    CourseGrade, Student
)


class TestCourseGrade:
    """Tests for CourseGrade dataclass."""
    
    def test_course_grade_creation(self) -> None:
        """Test creating a course grade."""
        grade = CourseGrade(course_code="CS101", credits=3, grade="A")
        
        assert grade.course_code == "CS101"
        assert grade.credits == 3
        assert grade.grade == "A"
    
    def test_grade_points_a(self) -> None:
        """Test grade points for A."""
        grade = CourseGrade(course_code="CS101", credits=3, grade="A")
        assert grade.grade_points() == 4.0
    
    def test_grade_points_a_plus(self) -> None:
        """Test grade points for A+."""
        grade = CourseGrade(course_code="CS101", credits=3, grade="A+")
        assert grade.grade_points() == 4.0
    
    def test_grade_points_a_minus(self) -> None:
        """Test grade points for A-."""
        grade = CourseGrade(course_code="CS101", credits=3, grade="A-")
        assert grade.grade_points() == 3.7
    
    def test_grade_points_b_plus(self) -> None:
        """Test grade points for B+."""
        grade = CourseGrade(course_code="CS101", credits=3, grade="B+")
        assert grade.grade_points() == 3.3
    
    def test_grade_points_b(self) -> None:
        """Test grade points for B."""
        grade = CourseGrade(course_code="CS101", credits=3, grade="B")
        assert grade.grade_points() == 3.0
    
    def test_grade_points_b_minus(self) -> None:
        """Test grade points for B-."""
        grade = CourseGrade(course_code="CS101", credits=3, grade="B-")
        assert grade.grade_points() == 2.7
    
    def test_grade_points_c_plus(self) -> None:
        """Test grade points for C+."""
        grade = CourseGrade(course_code="CS101", credits=3, grade="C+")
        assert grade.grade_points() == 2.3
    
    def test_grade_points_c(self) -> None:
        """Test grade points for C."""
        grade = CourseGrade(course_code="CS101", credits=3, grade="C")
        assert grade.grade_points() == 2.0
    
    def test_grade_points_c_minus(self) -> None:
        """Test grade points for C-."""
        grade = CourseGrade(course_code="CS101", credits=3, grade="C-")
        assert grade.grade_points() == 1.7
    
    def test_grade_points_d_plus(self) -> None:
        """Test grade points for D+."""
        grade = CourseGrade(course_code="CS101", credits=3, grade="D+")
        assert grade.grade_points() == 1.3
    
    def test_grade_points_d(self) -> None:
        """Test grade points for D."""
        grade = CourseGrade(course_code="CS101", credits=3, grade="D")
        assert grade.grade_points() == 1.0
    
    def test_grade_points_d_minus(self) -> None:
        """Test grade points for D-."""
        grade = CourseGrade(course_code="CS101", credits=3, grade="D-")
        assert grade.grade_points() == 0.7
    
    def test_grade_points_f(self) -> None:
        """Test grade points for F."""
        grade = CourseGrade(course_code="CS101", credits=3, grade="F")
        assert grade.grade_points() == 0.0


class TestStudentBasic:
    """Tests for basic Student functionality."""
    
    def test_student_creation(self) -> None:
        """Test creating a student."""
        student = Student(
            student_id="S001",
            name="Alice Smith",
            major="Computer Science"
        )
        
        assert student.student_id == "S001"
        assert student.name == "Alice Smith"
        assert student.major == "Computer Science"
        assert student.grades == []
    
    def test_student_defaults(self) -> None:
        """Test default values."""
        student = Student(student_id="S001", name="Bob")
        
        assert student.major == "Undeclared"
        assert student.grades == []
    
    def test_student_no_grades_gpa(self) -> None:
        """Test GPA calculation with no grades."""
        student = Student(student_id="S001", name="Charlie")
        
        assert student.gpa == 0.0
        assert student.total_credits == 0


class TestStudentGPA:
    """Tests for GPA calculation."""
    
    def test_gpa_single_course(self) -> None:
        """Test GPA with a single course."""
        grades = [CourseGrade("CS101", 3, "A")]  # 4.0 * 3 = 12 / 3 = 4.0
        student = Student("S001", "Alice", grades=grades)
        
        assert student.gpa == 4.0
        assert student.total_credits == 3
    
    def test_gpa_multiple_courses(self) -> None:
        """Test GPA with multiple courses."""
        grades = [
            CourseGrade("CS101", 3, "A"),    # 4.0 * 3 = 12
            CourseGrade("MATH201", 4, "B"),  # 3.0 * 4 = 12
            CourseGrade("ENG102", 3, "A-")   # 3.7 * 3 = 11.1
        ]
        # Total: 35.1 / 10 = 3.51
        student = Student("S001", "Alice", grades=grades)
        
        assert student.gpa == 3.51
        assert student.total_credits == 10
    
    def test_gpa_all_same_grade(self) -> None:
        """Test GPA when all grades are the same."""
        grades = [
            CourseGrade("CS101", 3, "B"),
            CourseGrade("CS102", 3, "B")
        ]
        student = Student("S001", "Alice", grades=grades)
        
        assert student.gpa == 3.0


class TestStudentStanding:
    """Tests for academic standing calculation."""
    
    def test_standing_deans_list(self) -> None:
        """Test Dean's List standing."""
        grades = [
            CourseGrade("CS101", 4, "A"),
            CourseGrade("CS102", 4, "A"),
            CourseGrade("CS103", 4, "A-")  # 12 credits, high GPA
        ]
        student = Student("S001", "Alice", grades=grades)
        
        assert student.academic_standing == "Dean's List"
    
    def test_standing_good(self) -> None:
        """Test Good Standing."""
        grades = [CourseGrade("CS101", 3, "B")]  # GPA 3.0
        student = Student("S001", "Alice", grades=grades)
        
        assert student.academic_standing == "Good Standing"
    
    def test_standing_probation(self) -> None:
        """Test Probation standing."""
        grades = [CourseGrade("CS101", 3, "D")]  # GPA 1.0
        student = Student("S001", "Alice", grades=grades)
        
        assert student.academic_standing == "Probation"
    
    def test_standing_not_deans_with_low_credits(self) -> None:
        """Test that Dean's List requires 12+ credits."""
        grades = [
            CourseGrade("CS101", 3, "A"),
            CourseGrade("CS102", 3, "A")  # Only 6 credits, but GPA 4.0
        ]
        student = Student("S001", "Alice", grades=grades)
        
        assert student.gpa == 4.0
        assert student.academic_standing == "Good Standing"  # Not Dean's List


class TestStudentAddGrade:
    """Tests for adding grades."""
    
    def test_add_grade_updates_gpa(self) -> None:
        """Test that adding a grade recalculates GPA."""
        student = Student("S001", "Alice", grades=[CourseGrade("CS101", 3, "A")])
        initial_gpa = student.gpa
        
        student.add_grade(CourseGrade("CS102", 3, "C"))
        
        assert student.gpa != initial_gpa
        assert len(student.grades) == 2
    
    def test_add_grade_updates_credits(self) -> None:
        """Test that adding a grade updates total credits."""
        student = Student("S001", "Alice", grades=[CourseGrade("CS101", 3, "A")])
        
        student.add_grade(CourseGrade("CS102", 4, "B"))
        
        assert student.total_credits == 7
    
    def test_add_grade_updates_standing(self) -> None:
        """Test that adding a grade can change standing."""
        # Start with good grades but low credits
        student = Student("S001", "Alice", grades=[CourseGrade("CS101", 3, "A")])
        assert student.academic_standing == "Good Standing"
        
        # Add more credits with good grades
        student.add_grade(CourseGrade("CS102", 4, "A"))
        student.add_grade(CourseGrade("CS103", 4, "A"))
        student.add_grade(CourseGrade("CS104", 3, "A"))
        
        assert student.academic_standing == "Dean's List"


class TestStudentTranscript:
    """Tests for transcript generation."""
    
    def test_transcript_contains_student_info(self) -> None:
        """Test that transcript includes student information."""
        student = Student("S001", "Alice Smith", "CS")
        transcript = student.transcript()
        
        assert "Alice Smith" in transcript
        assert "S001" in transcript
        assert "CS" in transcript
    
    def test_transcript_contains_grades(self) -> None:
        """Test that transcript includes grades."""
        student = Student(
            "S001",
            "Alice",
            grades=[CourseGrade("CS101", 3, "A")]
        )
        transcript = student.transcript()
        
        assert "CS101" in transcript
        assert "A" in transcript
        assert "3 cr" in transcript or "cr" in transcript


class TestStudentHonors:
    """Tests for honors eligibility."""
    
    def test_honors_eligible(self) -> None:
        """Test eligibility for honors."""
        # Need 60+ credits and 3.5+ GPA
        grades = [
            CourseGrade(f"CS{i:03d}", 4, "A") for i in range(15)
        ]  # 60 credits, 4.0 GPA
        student = Student("S001", "Alice", grades=grades)
        
        assert student.honors_eligible() is True
    
    def test_honors_not_eligible_low_gpa(self) -> None:
        """Test not eligible due to low GPA."""
        grades = [
            CourseGrade(f"CS{i:03d}", 4, "B") for i in range(15)
        ]  # 60 credits, 3.0 GPA
        student = Student("S001", "Alice", grades=grades)
        
        assert student.honors_eligible() is False
    
    def test_honors_not_eligible_low_credits(self) -> None:
        """Test not eligible due to low credits."""
        grades = [CourseGrade("CS101", 3, "A")]  # Only 3 credits
        student = Student("S001", "Alice", grades=grades)
        
        assert student.honors_eligible() is False
