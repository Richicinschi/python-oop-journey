"""Problem 05: Configure Settings

Topic: Function Parameters - Combined Parameter Types
Difficulty: Medium

Write a function that configures application settings.

Function Signature:
    def configure_settings(
        app_name: str,
        debug: bool = False,
        **options: str | int | bool
    ) -> dict[str, str | int | bool]

Requirements:
    - app_name is required
    - debug has default False
    - **options captures additional settings
    - Return complete settings dictionary

Behavior Notes:
    - Combine required param, default param, and kwargs
    - Return dict with all settings
    - The debug param should be in the returned dict

Examples:
    >>> configure_settings("MyApp", debug=True, host="localhost", port=8080)
    {'app_name': 'MyApp', 'debug': True, 'host': 'localhost', 'port': 8080}
    
    Minimal config:
    >>> configure_settings("SimpleApp")
    {'app_name': 'SimpleApp', 'debug': False}
    
    With options:
    >>> configure_settings("WebApp", timeout=30, retries=3)
    {'app_name': 'WebApp', 'debug': False, 'timeout': 30, 'retries': 3}

Input Validation:
    - You may assume app_name is a string
    - debug is a boolean
    - options values are str, int, or bool

"""

from __future__ import annotations


def configure_settings(
    app_name: str,
    debug: bool = False,
    **options: str | int | bool
) -> dict[str, str | int | bool]:
    """Configure application settings.

    Args:
        app_name: The application name (required).
        debug: Debug mode flag (default False).
        **options: Additional configuration options.

    Returns:
        A dictionary with all settings.
    """
    raise NotImplementedError("Implement configure_settings")
