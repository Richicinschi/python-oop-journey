"""Tests for Problem 03: Auto Property Generation Metaclass."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day02.problem_03_auto_property_meta import (
    AutoPropertyMeta,
    Config,
    Person,
)


class TestAutoPropertyMeta:
    """Tests for the AutoPropertyMeta metaclass."""
    
    def test_metaclass_exists(self) -> None:
        """Test that AutoPropertyMeta is defined."""
        assert isinstance(AutoPropertyMeta, type)
    
    def test_auto_properties_created(self) -> None:
        """Test that properties are auto-created from annotations."""
        p = Person()
        
        # Should have properties
        assert hasattr(type(p), 'name')
        assert hasattr(type(p), 'age')
        assert hasattr(type(p), 'email')
        
        # Properties should be accessible
        p._name = "Alice"  # Set underlying directly
        assert p.name == "Alice"
    
    def test_type_checking_on_set(self) -> None:
        """Test that type checking is enforced."""
        p = Person()
        
        # Valid assignment
        p.name = "Alice"
        assert p.name == "Alice"
        
        # Invalid type should raise TypeError
        with pytest.raises(TypeError):
            p.age = "not an int"
    
    def test_type_checking_string(self) -> None:
        """Test type checking for string attributes."""
        p = Person()
        
        p.name = "Valid"
        assert p.name == "Valid"
        
        with pytest.raises(TypeError):
            p.name = 123  # Not a string


class TestPerson:
    """Tests for the Person class."""
    
    def test_person_init(self) -> None:
        """Test Person initialization."""
        p = Person(name="Bob", age=30, email="bob@example.com")
        assert p.name == "Bob"
        assert p.age == 30
        assert p.email == "bob@example.com"
    
    def test_person_init_defaults(self) -> None:
        """Test Person initialization with defaults."""
        p = Person()
        assert p.name == ""
        assert p.age == 0
        assert p.email == ""
    
    def test_person_str(self) -> None:
        """Test Person string representation."""
        p = Person(name="Alice", age=25)
        result = str(p)
        assert "Alice" in result
        assert "25" in result
    
    def test_person_type_enforcement(self) -> None:
        """Test that Person enforces types."""
        p = Person()
        
        p.name = "Test"
        p.age = 20
        p.email = "test@test.com"
        
        with pytest.raises(TypeError):
            p.name = 123
        
        with pytest.raises(TypeError):
            p.age = "twenty"


class TestConfig:
    """Tests for the Config class."""
    
    def test_config_init(self) -> None:
        """Test Config initialization."""
        c = Config(debug=True, timeout=60, api_url="http://api.test")
        assert c.debug is True
        assert c.timeout == 60
        assert c.api_url == "http://api.test"
    
    def test_config_defaults(self) -> None:
        """Test Config default values."""
        c = Config()
        assert c.debug is False
        assert c.timeout == 30
        assert c.api_url == "http://localhost"
        assert c.max_retries == 3
    
    def test_config_as_dict(self) -> None:
        """Test Config as_dict method."""
        c = Config(debug=True, timeout=45)
        result = c.as_dict()
        
        assert result['debug'] is True
        assert result['timeout'] == 45
        assert result['api_url'] == "http://localhost"
        assert result['max_retries'] == 3
    
    def test_config_type_enforcement(self) -> None:
        """Test that Config enforces types."""
        c = Config()
        
        c.debug = True
        c.timeout = 60
        
        with pytest.raises(TypeError):
            c.debug = "yes"  # Should be bool
        
        with pytest.raises(TypeError):
            c.timeout = "sixty"  # Should be int
