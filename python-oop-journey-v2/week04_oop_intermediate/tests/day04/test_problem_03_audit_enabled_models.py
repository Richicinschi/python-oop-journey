"""Tests for Problem 03: Audit Enabled Models."""

from __future__ import annotations

from datetime import datetime

import pytest

from week04_oop_intermediate.solutions.day04.problem_03_audit_enabled_models import (
    Auditable,
    Model,
    User,
    Versioned,
)


class TestAuditable:
    """Tests for the Auditable mixin."""
    
    def test_auditable_init(self) -> None:
        """Test that Auditable initializes _audit_trail."""
        
        class TestClass(Auditable):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        assert obj._audit_trail == []
        assert obj.get_audit_trail() == []
    
    def test_auditable_audit(self) -> None:
        """Test recording an audit entry."""
        
        class TestClass(Auditable):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        obj.audit("test_action", "test_user")
        
        trail = obj.get_audit_trail()
        assert len(trail) == 1
        assert trail[0]["action"] == "test_action"
        assert trail[0]["user"] == "test_user"
        assert isinstance(trail[0]["timestamp"], datetime)
    
    def test_auditable_audit_with_details(self) -> None:
        """Test recording an audit entry with details."""
        
        class TestClass(Auditable):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        details = {"key": "value", "count": 42}
        obj.audit("test", "user", details)
        
        trail = obj.get_audit_trail()
        assert trail[0]["details"] == details
    
    def test_auditable_get_changes_by_user(self) -> None:
        """Test filtering audit trail by user."""
        
        class TestClass(Auditable):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        obj.audit("action1", "alice")
        obj.audit("action2", "bob")
        obj.audit("action3", "alice")
        
        alice_changes = obj.get_changes_by_user("alice")
        assert len(alice_changes) == 2
        assert all(entry["user"] == "alice" for entry in alice_changes)
        
        bob_changes = obj.get_changes_by_user("bob")
        assert len(bob_changes) == 1
        assert bob_changes[0]["action"] == "action2"
    
    def test_auditable_get_audit_trail_returns_copy(self) -> None:
        """Test that get_audit_trail returns a copy."""
        
        class TestClass(Auditable):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        obj.audit("test", "user")
        
        trail1 = obj.get_audit_trail()
        trail2 = obj.get_audit_trail()
        
        assert trail1 is not trail2
        trail1.append({"hacked": True})
        assert len(obj.get_audit_trail()) == 1


class TestVersioned:
    """Tests for the Versioned mixin."""
    
    def test_versioned_init(self) -> None:
        """Test that Versioned initializes version and history."""
        
        class TestClass(Versioned):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        assert obj._version == 1
        assert obj.version == 1
        assert obj._version_history == []
    
    def test_versioned_bump_version(self) -> None:
        """Test bumping the version."""
        
        class TestClass(Versioned):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        obj.bump_version("Initial version")
        
        assert obj.version == 2
        history = obj.get_version_history()
        assert len(history) == 1
        assert history[0]["version"] == 1
        assert history[0]["description"] == "Initial version"
    
    def test_versioned_multiple_bumps(self) -> None:
        """Test multiple version bumps."""
        
        class TestClass(Versioned):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        obj.bump_version("Change 1")
        obj.bump_version("Change 2")
        obj.bump_version("Change 3")
        
        assert obj.version == 4
        assert len(obj.get_version_history()) == 3
    
    def test_versioned_rollback_to_version_valid(self) -> None:
        """Test rollback check for valid versions."""
        
        class TestClass(Versioned):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        obj.bump_version("Change 1")
        obj.bump_version("Change 2")
        
        assert obj.rollback_to_version(1) is True
        assert obj.rollback_to_version(2) is True
    
    def test_versioned_rollback_to_version_invalid(self) -> None:
        """Test rollback check for invalid versions."""
        
        class TestClass(Versioned):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        obj.bump_version("Change 1")
        
        assert obj.rollback_to_version(0) is False
        assert obj.rollback_to_version(2) is False  # Current version
        assert obj.rollback_to_version(5) is False
    
    def test_versioned_get_version_history_returns_copy(self) -> None:
        """Test that get_version_history returns a copy."""
        
        class TestClass(Versioned):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        obj.bump_version("Change")
        
        history1 = obj.get_version_history()
        history2 = obj.get_version_history()
        
        assert history1 is not history2


class TestModel:
    """Tests for the Model class."""
    
    def test_model_init(self) -> None:
        """Test Model initialization."""
        data = {"name": "Test", "value": 42}
        model = Model(1, data)
        
        assert model.id == 1
        assert model.get_data() == data
        assert model.get_data() is not data  # Should be a copy
    
    def test_model_init_creates_audit_entry(self) -> None:
        """Test that Model creation is audited."""
        data = {"name": "Test"}
        model = Model(1, data)
        
        trail = model.get_audit_trail()
        assert len(trail) == 1
        assert trail[0]["action"] == "created"
        assert trail[0]["user"] == "system"
    
    def test_model_init_starts_at_version_1(self) -> None:
        """Test that Model starts at version 1."""
        model = Model(1, {})
        assert model.version == 1
    
    def test_model_update(self) -> None:
        """Test updating model data."""
        model = Model(1, {"name": "Original"})
        
        model.update({"name": "Updated"}, "admin")
        
        assert model.get_data()["name"] == "Updated"
        assert model.version == 2
        
        trail = model.get_audit_trail()
        assert len(trail) == 2
        assert trail[1]["action"] == "updated"
        assert trail[1]["user"] == "admin"
    
    def test_model_multiple_updates(self) -> None:
        """Test multiple updates."""
        model = Model(1, {"a": 1, "b": 2})
        
        model.update({"a": 10}, "user1")
        model.update({"b": 20}, "user2")
        
        assert model.version == 3
        assert model.get_data() == {"a": 10, "b": 20}
    
    def test_model_mro(self) -> None:
        """Test Model's MRO."""
        expected_mro = (Model, Auditable, Versioned, object)
        assert Model.__mro__ == expected_mro


class TestUser:
    """Tests for the User class."""
    
    def test_user_init(self) -> None:
        """Test User initialization."""
        profile = {"email": "test@example.com", "role": "user"}
        user = User(1, "alice", profile)
        
        assert user.id == 1
        assert user.username == "alice"
        data = user.get_data()
        assert data["email"] == "test@example.com"
        assert data["active"] is True
    
    def test_user_is_active_default(self) -> None:
        """Test that users are active by default."""
        user = User(1, "alice", {})
        assert user.is_active() is True
    
    def test_user_deactivate(self) -> None:
        """Test deactivating a user."""
        user = User(1, "alice", {})
        
        user.deactivate("admin")
        
        assert user.is_active() is False
        assert user.get_data()["active"] is False
        
        # Check audit trail
        trail = user.get_audit_trail()
        assert any(entry["action"] == "deactivated" for entry in trail)
    
    def test_user_deactivate_bumps_version(self) -> None:
        """Test that deactivation bumps version."""
        user = User(1, "alice", {})
        initial_version = user.version
        
        user.deactivate("admin")
        
        assert user.version == initial_version + 1
    
    def test_user_update(self) -> None:
        """Test updating user data."""
        user = User(1, "alice", {"email": "old@example.com"})
        
        user.update({"email": "new@example.com"}, "alice")
        
        assert user.get_data()["email"] == "new@example.com"
        assert user.version == 2
    
    def test_user_get_changes_by_user(self) -> None:
        """Test getting changes by a specific user."""
        user = User(1, "alice", {"role": "user"})
        
        user.update({"role": "admin"}, "alice")
        user.deactivate("bob")
        
        alice_changes = user.get_changes_by_user("alice")
        assert len(alice_changes) == 1  # update only (creation is by "system")
        assert alice_changes[0]["action"] == "updated"
    
    def test_user_mro(self) -> None:
        """Test User's MRO."""
        expected_mro = (User, Model, Auditable, Versioned, object)
        assert User.__mro__ == expected_mro
