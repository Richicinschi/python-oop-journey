"""Tests for Problem 02: Dynamic Method Router."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day06.problem_02_dynamic_method_router import (
    APIClientRouter,
    MethodRouter,
)


class TestMethodRouter:
    """Tests for the MethodRouter class."""
    
    def test_init(self) -> None:
        """Test router initialization."""
        router = MethodRouter()
        assert router.list_prefixes() == []
    
    def test_register_prefix(self) -> None:
        """Test registering a prefix handler."""
        router = MethodRouter()
        handler = lambda *args: f"handled: {args}"
        
        router.register_prefix("get", handler)
        
        assert "get" in router.list_prefixes()
    
    def test_dynamic_method_call_simple(self) -> None:
        """Test calling a dynamically routed method."""
        router = MethodRouter()
        router.register_prefix("get", lambda *parts: f"Getting: {' '.join(parts)}")
        
        result = router.get_user()
        
        assert result == "Getting: user"
    
    def test_dynamic_method_call_with_args(self) -> None:
        """Test calling a dynamically routed method with additional args."""
        router = MethodRouter()
        router.register_prefix("get", lambda *args: f"Getting: {args}")
        
        result = router.get_user(123, "extra")
        
        assert "user" in str(result)
        assert "123" in str(result)
    
    def test_dynamic_method_call_nested(self) -> None:
        """Test calling with nested name (multiple underscores)."""
        router = MethodRouter()
        router.register_prefix("get", lambda *parts: parts)
        
        result = router.get_user_profile_settings()
        
        assert result == ("user", "profile", "settings")
    
    def test_multiple_prefixes(self) -> None:
        """Test multiple registered prefixes."""
        router = MethodRouter()
        router.register_prefix("get", lambda x: f"GET {x}")
        router.register_prefix("set", lambda x, y: f"SET {x}={y}")
        router.register_prefix("delete", lambda x: f"DELETE {x}")
        
        assert router.get_item() == "GET item"
        assert router.set_config("debug") == "SET config=debug"
        assert router.delete_user() == "DELETE user"
    
    def test_longest_prefix_match(self) -> None:
        """Test that longest prefix is matched first."""
        router = MethodRouter()
        router.register_prefix("get", lambda: "short")
        router.register_prefix("get_special", lambda: "long")
        
        # Should match the longer prefix
        result = router.get_special_item()
        assert result == "long"
        
        # Should match the shorter prefix
        result = router.get_normal()
        assert result == "short"
    
    def test_unregister(self) -> None:
        """Test unregistering a prefix."""
        router = MethodRouter()
        router.register_prefix("get", lambda: "test")
        
        assert router.unregister("get") is True
        assert router.unregister("get") is False
        assert "get" not in router.list_prefixes()
    
    def test_fallback_handler(self) -> None:
        """Test fallback handler for unmatched methods."""
        router = MethodRouter()
        router.register_fallback(
            lambda name, args: f"Fallback: {name}({args})"
        )
        
        result = router.undefined_method("arg1", "arg2")
        
        assert "Fallback" in result
        assert "undefined_method" in result
    
    def test_attribute_error_no_handler(self) -> None:
        """Test that AttributeError is raised with no matching handler."""
        router = MethodRouter()
        
        with pytest.raises(AttributeError) as exc_info:
            router.undefined_method()
        
        assert "undefined_method" in str(exc_info.value)
    
    def test_exact_prefix_match(self) -> None:
        """Test calling the exact prefix as method name."""
        router = MethodRouter()
        router.register_prefix("reset", lambda: "Resetting all")
        
        result = router.reset
        # Note: this returns a callable since it's accessed via __getattr__
        # The actual call happens when we invoke it
        result = router.reset()
        
        assert result == "Resetting all"


class TestAPIClientRouter:
    """Tests for the APIClientRouter class."""
    
    def test_init(self) -> None:
        """Test client initialization."""
        client = APIClientRouter("https://api.example.com")
        assert client.base_url == "https://api.example.com"
    
    def test_init_trailing_slash(self) -> None:
        """Test that trailing slash is removed from base_url."""
        client = APIClientRouter("https://api.example.com/")
        assert client.base_url == "https://api.example.com"
    
    def test_get_request(self) -> None:
        """Test GET request routing."""
        client = APIClientRouter("https://api.example.com")
        
        result = client.get_user()
        
        assert result == "GET https://api.example.com/user"
    
    def test_get_request_with_id(self) -> None:
        """Test GET request with path parameter."""
        client = APIClientRouter("https://api.example.com")
        
        result = client.get_user(123)
        
        assert result == "GET https://api.example.com/user/123"
    
    def test_post_request(self) -> None:
        """Test POST request routing."""
        client = APIClientRouter("https://api.example.com")
        
        result = client.create_order(item="book")
        
        assert "POST" in result
        assert "https://api.example.com/order" in result
        assert "item" in result
    
    def test_put_request(self) -> None:
        """Test PUT request routing."""
        client = APIClientRouter("https://api.example.com")
        
        result = client.update_user(123, name="Alice")
        
        assert "PUT" in result
        assert "user/123" in result
    
    def test_patch_request(self) -> None:
        """Test PATCH request routing."""
        client = APIClientRouter("https://api.example.com")
        
        result = client.patch_user(123, status="active")
        
        assert "PATCH" in result
    
    def test_delete_request(self) -> None:
        """Test DELETE request routing."""
        client = APIClientRouter("https://api.example.com")
        
        result = client.delete_user(123)
        
        assert "DELETE" in result
        assert "user/123" in result
    
    def test_alternative_prefixes(self) -> None:
        """Test alternative prefixes for same HTTP method."""
        client = APIClientRouter("https://api.example.com")
        
        # Both fetch and get should produce GET
        fetch_result = client.fetch_data()
        get_result = client.get_data()
        
        assert "GET" in fetch_result
        assert "GET" in get_result
        
        # Both create and post should produce POST
        create_result = client.create_item()
        post_result = client.post_item()
        
        assert "POST" in create_result
        assert "POST" in post_result
    
    def test_history_tracking(self) -> None:
        """Test that requests are recorded in history."""
        client = APIClientRouter("https://api.example.com")
        
        client.get_user(1)
        client.create_order(item="book")
        client.delete_user(1)
        
        history = client.get_history()
        
        assert len(history) == 3
        assert "GET" in history[0]
        assert "POST" in history[1]
        assert "DELETE" in history[2]
    
    def test_clear_history(self) -> None:
        """Test clearing request history."""
        client = APIClientRouter("https://api.example.com")
        
        client.get_user()
        client.clear_history()
        
        assert client.get_history() == []
    
    def test_attribute_error_invalid_method(self) -> None:
        """Test that invalid method names raise AttributeError."""
        client = APIClientRouter("https://api.example.com")
        
        with pytest.raises(AttributeError) as exc_info:
            client.invalid_method()
        
        assert "invalid_method" in str(exc_info.value)
    
    def test_nested_resource_path(self) -> None:
        """Test that underscores are converted to path separators."""
        client = APIClientRouter("https://api.example.com")
        
        result = client.get_user_profile_settings()
        
        assert "user/profile/settings" in result
