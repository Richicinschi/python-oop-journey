"""Reference solution for Problem 01: Module Counter."""

from __future__ import annotations

# Module-level counter variable
_import_count: int = 0


def _increment_on_import() -> None:
    """Increment the import counter. Called when module is loaded."""
    global _import_count
    _import_count += 1


# Increment counter when this module is loaded
_increment_on_import()


def get_import_count() -> int:
    """Return the number of times this module has been imported.
    
    Returns:
        The current import count
    """
    return _import_count


def reset_import_count() -> None:
    """Reset the import counter to zero."""
    global _import_count
    _import_count = 0
