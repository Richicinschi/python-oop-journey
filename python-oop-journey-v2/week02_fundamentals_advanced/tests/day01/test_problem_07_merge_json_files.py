"""Tests for Problem 07: Merge JSON Files."""

from __future__ import annotations

import json
import pytest

from week02_fundamentals_advanced.solutions.day01.problem_07_merge_json_files import merge_json_files

import os
import shutil
from pathlib import Path

# Environment workaround for tmp_path permission issues
@pytest.fixture
def safe_tmp_path(monkeypatch):
    """Provide a temporary path that works in restricted environments."""
    test_dir = Path(os.getcwd()) / '.test_tmp'
    test_dir.mkdir(exist_ok=True)
    try:
        yield test_dir
    finally:
        if test_dir.exists():
            shutil.rmtree(test_dir, ignore_errors=True)



def test_merge_json_files_basic(safe_tmp_path) -> None:
    """Test basic JSON file merging."""
    file1 = safe_tmp_path / "a.json"
    file2 = safe_tmp_path / "b.json"
    
    file1.write_text(json.dumps({"name": "app", "debug": True}))
    file2.write_text(json.dumps({"port": 8080, "debug": False}))
    
    result = merge_json_files([file1, file2])
    
    assert result["name"] == "app"
    assert result["port"] == 8080
    assert result["debug"] == False  # Later file overrides
    assert result["_merged_count"] == 2


def test_merge_json_files_empty_list() -> None:
    """Test merging empty list."""
    result = merge_json_files([])
    assert result == {"_merged_count": 0}


def test_merge_json_files_single_file(safe_tmp_path) -> None:
    """Test merging single file."""
    file1 = safe_tmp_path / "config.json"
    file1.write_text(json.dumps({"key": "value"}))
    
    result = merge_json_files([file1])
    
    assert result["key"] == "value"
    assert result["_merged_count"] == 1


def test_merge_json_files_skips_nonexistent(safe_tmp_path) -> None:
    """Test that non-existent files are skipped."""
    file1 = safe_tmp_path / "exists.json"
    file1.write_text(json.dumps({"key": "value"}))
    
    result = merge_json_files([file1, safe_tmp_path / "nonexistent.json"])
    
    assert result["key"] == "value"
    assert result["_merged_count"] == 1


def test_merge_json_files_skips_invalid_json(safe_tmp_path) -> None:
    """Test that invalid JSON files are skipped."""
    file1 = safe_tmp_path / "valid.json"
    file2 = safe_tmp_path / "invalid.json"
    
    file1.write_text(json.dumps({"key": "value"}))
    file2.write_text("not valid json")
    
    result = merge_json_files([file1, file2])
    
    assert result["key"] == "value"
    assert result["_merged_count"] == 1


def test_merge_json_files_all_invalid(safe_tmp_path) -> None:
    """Test when all files are invalid."""
    file1 = safe_tmp_path / "a.json"
    file2 = safe_tmp_path / "b.json"
    
    file1.write_text("invalid")
    file2.write_text("also invalid")
    
    result = merge_json_files([file1, file2])
    
    assert result == {"_merged_count": 0}


def test_merge_json_files_non_dict_content(safe_tmp_path) -> None:
    """Test that non-dict JSON content is handled."""
    file1 = safe_tmp_path / "list.json"
    file1.write_text(json.dumps([1, 2, 3]))
    
    result = merge_json_files([file1])
    
    assert result == {"_merged_count": 0}


def test_merge_json_files_nested_dicts(safe_tmp_path) -> None:
    """Test merging nested dictionaries (shallow merge)."""
    file1 = safe_tmp_path / "a.json"
    file2 = safe_tmp_path / "b.json"
    
    file1.write_text(json.dumps({"config": {"debug": True}}))
    file2.write_text(json.dumps({"config": {"port": 8080}}))
    
    result = merge_json_files([file1, file2])
    
    # Shallow merge - second config replaces first entirely
    assert result["config"] == {"port": 8080}
    assert result["_merged_count"] == 2
