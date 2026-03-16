"""Reference solution for Problem 03: Notification Dispatcher Fixture Suite."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Generic, Optional, TypeVar
from datetime import datetime


class NotificationPriority(Enum):
    """Priority levels for notifications."""
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()
    URGENT = auto()


class NotificationChannel(Enum):
    """Available notification channels."""
    EMAIL = auto()
    SMS = auto()
    PUSH = auto()


@dataclass
class Notification:
    """Domain object representing a notification to be sent."""
    recipient_id: str
    message: str
    channel: NotificationChannel
    priority: NotificationPriority = NotificationPriority.NORMAL
    metadata: dict[str, str] = field(default_factory=dict)


T = TypeVar('T')


@dataclass
class DispatchResult:
    """Result of a notification dispatch attempt."""
    notification: Notification
    success: bool
    timestamp: str
    error_message: Optional[str] = None
    provider_response: Optional[str] = None


class NotificationProvider(ABC, Generic[T]):
    """Abstract provider for sending notifications via a specific channel."""
    
    @abstractmethod
    def send(self, notification: Notification) -> T:
        """Send a notification through this provider."""
        pass
    
    @abstractmethod
    def get_channel(self) -> NotificationChannel:
        """Return the channel this provider handles."""
        pass
    
    @abstractmethod
    def is_healthy(self) -> bool:
        """Check if the provider is available and healthy."""
        pass


class NotificationDispatcher:
    """Routes notifications to appropriate providers based on channel."""
    
    def __init__(self) -> None:
        """Initialize with empty provider registry."""
        self._providers: dict[NotificationChannel, NotificationProvider] = {}
        self._stats = {"total": 0, "success": 0, "failed": 0}
    
    def register_provider(self, provider: NotificationProvider) -> None:
        """Register a provider for its channel."""
        channel = provider.get_channel()
        if channel in self._providers:
            raise ValueError(f"Provider for channel {channel} already registered")
        self._providers[channel] = provider
    
    def dispatch(self, notification: Notification) -> DispatchResult:
        """Dispatch a notification to the appropriate provider."""
        self._stats["total"] += 1
        
        channel = notification.channel
        provider = self._providers.get(channel)
        
        if provider is None:
            self._stats["failed"] += 1
            raise RuntimeError(f"No provider registered for channel {channel}")
        
        if not provider.is_healthy():
            self._stats["failed"] += 1
            return DispatchResult(
                notification=notification,
                success=False,
                timestamp=datetime.now().isoformat(),
                error_message=f"Provider for {channel} is not healthy"
            )
        
        try:
            response = provider.send(notification)
            self._stats["success"] += 1
            return DispatchResult(
                notification=notification,
                success=True,
                timestamp=datetime.now().isoformat(),
                provider_response=str(response)
            )
        except Exception as e:
            self._stats["failed"] += 1
            return DispatchResult(
                notification=notification,
                success=False,
                timestamp=datetime.now().isoformat(),
                error_message=str(e)
            )
    
    def dispatch_batch(self, notifications: list[Notification]) -> list[DispatchResult]:
        """Dispatch multiple notifications in priority order."""
        priority_order = {
            NotificationPriority.URGENT: 0,
            NotificationPriority.HIGH: 1,
            NotificationPriority.NORMAL: 2,
            NotificationPriority.LOW: 3
        }
        
        sorted_notifications = sorted(
            notifications,
            key=lambda n: priority_order[n.priority]
        )
        
        results = []
        original_indices = {id(n): i for i, n in enumerate(notifications)}
        temp_results: dict[int, DispatchResult] = {}
        
        for notification in sorted_notifications:
            result = self.dispatch(notification)
            temp_results[original_indices[id(notification)]] = result
        
        # Return results in original order
        for i in range(len(notifications)):
            results.append(temp_results[i])
        
        return results
    
    def get_provider_for(self, channel: NotificationChannel) -> Optional[NotificationProvider]:
        """Get the registered provider for a channel."""
        return self._providers.get(channel)
    
    def is_channel_available(self, channel: NotificationChannel) -> bool:
        """Check if a channel has a healthy provider."""
        provider = self._providers.get(channel)
        return provider.is_healthy() if provider else False
    
    def get_stats(self) -> dict[str, int]:
        """Return dispatch statistics."""
        return self._stats.copy()


class EmailProvider(NotificationProvider[dict]):
    """Email notification provider."""
    
    def __init__(self, failure_rate: float = 0.0, latency_ms: int = 0) -> None:
        """Initialize provider."""
        self._failure_rate = max(0.0, min(1.0, failure_rate))
        self._latency_ms = max(0, latency_ms)
        self._healthy = True
        self._sent_count = 0
    
    def send(self, notification: Notification) -> dict:
        """Send email notification."""
        import random
        import time
        
        if self._latency_ms > 0:
            time.sleep(self._latency_ms / 1000.0)
        
        if random.random() < self._failure_rate:
            raise RuntimeError("Simulated email delivery failure")
        
        self._sent_count += 1
        return {
            "message_id": f"email_{self._sent_count}",
            "recipient": notification.recipient_id,
            "status": "sent"
        }
    
    def get_channel(self) -> NotificationChannel:
        """Return EMAIL channel."""
        return NotificationChannel.EMAIL
    
    def is_healthy(self) -> bool:
        """Check health status."""
        return self._healthy
    
    def set_healthy(self, healthy: bool) -> None:
        """Set health status (for testing)."""
        self._healthy = healthy


class SMSProvider(NotificationProvider[str]):
    """SMS notification provider."""
    
    def __init__(self, max_length: int = 160, failure_rate: float = 0.0) -> None:
        """Initialize provider."""
        self._max_length = max_length
        self._failure_rate = max(0.0, min(1.0, failure_rate))
        self._healthy = True
        self._sent_count = 0
    
    def send(self, notification: Notification) -> str:
        """Send SMS notification."""
        import random
        
        if len(notification.message) > self._max_length:
            raise ValueError(f"Message exceeds {self._max_length} characters")
        
        if random.random() < self._failure_rate:
            raise RuntimeError("Simulated SMS delivery failure")
        
        self._sent_count += 1
        return f"SMS_{self._sent_count}:sent"
    
    def get_channel(self) -> NotificationChannel:
        """Return SMS channel."""
        return NotificationChannel.SMS
    
    def is_healthy(self) -> bool:
        """Check health status."""
        return self._healthy
    
    def set_healthy(self, healthy: bool) -> None:
        """Set health status (for testing)."""
        self._healthy = healthy


class PushProvider(NotificationProvider[bool]):
    """Push notification provider."""
    
    def __init__(self, requires_ack: bool = False) -> None:
        """Initialize provider."""
        self._requires_ack = requires_ack
        self._healthy = True
        self._sent_count = 0
        self._acked: set[str] = set()
    
    def send(self, notification: Notification) -> bool:
        """Send push notification."""
        self._sent_count += 1
        message_id = f"push_{notification.recipient_id}_{self._sent_count}"
        if not self._requires_ack:
            return True
        return message_id in self._acked
    
    def get_channel(self) -> NotificationChannel:
        """Return PUSH channel."""
        return NotificationChannel.PUSH
    
    def is_healthy(self) -> bool:
        """Check health status."""
        return self._healthy
    
    def set_healthy(self, healthy: bool) -> None:
        """Set health status (for testing)."""
        self._healthy = healthy
    
    def acknowledge(self, message_id: str) -> None:
        """Acknowledge a message (for testing)."""
        self._acked.add(message_id)
