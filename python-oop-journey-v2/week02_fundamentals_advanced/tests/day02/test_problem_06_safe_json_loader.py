"""Tests for Problem 06: Safe JSON Loader."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from week02_fundamentals_advanced.solutions.day02.problem_06_safe_json_loader import (
    safe_json_loader,
)


def test_safe_json_loader_valid_file() -> None:
    """Test loading valid JSON file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"key": "value", "number": 42}, f)
        temp_path = f.name
    
    try:
        result = safe_json_loader(temp_path)
        assert result == {"key": "value", "number": 42}
    finally:
        Path(temp_path).unlink()


def test_safe_json_loader_file_not_found() -> None:
    """Test loading non-existent file returns empty dict."""
    result = safe_json_loader("/nonexistent/path/file.json")
    assert result == {}


def test_safe_json_loader_invalid_json() -> None:
    """Test loading invalid JSON returns empty dict."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("not valid json {{")
        temp_path = f.name
    
    try:
        result = safe_json_loader(temp_path)
        assert result == {}
    finally:
        Path(temp_path).unlink()


def test_safe_json_loader_empty_file() -> None:
    """Test loading empty file returns empty dict."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("")
        temp_path = f.name
    
    try:
        result = safe_json_loader(temp_path)
        assert result == {}
    finally:
        Path(temp_path).unlink()


def test_safe_json_loader_non_dict_json() -> None:
    """Test loading JSON array returns empty dict."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([1, 2, 3], f)
        temp_path = f.name
    
    try:
        result = safe_json_loader(temp_path)
        assert result == {}
    finally:
        Path(temp_path).unlink()


def test_safe_json_loader_nested_objects() -> None:
    """Test loading nested JSON objects."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"outer": {"inner": "value"}, "list": [1, 2, 3]}, f)
        temp_path = f.name
    
    try:
        result = safe_json_loader(temp_path)
        assert result == {"outer": {"inner": "value"}, "list": [1, 2, 3]}
    finally:
        Path(temp_path).unlink()


def test_safe_json_loader_path_object() -> None:
    """Test loading with Path object."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"test": "data"}, f)
        temp_path = Path(f.name)
    
    try:
        result = safe_json_loader(temp_path)
        assert result == {"test": "data"}
    finally:
        temp_path.unlink()


def test_safe_json_loader_empty_object() -> None:
    """Test loading empty JSON object."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({}, f)
        temp_path = f.name
    
    try:
        result = safe_json_loader(temp_path)
        assert result == {}
    finally:
        Path(temp_path).unlink()
