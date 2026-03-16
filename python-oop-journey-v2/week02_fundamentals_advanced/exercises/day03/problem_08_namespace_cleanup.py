"""Problem 08: Namespace Cleanup

Topic: Namespace management, selective imports, import patterns
Difficulty: Medium

Create a module that demonstrates proper namespace management. Implement
functions that help inspect and clean up Python namespaces, and show how
to selectively import to avoid namespace pollution.

Requirements:
    - Implement functions to inspect and manage module namespaces
    - get_module_public_names(module): Get public names from a module
    - get_module_all_names(module): Get __all__ if defined
    - filter_namespace(names, pattern): Filter names by glob pattern
    - ImportCleaner class to temporarily import and clean up
    - clean_namespace(globals_dict, keep_pattern): Remove imported names

Example:
    # Inspect a module
    import math
    public_names = get_module_public_names(math)
    print('pi' in public_names)  # True
    print('_something' in public_names)  # False (starts with _)
    
    # Temporary import with automatic cleanup
    with ImportCleaner() as cleaner:
        import tempfile
        # use tempfile...
    # tempfile is no longer in namespace
    
    # Clean up namespace selectively
    cleanup_namespace(globals(), keep_pattern=['main', 'app_*'])

Hints:
    * Hint 1: Use dir(module) to get all names, then filter with
      name.startswith('_') to identify private names. For __all__,
      use hasattr() and getattr() to safely check and retrieve it.
    
    * Hint 2: The ImportCleaner context manager should:
      - __enter__: Record current namespace keys (self.before = set(ns.keys()))
      - __exit__: Find new keys (set(ns.keys()) - self.before) and delete them
      - Support custom namespace or use caller's module via sys._getframe()
    
    * Hint 3: cleanup_namespace should use fnmatch for pattern matching.
      Keep builtins (names starting AND ending with '__') unless specified.
      Return a list of removed names for verification.

Debugging Tips:
    - "Name not found" errors: You may be deleting names while iterating
      over the dictionary - collect keys to delete first, then delete them
    - ImportCleaner not removing: Ensure you're tracking the same dict object
    - Pattern matching fails: fnmatch uses Unix shell-style wildcards (*, ?, [seq])
    - Modifying dict during iteration: This raises RuntimeError in Python 3.x
"""

from __future__ import annotations

import fnmatch
import sys
from types import ModuleType
from typing import Any, Dict, List, Optional, Set, Iterator


def get_module_public_names(module: ModuleType) -> List[str]:
    """Get all public names from a module.
    
    Public names are those that don't start with underscore.
    
    Args:
        module: The module to inspect
        
    Returns:
        Sorted list of public attribute names
    """
    raise NotImplementedError("Implement get_module_public_names")


def get_module_all_names(module: ModuleType) -> Optional[List[str]]:
    """Get the __all__ list from a module if defined.
    
    Args:
        module: The module to inspect
        
    Returns:
        List of names in __all__, or None if not defined
    """
    raise NotImplementedError("Implement get_module_all_names")


def get_module_imported_names(module: ModuleType) -> List[str]:
    """Get names that were imported from other modules.
    
    Heuristic: Check if attribute has different __module__.
    
    Args:
        module: The module to inspect
        
    Returns:
        List of imported attribute names
    """
    raise NotImplementedError("Implement get_module_imported_names")


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
    raise NotImplementedError("Implement filter_namespace")


def get_namespace_summary(globals_dict: Dict[str, Any]) -> Dict[str, List[str]]:
    """Get a summary of a namespace categorized by type.
    
    Args:
        globals_dict: The globals() dictionary to analyze
        
    Returns:
        Dictionary with keys: 'modules', 'functions', 'classes', 
        'variables', 'private'
    """
    raise NotImplementedError("Implement get_namespace_summary")


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
        raise NotImplementedError("Implement __init__")
    
    def __enter__(self) -> ImportCleaner:
        """Enter context, record current namespace state."""
        raise NotImplementedError("Implement __enter__")
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context, remove newly added names."""
        raise NotImplementedError("Implement __exit__")
    
    def get_added_names(self) -> Set[str]:
        """Get names that were added during the context.
        
        Returns:
            Set of names added to namespace
        """
        raise NotImplementedError("Implement get_added_names")


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
    raise NotImplementedError("Implement cleanup_namespace")


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
    raise NotImplementedError("Implement selective_import")
