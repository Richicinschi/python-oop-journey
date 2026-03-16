"""Reference solution for Problem 08: Read-Only Attribute."""

from __future__ import annotations

from typing import Any


class ReadOnly:
    """A descriptor that allows write-once semantics."""
    
    def __init__(self, default: Any = None, allow_deletion: bool = False) -> None:
        self.default = default
        self.allow_deletion = allow_deletion
        self.name = ""
        self.storage_name = ""
        self.set_flag_name = ""
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.storage_name = f"_{name}"
        self.set_flag_name = f"_{name}_is_set"
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        
        if not hasattr(instance, self.set_flag_name) and self.default is not None:
            return self.default
        
        if not hasattr(instance, self.storage_name):
            raise AttributeError(f"'{self.name}' has not been set")
        
        return getattr(instance, self.storage_name)
    
    def __set__(self, instance: object, value: Any) -> None:
        if hasattr(instance, self.set_flag_name):
            raise AttributeError(f"Cannot modify read-only attribute '{self.name}'")
        
        setattr(instance, self.set_flag_name, True)
        setattr(instance, self.storage_name, value)
    
    def __delete__(self, instance: object) -> None:
        if not self.allow_deletion:
            raise AttributeError(f"Cannot delete read-only attribute '{self.name}'")
        
        if hasattr(instance, self.set_flag_name):
            delattr(instance, self.set_flag_name)
        if hasattr(instance, self.storage_name):
            delattr(instance, self.storage_name)
    
    def is_set(self, instance: object) -> bool:
        return hasattr(instance, self.set_flag_name)


class ImmutableID:
    """An immutable identifier that can only be set once."""
    
    id = ReadOnly()
    
    def __init__(self, id_value: str) -> None:
        self.id = id_value


class Configuration:
    """Application configuration with read-only settings."""
    
    api_key = ReadOnly()
    base_url = ReadOnly(default="https://api.example.com")
    version = ReadOnly()
    
    def __init__(self, api_key: str, version: str, base_url: str | None = None) -> None:
        self.api_key = api_key
        self.version = version
        if base_url is not None:
            self.base_url = base_url
    
    def is_fully_configured(self) -> bool:
        return type(self).api_key.is_set(self) and type(self).version.is_set(self)


class ResettableToken:
    """A token that can be reset but not directly modified."""
    
    token = ReadOnly(allow_deletion=True)
    
    def __init__(self) -> None:
        pass
    
    def generate_token(self, value: str) -> None:
        if type(self).token.is_set(self):
            del self.token
        self.token = value
    
    def revoke_token(self) -> None:
        if type(self).token.is_set(self):
            del self.token
    
    def is_valid(self) -> bool:
        return type(self).token.is_set(self)
