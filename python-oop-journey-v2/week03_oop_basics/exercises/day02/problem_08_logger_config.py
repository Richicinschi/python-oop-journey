"""Problem 08: Logger Config

Topic: @classmethod config management
Difficulty: Medium

Create a Logger class that uses class methods to manage global
configuration settings.

Example:
    >>> # Default log level
    >>> Logger.get_level()
    'INFO'
    >>> 
    >>> # Set global log level
    >>> Logger.set_level('DEBUG')
    >>> Logger.get_level()
    'DEBUG'
    >>> 
    >>> # Create loggers that use global config
    >>> log1 = Logger("app")
    >>> log1.level
    'DEBUG'
    >>> 
    >>> # Create logger with custom level
    >>> log2 = Logger.with_custom_level("db", "ERROR")
    >>> log2.level
    'ERROR'
    >>> 
    >>> # Check if level is enabled
    >>> Logger.is_level_enabled('DEBUG')
    True
    >>> Logger.is_level_enabled('WARNING')
    True  # WARNING is higher than DEBUG
    >>> Logger.is_level_enabled('ERROR')
    True

Requirements:
    - _level: class-level variable, default 'INFO'
    - _levels: class-level dict mapping level names to numeric values
      {'DEBUG': 10, 'INFO': 20, 'WARNING': 30, 'ERROR': 40, 'CRITICAL': 50}
    - __init__(self, name: str): creates logger with current class level
    - set_level(cls, level: str): classmethod to set global level
    - get_level(cls) -> str: classmethod to get global level
    - is_level_enabled(cls, level: str) -> bool: classmethod
      Returns True if given level >= current level
    - with_custom_level(cls, name: str, level: str): classmethod factory
      Creates logger with custom level (not affecting global)

Hints:
    - Hint 1: Class methods use 'cls' not 'self' - use cls._level to access class var
    - Hint 2: is_level_enabled compares numeric values: _levels[level] >= _levels[_level]
    - Hint 3: with_custom_level creates instance directly (obj = cls.__new__(cls)) then sets attrs
"""

from __future__ import annotations


class Logger:
    """Logger class with class-level configuration."""
    
    _level: str = "INFO"
    _levels: dict[str, int] = {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50,
    }
    
    def __init__(self, name: str) -> None:
        """Initialize a logger with the current class level.
        
        Args:
            name: Logger name
        """
        raise NotImplementedError("Implement __init__")
    
    @classmethod
    def set_level(cls, level: str) -> None:
        """Set the global log level.
        
        Args:
            level: New log level (must be in _levels)
            
        Raises:
            ValueError: If level is not valid
        """
        raise NotImplementedError("Implement set_level")
    
    @classmethod
    def get_level(cls) -> str:
        """Get the current global log level.
        
        Returns:
            Current log level
        """
        raise NotImplementedError("Implement get_level")
    
    @classmethod
    def is_level_enabled(cls, level: str) -> bool:
        """Check if a log level is enabled.
        
        A level is enabled if its numeric value >= current level's value.
        
        Args:
            level: Level to check
            
        Returns:
            True if level would be logged, False otherwise
        """
        raise NotImplementedError("Implement is_level_enabled")
    
    @classmethod
    def with_custom_level(cls, name: str, level: str) -> Logger:
        """Create a logger with a custom level.
        
        Args:
            name: Logger name
            level: Custom log level
            
        Returns:
            New Logger instance with custom level
        """
        raise NotImplementedError("Implement with_custom_level")
