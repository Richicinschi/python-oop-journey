"""Problem 02: Dynamic Method Router.

Topic: __getattr__, Dynamic Dispatch
Difficulty: Medium

Implement a router that dynamically handles method calls based on method name patterns.

This is useful for:
- API clients that handle different endpoints dynamically
- Event handlers that route based on event type
- Plugin systems that register handlers dynamically
- Proxy objects that forward calls

Example:
    >>> router = MethodRouter()
    >>> router.register_prefix("get", lambda name: f"Getting {name}")
    >>> router.register_prefix("set", lambda name, value: f"Setting {name}={value}")
    
    >>> router.get_user()  # Dynamically routed
    'Getting user'
    
    >>> router.set_config("debug", True)  # Dynamically routed
    'Setting config=True'
    
    >>> router.handle_undefined()  # Falls back to default
    Raises AttributeError
"""

from __future__ import annotations

from typing import Any, Callable


class MethodRouter:
    """Routes method calls dynamically based on name patterns.
    
    This class allows registering handlers for method name prefixes.
    When an undefined method is called, it checks registered prefixes
    and routes to the appropriate handler.
    
    Attributes:
        _handlers: Mapping of prefixes to handler functions.
        _fallback: Optional fallback handler for unmatched calls.
    """
    
    def __init__(self) -> None:
        """Initialize the method router."""
        raise NotImplementedError("Implement __init__")
    
    def register_prefix(
        self,
        prefix: str,
        handler: Callable[..., Any],
    ) -> None:
        """Register a handler for methods starting with a prefix.
        
        The handler receives the rest of the method name (after the prefix)
        split by underscores, plus any additional arguments.
        
        Args:
            prefix: The method name prefix (e.g., "get", "set").
            handler: Function to call when a matching method is invoked.
        """
        raise NotImplementedError("Implement register_prefix")
    
    def register_fallback(self, handler: Callable[[str, tuple[Any, ...]], Any]) -> None:
        """Register a fallback handler for unmatched method calls.
        
        Args:
            handler: Function called with (method_name, args) when no prefix matches.
        """
        raise NotImplementedError("Implement register_fallback")
    
    def __getattr__(self, name: str) -> Callable[..., Any]:
        """Handle undefined attribute access by routing to registered handlers.
        
        This is called when an attribute is not found through normal lookup.
        
        Args:
            name: The attribute/method name being accessed.
        
        Returns:
            A callable that will invoke the appropriate handler.
        
        Raises:
            AttributeError: If no handler matches and no fallback is registered.
        """
        raise NotImplementedError("Implement __getattr__")
    
    def unregister(self, prefix: str) -> bool:
        """Unregister a prefix handler.
        
        Args:
            prefix: The prefix to unregister.
        
        Returns:
            True if a handler was removed, False otherwise.
        """
        raise NotImplementedError("Implement unregister")
    
    def list_prefixes(self) -> list[str]:
        """List all registered prefixes.
        
        Returns:
            List of registered prefixes.
        """
        raise NotImplementedError("Implement list_prefixes")


class APIClientRouter:
    """A concrete example: API client with dynamic endpoint routing.
    
    Provides methods like get_user(), create_order(), delete_item(id), etc.
    dynamically based on HTTP verb prefixes.
    
    Example:
        >>> client = APIClientRouter(base_url="https://api.example.com")
        >>> client.get_user(123)  # GET /users/123
        'GET https://api.example.com/users/123'
        >>> client.create_order({"item": "book"})  # POST /orders
        'POST https://api.example.com/orders with {"item": "book"}'
    """
    
    def __init__(self, base_url: str) -> None:
        """Initialize the API client.
        
        Args:
            base_url: The base URL for the API.
        """
        raise NotImplementedError("Implement __init__")
    
    def __getattr__(self, name: str) -> Callable[..., Any]:
        """Route API calls based on method name.
        
        Supported prefixes:
        - get_*: GET request
        - create_*, post_*: POST request
        - update_*, put_*: PUT request
        - patch_*: PATCH request
        - delete_*, remove_*: DELETE request
        
        Args:
            name: The method name (e.g., "get_user", "create_order").
        
        Returns:
            A function that makes the appropriate HTTP request.
        """
        raise NotImplementedError("Implement __getattr__")
