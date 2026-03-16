"""Tests for Problem 07: Student and Graduate Student."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day01.problem_07_student_and_graduate_student import (
    Student, GraduateStudent
)


class TestStudent:
    """Tests for the base Student class."""
    
    def test_student_init(self) -> None:
        student = Student("S001", "John Doe", "john@example.com", "Computer Science")
        assert student.student_id == "S001"
        assert student.name == "John Doe"
        assert student.email == "john@example.com"
        assert student.major == "Computer Science"
    
    def test_student_enroll(self) -> None:
        student = Student("S001", "John Doe", "john@example.com", "CS")
        result = student.enroll("CS101")
        assert result is True
    
    def test_student_enroll_duplicate(self) -> None:
        student = Student("S001", "John Doe", "john@example.com", "CS")
        student.enroll("CS101")
        result = student.enroll("CS101")
        assert result is False
    
    def test_student_drop_course(self) -> None:
        student = Student("S001", "John Doe", "john@example.com", "CS")
        student.enroll("CS101")
        result = student.drop_course("CS101")
        assert result is True
    
    def test_student_drop_not_enrolled(self) -> None:
        student = Student("S001", "John Doe", "john@example.com", "CS")
        result = student.drop_course("CS101")
        assert result is False
    
    def test_student_complete_course(self) -> None:
        student = Student("S001", "John Doe", "john@example.com", "CS")
        student.enroll("CS101")
        result = student.complete_course("CS101", 3.5)
        assert result is True
        assert student.calculate_gpa() == 3.5
    
    def test_student_complete_not_enrolled(self) -> None:
        student = Student("S001", "John Doe", "john@example.com", "CS")
        result = student.complete_course("CS101", 3.5)
        assert result is False
    
    def test_student_calculate_gpa(self) -> None:
        student = Student("S001", "John Doe", "john@example.com", "CS")
        student.enroll("CS101")
        student.enroll("CS102")
        student.complete_course("CS101", 4.0)
        student.complete_course("CS102", 3.0)
        assert student.calculate_gpa() == 3.5
    
    def test_student_calculate_gpa_empty(self) -> None:
        student = Student("S001", "John Doe", "john@example.com", "CS")
        assert student.calculate_gpa() == 0.0
    
    def test_student_academic_status_honors(self) -> None:
        student = Student("S001", "John Doe", "john@example.com", "CS")
        student.enroll("CS101")
        student.complete_course("CS101", 3.5)
        assert student.get_academic_status() == "Honors"
    
    def test_student_academic_status_good_standing(self) -> None:
        student = Student("S001", "John Doe", "john@example.com", "CS")
        student.enroll("CS101")
        student.complete_course("CS101", 3.0)
        assert student.get_academic_status() == "Good Standing"
    
    def test_student_academic_status_probation(self) -> None:
        student = Student("S001", "John Doe", "john@example.com", "CS")
        student.enroll("CS101")
        student.complete_course("CS101", 1.5)
        assert student.get_academic_status() == "Probation"
    
    def test_student_get_info(self) -> None:
        student = Student("S001", "John Doe", "john@example.com", "CS")
        info = student.get_student_info()
        assert "S001" in info
        assert "John Doe" in info
        assert "CS" in info
    
    def test_student_credits_completed(self) -> None:
        student = Student("S001", "John Doe", "john@example.com", "CS")
        student.enroll("CS101")
        student.enroll("CS102")
        student.complete_course("CS101", 3.5)
        student.complete_course("CS102", 4.0)
        assert student.get_credits_completed() == 6  # 2 courses * 3 credits


class TestGraduateStudent:
    """Tests for the GraduateStudent class."""
    
    def test_grad_student_inheritance(self) -> None:
        grad = GraduateStudent("G001", "Jane Smith", "jane@example.com", "PhD CS", "Dr. Advisor")
        assert isinstance(grad, Student)
    
    def test_grad_student_init(self) -> None:
        grad = GraduateStudent("G001", "Jane Smith", "jane@example.com", "PhD CS", "Dr. Advisor", True, 2500.0)
        assert grad.student_id == "G001"
        assert grad.advisor == "Dr. Advisor"
        assert grad.is_ta is True
        assert grad.stipend == 2500.0
    
    def test_grad_student_init_defaults(self) -> None:
        grad = GraduateStudent("G001", "Jane Smith", "jane@example.com", "PhD CS", "Dr. Advisor")
        assert grad.is_ta is False
        assert grad.stipend == 2000.0
    
    def test_grad_student_get_info(self) -> None:
        grad = GraduateStudent("G001", "Jane Smith", "jane@example.com", "PhD CS", "Dr. Advisor")
        info = grad.get_student_info()
        assert "Dr. Advisor" in info
        assert "not_started" in info
    
    def test_grad_student_set_thesis_title(self) -> None:
        grad = GraduateStudent("G001", "Jane Smith", "jane@example.com", "PhD CS", "Dr. Advisor")
        grad.set_thesis_title("Machine Learning Applications")
        assert grad.thesis_title == "Machine Learning Applications"
        assert grad.thesis_status == "in_progress"
    
    def test_grad_student_update_thesis_status_valid(self) -> None:
        grad = GraduateStudent("G001", "Jane Smith", "jane@example.com", "PhD CS", "Dr. Advisor")
        grad.set_thesis_title("ML Applications")
        assert grad.update_thesis_status("defended") is True
        assert grad.thesis_status == "defended"
        assert grad.update_thesis_status("approved") is True
        assert grad.thesis_status == "approved"
    
    def test_grad_student_update_thesis_status_invalid(self) -> None:
        grad = GraduateStudent("G001", "Jane Smith", "jane@example.com", "PhD CS", "Dr. Advisor")
        assert grad.update_thesis_status("approved") is False  # Can't jump to approved
    
    def test_grad_student_add_publication(self) -> None:
        grad = GraduateStudent("G001", "Jane Smith", "jane@example.com", "PhD CS", "Dr. Advisor")
        grad.add_publication("Deep Learning", "Nature", 2023)
        assert grad.get_publication_count() == 1
    
    def test_grad_student_can_graduate_true(self) -> None:
        grad = GraduateStudent("G001", "Jane Smith", "jane@example.com", "PhD CS", "Dr. Advisor")
        grad.set_thesis_title("ML Applications")
        # Complete 10 courses with good grades
        for i in range(10):
            grad.enroll(f"CS{i}")
            grad.complete_course(f"CS{i}", 3.5)
        grad.update_thesis_status("defended")
        grad.update_thesis_status("approved")
        assert grad.can_graduate() is True
    
    def test_grad_student_can_graduate_insufficient_courses(self) -> None:
        grad = GraduateStudent("G001", "Jane Smith", "jane@example.com", "PhD CS", "Dr. Advisor")
        grad.set_thesis_title("ML Applications")
        grad.update_thesis_status("defended")
        grad.update_thesis_status("approved")
        # Only 5 courses
        for i in range(5):
            grad.enroll(f"CS{i}")
            grad.complete_course(f"CS{i}", 3.5)
        assert grad.can_graduate() is False
    
    def test_grad_student_can_graduate_low_gpa(self) -> None:
        grad = GraduateStudent("G001", "Jane Smith", "jane@example.com", "PhD CS", "Dr. Advisor")
        grad.set_thesis_title("ML Applications")
        grad.update_thesis_status("defended")
        grad.update_thesis_status("approved")
        for i in range(10):
            grad.enroll(f"CS{i}")
            grad.complete_course(f"CS{i}", 2.5)  # Below 3.0
        assert grad.can_graduate() is False
    
    def test_grad_student_can_graduate_thesis_not_approved(self) -> None:
        grad = GraduateStudent("G001", "Jane Smith", "jane@example.com", "PhD CS", "Dr. Advisor")
        grad.set_thesis_title("ML Applications")
        for i in range(10):
            grad.enroll(f"CS{i}")
            grad.complete_course(f"CS{i}", 3.5)
        grad.update_thesis_status("defended")  # Not yet approved
        assert grad.can_graduate() is False
    
    def test_grad_student_toggle_ta(self) -> None:
        grad = GraduateStudent("G001", "Jane Smith", "jane@example.com", "PhD CS", "Dr. Advisor", False)
        result = grad.toggle_ta_status()
        assert result is True
        assert grad.is_ta is True
        result = grad.toggle_ta_status()
        assert result is False
        assert grad.is_ta is False


class TestPolymorphism:
    """Tests demonstrating polymorphic behavior."""
    
    def test_polymorphic_student_info(self) -> None:
        students: list[Student] = [
            Student("S001", "John", "john@example.com", "CS"),
            GraduateStudent("G001", "Jane", "jane@example.com", "PhD CS", "Dr. Advisor")
        ]
        
        infos = [s.get_student_info() for s in students]
        assert "S001" in infos[0]
        assert "G001" in infos[1]
        assert "Advisor" in infos[1]
    
    def test_polymorphic_gpa_calculation(self) -> None:
        students: list[Student] = [
            Student("S001", "John", "john@example.com", "CS"),
            GraduateStudent("G001", "Jane", "jane@example.com", "PhD CS", "Dr. Advisor")
        ]
        
        # Both can calculate GPA (base behavior)
        for student in students:
            student.enroll("CS101")
            student.complete_course("CS101", 3.5)
            assert student.calculate_gpa() == 3.5
