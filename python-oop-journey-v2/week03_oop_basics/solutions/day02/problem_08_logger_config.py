"""Solution for Problem 08: Logger Config."""

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
        self.name = name
        self.level = self._level
    
    @classmethod
    def set_level(cls, level: str) -> None:
        """Set the global log level.
        
        Args:
            level: New log level (must be in _levels)
            
        Raises:
            ValueError: If level is not valid
        """
        if level not in cls._levels:
            raise ValueError(f"Invalid log level: {level}")
        cls._level = level
    
    @classmethod
    def get_level(cls) -> str:
        """Get the current global log level.
        
        Returns:
            Current log level
        """
        return cls._level
    
    @classmethod
    def is_level_enabled(cls, level: str) -> bool:
        """Check if a log level is enabled.
        
        A level is enabled if its numeric value >= current level's value.
        
        Args:
            level: Level to check
            
        Returns:
            True if level would be logged, False otherwise
        """
        if level not in cls._levels:
            return False
        return cls._levels[level] >= cls._levels[cls._level]
    
    @classmethod
    def with_custom_level(cls, name: str, level: str) -> Logger:
        """Create a logger with a custom level.
        
        Args:
            name: Logger name
            level: Custom log level
            
        Returns:
            New Logger instance with custom level
        """
        if level not in cls._levels:
            raise ValueError(f"Invalid log level: {level}")
        logger = cls(name)
        logger.level = level
        return logger
