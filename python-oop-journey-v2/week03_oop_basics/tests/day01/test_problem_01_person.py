"""Tests for Problem 01: Person Class."""

from __future__ import annotations

from week03_oop_basics.solutions.day01.problem_01_person import Person


def test_person_creation() -> None:
    """Test that a Person can be created with name and age."""
    person = Person("Alice", 30)
    assert person.name == "Alice"
    assert person.age == 30


def test_person_different_values() -> None:
    """Test creating persons with different values."""
    person1 = Person("Bob", 25)
    person2 = Person("Charlie", 40)
    
    assert person1.name == "Bob"
    assert person1.age == 25
    assert person2.name == "Charlie"
    assert person2.age == 40


def test_person_str() -> None:
    """Test the __str__ method."""
    person = Person("Alice", 30)
    result = str(person)
    assert "Alice" in result
    assert "30" in result


def test_person_repr() -> None:
    """Test the __repr__ method."""
    person = Person("Alice", 30)
    result = repr(person)
    assert "Person" in result
    assert "Alice" in result
    assert "30" in result


def test_person_attributes_accessible() -> None:
    """Test that attributes are directly accessible."""
    person = Person("Test", 20)
    assert hasattr(person, "name")
    assert hasattr(person, "age")
