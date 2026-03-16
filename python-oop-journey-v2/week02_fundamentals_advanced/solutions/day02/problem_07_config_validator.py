"""Solution for Problem 07: Configuration Validator."""

from __future__ import annotations


def config_validator(config: dict) -> list[str]:
    """Validate a configuration dictionary.

    Args:
        config: The configuration dictionary to validate

    Returns:
        A list of error messages (empty if config is valid)
    """
    errors: list[str] = []

    # Validate host (required, non-empty string)
    if "host" not in config:
        errors.append("host is required")
    elif not isinstance(config["host"], str):
        errors.append("host must be a string")
    elif config["host"] == "":
        errors.append("host cannot be empty")

    # Validate port (required, int 1-65535)
    if "port" not in config:
        errors.append("port is required")
    elif not isinstance(config["port"], int):
        errors.append("port must be an integer")
    elif not 1 <= config["port"] <= 65535:
        errors.append("port must be between 1 and 65535")

    # Validate debug (optional, boolean)
    if "debug" in config and not isinstance(config["debug"], bool):
        errors.append("debug must be a boolean")

    return errors
