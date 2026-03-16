"""Tests for Problem 08: Namespace Cleanup."""

from __future__ import annotations

import math

from week02_fundamentals_advanced.solutions.day03.problem_08_namespace_cleanup import (
    get_module_public_names,
    get_module_all_names,
    filter_namespace,
    get_namespace_summary,
    ImportCleaner,
    cleanup_namespace,
    selective_import,
)


# ===== Module inspection tests =====
def test_get_module_public_names() -> None:
    """Test getting public names from a module."""
    names = get_module_public_names(math)
    assert "pi" in names
    assert "sin" in names
    assert "cos" in names
    # Private names should not be included
    assert not any(name.startswith("_") for name in names)


def test_get_module_all_names() -> None:
    """Test getting __all__ from a module."""
    # math module doesn't have __all__
    all_names = get_module_all_names(math)
    # May be None or a list depending on Python version
    assert all_names is None or isinstance(all_names, list)


def test_filter_namespace() -> None:
    """Test filtering namespace names."""
    names = ["test_foo", "test_bar", "util", "helper"]
    
    result = filter_namespace(names, "test_*")
    assert result == ["test_foo", "test_bar"]
    
    result = filter_namespace(names, "*il")
    assert result == ["util"]
    
    result = filter_namespace(names, "*")
    assert result == names


# ===== Namespace summary tests =====
def test_get_namespace_summary() -> None:
    """Test namespace summary."""
    test_ns = {
        "my_var": 42,
        "my_func": lambda: None,
        "MyClass": type("MyClass", (), {}),
        "_private": "secret",
        "math": math,
    }
    
    summary = get_namespace_summary(test_ns)
    
    assert "my_var" in summary["variables"]
    assert "my_func" in summary["functions"]
    assert "MyClass" in summary["classes"]
    assert "_private" in summary["private"]
    assert "math" in summary["modules"]


# ===== ImportCleaner tests =====
def test_import_cleaner_removes_imports() -> None:
    """Test that ImportCleaner removes added imports."""
    namespace: dict = {}
    
    with ImportCleaner(namespace) as cleaner:
        namespace["test_value"] = 42
        # Verify it was added
        assert "test_value" in namespace
    
    # After exit, should be removed
    assert "test_value" not in namespace


def test_import_cleaner_get_added_names() -> None:
    """Test getting names added during context."""
    namespace = {"existing": "value"}
    
    with ImportCleaner(namespace) as cleaner:
        namespace["new1"] = 1
        namespace["new2"] = 2
        added = cleaner.get_added_names()
    
    assert "new1" in added
    assert "new2" in added
    assert "existing" not in added


def test_import_cleaner_preserves_existing() -> None:
    """Test that ImportCleaner preserves pre-existing names."""
    namespace = {"existing": "value"}
    
    with ImportCleaner(namespace):
        namespace["new"] = "new_value"
    
    assert "existing" in namespace
    assert namespace["existing"] == "value"


# ===== cleanup_namespace tests =====
def test_cleanup_namespace_with_pattern() -> None:
    """Test cleanup with pattern matching."""
    namespace = {
        "test_func": lambda: None,
        "test_var": 42,
        "keep_this": "value",
        "main": "important",
    }
    
    removed = cleanup_namespace(namespace, remove_patterns=["test_*"])
    
    assert "test_func" in removed
    assert "test_var" in removed
    assert "test_func" not in namespace
    assert "keep_this" in namespace


def test_cleanup_namespace_keep_list() -> None:
    """Test cleanup with keep list."""
    namespace = {
        "test_main": "value",
        "test_other": "other",
        "regular": "value",
    }
    
    removed = cleanup_namespace(
        namespace,
        keep=["test_main"],
        remove_patterns=["test_*"]
    )
    
    assert "test_other" in removed
    assert "test_main" in namespace  # Should be kept


def test_cleanup_namespace_keep_builtins() -> None:
    """Test that builtins are preserved by default."""
    namespace = {
        "__name__": "test",
        "__file__": "test.py",
        "regular": "value",
    }
    
    cleanup_namespace(namespace, remove_patterns=["*"])
    
    assert "__name__" in namespace
    assert "__file__" in namespace


# ===== selective_import tests =====
def test_selective_import() -> None:
    """Test selective import functionality."""
    namespace: dict = {}
    
    imported = selective_import("math", ["sin", "cos", "pi"], namespace)
    
    assert "sin" in namespace
    assert "cos" in namespace
    assert "pi" in namespace
    assert "tan" not in namespace
    
    assert "sin" in imported
    assert callable(imported["sin"])
    assert imported["pi"] == math.pi


def test_selective_import_returns_dict() -> None:
    """Test that selective_import returns the imported names."""
    imported = selective_import("math", ["sqrt", "e"], {})
    
    assert isinstance(imported, dict)
    assert len(imported) == 2
    assert "sqrt" in imported
    assert "e" in imported
