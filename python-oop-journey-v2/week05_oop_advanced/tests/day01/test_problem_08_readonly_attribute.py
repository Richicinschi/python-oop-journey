"""Tests for Problem 08: Read-Only Attribute."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day01.problem_08_readonly_attribute import (
    ReadOnly, ImmutableID, Configuration, ResettableToken
)


class TestReadOnly:
    """Tests for the ReadOnly descriptor."""
    
    def test_value_can_be_set_once(self) -> None:
        class TestClass:
            value = ReadOnly()
            
            def __init__(self, v: str) -> None:
                self.value = v
        
        obj = TestClass("test")
        assert obj.value == "test"
    
    def test_second_set_raises_error(self) -> None:
        class TestClass:
            value = ReadOnly()
            
            def __init__(self, v: str) -> None:
                self.value = v
        
        obj = TestClass("test")
        with pytest.raises(AttributeError, match="read-only"):
            obj.value = "new_value"
    
    def test_default_value(self) -> None:
        class TestClass:
            value = ReadOnly(default="default")
        
        obj = TestClass()
        assert obj.value == "default"
    
    def test_default_can_be_overridden_once(self) -> None:
        class TestClass:
            value = ReadOnly(default="default")
        
        obj = TestClass()
        obj.value = "custom"
        assert obj.value == "custom"
        
        with pytest.raises(AttributeError):
            obj.value = "another"
    
    def test_is_set_method(self) -> None:
        class TestClass:
            value = ReadOnly()
        
        obj = TestClass()
        assert TestClass.__dict__['value'].is_set(obj) is False
        
        obj.value = "test"
        assert TestClass.__dict__['value'].is_set(obj) is True
    
    def test_access_before_set_raises(self) -> None:
        class TestClass:
            value = ReadOnly()
        
        obj = TestClass()
        with pytest.raises(AttributeError):
            _ = obj.value


class TestImmutableID:
    """Tests for the ImmutableID class."""
    
    def test_id_set_on_creation(self) -> None:
        id_obj = ImmutableID("user-123")
        assert id_obj.id == "user-123"
    
    def test_id_cannot_be_changed(self) -> None:
        id_obj = ImmutableID("user-123")
        with pytest.raises(AttributeError):
            id_obj.id = "user-456"


class TestConfiguration:
    """Tests for the Configuration class."""
    
    def test_config_creation(self) -> None:
        config = Configuration("secret-key", "1.0.0")
        assert config.api_key == "secret-key"
        assert config.version == "1.0.0"
        assert config.base_url == "https://api.example.com"
    
    def test_config_with_custom_base_url(self) -> None:
        config = Configuration("key", "1.0.0", "https://custom.com")
        assert config.base_url == "https://custom.com"
    
    def test_api_key_cannot_be_changed(self) -> None:
        config = Configuration("secret", "1.0.0")
        with pytest.raises(AttributeError):
            config.api_key = "new-secret"
    
    def test_is_fully_configured(self) -> None:
        config = Configuration("key", "1.0.0")
        assert config.is_fully_configured() is True
    
    def test_version_cannot_be_changed(self) -> None:
        config = Configuration("secret", "1.0.0")
        with pytest.raises(AttributeError):
            config.version = "2.0.0"


class TestResettableToken:
    """Tests for the ResettableToken class."""
    
    def test_token_not_set_initially(self) -> None:
        token = ResettableToken()
        assert token.is_valid() is False
    
    def test_generate_token(self) -> None:
        token = ResettableToken()
        token.generate_token("abc123")
        assert token.token == "abc123"
        assert token.is_valid() is True
    
    def test_token_cannot_be_directly_modified(self) -> None:
        token = ResettableToken()
        token.generate_token("abc123")
        with pytest.raises(AttributeError):
            token.token = "xyz789"
    
    def test_revoke_token(self) -> None:
        token = ResettableToken()
        token.generate_token("abc123")
        token.revoke_token()
        assert token.is_valid() is False
    
    def test_generate_after_revoke(self) -> None:
        token = ResettableToken()
        token.generate_token("abc123")
        token.revoke_token()
        token.generate_token("new-token")
        assert token.token == "new-token"
