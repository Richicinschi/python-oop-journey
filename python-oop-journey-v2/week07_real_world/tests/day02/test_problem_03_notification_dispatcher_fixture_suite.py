"""Tests for Problem 03: Notification Dispatcher Fixture Suite."""

from __future__ import annotations

from typing import Generator
from unittest.mock import Mock, patch

import pytest

from week07_real_world.solutions.day02.problem_03_notification_dispatcher_fixture_suite import (
    DispatchResult,
    EmailProvider,
    Notification,
    NotificationChannel,
    NotificationDispatcher,
    NotificationPriority,
    NotificationProvider,
    PushProvider,
    SMSProvider,
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def dispatcher() -> NotificationDispatcher:
    """Fresh dispatcher instance for each test."""
    return NotificationDispatcher()


@pytest.fixture
def email_provider() -> EmailProvider:
    """Configured email provider."""
    return EmailProvider(failure_rate=0.0)


@pytest.fixture
def sms_provider() -> SMSProvider:
    """Configured SMS provider."""
    return SMSProvider(failure_rate=0.0)


@pytest.fixture
def push_provider() -> PushProvider:
    """Configured push provider."""
    return PushProvider(requires_ack=False)


@pytest.fixture
def fully_configured_dispatcher(
    dispatcher: NotificationDispatcher,
    email_provider: EmailProvider,
    sms_provider: SMSProvider,
    push_provider: PushProvider,
) -> NotificationDispatcher:
    """Dispatcher with all providers registered."""
    dispatcher.register_provider(email_provider)
    dispatcher.register_provider(sms_provider)
    dispatcher.register_provider(push_provider)
    return dispatcher


@pytest.fixture
def sample_notifications() -> list[Notification]:
    """Sample notifications for batch testing."""
    return [
        Notification("user1", "Hello", NotificationChannel.EMAIL, NotificationPriority.NORMAL),
        Notification("user2", "Urgent!", NotificationChannel.SMS, NotificationPriority.URGENT),
        Notification("user3", "Low priority", NotificationChannel.PUSH, NotificationPriority.LOW),
    ]


@pytest.fixture
def unhealthy_email_provider() -> EmailProvider:
    """Email provider in unhealthy state."""
    provider = EmailProvider()
    provider.set_healthy(False)
    return provider


# ============================================================================
# TESTS
# ============================================================================

class TestNotificationDispatcherRegistration:
    """Tests for provider registration."""
    
    def test_register_provider_succeeds(self, dispatcher: NotificationDispatcher, email_provider: EmailProvider) -> None:
        """Should successfully register a provider."""
        dispatcher.register_provider(email_provider)
        
        assert dispatcher.get_provider_for(NotificationChannel.EMAIL) == email_provider
    
    def test_register_duplicate_provider_raises(self, dispatcher: NotificationDispatcher, email_provider: EmailProvider) -> None:
        """Should raise when registering duplicate channel."""
        dispatcher.register_provider(email_provider)
        
        with pytest.raises(ValueError, match="already registered"):
            dispatcher.register_provider(EmailProvider())
    
    def test_get_provider_for_unregistered_returns_none(self, dispatcher: NotificationDispatcher) -> None:
        """Should return None for unregistered channel."""
        result = dispatcher.get_provider_for(NotificationChannel.EMAIL)
        
        assert result is None


class TestNotificationDispatcherDispatch:
    """Tests for single notification dispatch."""
    
    def test_dispatch_success(self, fully_configured_dispatcher: NotificationDispatcher) -> None:
        """Should successfully dispatch notification."""
        notification = Notification(
            recipient_id="user@example.com",
            message="Test message",
            channel=NotificationChannel.EMAIL
        )
        
        result = fully_configured_dispatcher.dispatch(notification)
        
        assert result.success is True
        assert result.notification == notification
    
    def test_dispatch_no_provider_raises(self, dispatcher: NotificationDispatcher) -> None:
        """Should raise when no provider for channel."""
        notification = Notification(
            recipient_id="user",
            message="Test",
            channel=NotificationChannel.EMAIL
        )
        
        with pytest.raises(RuntimeError, match="No provider"):
            dispatcher.dispatch(notification)
    
    def test_dispatch_unhealthy_provider_fails_gracefully(
        self,
        dispatcher: NotificationDispatcher,
        unhealthy_email_provider: EmailProvider,
    ) -> None:
        """Should return failed result when provider unhealthy."""
        dispatcher.register_provider(unhealthy_email_provider)
        
        notification = Notification(
            recipient_id="user@example.com",
            message="Test",
            channel=NotificationChannel.EMAIL
        )
        
        result = dispatcher.dispatch(notification)
        
        assert result.success is False
        assert "not healthy" in result.error_message.lower()


class TestNotificationDispatcherBatch:
    """Tests for batch dispatch."""
    
    def test_dispatch_batch_returns_results_for_all(
        self,
        fully_configured_dispatcher: NotificationDispatcher,
        sample_notifications: list[Notification],
    ) -> None:
        """Should return result for each notification."""
        results = fully_configured_dispatcher.dispatch_batch(sample_notifications)
        
        assert len(results) == len(sample_notifications)
        assert all(isinstance(r, DispatchResult) for r in results)
    
    def test_dispatch_batch_respects_priority_order(
        self,
        dispatcher: NotificationDispatcher,
        email_provider: EmailProvider,
    ) -> None:
        """Should process URGENT before NORMAL before LOW."""
        dispatcher.register_provider(email_provider)
        
        notifications = [
            Notification("u1", "Low", NotificationChannel.EMAIL, NotificationPriority.LOW),
            Notification("u2", "Urgent", NotificationChannel.EMAIL, NotificationPriority.URGENT),
            Notification("u3", "Normal", NotificationChannel.EMAIL, NotificationPriority.NORMAL),
            Notification("u4", "High", NotificationChannel.EMAIL, NotificationPriority.HIGH),
        ]
        
        # Patch the provider to track call order
        call_order = []
        original_send = email_provider.send
        
        def tracking_send(notification: Notification) -> dict:
            call_order.append(notification.priority)
            return original_send(notification)
        
        email_provider.send = tracking_send
        
        dispatcher.dispatch_batch(notifications)
        
        # Should be processed in priority order
        assert call_order[0] == NotificationPriority.URGENT
        assert call_order[1] == NotificationPriority.HIGH
        assert call_order[2] == NotificationPriority.NORMAL
        assert call_order[3] == NotificationPriority.LOW
    
    def test_dispatch_batch_returns_results_in_original_order(
        self,
        fully_configured_dispatcher: NotificationDispatcher,
    ) -> None:
        """Results should correspond to input order, not processing order."""
        notifications = [
            Notification("u1", "Low", NotificationChannel.EMAIL, NotificationPriority.LOW),
            Notification("u2", "Urgent", NotificationChannel.EMAIL, NotificationPriority.URGENT),
        ]
        
        results = fully_configured_dispatcher.dispatch_batch(notifications)
        
        assert results[0].notification.recipient_id == "u1"
        assert results[1].notification.recipient_id == "u2"


class TestNotificationDispatcherStats:
    """Tests for statistics tracking."""
    
    def test_stats_initially_zero(self, dispatcher: NotificationDispatcher) -> None:
        """Should start with zero stats."""
        stats = dispatcher.get_stats()
        
        assert stats == {"total": 0, "success": 0, "failed": 0}
    
    def test_stats_track_successful_dispatch(
        self,
        fully_configured_dispatcher: NotificationDispatcher,
    ) -> None:
        """Should increment success counter."""
        notification = Notification("u", "Test", NotificationChannel.EMAIL)
        
        fully_configured_dispatcher.dispatch(notification)
        stats = fully_configured_dispatcher.get_stats()
        
        assert stats["total"] == 1
        assert stats["success"] == 1
        assert stats["failed"] == 0
    
    def test_stats_track_failed_dispatch(
        self,
        dispatcher: NotificationDispatcher,
        unhealthy_email_provider: EmailProvider,
    ) -> None:
        """Should increment failed counter for unhealthy provider."""
        dispatcher.register_provider(unhealthy_email_provider)
        notification = Notification("u", "Test", NotificationChannel.EMAIL)
        
        dispatcher.dispatch(notification)
        stats = dispatcher.get_stats()
        
        assert stats["total"] == 1
        assert stats["success"] == 0
        assert stats["failed"] == 1


class TestNotificationDispatcherChannelAvailability:
    """Tests for channel availability checking."""
    
    def test_channel_available_when_provider_healthy(
        self,
        dispatcher: NotificationDispatcher,
        email_provider: EmailProvider,
    ) -> None:
        """Should report available when provider healthy."""
        dispatcher.register_provider(email_provider)
        
        assert dispatcher.is_channel_available(NotificationChannel.EMAIL) is True
    
    def test_channel_unavailable_when_no_provider(
        self, dispatcher: NotificationDispatcher
    ) -> None:
        """Should report unavailable when no provider registered."""
        assert dispatcher.is_channel_available(NotificationChannel.EMAIL) is False
    
    def test_channel_unavailable_when_provider_unhealthy(
        self,
        dispatcher: NotificationDispatcher,
        unhealthy_email_provider: EmailProvider,
    ) -> None:
        """Should report unavailable when provider unhealthy."""
        dispatcher.register_provider(unhealthy_email_provider)
        
        assert dispatcher.is_channel_available(NotificationChannel.EMAIL) is False


class TestEmailProvider:
    """Tests for EmailProvider."""
    
    def test_send_returns_dict_with_expected_keys(self) -> None:
        """Should return dict with message info."""
        provider = EmailProvider()
        notification = Notification("user@example.com", "Hello", NotificationChannel.EMAIL)
        
        result = provider.send(notification)
        
        assert "message_id" in result
        assert "recipient" in result
        assert result["status"] == "sent"
    
    def test_send_with_failure_rate_can_fail(self) -> None:
        """Should occasionally fail with non-zero failure rate."""
        provider = EmailProvider(failure_rate=1.0)  # Always fail
        notification = Notification("u", "Test", NotificationChannel.EMAIL)
        
        with pytest.raises(RuntimeError, match="failure"):
            provider.send(notification)
    
    def test_get_channel_returns_email(self) -> None:
        """Should return EMAIL channel."""
        provider = EmailProvider()
        
        assert provider.get_channel() == NotificationChannel.EMAIL
    
    def test_is_healthy_defaults_true(self) -> None:
        """Should start healthy."""
        provider = EmailProvider()
        
        assert provider.is_healthy() is True


class TestSMSProvider:
    """Tests for SMSProvider."""
    
    def test_send_validates_max_length(self) -> None:
        """Should raise when message too long."""
        provider = SMSProvider(max_length=10)
        notification = Notification("user", "This is way too long", NotificationChannel.SMS)
        
        with pytest.raises(ValueError, match="exceeds"):
            provider.send(notification)
    
    def test_send_short_message_succeeds(self) -> None:
        """Should send short messages."""
        provider = SMSProvider(max_length=160)
        notification = Notification("user", "Short", NotificationChannel.SMS)
        
        result = provider.send(notification)
        
        assert result.startswith("SMS_")
        assert ":sent" in result


class TestPushProvider:
    """Tests for PushProvider."""
    
    def test_send_without_ack_returns_true(self) -> None:
        """Should return True when no ack required."""
        provider = PushProvider(requires_ack=False)
        notification = Notification("device", "Push msg", NotificationChannel.PUSH)
        
        result = provider.send(notification)
        
        assert result is True
    
    def test_send_with_ack_unacknowledged_returns_false(self) -> None:
        """Should return False when ack required but not given."""
        provider = PushProvider(requires_ack=True)
        notification = Notification("device", "Push msg", NotificationChannel.PUSH)
        
        result = provider.send(notification)
        
        assert result is False


class TestProviderComposition:
    """Tests demonstrating fixture composition patterns."""
    
    @pytest.fixture
    def mixed_health_dispatcher(
        self, dispatcher: NotificationDispatcher
    ) -> NotificationDispatcher:
        """Dispatcher with mix of healthy and unhealthy providers."""
        healthy_email = EmailProvider()
        unhealthy_sms = SMSProvider()
        unhealthy_sms.set_healthy(False)
        healthy_push = PushProvider()
        
        dispatcher.register_provider(healthy_email)
        dispatcher.register_provider(unhealthy_sms)
        dispatcher.register_provider(healthy_push)
        
        return dispatcher
    
    def test_mixed_health_channels(
        self, mixed_health_dispatcher: NotificationDispatcher
    ) -> None:
        """Should correctly report availability per channel."""
        assert mixed_health_dispatcher.is_channel_available(NotificationChannel.EMAIL) is True
        assert mixed_health_dispatcher.is_channel_available(NotificationChannel.SMS) is False
        assert mixed_health_dispatcher.is_channel_available(NotificationChannel.PUSH) is True
