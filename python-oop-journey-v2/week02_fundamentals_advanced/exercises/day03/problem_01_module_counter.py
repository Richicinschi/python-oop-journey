"""Problem 01: Module Counter

Topic: Module-level state, import tracking
Difficulty: Easy

Create a module that tracks how many times it has been imported
across the entire program. The counter should persist and increment
each time the module is imported (in different files).

Requirements:
    - Create a module-level variable to track import count
    - Provide get_import_count() to retrieve current count
    - Provide reset_import_count() to reset to zero
    - The counter increments each time the module is loaded

Example:
    # First import in any file
    import problem_01_module_counter
    print(get_import_count())  # 1
    
    # In another file, when imported again
    import problem_01_module_counter
    print(get_import_count())  # 2 (same module, count persists)

Note: In practice, Python only loads a module once per interpreter session.
This exercise simulates tracking that single load event.
"""

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
    raise NotImplementedError("Implement get_import_count")


def reset_import_count() -> None:
    """Reset the import counter to zero."""
    raise NotImplementedError("Implement reset_import_count")
