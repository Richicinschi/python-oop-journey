"""Tests for Problem 01: Notification Services."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day02.problem_01_notification_services import (
    BaseNotification,
    EmailNotification,
    PushNotification,
    SMSNotification,
)


class TestBaseNotification:
    """Tests for BaseNotification class."""

    def test_init_sets_message(self) -> None:
        """Test that message is set correctly."""
        notification = BaseNotification("Hello")
        assert notification.message == "Hello"

    def test_send_returns_expected_string(self) -> None:
        """Test send() returns correct format."""
        notification = BaseNotification("Test message")
        result = notification.send()
        assert result == "Notification sent: Test message"

    def test_send_logs_action(self, capsys: pytest.CaptureFixture) -> None:
        """Test that send() logs to stdout."""
        notification = BaseNotification("Test")
        notification.send()
        captured = capsys.readouterr()
        assert "[LOG]" in captured.out
        assert "Sending notification" in captured.out


class TestEmailNotification:
    """Tests for EmailNotification class."""

    def test_init_sets_all_attributes(self) -> None:
        """Test that all attributes are set."""
        email = EmailNotification("Hello", "user@example.com", "Greeting")
        assert email.message == "Hello"
        assert email.recipient == "user@example.com"
        assert email.subject == "Greeting"

    def test_send_returns_expected_format(self) -> None:
        """Test send() returns correct email format."""
        email = EmailNotification("Hello", "user@example.com", "Greeting")
        result = email.send()
        assert result == "Email to user@example.com [Greeting]: Hello"

    def test_send_logs_action(self, capsys: pytest.CaptureFixture) -> None:
        """Test that send() logs to stdout."""
        email = EmailNotification("Hello", "user@test.com", "Subject")
        email.send()
        captured = capsys.readouterr()
        assert "[LOG]" in captured.out

    def test_inheritance_from_base(self) -> None:
        """Test that EmailNotification inherits from BaseNotification."""
        assert issubclass(EmailNotification, BaseNotification)


class TestSMSNotification:
    """Tests for SMSNotification class."""

    def test_init_sets_all_attributes(self) -> None:
        """Test that all attributes are set."""
        sms = SMSNotification("Code: 1234", "+1234567890")
        assert sms.message == "Code: 1234"
        assert sms.phone_number == "+1234567890"

    def test_init_validates_phone_number(self) -> None:
        """Test that invalid phone numbers raise ValueError."""
        with pytest.raises(ValueError, match="start with"):
            SMSNotification("Test", "1234567890")

    def test_init_validates_empty_phone(self) -> None:
        """Test that empty phone number raises ValueError."""
        with pytest.raises(ValueError, match="start with"):
            SMSNotification("Test", "")

    def test_send_returns_expected_format(self) -> None:
        """Test send() returns correct SMS format."""
        sms = SMSNotification("Code: 1234", "+1234567890")
        result = sms.send()
        assert result == "SMS to +1234567890: Code: 1234"

    def test_send_logs_action(self, capsys: pytest.CaptureFixture) -> None:
        """Test that send() logs to stdout."""
        sms = SMSNotification("Hello", "+1234567890")
        sms.send()
        captured = capsys.readouterr()
        assert "[LOG]" in captured.out

    def test_inheritance_from_base(self) -> None:
        """Test that SMSNotification inherits from BaseNotification."""
        assert issubclass(SMSNotification, BaseNotification)


class TestPushNotification:
    """Tests for PushNotification class."""

    def test_init_sets_default_priority(self) -> None:
        """Test that default priority is 'normal'."""
        push = PushNotification("Hello")
        assert push.priority == "normal"

    def test_init_accepts_custom_priority(self) -> None:
        """Test that custom priority is accepted."""
        push = PushNotification("Hello", "high")
        assert push.priority == "high"

    def test_init_validates_priority(self) -> None:
        """Test that invalid priority raises ValueError."""
        with pytest.raises(ValueError, match="Priority must be"):
            PushNotification("Hello", "invalid")

    def test_send_returns_expected_format_low(self) -> None:
        """Test send() returns correct format for low priority."""
        push = PushNotification("Hello", "low")
        result = push.send()
        assert result == "Push [low]: Hello"

    def test_send_returns_expected_format_urgent(self) -> None:
        """Test send() returns correct format for urgent priority."""
        push = PushNotification("Alert!", "urgent")
        result = push.send()
        assert result == "Push [urgent]: Alert!"

    def test_send_logs_action(self, capsys: pytest.CaptureFixture) -> None:
        """Test that send() logs to stdout."""
        push = PushNotification("Hello", "normal")
        push.send()
        captured = capsys.readouterr()
        assert "[LOG]" in captured.out

    def test_priorities_constant(self) -> None:
        """Test that PRIORITIES constant exists and has expected values."""
        expected = ("low", "normal", "high", "urgent")
        assert PushNotification.PRIORITIES == expected

    def test_inheritance_from_base(self) -> None:
        """Test that PushNotification inherits from BaseNotification."""
        assert issubclass(PushNotification, BaseNotification)
