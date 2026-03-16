"""Tests for Problem 10: Auto-Serialization Metaclass."""

from __future__ import annotations

import json

import pytest

from week05_oop_advanced.solutions.day02.problem_10_serializable_meta import (
    Address,
    Company,
    Person,
    Serializable,
    SerializableMeta,
)


class TestSerializableMeta:
    """Tests for the SerializableMeta metaclass."""
    
    def test_metaclass_exists(self) -> None:
        """Test that SerializableMeta is defined."""
        assert isinstance(SerializableMeta, type)
    
    def test_auto_to_dict_generated(self) -> None:
        """Test that to_dict is auto-generated."""
        p = Person(name="Alice", age=30)
        result = p.to_dict()
        
        assert "name" in result
        assert "age" in result
        assert result["name"] == "Alice"
        assert result["age"] == 30
    
    def test_auto_from_dict_generated(self) -> None:
        """Test that from_dict is auto-generated."""
        data = {"name": "Bob", "age": 25, "email": "bob@example.com"}
        p = Person.from_dict(data)
        
        assert isinstance(p, Person)
        assert p.name == "Bob"
        assert p.age == 25
    
    def test_from_dict_preserves_defaults(self) -> None:
        """Test that from_dict uses defaults for missing fields."""
        data = {"name": "Charlie"}  # Missing age and email
        p = Person.from_dict(data)
        
        assert p.name == "Charlie"
        assert p.age == 0  # Default
        assert p.email == ""  # Default


class TestSerializable:
    """Tests for the Serializable base class."""
    
    def test_serializable_has_methods(self) -> None:
        """Test that Serializable provides base methods."""
        assert hasattr(Serializable, 'to_dict')
        assert hasattr(Serializable, 'from_dict')
        assert hasattr(Serializable, 'to_json')
        assert hasattr(Serializable, 'from_json')
    
    def test_to_json(self) -> None:
        """Test to_json method."""
        p = Person(name="Alice", age=30)
        json_str = p.to_json()
        
        # Should be valid JSON
        data = json.loads(json_str)
        assert data["name"] == "Alice"
        assert data["age"] == 30
    
    def test_to_json_with_indent(self) -> None:
        """Test to_json with indentation."""
        p = Person(name="Alice")
        json_str = p.to_json(indent=2)
        
        # Should contain newlines when indented
        assert "\n" in json_str
    
    def test_from_json(self) -> None:
        """Test from_json method."""
        json_str = '{"name": "Bob", "age": 25}'
        p = Person.from_json(json_str)
        
        assert isinstance(p, Person)
        assert p.name == "Bob"
        assert p.age == 25


class TestPerson:
    """Tests for the Person class."""
    
    def test_person_init(self) -> None:
        """Test Person initialization."""
        p = Person(name="Alice", age=30, email="alice@example.com")
        assert p.name == "Alice"
        assert p.age == 30
        assert p.email == "alice@example.com"
    
    def test_person_serialization(self) -> None:
        """Test Person serialization."""
        p = Person(name="Alice", age=30)
        data = p.to_dict()
        
        assert data == {"name": "Alice", "age": 30, "email": ""}
    
    def test_person_deserialization(self) -> None:
        """Test Person deserialization."""
        p = Person.from_dict({"name": "Bob", "age": 25, "email": "bob@test.com"})
        
        assert p.name == "Bob"
        assert p.age == 25
        assert p.email == "bob@test.com"


class TestAddress:
    """Tests for the Address class."""
    
    def test_address_init(self) -> None:
        """Test Address initialization."""
        addr = Address(
            street="123 Main St",
            city="Springfield",
            country="USA",
            postal_code="12345",
        )
        
        assert addr.street == "123 Main St"
        assert addr.city == "Springfield"
        assert addr.country == "USA"
        assert addr.postal_code == "12345"
    
    def test_address_serialization(self) -> None:
        """Test Address serialization."""
        addr = Address(street="123 Main St", city="Springfield")
        data = addr.to_dict()
        
        assert data["street"] == "123 Main St"
        assert data["city"] == "Springfield"
        assert data["country"] == ""
        assert data["postal_code"] == ""


class TestCompany:
    """Tests for the Company class."""
    
    def test_company_init(self) -> None:
        """Test Company initialization."""
        addr = Address(street="123 Main St", city="Springfield")
        company = Company(name="Acme Inc", founded_year=2000, address=addr)
        
        assert company.name == "Acme Inc"
        assert company.founded_year == 2000
        assert company.address is addr
        assert company.employees == []
    
    def test_company_add_employee(self) -> None:
        """Test adding employees to company."""
        company = Company(name="Acme Inc")
        emp = Person(name="Alice", age=30)
        
        company.add_employee(emp)
        
        assert len(company.employees) == 1
        assert company.employees[0].name == "Alice"
    
    def test_company_employee_count(self) -> None:
        """Test employee count."""
        company = Company(name="Acme Inc")
        assert company.employee_count() == 0
        
        company.add_employee(Person(name="Alice"))
        company.add_employee(Person(name="Bob"))
        assert company.employee_count() == 2
    
    def test_company_nested_serialization(self) -> None:
        """Test Company serialization with nested objects."""
        addr = Address(street="123 Main St", city="Springfield")
        emp1 = Person(name="Alice", age=30)
        emp2 = Person(name="Bob", age=25)
        
        company = Company(
            name="Acme Inc",
            founded_year=2000,
            address=addr,
            employees=[emp1, emp2],
        )
        
        data = company.to_dict()
        
        # Top level
        assert data["name"] == "Acme Inc"
        assert data["founded_year"] == 2000
        
        # Nested address should be dict
        assert isinstance(data["address"], dict)
        assert data["address"]["street"] == "123 Main St"
        
        # Nested employees should be list of dicts
        assert isinstance(data["employees"], list)
        assert len(data["employees"]) == 2
        assert data["employees"][0]["name"] == "Alice"
        assert data["employees"][1]["name"] == "Bob"
    
    def test_company_exclude_fields(self) -> None:
        """Test that excluded fields are not serialized."""
        company = Company(name="Acme Inc")
        data = company.to_dict()
        
        # _internal_id should be excluded
        assert "_internal_id" not in data
        assert "name" in data
    
    def test_company_to_json(self) -> None:
        """Test Company JSON serialization."""
        company = Company(name="Acme Inc", founded_year=2000)
        json_str = company.to_json()
        
        # Should be valid JSON
        data = json.loads(json_str)
        assert data["name"] == "Acme Inc"
        assert data["founded_year"] == 2000
