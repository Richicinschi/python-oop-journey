"""Problem 08: Read-Only Attribute

Topic: Write-once then read-only
Difficulty: Medium

Create a descriptor that allows setting a value once, then makes it read-only.
"""

from __future__ import annotations

from typing import Any


class ReadOnly:
    """A descriptor that allows write-once semantics.
    
    The descriptor should:
    - Allow setting the value exactly once per instance
    - Raise AttributeError on subsequent attempts to set
    - Support an optional default value
    - Optionally allow deletion and reset
    
    Attributes:
        default: Optional default value
        allow_deletion: Whether deletion resets the read-only state
    """
    
    def __init__(self, default: Any = None, allow_deletion: bool = False) -> None:
        """Initialize with optional default.
        
        Args:
            default: Default value (can be overridden once)
            allow_deletion: If True, deletion allows the value to be set again
        """
        raise NotImplementedError("Implement ReadOnly.__init__")
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Called when descriptor is assigned to class.
        
        Args:
            owner: The class
            name: The attribute name
        """
        raise NotImplementedError("Implement ReadOnly.__set_name__")
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        """Get the attribute value.
        
        Args:
            instance: The instance, or None for class access
            owner: The owner class
            
        Returns:
            The stored value, or self if class access
            
        Raises:
            AttributeError: If value hasn't been set and no default
        """
        raise NotImplementedError("Implement ReadOnly.__get__")
    
    def __set__(self, instance: object, value: Any) -> None:
        """Set the attribute value (only once).
        
        Args:
            instance: The instance
            value: The value to set
            
        Raises:
            AttributeError: If value has already been set
        """
        raise NotImplementedError("Implement ReadOnly.__set__")
    
    def __delete__(self, instance: object) -> None:
        """Delete the attribute.
        
        Args:
            instance: The instance
            
        Raises:
            AttributeError: If deletion is not allowed or value not set
        """
        raise NotImplementedError("Implement ReadOnly.__delete__")
    
    def is_set(self, instance: object) -> bool:
        """Check if the value has been set for an instance.
        
        Args:
            instance: The instance to check
            
        Returns:
            True if value has been set
        """
        raise NotImplementedError("Implement ReadOnly.is_set")


class ImmutableID:
    """An immutable identifier that can only be set once.
    
    Attributes:
        id: The unique identifier (read-only after setting)
    """
    
    id = ReadOnly()
    
    def __init__(self, id_value: str) -> None:
        """Initialize with immutable ID.
        
        Args:
            id_value: The unique identifier
        """
        raise NotImplementedError("Implement ImmutableID.__init__")


class Configuration:
    """Application configuration with read-only settings.
    
    Attributes (read-only):
        api_key: API authentication key
        base_url: Base URL for API
        version: Application version
    """
    
    api_key = ReadOnly()
    base_url = ReadOnly(default="https://api.example.com")
    version = ReadOnly()
    
    def __init__(self, api_key: str, version: str, base_url: str | None = None) -> None:
        """Initialize configuration.
        
        Args:
            api_key: API key (required)
            version: Version string (required)
            base_url: Optional base URL (overrides default)
        """
        raise NotImplementedError("Implement Configuration.__init__")
    
    def is_fully_configured(self) -> bool:
        """Check if all required settings are set.
        
        Returns:
            True if api_key and version are set
        """
        raise NotImplementedError("Implement Configuration.is_fully_configured")


class ResettableToken:
    """A token that can be reset but not directly modified.
    
    Attributes (read-only with deletion allowed):
        token: The authentication token
    """
    
    token = ReadOnly(allow_deletion=True)
    
    def __init__(self) -> None:
        """Initialize without a token."""
        pass
    
    def generate_token(self, value: str) -> None:
        """Generate a new token.
        
        Args:
            value: The token value
        """
        raise NotImplementedError("Implement ResettableToken.generate_token")
    
    def revoke_token(self) -> None:
        """Revoke the current token."""
        raise NotImplementedError("Implement ResettableToken.revoke_token")
    
    def is_valid(self) -> bool:
        """Check if a token is set.
        
        Returns:
            True if token has been set
        """
        raise NotImplementedError("Implement ResettableToken.is_valid")


# Hints for Read-Only Attribute (Medium):
# 
# Hint 1 - Conceptual nudge:
# You need to track which instances have had their value set. A dictionary mapping
# instances to values works, but consider: what should happen if someone accesses
# the attribute before setting it?
#
# Hint 2 - Structural plan:
# - Use __set_name__ to capture the attribute name
# - Store values in a dictionary keyed by instance id or using WeakKeyDictionary
# - Track a separate set of "already set" instances
# - Raise AttributeError with a clear message on subsequent sets
# - For deletion support, remove from the "set" tracking when deleted
#
# Hint 3 - Edge-case warning:
# What about deletion? If allow_deletion=True, removing an instance from your "set"
# tracking allows it to be set again. Also, handle class access (instance is None)
# by returning self.
