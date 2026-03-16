"""Tests for Problem 04: Request Context."""

from __future__ import annotations

from typing import Any

import pytest

from week07_real_world.solutions.day05.problem_04_request_context import (
    Logger,
    RequestContext,
    RequestContextManager,
    RequestStatus,
    UserInfo,
)


class MockLogger(Logger):
    """Mock logger for testing."""
    
    def __init__(self) -> None:
        self.info_logs: list[tuple[str, dict[str, Any]]] = []
        self.error_logs: list[tuple[str, dict[str, Any]]] = []
    
    def info(self, message: str, **kwargs: Any) -> None:
        self.info_logs.append((message, kwargs))
    
    def error(self, message: str, **kwargs: Any) -> None:
        self.error_logs.append((message, kwargs))


@pytest.fixture
def mock_logger() -> MockLogger:
    """Create a mock logger."""
    return MockLogger()


@pytest.fixture
def context_manager(mock_logger: MockLogger) -> RequestContextManager:
    """Create a RequestContextManager with mock logger."""
    return RequestContextManager(logger=mock_logger)


@pytest.fixture
def sample_user() -> UserInfo:
    """Create a sample user."""
    return UserInfo(user_id=123, username="alice", roles=("user", "admin"))


class TestUserInfo:
    """Tests for UserInfo class."""
    
    def test_is_authenticated_true(self) -> None:
        """Test is_authenticated with valid user ID."""
        user = UserInfo(user_id=123, username="alice")
        assert user.is_authenticated
    
    def test_is_authenticated_false(self) -> None:
        """Test is_authenticated with anonymous user."""
        user = UserInfo(user_id=0, username="anonymous")
        assert not user.is_authenticated
    
    def test_has_role_true(self) -> None:
        """Test has_role with existing role."""
        user = UserInfo(user_id=123, username="alice", roles=("admin",))
        assert user.has_role("admin")
    
    def test_has_role_false(self) -> None:
        """Test has_role with non-existent role."""
        user = UserInfo(user_id=123, username="alice", roles=("user",))
        assert not user.has_role("admin")


class TestRequestContext:
    """Tests for RequestContext class."""
    
    def test_create_generates_uuid(self) -> None:
        """Test that create generates a UUID request_id."""
        ctx = RequestContext.create()
        
        assert len(ctx.request_id) == 36  # UUID format
        assert "-" in ctx.request_id
    
    def test_create_with_user_info(self, sample_user: UserInfo) -> None:
        """Test creation with user info."""
        ctx = RequestContext.create(user_info=sample_user)
        
        assert ctx.user_info == sample_user
        assert ctx.is_authenticated
    
    def test_create_defaults_to_anonymous(self) -> None:
        """Test that create defaults to anonymous user."""
        ctx = RequestContext.create()
        
        assert ctx.user_info.user_id == 0
        assert ctx.user_info.username == "anonymous"
        assert not ctx.is_authenticated
    
    def test_create_with_correlation_id(self) -> None:
        """Test creation with correlation ID."""
        ctx = RequestContext.create(correlation_id="corr-123")
        
        assert ctx.correlation_id == "corr-123"
    
    def test_create_with_metadata(self) -> None:
        """Test creation with metadata."""
        meta = {"key": "value"}
        ctx = RequestContext.create(metadata=meta)
        
        assert ctx.metadata["key"] == "value"
    
    def test_status_starts_pending(self) -> None:
        """Test that new context starts with PENDING status."""
        ctx = RequestContext.create()
        
        assert ctx.status == RequestStatus.PENDING
    
    def test_with_status_creates_new_context(self) -> None:
        """Test that with_status creates new context."""
        ctx = RequestContext.create()
        new_ctx = ctx.with_status(RequestStatus.PROCESSING)
        
        assert new_ctx.status == RequestStatus.PROCESSING
        assert ctx.status == RequestStatus.PENDING  # Original unchanged
    
    def test_is_complete_pending(self) -> None:
        """Test is_complete with PENDING status."""
        ctx = RequestContext.create()
        assert not ctx.is_complete
    
    def test_is_complete_completed(self) -> None:
        """Test is_complete with COMPLETED status."""
        ctx = RequestContext.create().with_status(RequestStatus.COMPLETED)
        assert ctx.is_complete
    
    def test_is_complete_failed(self) -> None:
        """Test is_complete with FAILED status."""
        ctx = RequestContext.create().with_status(RequestStatus.FAILED)
        assert ctx.is_complete
    
    def test_with_metadata_creates_new_context(self) -> None:
        """Test that with_metadata creates new context."""
        ctx = RequestContext.create()
        new_ctx = ctx.with_metadata("new_key", "new_value")
        
        assert new_ctx.metadata["new_key"] == "new_value"
        assert "new_key" not in ctx.metadata  # Original unchanged
    
    def test_with_metadata_preserves_existing(self) -> None:
        """Test that with_metadata preserves existing metadata."""
        ctx = RequestContext.create(metadata={"old": "value"})
        new_ctx = ctx.with_metadata("new", "new_value")
        
        assert new_ctx.metadata["old"] == "value"
        assert new_ctx.metadata["new"] == "new_value"
    
    def test_duration_ms_increases(self) -> None:
        """Test that duration_ms increases over time."""
        import time
        
        ctx = RequestContext.create()
        duration1 = ctx.duration_ms
        
        time.sleep(0.01)  # Small delay
        duration2 = ctx.duration_ms
        
        assert duration2 >= duration1
    
    def test_get_set_current(self) -> None:
        """Test getting and setting current context."""
        ctx = RequestContext.create()
        
        # Set current
        token = RequestContext.set_current(ctx)
        
        # Get current
        current = RequestContext.get_current()
        assert current == ctx
        
        # Reset
        RequestContext.set_current(None)


class TestRequestContextManager:
    """Tests for RequestContextManager class."""
    
    def test_start_request_creates_context(
        self,
        context_manager: RequestContextManager,
        mock_logger: MockLogger,
    ) -> None:
        """Test that start_request creates a context."""
        ctx = context_manager.start_request()
        
        assert ctx.status == RequestStatus.PROCESSING
        assert ctx.request_id is not None
    
    def test_start_request_sets_current(
        self,
        context_manager: RequestContextManager,
    ) -> None:
        """Test that start_request sets context as current."""
        ctx = context_manager.start_request()
        
        current = RequestContext.get_current()
        assert current == ctx
        
        # Cleanup
        RequestContext.set_current(None)
    
    def test_start_request_logs(
        self,
        context_manager: RequestContextManager,
        mock_logger: MockLogger,
        sample_user: UserInfo,
    ) -> None:
        """Test that start_request logs the request."""
        ctx = context_manager.start_request(user_info=sample_user)
        
        assert len(mock_logger.info_logs) == 1
        message, kwargs = mock_logger.info_logs[0]
        assert "started" in message
        assert kwargs["request_id"] == ctx.request_id
        assert kwargs["user_id"] == 123
        assert kwargs["username"] == "alice"
    
    def test_complete_request_updates_status(
        self,
        context_manager: RequestContextManager,
    ) -> None:
        """Test that complete_request updates status."""
        ctx = context_manager.start_request()
        completed = context_manager.complete_request(ctx)
        
        assert completed.status == RequestStatus.COMPLETED
        assert completed.is_complete
    
    def test_complete_request_logs(
        self,
        context_manager: RequestContextManager,
        mock_logger: MockLogger,
    ) -> None:
        """Test that complete_request logs completion."""
        ctx = context_manager.start_request()
        context_manager.complete_request(ctx)
        
        assert len(mock_logger.info_logs) == 2
        message, kwargs = mock_logger.info_logs[1]
        assert "completed" in message
        assert "duration_ms" in kwargs
    
    def test_fail_request_updates_status(
        self,
        context_manager: RequestContextManager,
    ) -> None:
        """Test that fail_request updates status."""
        ctx = context_manager.start_request()
        failed = context_manager.fail_request(ctx, "Something went wrong")
        
        assert failed.status == RequestStatus.FAILED
        assert failed.is_complete
    
    def test_fail_request_logs_error(
        self,
        context_manager: RequestContextManager,
        mock_logger: MockLogger,
    ) -> None:
        """Test that fail_request logs error."""
        ctx = context_manager.start_request()
        context_manager.fail_request(ctx, Exception("Test error"))
        
        assert len(mock_logger.error_logs) == 1
        message, kwargs = mock_logger.error_logs[0]
        assert "failed" in message
        assert "error" in kwargs
        assert "Test error" in kwargs["error"]
    
    def test_log_info_includes_context(
        self,
        context_manager: RequestContextManager,
        mock_logger: MockLogger,
    ) -> None:
        """Test that log_info includes context info."""
        ctx = context_manager.start_request()
        context_manager.log_info("Test message", extra_field="extra")
        
        # Should have start log and our log
        assert len(mock_logger.info_logs) == 2
        message, kwargs = mock_logger.info_logs[1]
        assert message == "Test message"
        assert kwargs["request_id"] == ctx.request_id
        assert kwargs["user_id"] == ctx.user_info.user_id
        assert kwargs["extra_field"] == "extra"
    
    def test_log_info_without_context(
        self,
        context_manager: RequestContextManager,
        mock_logger: MockLogger,
    ) -> None:
        """Test log_info when no context is set."""
        # Ensure no context is set
        RequestContext.set_current(None)
        
        context_manager.log_info("Test message")
        
        assert len(mock_logger.info_logs) == 1
        message, kwargs = mock_logger.info_logs[0]
        assert message == "Test message"
        # Should not have request_id or user_id
        assert "request_id" not in kwargs
    
    def test_log_error_includes_context(
        self,
        context_manager: RequestContextManager,
        mock_logger: MockLogger,
    ) -> None:
        """Test that log_error includes context info."""
        ctx = context_manager.start_request()
        context_manager.log_error("Error message")
        
        assert len(mock_logger.error_logs) == 1
        message, kwargs = mock_logger.error_logs[0]
        assert message == "Error message"
        assert kwargs["request_id"] == ctx.request_id
    
    def test_get_current_context(
        self,
        context_manager: RequestContextManager,
    ) -> None:
        """Test getting current context through manager."""
        ctx = context_manager.start_request()
        
        current = context_manager.get_current_context()
        assert current == ctx
        
        # Cleanup
        RequestContext.set_current(None)
    
    def test_get_current_context_none(
        self,
        context_manager: RequestContextManager,
    ) -> None:
        """Test getting current context when none is set."""
        RequestContext.set_current(None)
        
        current = context_manager.get_current_context()
        assert current is None
