"""Problem 06: School Classroom.

Implement a School system with Classrooms, Teachers, and Students.
This demonstrates multiple composition and aggregation relationships.

Classes to implement:
- Student: with attributes name, student_id, grade_level
- Teacher: with attributes name, subject, employee_id
- Classroom: with attributes room_number, capacity, teacher (aggregation)
- School: composes Classrooms, aggregates Teachers and Students

Methods required:
- Classroom.add_student(student: Student) -> bool - adds if under capacity
- Classroom.remove_student(student_id: str) -> bool
- Classroom.set_teacher(teacher: Teacher) -> None
- School.add_classroom(classroom: Classroom) - composition
- School.hire_teacher(teacher: Teacher) - aggregation
- School.enroll_student(student: Student) - aggregation
- School.assign_teacher_to_classroom(teacher_id: str, room_number: str) -> str
"""

from __future__ import annotations
from typing import Optional


class Student:
    """A student enrolled at the school."""
    
    def __init__(self, name: str, student_id: str, grade_level: int) -> None:
        # TODO: Initialize name, student_id, grade_level
        pass


class Teacher:
    """A teacher employed by the school."""
    
    def __init__(self, name: str, subject: str, employee_id: str) -> None:
        # TODO: Initialize name, subject, employee_id
        pass


class Classroom:
    """A classroom in the school (composed by School)."""
    
    def __init__(self, room_number: str, capacity: int) -> None:
        # TODO: Initialize room_number, capacity, students (empty list), teacher (None)
        pass
    
    def set_teacher(self, teacher: Teacher) -> None:
        # TODO: Assign teacher to classroom
        pass
    
    def add_student(self, student: Student) -> bool:
        # TODO: Add student if under capacity, return True if added
        pass
    
    def remove_student(self, student_id: str) -> bool:
        # TODO: Remove student by ID, return True if removed
        pass
    
    def get_student_count(self) -> int:
        # TODO: Return number of students in classroom
        pass
    
    def is_full(self) -> bool:
        # TODO: Return True if at capacity
        pass


class School:
    """A school composing classrooms, aggregating teachers and students."""
    
    def __init__(self, name: str) -> None:
        # TODO: Initialize name, classrooms dict, teachers dict, students dict
        pass
    
    def add_classroom(self, classroom: Classroom) -> None:
        # TODO: Add classroom to school
        pass
    
    def hire_teacher(self, teacher: Teacher) -> None:
        # TODO: Add teacher to school
        pass
    
    def enroll_student(self, student: Student) -> None:
        # TODO: Add student to school
        pass
    
    def assign_teacher_to_classroom(self, employee_id: str, room_number: str) -> str:
        # TODO: Find teacher and classroom, assign teacher, return status
        pass
    
    def enroll_student_in_classroom(self, student_id: str, room_number: str) -> str:
        # TODO: Find student and classroom, add student if space, return status
        pass
    
    def get_classroom_info(self, room_number: str) -> Optional[dict]:
        # TODO: Return dict with room info: teacher name, student count, capacity
        pass
