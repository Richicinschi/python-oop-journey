"""Tests for Problem 13: Requires Decorator."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day03.problem_13_requires_decorator import (
    requires, User, read_data, write_data, delete_resource
)


class TestRequiresDecorator:
    """Tests for the requires decorator."""
    
    def test_requires_allows_with_single_permission(self) -> None:
        """Test that user with required permission is allowed."""
        user = User("Alice", {"read"})
        
        result = read_data(user)
        
        assert result == "Data for Alice"
    
    def test_requires_denies_without_permission(self) -> None:
        """Test that user without required permission is denied."""
        user = User("Bob", {"write"})  # Missing "read"
        
        with pytest.raises(PermissionError) as exc_info:
            read_data(user)
        
        assert "Missing permissions" in str(exc_info.value)
    
    def test_requires_multiple_permissions(self) -> None:
        """Test that all required permissions must be present."""
        user_with_both = User("Admin", {"write", "admin"})
        result = write_data(user_with_both, "test data")
        assert result == "Wrote 'test data' for Admin"
        
        user_with_one = User("Writer", {"write"})
        with pytest.raises(PermissionError):
            write_data(user_with_one, "test data")
    
    def test_requires_with_extra_permissions(self) -> None:
        """Test that extra permissions don't cause issues."""
        user = User("SuperUser", {"read", "write", "admin", "delete"})
        
        result = read_data(user)
        assert result == "Data for SuperUser"
    
    def test_requires_case_sensitive(self) -> None:
        """Test that permission names are case sensitive."""
        user = User("User", {"Read"})  # Capital R
        
        with pytest.raises(PermissionError):
            read_data(user)


class TestRequiresEdgeCases:
    """Tests for requires edge cases."""
    
    def test_requires_no_user_raises_error(self) -> None:
        """Test that missing user argument raises PermissionError."""
        
        @requires({"admin"})
        def admin_only(user: User) -> str:
            return "Admin only"
        
        with pytest.raises(PermissionError) as exc_info:
            admin_only()  # type: ignore
        
        assert "No user provided" in str(exc_info.value)
    
    def test_requires_user_without_permissions_attr(self) -> None:
        """Test user without permissions attribute."""
        
        class FakeUser:
            def __init__(self) -> None:
                self.name = "Fake"
        
        fake_user = FakeUser()
        
        @requires({"read"})
        def func(user) -> str:  # type: ignore
            return "ok"
        
        with pytest.raises(PermissionError) as exc_info:
            func(fake_user)
        
        # The decorator looks for 'permissions' attr; if not found, reports no user
        assert "No user provided" in str(exc_info.value) or "no permissions attribute" in str(exc_info.value)
    
    def test_requires_empty_permission_set(self) -> None:
        """Test with empty required permissions."""
        
        @requires(set())
        def no_requirements(user: User) -> str:
            return "Always allowed"
        
        user = User("Anyone", set())
        result = no_requirements(user)
        
        assert result == "Always allowed"
    
    def test_requires_preserves_function_name(self) -> None:
        """Test that requires preserves function name."""
        assert read_data.__name__ == "read_data"
