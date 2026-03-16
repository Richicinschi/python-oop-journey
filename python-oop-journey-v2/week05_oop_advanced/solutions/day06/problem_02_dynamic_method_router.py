"""Reference solution for Problem 02: Dynamic Method Router."""

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
        self._handlers: dict[str, Callable[..., Any]] = {}
        self._fallback: Callable[[str, tuple[Any, ...]], Any] | None = None
    
    def register_prefix(
        self,
        prefix: str,
        handler: Callable[..., Any],
    ) -> None:
        """Register a handler for methods starting with a prefix.
        
        Args:
            prefix: The method name prefix (e.g., "get", "set").
            handler: Function to call when a matching method is invoked.
        """
        self._handlers[prefix] = handler
    
    def register_fallback(self, handler: Callable[[str, tuple[Any, ...]], Any]) -> None:
        """Register a fallback handler for unmatched method calls.
        
        Args:
            handler: Function called with (method_name, args) when no prefix matches.
        """
        self._fallback = handler
    
    def __getattr__(self, name: str) -> Callable[..., Any]:
        """Handle undefined attribute access by routing to registered handlers.
        
        Args:
            name: The attribute/method name being accessed.
        
        Returns:
            A callable that will invoke the appropriate handler.
        
        Raises:
            AttributeError: If no handler matches and no fallback is registered.
        """
        # Check for registered prefixes (longest first to avoid partial matches)
        for prefix in sorted(self._handlers.keys(), key=len, reverse=True):
            if name.startswith(prefix + '_') or name == prefix:
                handler = self._handlers[prefix]
                
                # Extract the suffix (rest of the method name after prefix)
                if name == prefix:
                    suffix = ''
                else:
                    suffix = name[len(prefix) + 1:]  # +1 for the underscore
                
                def make_caller(
                    h: Callable[..., Any] = handler,
                    s: str = suffix,
                ) -> Callable[..., Any]:
                    def caller(*args: Any, **kwargs: Any) -> Any:
                        if s:
                            # Split suffix by underscores and pass as first args
                            parts = s.split('_')
                            # Only pass parts if handler accepts them
                            try:
                                return h(*parts, *args, **kwargs)
                            except TypeError:
                                # Handler doesn't accept arguments, call without
                                return h(*args, **kwargs)
                        else:
                            return h(*args, **kwargs)
                    return caller
                
                return make_caller()
        
        # No prefix matched - use fallback if available
        if self._fallback is not None:
            def fallback_caller(*args: Any, **kwargs: Any) -> Any:
                return self._fallback(name, args)
            return fallback_caller
        
        # No handler found
        raise AttributeError(
            f"'{self.__class__.__name__}' has no attribute '{name}' "
            f"and no matching prefix handler"
        )
    
    def unregister(self, prefix: str) -> bool:
        """Unregister a prefix handler.
        
        Args:
            prefix: The prefix to unregister.
        
        Returns:
            True if a handler was removed, False otherwise.
        """
        if prefix in self._handlers:
            del self._handlers[prefix]
            return True
        return False
    
    def list_prefixes(self) -> list[str]:
        """List all registered prefixes.
        
        Returns:
            List of registered prefixes.
        """
        return list(self._handlers.keys())


class APIClientRouter:
    """A concrete example: API client with dynamic endpoint routing.
    
    Provides methods like get_user(), create_order(), delete_item(id), etc.
    dynamically based on HTTP verb prefixes.
    """
    
    HTTP_METHODS: dict[str, str] = {
        'get': 'GET',
        'fetch': 'GET',
        'create': 'POST',
        'post': 'POST',
        'add': 'POST',
        'update': 'PUT',
        'put': 'PUT',
        'modify': 'PUT',
        'patch': 'PATCH',
        'delete': 'DELETE',
        'remove': 'DELETE',
    }
    
    def __init__(self, base_url: str) -> None:
        """Initialize the API client.
        
        Args:
            base_url: The base URL for the API.
        """
        self.base_url = base_url.rstrip('/')
        self._history: list[str] = []
    
    def __getattr__(self, name: str) -> Callable[..., Any]:
        """Route API calls based on method name.
        
        Args:
            name: The method name (e.g., "get_user", "create_order").
        
        Returns:
            A function that makes the appropriate HTTP request.
        
        Raises:
            AttributeError: If the method name doesn't match any HTTP verb pattern.
        """
        # Find matching HTTP method
        method = None
        resource = None
        
        for prefix, http_method in self.HTTP_METHODS.items():
            if name.startswith(prefix + '_'):
                method = http_method
                resource = name[len(prefix) + 1:].replace('_', '/')
                break
            elif name == prefix:
                method = http_method
                resource = ''
                break
        
        if method is None:
            raise AttributeError(
                f"'{self.__class__.__name__}' has no attribute '{name}'. "
                f"Expected one of: "
                f"{', '.join(f'{v}_resource' for v in set(self.HTTP_METHODS.keys()))}"
            )
        
        def make_request(*args: Any, **kwargs: Any) -> str:
            """Make the HTTP request."""
            # Build URL
            url = f"{self.base_url}/{resource}"
            
            # Add path parameters from args
            if args:
                url += '/' + '/'.join(str(a) for a in args)
            
            # Build request description
            if kwargs:
                request_desc = f"{method} {url} with {kwargs}"
            else:
                request_desc = f"{method} {url}"
            
            # Record in history
            self._history.append(request_desc)
            
            return request_desc
        
        return make_request
    
    def get_history(self) -> list[str]:
        """Get the request history.
        
        Returns:
            List of requests made.
        """
        return self._history.copy()
    
    def clear_history(self) -> None:
        """Clear the request history."""
        self._history.clear()
