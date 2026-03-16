"""Tests for Problem 05: Student Registry."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day02.problem_05_student_registry import Student


class TestStudentRegistry:
    """Test suite for Student registry pattern."""
    
    def setup_method(self) -> None:
        """Clear registry before each test."""
        Student._registry.clear()
    
    def teardown_method(self) -> None:
        """Clear registry after each test."""
        Student._registry.clear()
    
    def test_init_registers_student(self) -> None:
        """Test that __init__ registers the student."""
        s = Student("Alice", 101)
        assert 101 in Student._registry
        assert Student._registry[101] is s
    
    def test_get_count_empty(self) -> None:
        """Test get_count with no students."""
        assert Student.get_count() == 0
    
    def test_get_count_multiple(self) -> None:
        """Test get_count with multiple students."""
        Student("Alice", 101)
        Student("Bob", 102)
        assert Student.get_count() == 2
    
    def test_list_all_empty(self) -> None:
        """Test list_all with no students."""
        assert Student.list_all() == []
    
    def test_list_all_multiple(self) -> None:
        """Test list_all with multiple students."""
        Student("Alice", 101)
        Student("Bob", 102)
        result = Student.list_all()
        assert "Alice (101)" in result
        assert "Bob (102)" in result
        assert len(result) == 2
    
    def test_find_by_id_exists(self) -> None:
        """Test find_by_id with existing student."""
        Student("Alice", 101)
        assert Student.find_by_id(101) == "Alice (101)"
    
    def test_find_by_id_not_exists(self) -> None:
        """Test find_by_id with non-existing student."""
        assert Student.find_by_id(999) is None
    
    def test_unregister_removes_student(self) -> None:
        """Test unregister removes student from registry."""
        s = Student("Alice", 101)
        assert Student.get_count() == 1
        s.unregister()
        assert Student.get_count() == 0
        assert Student.find_by_id(101) is None
    
    def test_unregister_one_of_many(self) -> None:
        """Test unregister removes only the specified student."""
        s1 = Student("Alice", 101)
        s2 = Student("Bob", 102)
        s1.unregister()
        assert Student.get_count() == 1
        assert Student.find_by_id(102) == "Bob (102)"
    
    def test_repr(self) -> None:
        """Test string representation."""
        s = Student("Alice", 101)
        assert repr(s) == "Alice (101)"
        assert str(s) == "Alice (101)"
