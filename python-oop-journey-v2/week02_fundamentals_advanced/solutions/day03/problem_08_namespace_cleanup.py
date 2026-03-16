"""Reference solution for Problem 08: Namespace Cleanup."""

from __future__ import annotations

import fnmatch
import sys
import importlib
from types import ModuleType, FunctionType
from typing import Any, Dict, List, Optional, Set, Iterator


def get_module_public_names(module: ModuleType) -> List[str]:
    """Get all public names from a module.
    
    Public names are those that don't start with underscore.
    
    Args:
        module: The module to inspect
        
    Returns:
        Sorted list of public attribute names
    """
    names = [name for name in dir(module) if not name.startswith("_")]
    return sorted(names)


def get_module_all_names(module: ModuleType) -> Optional[List[str]]:
    """Get the __all__ list from a module if defined.
    
    Args:
        module: The module to inspect
        
    Returns:
        List of names in __all__, or None if not defined
    """
    return getattr(module, "__all__", None)


def get_module_imported_names(module: ModuleType) -> List[str]:
    """Get names that were imported from other modules.
    
    Heuristic: Check if attribute has different __module__.
    
    Args:
        module: The module to inspect
        
    Returns:
        List of imported attribute names
    """
    module_name = module.__name__
    imported = []
    for name in dir(module):
        if name.startswith("_"):
            continue
        try:
            attr = getattr(module, name)
            attr_module = getattr(attr, "__module__", None)
            if attr_module and attr_module != module_name:
                imported.append(name)
        except Exception:
            pass
    return sorted(imported)


def filter_namespace(names: List[str], pattern: str) -> List[str]:
    """Filter a list of names by glob pattern.
    
    Args:
        names: List of names to filter
        pattern: Glob pattern (e.g., 'test_*', '*_utils')
        
    Returns:
        List of names matching the pattern
        
    Example:
        >>> filter_namespace(['test_foo', 'test_bar', 'util'], 'test_*')
        ['test_foo', 'test_bar']
    """
    return [name for name in names if fnmatch.fnmatch(name, pattern)]


def get_namespace_summary(globals_dict: Dict[str, Any]) -> Dict[str, List[str]]:
    """Get a summary of a namespace categorized by type.
    
    Args:
        globals_dict: The globals() dictionary to analyze
        
    Returns:
        Dictionary with keys: 'modules', 'functions', 'classes', 
        'variables', 'private'
    """
    summary: Dict[str, List[str]] = {
        "modules": [],
        "functions": [],
        "classes": [],
        "variables": [],
        "private": [],
    }
    
    for name, value in globals_dict.items():
        if name.startswith("_"):
            summary["private"].append(name)
        elif isinstance(value, ModuleType):
            summary["modules"].append(name)
        elif isinstance(value, type):
            summary["classes"].append(name)
        elif callable(value):
            summary["functions"].append(name)
        else:
            summary["variables"].append(name)
    
    # Sort each category
    for key in summary:
        summary[key].sort()
    
    return summary


class ImportCleaner:
    """Context manager for temporary imports with automatic cleanup.
    
    Tracks imports made while the context is active and removes them
    from the namespace on exit.
    
    Example:
        original_names = set(dir())
        with ImportCleaner() as cleaner:
            import json
            import os
            print(json.loads('{}'))  # Works fine
        # json and os no longer in module namespace
        
        # Alternative: specify target namespace
        with ImportCleaner(target_namespace=globals()):
            import tempfile
            # tempfile available here
        # tempfile removed from globals
    """
    
    def __init__(self, target_namespace: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the import cleaner.
        
        Args:
            target_namespace: Namespace to clean (defaults to caller's module)
        """
        self._target = target_namespace
        self._original_names: Set[str] = set()
    
    def __enter__(self) -> ImportCleaner:
        """Enter context, record current namespace state."""
        if self._target is None:
            # Get the caller's globals
            import inspect
            frame = inspect.currentframe()
            if frame and frame.f_back:
                self._target = frame.f_back.f_globals
        
        if self._target is not None:
            self._original_names = set(self._target.keys())
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context, remove newly added names."""
        if self._target is not None:
            current_names = set(self._target.keys())
            added = current_names - self._original_names
            for name in added:
                del self._target[name]
    
    def get_added_names(self) -> Set[str]:
        """Get names that were added during the context.
        
        Returns:
            Set of names added to namespace
        """
        if self._target is None:
            return set()
        current_names = set(self._target.keys())
        return current_names - self._original_names


def cleanup_namespace(
    namespace: Dict[str, Any], 
    keep: Optional[List[str]] = None,
    remove_patterns: Optional[List[str]] = None,
    keep_builtins: bool = True
) -> List[str]:
    """Clean up a namespace by removing selected names.
    
    Args:
        namespace: The namespace dictionary (usually globals())
        keep: List of names to always keep
        remove_patterns: Glob patterns for names to remove
        keep_builtins: Whether to keep names starting and ending with __
        
    Returns:
        List of names that were removed
        
    Example:
        # Remove all test_* names but keep test_main
        cleanup_namespace(
            globals(),
            keep=['test_main'],
            remove_patterns=['test_*']
        )
    """
    keep_set = set(keep or [])
    removed: List[str] = []
    
    names_to_check = list(namespace.keys())
    
    for name in names_to_check:
        # Skip if in keep list
        if name in keep_set:
            continue
        
        # Skip builtins if requested
        if keep_builtins and name.startswith("__") and name.endswith("__"):
            continue
        
        # Check if name matches any remove pattern
        should_remove = False
        if remove_patterns:
            for pattern in remove_patterns:
                if fnmatch.fnmatch(name, pattern):
                    should_remove = True
                    break
        
        # If no patterns specified, don't remove by default
        # (patterns must be explicitly provided)
        if remove_patterns and should_remove:
            del namespace[name]
            removed.append(name)
    
    return removed


def selective_import(
    module_name: str, 
    names: List[str],
    namespace: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Import specific names from a module into a namespace.
    
    Like 'from module import name1, name2' but programmatic.
    
    Args:
        module_name: Name of module to import from
        names: Names to import
        namespace: Target namespace (defaults to caller's globals)
        
    Returns:
        Dictionary of imported names
        
    Example:
        imported = selective_import('math', ['sin', 'cos', 'pi'])
        print(imported['sin'](0))  # 0.0
        print(imported['pi'])      # 3.14159...
    """
    if namespace is None:
        import inspect
        frame = inspect.currentframe()
        if frame and frame.f_back:
            namespace = frame.f_back.f_globals
        else:
            namespace = {}
    
    module = importlib.import_module(module_name)
    imported: Dict[str, Any] = {}
    
    for name in names:
        if hasattr(module, name):
            value = getattr(module, name)
            namespace[name] = value
            imported[name] = value
    
    return imported
