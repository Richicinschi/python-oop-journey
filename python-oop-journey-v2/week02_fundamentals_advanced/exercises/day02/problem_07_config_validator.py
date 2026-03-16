"""Problem 07: Configuration Validator

Topic: Comprehensive Validation
Difficulty: Medium

Validate a configuration dictionary with multiple requirements.

Examples:
    >>> config_validator({"host": "localhost", "port": 8080, "debug": False})
    []
    >>> config_validator({"host": "", "port": 70000})
    ["host cannot be empty", "port must be between 1 and 65535"]
    >>> config_validator({})
    ["host is required", "port is required"]

Requirements:
    - Return a list of error messages (empty list if valid)
    - Required fields: 'host' (non-empty string), 'port' (int 1-65535)
    - Optional field: 'debug' (boolean, defaults to False)
    - Collect all validation errors, don't stop at first error
"""

from __future__ import annotations


def config_validator(config: dict) -> list[str]:
    """Validate a configuration dictionary.

    Args:
        config: The configuration dictionary to validate

    Returns:
        A list of error messages (empty if config is valid)
    """
    raise NotImplementedError("Implement config_validator")
