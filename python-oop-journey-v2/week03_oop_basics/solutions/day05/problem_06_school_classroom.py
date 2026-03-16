"""Solution for Problem 06: School Classroom.

School with Classrooms, Teachers, and Students - demonstrates
multiple composition and aggregation relationships.
"""

from __future__ import annotations
from typing import Optional


class Student:
    """A student enrolled at the school.
    
    Students exist independently and can exist after leaving school.
    """
    
    def __init__(self, name: str, student_id: str, grade_level: int) -> None:
        """Initialize the student.
        
        Args:
            name: Student name.
            student_id: Unique student ID.
            grade_level: Grade level (1-12, etc.).
        """
        self.name = name
        self.student_id = student_id
        self.grade_level = grade_level


class Teacher:
    """A teacher employed by the school.
    
    Teachers exist independently and can teach at multiple schools.
    """
    
    def __init__(self, name: str, subject: str, employee_id: str) -> None:
        """Initialize the teacher.
        
        Args:
            name: Teacher name.
            subject: Subject taught.
            employee_id: Employee ID.
        """
        self.name = name
        self.subject = subject
        self.employee_id = employee_id


class Classroom:
    """A classroom in the school (composed by School).
    
    The classroom is part of the school building and cannot
    exist independently.
    """
    
    def __init__(self, room_number: str, capacity: int) -> None:
        """Initialize the classroom.
        
        Args:
            room_number: Room identifier.
            capacity: Maximum number of students.
        """
        self.room_number = room_number
        self.capacity = capacity
        self.students: list[Student] = []
        self.teacher: Teacher | None = None
    
    def set_teacher(self, teacher: Teacher) -> None:
        """Assign a teacher to the classroom.
        
        Args:
            teacher: Teacher to assign.
        """
        self.teacher = teacher
    
    def add_student(self, student: Student) -> bool:
        """Add a student to the classroom.
        
        Args:
            student: Student to add.
            
        Returns:
            True if added, False if at capacity.
        """
        if len(self.students) >= self.capacity:
            return False
        self.students.append(student)
        return True
    
    def remove_student(self, student_id: str) -> bool:
        """Remove a student from the classroom.
        
        Args:
            student_id: ID of student to remove.
            
        Returns:
            True if removed, False if not found.
        """
        for i, student in enumerate(self.students):
            if student.student_id == student_id:
                self.students.pop(i)
                return True
        return False
    
    def get_student_count(self) -> int:
        """Get number of students in classroom.
        
        Returns:
            Student count.
        """
        return len(self.students)
    
    def is_full(self) -> bool:
        """Check if classroom is at capacity.
        
        Returns:
            True if full, False otherwise.
        """
        return len(self.students) >= self.capacity
    
    def get_student_ids(self) -> list[str]:
        """Get list of student IDs.
        
        Returns:
            List of student IDs.
        """
        return [s.student_id for s in self.students]


class School:
    """A school composing classrooms, aggregating teachers and students.
    
    Classrooms are composed (owned by the school), while teachers
    and students are aggregated (exist independently).
    """
    
    def __init__(self, name: str) -> None:
        """Initialize the school.
        
        Args:
            name: School name.
        """
        self.name = name
        self.classrooms: dict[str, Classroom] = {}  # room_number -> Classroom
        self.teachers: dict[str, Teacher] = {}  # employee_id -> Teacher
        self.students: dict[str, Student] = {}  # student_id -> Student
    
    def add_classroom(self, classroom: Classroom) -> None:
        """Add a classroom to the school.
        
        Args:
            classroom: Classroom to add (composition).
        """
        self.classrooms[classroom.room_number] = classroom
    
    def hire_teacher(self, teacher: Teacher) -> None:
        """Hire a teacher.
        
        Args:
            teacher: Teacher to hire (aggregation).
        """
        self.teachers[teacher.employee_id] = teacher
    
    def enroll_student(self, student: Student) -> None:
        """Enroll a student.
        
        Args:
            student: Student to enroll (aggregation).
        """
        self.students[student.student_id] = student
    
    def assign_teacher_to_classroom(self, employee_id: str, room_number: str) -> str:
        """Assign a teacher to a classroom.
        
        Args:
            employee_id: Teacher's employee ID.
            room_number: Classroom room number.
            
        Returns:
            Status message.
        """
        teacher = self.teachers.get(employee_id)
        if teacher is None:
            return f"Teacher {employee_id} not found"
        
        classroom = self.classrooms.get(room_number)
        if classroom is None:
            return f"Classroom {room_number} not found"
        
        classroom.set_teacher(teacher)
        return f"{teacher.name} assigned to classroom {room_number}"
    
    def enroll_student_in_classroom(self, student_id: str, room_number: str) -> str:
        """Enroll a student in a classroom.
        
        Args:
            student_id: Student's ID.
            room_number: Classroom room number.
            
        Returns:
            Status message.
        """
        student = self.students.get(student_id)
        if student is None:
            return f"Student {student_id} not enrolled"
        
        classroom = self.classrooms.get(room_number)
        if classroom is None:
            return f"Classroom {room_number} not found"
        
        if classroom.add_student(student):
            return f"{student.name} enrolled in classroom {room_number}"
        return f"Classroom {room_number} is full"
    
    def get_classroom_info(self, room_number: str) -> Optional[dict]:
        """Get classroom information.
        
        Args:
            room_number: Room number to query.
            
        Returns:
            Dictionary with classroom info or None if not found.
        """
        classroom = self.classrooms.get(room_number)
        if classroom is None:
            return None
        
        return {
            "room_number": classroom.room_number,
            "teacher": classroom.teacher.name if classroom.teacher else None,
            "student_count": classroom.get_student_count(),
            "capacity": classroom.capacity,
        }
    
    def get_total_students(self) -> int:
        """Get total enrolled students.
        
        Returns:
            Total student count.
        """
        return len(self.students)
    
    def get_total_teachers(self) -> int:
        """Get total hired teachers.
        
        Returns:
            Total teacher count.
        """
        return len(self.teachers)
