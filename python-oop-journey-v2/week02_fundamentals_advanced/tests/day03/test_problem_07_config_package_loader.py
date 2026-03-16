"""Tests for Problem 07: Config Package Loader."""

from __future__ import annotations

import json
import os
import tempfile

from week02_fundamentals_advanced.solutions.day03.problem_07_config_package_loader import (
    Config,
    ConfigLoader,
)


# ===== Config tests =====
def test_config_get() -> None:
    """Test Config get method."""
    config = Config({"name": "test", "nested": {"key": "value"}})
    assert config.get("name") == "test"
    assert config.get("nested.key") == "value"


def test_config_get_default() -> None:
    """Test Config get with default."""
    config = Config({})
    assert config.get("missing", "default") == "default"


def test_config_get_int() -> None:
    """Test Config get_int."""
    config = Config({"port": "8080", "count": 42})
    assert config.get_int("port") == 8080
    assert config.get_int("count") == 42
    assert config.get_int("missing", 100) == 100


def test_config_get_float() -> None:
    """Test Config get_float."""
    config = Config({"rate": "3.14", "value": 2.5})
    assert abs(config.get_float("rate") - 3.14) < 0.001
    assert config.get_float("value") == 2.5


def test_config_get_bool() -> None:
    """Test Config get_bool."""
    config = Config({
        "flag1": "true",
        "flag2": "yes",
        "flag3": "1",
        "flag4": "on",
        "flag5": True,
        "flag6": "false",
        "flag7": "no",
    })
    assert config.get_bool("flag1") is True
    assert config.get_bool("flag2") is True
    assert config.get_bool("flag3") is True
    assert config.get_bool("flag4") is True
    assert config.get_bool("flag5") is True
    assert config.get_bool("flag6") is False
    assert config.get_bool("flag7") is False
    assert config.get_bool("missing", True) is True


def test_config_has() -> None:
    """Test Config has method."""
    config = Config({"name": "test"})
    assert config.has("name") is True
    assert config.has("missing") is False


def test_config_to_dict() -> None:
    """Test Config to_dict."""
    data = {"name": "test"}
    config = Config(data)
    assert config.to_dict() == data


# ===== ConfigLoader tests =====
def test_loader_set_defaults() -> None:
    """Test setting defaults."""
    loader = ConfigLoader()
    loader.set_defaults({"key": "value"})
    config = loader.get_config()
    assert config.get("key") == "value"


def test_loader_load_from_file() -> None:
    """Test loading from JSON file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"name": "from_file"}, f)
        filepath = f.name
    
    try:
        loader = ConfigLoader()
        loader.set_defaults({"name": "default"})
        loader.load_from_file(filepath)
        config = loader.get_config()
        assert config.get("name") == "from_file"
    finally:
        os.unlink(filepath)


def test_loader_missing_file_ignored() -> None:
    """Test that missing files are silently ignored."""
    loader = ConfigLoader()
    loader.set_defaults({"key": "value"})
    loader.load_from_file("/nonexistent/path/config.json")
    config = loader.get_config()
    assert config.get("key") == "value"


def test_loader_merge_order() -> None:
    """Test that file overrides defaults."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"override": "file_value"}, f)
        filepath = f.name
    
    try:
        loader = ConfigLoader()
        loader.set_defaults({"default": "def_value", "override": "def_value"})
        loader.load_from_file(filepath)
        config = loader.get_config()
        assert config.get("default") == "def_value"
        assert config.get("override") == "file_value"
    finally:
        os.unlink(filepath)


def test_loader_load_from_env() -> None:
    """Test loading from environment variables."""
    # Set test env vars
    os.environ["CONFIG_TEST_KEY"] = "env_value"
    os.environ["CONFIG_DATABASE__HOST"] = "localhost"
    os.environ["CONFIG_DATABASE__PORT"] = "5432"
    
    try:
        loader = ConfigLoader()
        loader.set_defaults({"test_key": "default"})
        loader.load_from_env()
        config = loader.get_config()
        assert config.get("test_key") == "env_value"
        assert config.get("database.host") == "localhost"
        assert config.get("database.port") == "5432"
    finally:
        del os.environ["CONFIG_TEST_KEY"]
        del os.environ["CONFIG_DATABASE__HOST"]
        del os.environ["CONFIG_DATABASE__PORT"]


def test_loader_env_overrides_file() -> None:
    """Test that env vars override file config."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"priority": "file"}, f)
        filepath = f.name
    
    os.environ["CONFIG_PRIORITY"] = "env"
    
    try:
        loader = ConfigLoader()
        loader.load_from_file(filepath)
        loader.load_from_env()
        config = loader.get_config()
        assert config.get("priority") == "env"
    finally:
        os.unlink(filepath)
        del os.environ["CONFIG_PRIORITY"]


def test_loader_validate_required_success() -> None:
    """Test validation with all required keys present."""
    loader = ConfigLoader()
    loader.set_defaults({"key1": "value1", "key2": "value2"})
    # Should not raise
    loader.validate_required(["key1", "key2"])


def test_loader_validate_required_failure() -> None:
    """Test validation with missing keys."""
    loader = ConfigLoader()
    loader.set_defaults({"key1": "value1"})
    try:
        loader.validate_required(["key1", "missing_key"])
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "missing_key" in str(e)


def test_loader_nested_validation() -> None:
    """Test validation with nested keys."""
    loader = ConfigLoader()
    loader.set_defaults({"database": {"host": "localhost"}})
    loader.validate_required(["database.host"])
