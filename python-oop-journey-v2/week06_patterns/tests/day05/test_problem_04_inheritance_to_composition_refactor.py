"""Tests for Problem 04: Inheritance to Composition Refactor."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day05.problem_04_inheritance_to_composition_refactor import (
    AuditLogger,
    EmailTransport,
    EncryptionLayer,
    InMemoryAuditLogger,
    NotificationMessage,
    NotificationResult,
    NotificationService,
    SecurityLayer,
    SmsTransport,
    Transport,
)


class TestNotificationMessage:
    """Tests for NotificationMessage dataclass."""
    
    def test_message_creation(self) -> None:
        message = NotificationMessage(
            content="Hello",
            recipient="user@example.com",
            subject="Test",
            priority="high",
        )
        assert message.content == "Hello"
        assert message.recipient == "user@example.com"


class TestNotificationResult:
    """Tests for NotificationResult dataclass."""
    
    def test_result_creation(self) -> None:
        result = NotificationResult(
            success=True,
            message_id="msg_123",
            transport_used="email",
            details={},
        )
        assert result.success is True
        assert result.message_id == "msg_123"


class TestEmailTransport:
    """Tests for EmailTransport."""
    
    def test_transport_name(self) -> None:
        transport = EmailTransport("smtp.example.com")
        assert transport.get_transport_name() == "email"
    
    def test_is_available_with_server(self) -> None:
        transport = EmailTransport("smtp.example.com")
        assert transport.is_available() is True
    
    def test_is_available_without_server(self) -> None:
        transport = EmailTransport("")
        assert transport.is_available() is False
    
    def test_send(self) -> None:
        transport = EmailTransport("smtp.example.com")
        message = NotificationMessage(
            content="Test message",
            recipient="user@example.com",
            subject="Test Subject",
        )
        
        result = transport.send(message)
        
        assert isinstance(result, NotificationResult)
        assert result.success is True
        assert result.transport_used == "email"
        assert "smtp.example.com" in result.details["smtp_server"]


class TestSmsTransport:
    """Tests for SmsTransport."""
    
    def test_transport_name(self) -> None:
        transport = SmsTransport("AC123")
        assert transport.get_transport_name() == "sms"
    
    def test_send(self) -> None:
        transport = SmsTransport("AC123")
        message = NotificationMessage(
            content="SMS text",
            recipient="+1234567890",
        )
        
        result = transport.send(message)
        
        assert isinstance(result, NotificationResult)
        assert result.success is True
        assert result.transport_used == "sms"


class TestEncryptionLayer:
    """Tests for EncryptionLayer."""
    
    def test_process_outgoing(self) -> None:
        layer = EncryptionLayer("secret_key")
        encrypted = layer.process_outgoing("Hello")
        
        assert "[ENCRYPTED:secret_key]" in encrypted
        assert "Hello" in encrypted
        assert "[/ENCRYPTED]" in encrypted
    
    def test_process_incoming(self) -> None:
        layer = EncryptionLayer("secret_key")
        encrypted = "[ENCRYPTED:secret_key]Hello[/ENCRYPTED]"
        decrypted = layer.process_incoming(encrypted)
        
        assert decrypted == "Hello"
    
    def test_process_incoming_plain_text(self) -> None:
        layer = EncryptionLayer("secret_key")
        plain = "Plain text"
        result = layer.process_incoming(plain)
        
        assert result == "Plain text"
    
    def test_security_description(self) -> None:
        layer = EncryptionLayer("my_secret_key")
        desc = layer.get_security_description()
        
        assert "Encryption" in desc
        assert "my" in desc  # First part of key


class TestInMemoryAuditLogger:
    """Tests for InMemoryAuditLogger."""
    
    def test_log_send(self) -> None:
        logger = InMemoryAuditLogger()
        message = NotificationMessage(content="Test", recipient="user@example.com")
        result = NotificationResult(True, "msg_123", "email", {})
        
        logger.log_send(message, result)
        
        logs = logger.get_logs()
        assert len(logs) == 1
        assert "AUDIT" in logs[0]
        assert "user@example.com" in logs[0]
    
    def test_multiple_logs(self) -> None:
        logger = InMemoryAuditLogger()
        
        for i in range(3):
            message = NotificationMessage(content=f"Msg {i}", recipient=f"user{i}@test.com")
            result = NotificationResult(True, f"msg_{i}", "email", {})
            logger.log_send(message, result)
        
        assert len(logger.get_logs()) == 3


class TestNotificationService:
    """Tests for NotificationService."""
    
    def test_simple_notification(self) -> None:
        transport = EmailTransport("smtp.example.com")
        service = NotificationService(transport)
        
        message = NotificationMessage(content="Hello", recipient="user@test.com")
        result = service.send(message)
        
        assert result.success is True
        assert service.get_sent_count() == 1
    
    def test_notification_with_encryption(self) -> None:
        transport = EmailTransport("smtp.example.com")
        security = EncryptionLayer("key123")
        service = NotificationService(transport, security=security)
        
        message = NotificationMessage(content="Secret", recipient="user@test.com")
        result = service.send(message)
        
        assert result.success is True
        assert "[ENCRYPTED:" in result.details["content_preview"]
    
    def test_notification_with_audit(self) -> None:
        transport = EmailTransport("smtp.example.com")
        audit = InMemoryAuditLogger()
        service = NotificationService(transport, audit=audit)
        
        message = NotificationMessage(content="Test", recipient="user@test.com")
        service.send(message)
        
        logs = service.get_audit_logs()
        assert len(logs) == 1
    
    def test_notification_with_all_layers(self) -> None:
        transport = EmailTransport("smtp.example.com")
        security = EncryptionLayer("key123")
        audit = InMemoryAuditLogger()
        service = NotificationService(transport, security=security, audit=audit)
        
        message = NotificationMessage(content="Secure", recipient="user@test.com")
        result = service.send(message)
        
        assert result.success is True
        assert service.get_sent_count() == 1
        assert len(service.get_audit_logs()) == 1
    
    def test_get_capabilities(self) -> None:
        transport = EmailTransport("smtp.example.com")
        security = EncryptionLayer("key")
        audit = InMemoryAuditLogger()
        
        # Minimal service
        minimal = NotificationService(transport)
        assert minimal.get_capabilities() == {
            "transport": True,
            "security": False,
            "audit": False,
        }
        
        # Full service
        full = NotificationService(transport, security=security, audit=audit)
        assert full.get_capabilities() == {
            "transport": True,
            "security": True,
            "audit": True,
        }


class TestCompositionBenefits:
    """Tests demonstrating composition benefits over inheritance."""
    
    def test_runtime_behavior_change(self) -> None:
        """Can swap components at runtime (vs fixed inheritance)."""
        # Start with email
        service = NotificationService(EmailTransport("smtp.example.com"))
        
        # In inheritance, we'd be locked into email
        # With composition, we can create a new service with SMS
        sms_service = NotificationService(SmsTransport("AC123"))
        
        # Both work independently
        email_result = service.send(NotificationMessage("Hi", "user@test.com"))
        sms_result = sms_service.send(NotificationMessage("Hi", "+1234567890"))
        
        assert email_result.transport_used == "email"
        assert sms_result.transport_used == "sms"
    
    def test_mix_and_match_behaviors(self) -> None:
        """Can combine behaviors independently (vs fixed inheritance chains)."""
        # Email + Security (no audit)
        email_secure = NotificationService(
            EmailTransport("smtp.example.com"),
            security=EncryptionLayer("key"),
        )
        
        # SMS + Audit (no security)
        sms_audited = NotificationService(
            SmsTransport("AC123"),
            audit=InMemoryAuditLogger(),
        )
        
        # All three
        full_service = NotificationService(
            EmailTransport("smtp.example.com"),
            security=EncryptionLayer("key"),
            audit=InMemoryAuditLogger(),
        )
        
        # All work correctly with their specific configurations
        assert email_secure.get_capabilities()["security"] is True
        assert email_secure.get_capabilities()["audit"] is False
        
        assert sms_audited.get_capabilities()["security"] is False
        assert sms_audited.get_capabilities()["audit"] is True
        
        assert full_service.get_capabilities() == {
            "transport": True,
            "security": True,
            "audit": True,
        }
    
    def test_no_fragile_base_class(self) -> None:
        """Changes to one component don't affect others."""
        # Create multiple services
        service1 = NotificationService(EmailTransport("smtp1.com"))
        service2 = NotificationService(EmailTransport("smtp2.com"))
        
        # Use service1
        service1.send(NotificationMessage("Hi", "user@test.com"))
        
        # service2 is unaffected
        assert service2.get_sent_count() == 0
    
    def test_testability_with_mocks(self) -> None:
        """Can inject test doubles easily."""
        # Create a mock transport for testing
        class MockTransport(Transport):
            def __init__(self) -> None:
                self.sent_messages: list[NotificationMessage] = []
            
            def send(self, message: NotificationMessage) -> NotificationResult:
                self.sent_messages.append(message)
                return NotificationResult(True, "mock_123", "mock", {})
            
            def get_transport_name(self) -> str:
                return "mock"
            
            def is_available(self) -> bool:
                return True
        
        mock_transport = MockTransport()
        service = NotificationService(mock_transport)
        
        message = NotificationMessage("Test", "user@test.com")
        service.send(message)
        
        # Verify mock was used
        assert len(mock_transport.sent_messages) == 1
        assert mock_transport.sent_messages[0].content == "Test"
