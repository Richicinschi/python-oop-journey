"""Tests for Problem 01: Factory Method Notifications."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day01.problem_01_factory_method_notifications import (
    Notification,
    EmailNotification,
    SMSNotification,
    PushNotification,
    NotificationFactory,
    EmailNotificationFactory,
    SMSNotificationFactory,
    PushNotificationFactory,
)


class TestEmailNotification:
    """Tests for EmailNotification class."""
    
    def test_init(self) -> None:
        notification = EmailNotification("user@example.com")
        assert notification.recipient == "user@example.com"
    
    def test_send(self) -> None:
        notification = EmailNotification("user@example.com")
        result = notification.send("Hello!")
        assert result == "[EMAIL] To: user@example.com | Message: Hello!"
    
    def test_get_channel(self) -> None:
        notification = EmailNotification("user@example.com")
        assert notification.get_channel() == "email"
    
    def test_isinstance_of_notification(self) -> None:
        notification = EmailNotification("user@example.com")
        assert isinstance(notification, Notification)


class TestSMSNotification:
    """Tests for SMSNotification class."""
    
    def test_init(self) -> None:
        notification = SMSNotification("+1234567890")
        assert notification.recipient == "+1234567890"
    
    def test_send(self) -> None:
        notification = SMSNotification("+1234567890")
        result = notification.send("Hello!")
        assert result == "[SMS] To: +1234567890 | Message: Hello!"
    
    def test_get_channel(self) -> None:
        notification = SMSNotification("+1234567890")
        assert notification.get_channel() == "sms"
    
    def test_isinstance_of_notification(self) -> None:
        notification = SMSNotification("+1234567890")
        assert isinstance(notification, Notification)


class TestPushNotification:
    """Tests for PushNotification class."""
    
    def test_init(self) -> None:
        notification = PushNotification("device_token_123")
        assert notification.recipient == "device_token_123"
    
    def test_send(self) -> None:
        notification = PushNotification("device_token_123")
        result = notification.send("Hello!")
        assert result == "[PUSH] To: device_token_123 | Message: Hello!"
    
    def test_get_channel(self) -> None:
        notification = PushNotification("device_token_123")
        assert notification.get_channel() == "push"
    
    def test_isinstance_of_notification(self) -> None:
        notification = PushNotification("device_token_123")
        assert isinstance(notification, Notification)


class TestEmailNotificationFactory:
    """Tests for EmailNotificationFactory class."""
    
    def test_isinstance_of_factory(self) -> None:
        factory = EmailNotificationFactory()
        assert isinstance(factory, NotificationFactory)
    
    def test_create_notification(self) -> None:
        factory = EmailNotificationFactory()
        notification = factory.create_notification("user@example.com")
        assert isinstance(notification, EmailNotification)
        assert notification.recipient == "user@example.com"
    
    def test_send_notification(self) -> None:
        factory = EmailNotificationFactory()
        result = factory.send_notification("user@example.com", "Test message")
        assert "[EMAIL]" in result
        assert "user@example.com" in result
        assert "Test message" in result


class TestSMSNotificationFactory:
    """Tests for SMSNotificationFactory class."""
    
    def test_isinstance_of_factory(self) -> None:
        factory = SMSNotificationFactory()
        assert isinstance(factory, NotificationFactory)
    
    def test_create_notification(self) -> None:
        factory = SMSNotificationFactory()
        notification = factory.create_notification("+1234567890")
        assert isinstance(notification, SMSNotification)
        assert notification.recipient == "+1234567890"
    
    def test_send_notification(self) -> None:
        factory = SMSNotificationFactory()
        result = factory.send_notification("+1234567890", "Test message")
        assert "[SMS]" in result
        assert "+1234567890" in result
        assert "Test message" in result


class TestPushNotificationFactory:
    """Tests for PushNotificationFactory class."""
    
    def test_isinstance_of_factory(self) -> None:
        factory = PushNotificationFactory()
        assert isinstance(factory, NotificationFactory)
    
    def test_create_notification(self) -> None:
        factory = PushNotificationFactory()
        notification = factory.create_notification("device_token_123")
        assert isinstance(notification, PushNotification)
        assert notification.recipient == "device_token_123"
    
    def test_send_notification(self) -> None:
        factory = PushNotificationFactory()
        result = factory.send_notification("device_token_123", "Test message")
        assert "[PUSH]" in result
        assert "device_token_123" in result
        assert "Test message" in result


class TestPolymorphism:
    """Tests demonstrating polymorphic behavior."""
    
    def test_factories_produce_correct_types(self) -> None:
        factories: list[NotificationFactory] = [
            EmailNotificationFactory(),
            SMSNotificationFactory(),
            PushNotificationFactory(),
        ]
        recipients = ["user@example.com", "+1234567890", "device_token_123"]
        expected_channels = ["email", "sms", "push"]
        
        for factory, recipient, expected_channel in zip(factories, recipients, expected_channels):
            notification = factory.create_notification(recipient)
            assert notification.get_channel() == expected_channel
    
    def test_uniform_send_interface(self) -> None:
        notifications: list[Notification] = [
            EmailNotification("user@example.com"),
            SMSNotification("+1234567890"),
            PushNotification("device_token_123"),
        ]
        
        for notification in notifications:
            result = notification.send("Test")
            assert "Test" in result
            assert notification.get_channel() in result.lower()


class TestExtensibility:
    """Tests demonstrating the extensibility of the pattern."""
    
    def test_new_notification_type_can_be_added(self) -> None:
        """Test that new notification types can be added without modifying existing code."""
        
        class SlackNotification(Notification):
            def send(self, message: str) -> str:
                return f"[SLACK] To: {self.recipient} | Message: {message}"
            
            def get_channel(self) -> str:
                return "slack"
        
        class SlackNotificationFactory(NotificationFactory):
            def create_notification(self, recipient: str) -> Notification:
                return SlackNotification(recipient)
        
        factory = SlackNotificationFactory()
        notification = factory.create_notification("#channel")
        result = factory.send_notification("#channel", "Hello Slack!")
        
        assert isinstance(notification, SlackNotification)
        assert notification.get_channel() == "slack"
        assert "[SLACK]" in result
