"""Tests for Problem 06: School Classroom."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day05.problem_06_school_classroom import (
    Student,
    Teacher,
    Classroom,
    School,
)


class TestStudent:
    """Tests for Student class."""
    
    def test_student_init(self) -> None:
        """Test student initialization."""
        student = Student("Alice", "STU001", 10)
        assert student.name == "Alice"
        assert student.student_id == "STU001"
        assert student.grade_level == 10


class TestTeacher:
    """Tests for Teacher class."""
    
    def test_teacher_init(self) -> None:
        """Test teacher initialization."""
        teacher = Teacher("Mr. Smith", "Math", "EMP001")
        assert teacher.name == "Mr. Smith"
        assert teacher.subject == "Math"
        assert teacher.employee_id == "EMP001"


class TestClassroom:
    """Tests for Classroom class."""
    
    def test_classroom_init(self) -> None:
        """Test classroom initialization."""
        classroom = Classroom("101", 30)
        assert classroom.room_number == "101"
        assert classroom.capacity == 30
        assert classroom.students == []
        assert classroom.teacher is None
    
    def test_set_teacher(self) -> None:
        """Test setting teacher."""
        classroom = Classroom("101", 30)
        teacher = Teacher("Mr. Smith", "Math", "EMP001")
        classroom.set_teacher(teacher)
        assert classroom.teacher is teacher
    
    def test_add_student(self) -> None:
        """Test adding student."""
        classroom = Classroom("101", 30)
        student = Student("Alice", "STU001", 10)
        result = classroom.add_student(student)
        assert result is True
        assert len(classroom.students) == 1
    
    def test_add_student_over_capacity(self) -> None:
        """Test adding student when at capacity."""
        classroom = Classroom("101", 1)
        classroom.add_student(Student("Alice", "STU001", 10))
        result = classroom.add_student(Student("Bob", "STU002", 10))
        assert result is False
    
    def test_remove_student(self) -> None:
        """Test removing student."""
        classroom = Classroom("101", 30)
        classroom.add_student(Student("Alice", "STU001", 10))
        result = classroom.remove_student("STU001")
        assert result is True
        assert len(classroom.students) == 0
    
    def test_remove_student_not_found(self) -> None:
        """Test removing non-existent student."""
        classroom = Classroom("101", 30)
        result = classroom.remove_student("INVALID")
        assert result is False
    
    def test_get_student_count(self) -> None:
        """Test getting student count."""
        classroom = Classroom("101", 30)
        assert classroom.get_student_count() == 0
        classroom.add_student(Student("Alice", "STU001", 10))
        assert classroom.get_student_count() == 1
    
    def test_is_full(self) -> None:
        """Test checking if classroom is full."""
        classroom = Classroom("101", 1)
        assert classroom.is_full() is False
        classroom.add_student(Student("Alice", "STU001", 10))
        assert classroom.is_full() is True


class TestSchool:
    """Tests for School class."""
    
    def test_school_init(self) -> None:
        """Test school initialization."""
        school = School("High School")
        assert school.name == "High School"
        assert school.classrooms == {}
        assert school.teachers == {}
        assert school.students == {}
    
    def test_add_classroom(self) -> None:
        """Test adding classroom."""
        school = School("High School")
        classroom = Classroom("101", 30)
        school.add_classroom(classroom)
        assert "101" in school.classrooms
    
    def test_hire_teacher(self) -> None:
        """Test hiring teacher."""
        school = School("High School")
        teacher = Teacher("Mr. Smith", "Math", "EMP001")
        school.hire_teacher(teacher)
        assert "EMP001" in school.teachers
    
    def test_enroll_student(self) -> None:
        """Test enrolling student."""
        school = School("High School")
        student = Student("Alice", "STU001", 10)
        school.enroll_student(student)
        assert "STU001" in school.students
    
    def test_assign_teacher_to_classroom(self) -> None:
        """Test assigning teacher to classroom."""
        school = School("High School")
        teacher = Teacher("Mr. Smith", "Math", "EMP001")
        classroom = Classroom("101", 30)
        school.hire_teacher(teacher)
        school.add_classroom(classroom)
        result = school.assign_teacher_to_classroom("EMP001", "101")
        assert "assigned" in result.lower()
        assert classroom.teacher is teacher
    
    def test_assign_teacher_not_found(self) -> None:
        """Test assigning non-existent teacher."""
        school = School("High School")
        classroom = Classroom("101", 30)
        school.add_classroom(classroom)
        result = school.assign_teacher_to_classroom("INVALID", "101")
        assert "not found" in result.lower()
    
    def test_enroll_student_in_classroom(self) -> None:
        """Test enrolling student in classroom."""
        school = School("High School")
        student = Student("Alice", "STU001", 10)
        classroom = Classroom("101", 30)
        school.enroll_student(student)
        school.add_classroom(classroom)
        result = school.enroll_student_in_classroom("STU001", "101")
        assert "enrolled" in result.lower()
        assert student in classroom.students
    
    def test_enroll_student_classroom_full(self) -> None:
        """Test enrolling in full classroom."""
        school = School("High School")
        student = Student("Alice", "STU001", 10)
        classroom = Classroom("101", 0)
        school.enroll_student(student)
        school.add_classroom(classroom)
        result = school.enroll_student_in_classroom("STU001", "101")
        assert "full" in result.lower()
    
    def test_get_classroom_info(self) -> None:
        """Test getting classroom info."""
        school = School("High School")
        teacher = Teacher("Mr. Smith", "Math", "EMP001")
        classroom = Classroom("101", 30)
        school.hire_teacher(teacher)
        school.add_classroom(classroom)
        school.assign_teacher_to_classroom("EMP001", "101")
        classroom.add_student(Student("Alice", "STU001", 10))
        
        info = school.get_classroom_info("101")
        assert info is not None
        assert info["room_number"] == "101"
        assert info["teacher"] == "Mr. Smith"
        assert info["student_count"] == 1
        assert info["capacity"] == 30
    
    def test_get_classroom_info_not_found(self) -> None:
        """Test getting info for non-existent classroom."""
        school = School("High School")
        info = school.get_classroom_info("999")
        assert info is None
    
    def test_get_total_students(self) -> None:
        """Test getting total students."""
        school = School("High School")
        school.enroll_student(Student("Alice", "STU001", 10))
        school.enroll_student(Student("Bob", "STU002", 11))
        assert school.get_total_students() == 2
    
    def test_get_total_teachers(self) -> None:
        """Test getting total teachers."""
        school = School("High School")
        school.hire_teacher(Teacher("Mr. Smith", "Math", "EMP001"))
        assert school.get_total_teachers() == 1
