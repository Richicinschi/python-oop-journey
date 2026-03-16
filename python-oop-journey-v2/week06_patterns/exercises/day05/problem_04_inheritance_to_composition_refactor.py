"""Problem 04: Inheritance to Composition Refactor

Topic: Pattern Tradeoffs and Anti-patterns
Difficulty: Medium

Refactor a deep inheritance hierarchy into a composition-based design.

The notification system uses a deep inheritance hierarchy that creates
rigid, hard-to-maintain code. Your task is to convert this to composition
using behavior-based components.

The inheritance hierarchy:
Notifier -> EmailNotifier -> SecureEmailNotifier -> AuditSecureEmailNotifier

Your task: Replace inheritance with composition by:
1. Creating Transport components (EmailTransport, SmsTransport)
2. Creating Security components (Encryption, Authentication)
3. Creating Audit components (Logger)
4. Building NotificationService that composes these behaviors

This allows mixing and matching behaviors at runtime instead of
being locked into a fixed inheritance chain.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


# BEFORE: Deep inheritance hierarchy (do not modify - for reference)
class Notifier:
    """Base notifier class."""
    
    def __init__(self) -> None:
        self._sent_count = 0
    
    def send(self, message: str, recipient: str) -> str:
        """Send a notification."""
        result = self._do_send(message, recipient)
        self._sent_count += 1
        return result
    
    def _do_send(self, message: str, recipient: str) -> str:
        raise NotImplementedError
    
    def get_sent_count(self) -> int:
        return self._sent_count


class EmailNotifier(Notifier):
    """Email notifier - 2nd level."""
    
    def __init__(self, smtp_server: str) -> None:
        super().__init__()
        self._smtp_server = smtp_server
    
    def _do_send(self, message: str, recipient: str) -> str:
        return f"Email via {self._smtp_server} to {recipient}: {message}"


class SecureEmailNotifier(EmailNotifier):
    """Secure email notifier - 3rd level."""
    
    def __init__(self, smtp_server: str, encryption_key: str) -> None:
        super().__init__(smtp_server)
        self._encryption_key = encryption_key
    
    def _do_send(self, message: str, recipient: str) -> str:
        encrypted = f"[ENCRYPTED({self._encryption_key})]{message}[/ENCRYPTED]"
        return f"Secure email via {self._smtp_server} to {recipient}: {encrypted}"


class AuditSecureEmailNotifier(SecureEmailNotifier):
    """Secure email with audit logging - 4th level."""
    
    def __init__(self, smtp_server: str, encryption_key: str, audit_log: list[str]) -> None:
        super().__init__(smtp_server, encryption_key)
        self._audit_log = audit_log
    
    def _do_send(self, message: str, recipient: str) -> str:
        result = super()._do_send(message, recipient)
        self._audit_log.append(f"AUDIT: Sent to {recipient} at 2024-01-01")
        return result


# SMS inheritance branch
class SmsNotifier(Notifier):
    """SMS notifier - 2nd level, parallel branch."""
    
    def __init__(self, twilio_account: str) -> None:
        super().__init__()
        self._twilio_account = twilio_account
    
    def _do_send(self, message: str, recipient: str) -> str:
        return f"SMS via {self._twilio_account} to {recipient}: {message}"


# AFTER: Your composition-based design (implement these)

@dataclass
class NotificationMessage:
    """Message data class."""
    content: str
    recipient: str
    subject: str | None = None
    priority: str = "normal"


@dataclass
class NotificationResult:
    """Result of sending a notification."""
    success: bool
    message_id: str
    transport_used: str
    details: dict[str, Any]


class Transport(ABC):
    """Abstract transport for sending notifications.
    
    Transports handle the actual delivery mechanism (email, SMS, etc.)
    without concern for security, auditing, etc.
    """
    
    @abstractmethod
    def send(self, message: NotificationMessage) -> NotificationResult:
        """Send the notification via this transport.
        
        Args:
            message: Message to send
        
        Returns:
            NotificationResult with delivery details
        """
        raise NotImplementedError("Implement send")
    
    @abstractmethod
    def get_transport_name(self) -> str:
        """Get name of this transport."""
        raise NotImplementedError("Implement get_transport_name")
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if transport is available/configured."""
        raise NotImplementedError("Implement is_available")


class EmailTransport(Transport):
    """Email transport implementation."""
    
    def __init__(self, smtp_server: str) -> None:
        """Initialize email transport.
        
        Args:
            smtp_server: SMTP server address
        """
        raise NotImplementedError("Implement __init__")
    
    def send(self, message: NotificationMessage) -> NotificationResult:
        """Send email."""
        raise NotImplementedError("Implement send")
    
    def get_transport_name(self) -> str:
        """Get transport name."""
        raise NotImplementedError("Implement get_transport_name")
    
    def is_available(self) -> bool:
        """Check if email transport is configured."""
        raise NotImplementedError("Implement is_available")


class SmsTransport(Transport):
    """SMS transport implementation."""
    
    def __init__(self, twilio_account: str) -> None:
        """Initialize SMS transport.
        
        Args:
            twilio_account: Twilio account identifier
        """
        raise NotImplementedError("Implement __init__")
    
    def send(self, message: NotificationMessage) -> NotificationResult:
        """Send SMS."""
        raise NotImplementedError("Implement send")
    
    def get_transport_name(self) -> str:
        """Get transport name."""
        raise NotImplementedError("Implement get_transport_name")
    
    def is_available(self) -> bool:
        """Check if SMS transport is configured."""
        raise NotImplementedError("Implement is_available")


class SecurityLayer(ABC):
    """Abstract security layer for message processing.
    
    Security layers can encrypt, sign, or otherwise transform messages
    before/after transport.
    """
    
    @abstractmethod
    def process_outgoing(self, content: str) -> str:
        """Process message before sending.
        
        Args:
            content: Original message content
        
        Returns:
            Processed content
        """
        raise NotImplementedError("Implement process_outgoing")
    
    @abstractmethod
    def process_incoming(self, content: str) -> str:
        """Process received message (for completeness).
        
        Args:
            content: Received message content
        
        Returns:
            Processed content
        """
        raise NotImplementedError("Implement process_incoming")
    
    @abstractmethod
    def get_security_description(self) -> str:
        """Get description of security applied."""
        raise NotImplementedError("Implement get_security_description")


class EncryptionLayer(SecurityLayer):
    """Encryption security layer."""
    
    def __init__(self, encryption_key: str) -> None:
        """Initialize encryption layer.
        
        Args:
            encryption_key: Key for encryption (simplified for exercise)
        """
        raise NotImplementedError("Implement __init__")
    
    def process_outgoing(self, content: str) -> str:
        """Encrypt content."""
        raise NotImplementedError("Implement process_outgoing")
    
    def process_incoming(self, content: str) -> str:
        """Decrypt content."""
        raise NotImplementedError("Implement process_incoming")
    
    def get_security_description(self) -> str:
        """Get security description."""
        raise NotImplementedError("Implement get_security_description")


class AuditLogger(ABC):
    """Abstract audit logger."""
    
    @abstractmethod
    def log_send(self, message: NotificationMessage, result: NotificationResult) -> None:
        """Log a send operation."""
        raise NotImplementedError("Implement log_send")
    
    @abstractmethod
    def get_logs(self) -> list[str]:
        """Get all log entries."""
        raise NotImplementedError("Implement get_logs")


class InMemoryAuditLogger(AuditLogger):
    """In-memory audit logger implementation."""
    
    def __init__(self) -> None:
        raise NotImplementedError("Implement __init__")
    
    def log_send(self, message: NotificationMessage, result: NotificationResult) -> None:
        """Log send operation to memory."""
        raise NotImplementedError("Implement log_send")
    
    def get_logs(self) -> list[str]:
        """Get all logged entries."""
        raise NotImplementedError("Implement get_logs")


class NotificationService:
    """Notification service using composition.
    
    Composes Transport, SecurityLayer, and AuditLogger to create
    flexible notification pipelines.
    
    Examples:
        # Simple email:
        service = NotificationService(EmailTransport("smtp.example.com"))
        
        # Secure email with audit:
        service = NotificationService(
            transport=EmailTransport("smtp.example.com"),
            security=EncryptionLayer("secret_key"),
            audit=InMemoryAuditLogger()
        )
        
        # SMS with audit but no encryption:
        service = NotificationService(
            transport=SmsTransport("AC123"),
            audit=InMemoryAuditLogger()
        )
    """
    
    def __init__(
        self,
        transport: Transport,
        security: SecurityLayer | None = None,
        audit: AuditLogger | None = None,
    ) -> None:
        """Initialize notification service with composed components.
        
        Args:
            transport: Transport layer for actual delivery
            security: Optional security layer for encryption/signing
            audit: Optional audit logger
        """
        raise NotImplementedError("Implement __init__")
    
    def send(self, message: NotificationMessage) -> NotificationResult:
        """Send notification using composed components.
        
        Process:
        1. Apply security if present (e.g., encrypt)
        2. Send via transport
        3. Audit if logger present
        
        Args:
            message: Message to send
        
        Returns:
            NotificationResult
        """
        raise NotImplementedError("Implement send")
    
    def get_sent_count(self) -> int:
        """Get count of sent notifications."""
        raise NotImplementedError("Implement get_sent_count")
    
    def get_audit_logs(self) -> list[str]:
        """Get audit logs if audit logger is configured."""
        raise NotImplementedError("Implement get_audit_logs")
    
    def get_capabilities(self) -> dict[str, bool]:
        """Get service capabilities.
        
        Returns:
            Dict with keys: transport, security, audit
        """
        raise NotImplementedError("Implement get_capabilities")
