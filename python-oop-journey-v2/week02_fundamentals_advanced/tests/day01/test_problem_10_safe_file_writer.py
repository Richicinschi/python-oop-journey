"""Tests for Problem 10: Safe File Writer."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day01.problem_10_safe_file_writer import SafeFileWriter

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



def test_safe_writer_creates_file(safe_tmp_path) -> None:
    """Test that writer creates new file."""
    target = safe_tmp_path / "output.txt"
    
    with SafeFileWriter(target) as f:
        f.write("content")
    
    assert target.exists()
    assert target.read_text() == "content"


def test_safe_writer_overwrites_existing(safe_tmp_path) -> None:
    """Test that writer overwrites existing file on success."""
    target = safe_tmp_path / "output.txt"
    target.write_text("old content")
    
    with SafeFileWriter(target) as f:
        f.write("new content")
    
    assert target.read_text() == "new content"


def test_safe_writer_preserves_on_exception(safe_tmp_path) -> None:
    """Test that original file is preserved on exception."""
    target = safe_tmp_path / "output.txt"
    target.write_text("original content")
    
    try:
        with SafeFileWriter(target) as f:
            f.write("partial content")
            raise ValueError("Test error")
    except ValueError:
        pass
    
    assert target.read_text() == "original content"


def test_safe_writer_no_temp_file_on_exception(safe_tmp_path) -> None:
    """Test that temp file is cleaned up on exception."""
    target = safe_tmp_path / "output.txt"
    temp_file = safe_tmp_path / "output.txt.tmp"
    
    try:
        with SafeFileWriter(target) as f:
            f.write("content")
            raise ValueError("Test error")
    except ValueError:
        pass
    
    assert not temp_file.exists()


def test_safe_writer_returns_file_object(safe_tmp_path) -> None:
    """Test that context manager returns writable file object."""
    target = safe_tmp_path / "output.txt"
    
    with SafeFileWriter(target) as f:
        assert hasattr(f, 'write')
        f.write("test")


def test_safe_writer_multiple_writes(safe_tmp_path) -> None:
    """Test multiple writes to the file."""
    target = safe_tmp_path / "output.txt"
    
    with SafeFileWriter(target) as f:
        f.write("line1\n")
        f.write("line2\n")
    
    assert target.read_text() == "line1\nline2\n"


def test_safe_writer_with_json(safe_tmp_path) -> None:
    """Test writing JSON content."""
    import json
    target = safe_tmp_path / "config.json"
    
    with SafeFileWriter(target) as f:
        json.dump({"key": "value", "number": 42}, f)
    
    result = json.loads(target.read_text())
    assert result["key"] == "value"
    assert result["number"] == 42


def test_safe_writer_new_file_on_exception(safe_tmp_path) -> None:
    """Test that no file is created for new file on exception."""
    target = safe_tmp_path / "new_file.txt"
    
    try:
        with SafeFileWriter(target) as f:
            f.write("content")
            raise ValueError("Test error")
    except ValueError:
        pass
    
    assert not target.exists()
