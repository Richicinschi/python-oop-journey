"""Tests for Problem 02: Person with Age Validation."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day03.problem_02_person_with_age_validation import (
    Person,
)


class TestPerson:
    """Test suite for Person class."""
    
    def test_initialization(self) -> None:
        """Test person initialization."""
        person = Person("Alice", 25)
        assert person.name == "Alice"
        assert person.age == 25
    
    def test_initialization_strips_name(self) -> None:
        """Test that name is stripped of whitespace."""
        person = Person("  Alice  ", 25)
        assert person.name == "Alice"
    
    def test_initialization_invalid_name_type(self) -> None:
        """Test initialization with non-string name raises TypeError."""
        with pytest.raises(TypeError, match="string"):
            Person(123, 25)  # type: ignore
    
    def test_initialization_empty_name(self) -> None:
        """Test initialization with empty name raises ValueError."""
        with pytest.raises(ValueError, match="empty"):
            Person("", 25)
    
    def test_initialization_whitespace_name(self) -> None:
        """Test initialization with whitespace-only name raises ValueError."""
        with pytest.raises(ValueError, match="empty"):
            Person("   ", 25)
    
    def test_initialization_invalid_age_negative(self) -> None:
        """Test initialization with negative age raises ValueError."""
        with pytest.raises(ValueError, match="Age must be between"):
            Person("Alice", -1)
    
    def test_initialization_invalid_age_too_high(self) -> None:
        """Test initialization with age > 150 raises ValueError."""
        with pytest.raises(ValueError, match="Age must be between"):
            Person("Alice", 151)
    
    def test_initialization_invalid_age_type(self) -> None:
        """Test initialization with non-int age raises TypeError."""
        with pytest.raises(TypeError, match="integer"):
            Person("Alice", 25.5)  # type: ignore
    
    def test_age_setter_valid(self) -> None:
        """Test age setter with valid value."""
        person = Person("Alice", 25)
        person.age = 30
        assert person.age == 30
    
    def test_age_setter_zero(self) -> None:
        """Test age setter with zero."""
        person = Person("Alice", 25)
        person.age = 0
        assert person.age == 0
    
    def test_age_setter_boundary_150(self) -> None:
        """Test age setter with boundary value 150."""
        person = Person("Alice", 25)
        person.age = 150
        assert person.age == 150
    
    def test_age_setter_negative_raises(self) -> None:
        """Test age setter with negative value raises ValueError."""
        person = Person("Alice", 25)
        with pytest.raises(ValueError, match="between 0 and 150"):
            person.age = -5
    
    def test_age_setter_too_high_raises(self) -> None:
        """Test age setter with value > 150 raises ValueError."""
        person = Person("Alice", 25)
        with pytest.raises(ValueError, match="between 0 and 150"):
            person.age = 200
    
    def test_age_setter_non_int_raises(self) -> None:
        """Test age setter with non-integer raises TypeError."""
        person = Person("Alice", 25)
        with pytest.raises(TypeError, match="integer"):
            person.age = "30"  # type: ignore
    
    def test_name_read_only(self) -> None:
        """Test that name is read-only after creation."""
        person = Person("Alice", 25)
        with pytest.raises(AttributeError):
            person.name = "Bob"  # type: ignore
    
    def test_is_adult_true(self) -> None:
        """Test is_adult returns True for age >= 18."""
        person = Person("Alice", 18)
        assert person.is_adult() is True
        person.age = 25
        assert person.is_adult() is True
    
    def test_is_adult_false(self) -> None:
        """Test is_adult returns False for age < 18."""
        person = Person("Alice", 17)
        assert person.is_adult() is False
        person.age = 0
        assert person.is_adult() is False
    
    def test_celebrate_birthday(self) -> None:
        """Test celebrate_birthday increments age."""
        person = Person("Alice", 25)
        person.celebrate_birthday()
        assert person.age == 26
    
    def test_celebrate_birthday_multiple(self) -> None:
        """Test celebrate_birthday called multiple times."""
        person = Person("Alice", 25)
        for _ in range(5):
            person.celebrate_birthday()
        assert person.age == 30
