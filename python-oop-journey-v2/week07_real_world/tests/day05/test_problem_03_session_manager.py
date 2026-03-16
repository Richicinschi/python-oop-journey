"""Tests for Problem 03: Session Manager."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import pytest

from week07_real_world.solutions.day05.problem_03_session_manager import (
    Session,
    SessionCreationResult,
    SessionManager,
    SessionStore,
)


class MockSessionStore(SessionStore):
    """Mock implementation of SessionStore for testing."""
    
    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}
        self._ttls: dict[str, int] = {}
    
    def save(self, session_id: str, session: Session, ttl: int) -> bool:
        self._sessions[session_id] = session
        self._ttls[session_id] = ttl
        return True
    
    def get(self, session_id: str) -> Session | None:
        return self._sessions.get(session_id)
    
    def delete(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            del self._ttls[session_id]
            return True
        return False
    
    def extend_ttl(self, session_id: str, additional_seconds: int) -> bool:
        session = self._sessions.get(session_id)
        if session is None:
            return False
        
        # Create new session with extended expiry
        new_expires = datetime.now() + timedelta(seconds=additional_seconds)
        new_session = Session(
            session_id=session.session_id,
            user_id=session.user_id,
            created_at=session.created_at,
            expires_at=new_expires,
            data=session.data,
        )
        self._sessions[session_id] = new_session
        self._ttls[session_id] += additional_seconds
        return True


class FailingSessionStore(SessionStore):
    """Mock store that always fails."""
    
    def save(self, session_id: str, session: Session, ttl: int) -> bool:
        return False
    
    def get(self, session_id: str) -> Session | None:
        return None
    
    def delete(self, session_id: str) -> bool:
        return False
    
    def extend_ttl(self, session_id: str, additional_seconds: int) -> bool:
        return False


@pytest.fixture
def session_manager() -> SessionManager:
    """Create a SessionManager with mock store."""
    return SessionManager(
        session_store=MockSessionStore(),
        default_ttl=3600,
    )


class TestSession:
    """Tests for Session dataclass."""
    
    def test_session_is_expired_true(self) -> None:
        """Test is_expired when session has expired."""
        session = Session(
            session_id="test",
            user_id=1,
            created_at=datetime.now() - timedelta(hours=2),
            expires_at=datetime.now() - timedelta(hours=1),
        )
        assert session.is_expired
    
    def test_session_is_expired_false(self) -> None:
        """Test is_expired when session is valid."""
        session = Session(
            session_id="test",
            user_id=1,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=1),
        )
        assert not session.is_expired
    
    def test_session_ttl_seconds(self) -> None:
        """Test ttl_seconds calculation."""
        session = Session(
            session_id="test",
            user_id=1,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(minutes=30),
        )
        # Allow for slight timing differences
        assert 1700 <= session.ttl_seconds <= 1800
    
    def test_session_ttl_seconds_expired(self) -> None:
        """Test ttl_seconds returns 0 for expired session."""
        session = Session(
            session_id="test",
            user_id=1,
            created_at=datetime.now() - timedelta(hours=2),
            expires_at=datetime.now() - timedelta(hours=1),
        )
        assert session.ttl_seconds == 0


class TestSessionManager:
    """Tests for SessionManager class."""
    
    def test_create_session_success(self, session_manager: SessionManager) -> None:
        """Test successful session creation."""
        result = session_manager.create_session(user_id=123)
        
        assert result.success
        assert result.session is not None
        assert result.session.user_id == 123
        assert len(result.session.session_id) >= 32
        assert not result.session.is_expired
    
    def test_create_session_with_data(
        self, session_manager: SessionManager
    ) -> None:
        """Test session creation with custom data."""
        data = {"ip": "127.0.0.1", "user_agent": "test"}
        result = session_manager.create_session(user_id=123, data=data)
        
        assert result.success
        assert result.session is not None
        assert result.session.data["ip"] == "127.0.0.1"
    
    def test_create_session_with_custom_ttl(
        self, session_manager: SessionManager
    ) -> None:
        """Test session creation with custom TTL."""
        result = session_manager.create_session(user_id=123, custom_ttl=7200)
        
        assert result.success
        assert result.session is not None
        # Session should be valid for at least 7000 seconds
        assert result.session.ttl_seconds >= 7000
    
    def test_create_session_store_failure(self) -> None:
        """Test session creation when store fails."""
        manager = SessionManager(
            session_store=FailingSessionStore(),
            default_ttl=3600,
        )
        result = manager.create_session(user_id=123)
        
        assert not result.success
        assert result.session is None
        assert "Failed to save" in result.error_message
    
    def test_validate_session_success(
        self, session_manager: SessionManager
    ) -> None:
        """Test validating a valid session."""
        create_result = session_manager.create_session(user_id=123)
        assert create_result.session is not None
        
        validated = session_manager.validate_session(
            create_result.session.session_id
        )
        
        assert validated is not None
        assert validated.user_id == 123
    
    def test_validate_session_not_found(
        self, session_manager: SessionManager
    ) -> None:
        """Test validating non-existent session."""
        result = session_manager.validate_session("invalid-id")
        
        assert result is None
    
    def test_validate_session_expired(self) -> None:
        """Test validating expired session."""
        store = MockSessionStore()
        manager = SessionManager(session_store=store, default_ttl=1)
        
        # Create a session
        result = manager.create_session(user_id=123)
        assert result.session is not None
        
        # Manually expire the session in store
        old_session = store._sessions[result.session.session_id]
        expired_session = Session(
            session_id=old_session.session_id,
            user_id=old_session.user_id,
            created_at=old_session.created_at,
            expires_at=datetime.now() - timedelta(seconds=1),
            data=old_session.data,
        )
        store._sessions[result.session.session_id] = expired_session
        
        # Validation should return None and delete the session
        validated = manager.validate_session(result.session.session_id)
        
        assert validated is None
        assert result.session.session_id not in store._sessions
    
    def test_invalidate_session_success(
        self, session_manager: SessionManager
    ) -> None:
        """Test successful session invalidation."""
        create_result = session_manager.create_session(user_id=123)
        assert create_result.session is not None
        
        success = session_manager.invalidate_session(
            create_result.session.session_id
        )
        
        assert success
        # Session should no longer exist
        assert session_manager.validate_session(
            create_result.session.session_id
        ) is None
    
    def test_invalidate_session_not_found(
        self, session_manager: SessionManager
    ) -> None:
        """Test invalidating non-existent session."""
        success = session_manager.invalidate_session("invalid-id")
        
        assert not success
    
    def test_refresh_session_success(
        self, session_manager: SessionManager
    ) -> None:
        """Test successful session refresh."""
        create_result = session_manager.create_session(user_id=123)
        assert create_result.session is not None
        
        original_expires = create_result.session.expires_at
        
        # Wait a tiny bit to ensure time difference
        import time
        time.sleep(0.01)
        
        refreshed = session_manager.refresh_session(
            create_result.session.session_id
        )
        
        assert refreshed is not None
        assert refreshed.expires_at > original_expires
    
    def test_refresh_session_not_found(
        self, session_manager: SessionManager
    ) -> None:
        """Test refreshing non-existent session."""
        result = session_manager.refresh_session("invalid-id")
        
        assert result is None
    
    def test_refresh_session_expired(self) -> None:
        """Test refreshing expired session."""
        store = MockSessionStore()
        manager = SessionManager(session_store=store, default_ttl=1)
        
        # Create and expire session
        result = manager.create_session(user_id=123)
        assert result.session is not None
        
        old_session = store._sessions[result.session.session_id]
        expired_session = Session(
            session_id=old_session.session_id,
            user_id=old_session.user_id,
            created_at=old_session.created_at,
            expires_at=datetime.now() - timedelta(seconds=1),
            data=old_session.data,
        )
        store._sessions[result.session.session_id] = expired_session
        
        refreshed = manager.refresh_session(result.session.session_id)
        
        assert refreshed is None
    
    def test_get_session_data_success(
        self, session_manager: SessionManager
    ) -> None:
        """Test getting session data."""
        result = session_manager.create_session(
            user_id=123,
            data={"key1": "value1", "key2": "value2"},
        )
        assert result.session is not None
        
        value = session_manager.get_session_data(
            result.session.session_id, "key1"
        )
        
        assert value == "value1"
    
    def test_get_session_data_not_found(
        self, session_manager: SessionManager
    ) -> None:
        """Test getting data from non-existent session."""
        value = session_manager.get_session_data("invalid-id", "key")
        
        assert value is None
    
    def test_get_session_data_key_not_found(
        self, session_manager: SessionManager
    ) -> None:
        """Test getting non-existent key from session."""
        result = session_manager.create_session(user_id=123, data={})
        assert result.session is not None
        
        value = session_manager.get_session_data(
            result.session.session_id, "missing"
        )
        
        assert value is None
    
    def test_set_session_data_success(
        self, session_manager: SessionManager
    ) -> None:
        """Test setting session data."""
        result = session_manager.create_session(user_id=123, data={})
        assert result.session is not None
        
        success = session_manager.set_session_data(
            result.session.session_id, "new_key", "new_value"
        )
        
        assert success
        
        # Verify data was set
        value = session_manager.get_session_data(
            result.session.session_id, "new_key"
        )
        assert value == "new_value"
    
    def test_set_session_data_not_found(
        self, session_manager: SessionManager
    ) -> None:
        """Test setting data on non-existent session."""
        success = session_manager.set_session_data("invalid-id", "key", "value")
        
        assert not success
    
    def test_set_session_data_preserves_existing(
        self, session_manager: SessionManager
    ) -> None:
        """Test that setting data preserves existing keys."""
        result = session_manager.create_session(
            user_id=123,
            data={"existing": "value"},
        )
        assert result.session is not None
        
        session_manager.set_session_data(
            result.session.session_id, "new", "new_value"
        )
        
        # Both keys should exist
        assert (
            session_manager.get_session_data(
                result.session.session_id, "existing"
            ) == "value"
        )
        assert (
            session_manager.get_session_data(
                result.session.session_id, "new"
            ) == "new_value"
        )
