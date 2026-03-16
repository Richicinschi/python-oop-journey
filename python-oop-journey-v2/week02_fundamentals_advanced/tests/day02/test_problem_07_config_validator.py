"""Tests for Problem 07: Configuration Validator."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day02.problem_07_config_validator import (
    config_validator,
)


def test_config_validator_valid() -> None:
    """Test valid configuration."""
    config = {"host": "localhost", "port": 8080}
    assert config_validator(config) == []
    
    config = {"host": "127.0.0.1", "port": 1, "debug": True}
    assert config_validator(config) == []
    
    config = {"host": "example.com", "port": 65535, "debug": False}
    assert config_validator(config) == []


def test_config_validator_missing_host() -> None:
    """Test missing host field."""
    config = {"port": 8080}
    errors = config_validator(config)
    assert "host is required" in errors


def test_config_validator_missing_port() -> None:
    """Test missing port field."""
    config = {"host": "localhost"}
    errors = config_validator(config)
    assert "port is required" in errors


def test_config_validator_empty_host() -> None:
    """Test empty host string."""
    config = {"host": "", "port": 8080}
    errors = config_validator(config)
    assert "host cannot be empty" in errors


def test_config_validator_host_not_string() -> None:
    """Test non-string host."""
    config = {"host": 123, "port": 8080}
    errors = config_validator(config)
    assert "host must be a string" in errors


def test_config_validator_port_out_of_range() -> None:
    """Test port out of valid range."""
    config = {"host": "localhost", "port": 0}
    errors = config_validator(config)
    assert "port must be between 1 and 65535" in errors
    
    config = {"host": "localhost", "port": 65536}
    errors = config_validator(config)
    assert "port must be between 1 and 65535" in errors


def test_config_validator_port_not_int() -> None:
    """Test non-integer port."""
    config = {"host": "localhost", "port": "8080"}
    errors = config_validator(config)
    assert "port must be an integer" in errors
    
    config = {"host": "localhost", "port": 8080.5}
    errors = config_validator(config)
    assert "port must be an integer" in errors


def test_config_validator_debug_not_bool() -> None:
    """Test non-boolean debug."""
    config = {"host": "localhost", "port": 8080, "debug": "true"}
    errors = config_validator(config)
    assert "debug must be a boolean" in errors


def test_config_validator_multiple_errors() -> None:
    """Test collecting multiple errors."""
    config = {}
    errors = config_validator(config)
    assert "host is required" in errors
    assert "port is required" in errors
    
    config = {"host": "", "port": 0, "debug": "yes"}
    errors = config_validator(config)
    assert "host cannot be empty" in errors
    assert "port must be between 1 and 65535" in errors
    assert "debug must be a boolean" in errors


def test_config_validator_empty_config() -> None:
    """Test empty config."""
    errors = config_validator({})
    assert len(errors) == 2
    assert "host is required" in errors
    assert "port is required" in errors
