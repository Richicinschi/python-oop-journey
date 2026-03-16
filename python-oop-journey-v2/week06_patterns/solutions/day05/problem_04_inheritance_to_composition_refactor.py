"""Problem 04: Inheritance to Composition Refactor - Solution.

Replaces deep inheritance with composable behaviors.

WHY COMPOSITION OVER DEEP INHERITANCE?
The original inheritance hierarchy (Notifier -> EmailNotifier -> SecureEmailNotifier
-> AuditSecureEmailNotifier) is rigid:
- Can't combine features in different ways (Email + Audit without Security)
- Changes at the top affect all descendants (fragile base class)
- Class names describe the entire feature stack (verbose)

COMPOSITION BENEFITS:
- Mix and match: Use EmailTransport with or without EncryptionLayer
- Runtime flexibility: Add/remove security or auditing as needed
- No inheritance baggage: Each component is independent
- Clear intent: Service configuration is visible in constructor calls

This demonstrates: "Composition over inheritance" - use inheritance for
"is-a" relationships, composition for "has-a" capabilities.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


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
    """Abstract transport for sending notifications."""
    
    @abstractmethod
    def send(self, message: NotificationMessage) -> NotificationResult:
        raise NotImplementedError
    
    @abstractmethod
    def get_transport_name(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def is_available(self) -> bool:
        raise NotImplementedError


class EmailTransport(Transport):
    """Email transport implementation."""
    
    def __init__(self, smtp_server: str) -> None:
        self._smtp_server = smtp_server
        self._available = bool(smtp_server)
    
    def send(self, message: NotificationMessage) -> NotificationResult:
        email_content = f"Subject: {message.subject}\n\n{message.content}"
        return NotificationResult(
            success=True,
            message_id=f"email_{hash(email_content) % 10000}",
            transport_used="email",
            details={
                "smtp_server": self._smtp_server,
                "recipient": message.recipient,
                "content_preview": email_content[:50],
            },
        )
    
    def get_transport_name(self) -> str:
        return "email"
    
    def is_available(self) -> bool:
        return self._available


class SmsTransport(Transport):
    """SMS transport implementation."""
    
    def __init__(self, twilio_account: str) -> None:
        self._twilio_account = twilio_account
        self._available = bool(twilio_account)
    
    def send(self, message: NotificationMessage) -> NotificationResult:
        return NotificationResult(
            success=True,
            message_id=f"sms_{hash(message.content) % 10000}",
            transport_used="sms",
            details={
                "twilio_account": self._twilio_account,
                "recipient": message.recipient,
                "message": message.content[:160],
            },
        )
    
    def get_transport_name(self) -> str:
        return "sms"
    
    def is_available(self) -> bool:
        return self._available


class SecurityLayer(ABC):
    """Abstract security layer for message processing."""
    
    @abstractmethod
    def process_outgoing(self, content: str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def process_incoming(self, content: str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def get_security_description(self) -> str:
        raise NotImplementedError


class EncryptionLayer(SecurityLayer):
    """Encryption security layer."""
    
    def __init__(self, encryption_key: str) -> None:
        self._encryption_key = encryption_key
    
    def process_outgoing(self, content: str) -> str:
        return f"[ENCRYPTED:{self._encryption_key}]{content}[/ENCRYPTED]"
    
    def process_incoming(self, content: str) -> str:
        # Simplified decryption for exercise
        if content.startswith("[ENCRYPTED:"):
            end_marker = content.find("]")
            return content[end_marker + 1 : content.find("[/ENCRYPTED]")]
        return content
    
    def get_security_description(self) -> str:
        return f"Encryption with key {self._encryption_key[:3]}..."


class AuditLogger(ABC):
    """Abstract audit logger."""
    
    @abstractmethod
    def log_send(self, message: NotificationMessage, result: NotificationResult) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_logs(self) -> list[str]:
        raise NotImplementedError


class InMemoryAuditLogger(AuditLogger):
    """In-memory audit logger implementation."""
    
    def __init__(self) -> None:
        self._logs: list[str] = []
    
    def log_send(self, message: NotificationMessage, result: NotificationResult) -> None:
        log_entry = (
            f"AUDIT: Sent to {message.recipient} via {result.transport_used} "
            f"(ID: {result.message_id})"
        )
        self._logs.append(log_entry)
    
    def get_logs(self) -> list[str]:
        return self._logs.copy()


class NotificationService:
    """Notification service using composition."""
    
    def __init__(
        self,
        transport: Transport,
        security: SecurityLayer | None = None,
        audit: AuditLogger | None = None,
    ) -> None:
        self._transport = transport
        self._security = security
        self._audit = audit
        self._sent_count = 0
    
    def send(self, message: NotificationMessage) -> NotificationResult:
        """Send notification using composed components."""
        # Apply security if present
        content = message.content
        if self._security:
            content = self._security.process_outgoing(content)
        
        # Create modified message with secured content
        secured_message = NotificationMessage(
            content=content,
            recipient=message.recipient,
            subject=message.subject,
            priority=message.priority,
        )
        
        # Send via transport
        result = self._transport.send(secured_message)
        
        if result.success:
            self._sent_count += 1
        
        # Audit if logger present
        if self._audit:
            self._audit.log_send(message, result)
        
        return result
    
    def get_sent_count(self) -> int:
        return self._sent_count
    
    def get_audit_logs(self) -> list[str]:
        if self._audit:
            return self._audit.get_logs()
        return []
    
    def get_capabilities(self) -> dict[str, bool]:
        return {
            "transport": True,
            "security": self._security is not None,
            "audit": self._audit is not None,
        }
