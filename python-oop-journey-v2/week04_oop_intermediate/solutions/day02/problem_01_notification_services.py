"""Reference solution for Problem 01: Notification Services."""

from __future__ import annotations


class BaseNotification:
    """Base notification class with common functionality."""

    def __init__(self, message: str) -> None:
        """Initialize with a message."""
        self.message = message

    def _log(self, action: str) -> None:
        """Log the notification action (print to stdout)."""
        print(f"[LOG] {action}")

    def send(self) -> str:
        """Send the notification. Returns confirmation message."""
        self._log(f"Sending notification: {self.message}")
        return f"Notification sent: {self.message}"


class EmailNotification(BaseNotification):
    """Email notification with recipient and subject."""

    def __init__(self, message: str, recipient: str, subject: str) -> None:
        """Initialize email notification.
        
        Args:
            message: The email body content
            recipient: Email address of recipient
            subject: Email subject line
        """
        super().__init__(message)
        self.recipient = recipient
        self.subject = subject

    def send(self) -> str:
        """Send email notification.
        
        Calls parent _log() method and returns formatted string.
        """
        self._log(f"Sending email to {self.recipient}")
        return f"Email to {self.recipient} [{self.subject}]: {self.message}"


class SMSNotification(BaseNotification):
    """SMS notification with phone number validation."""

    def __init__(self, message: str, phone_number: str) -> None:
        """Initialize SMS notification.
        
        Args:
            message: SMS text content
            phone_number: Recipient phone number
            
        Raises:
            ValueError: If phone_number is empty or doesn't start with '+'
        """
        if not phone_number or not phone_number.startswith("+"):
            raise ValueError("Phone number must start with '+'")
        super().__init__(message)
        self.phone_number = phone_number

    def send(self) -> str:
        """Send SMS notification.
        
        Calls parent _log() method and returns formatted string.
        """
        self._log(f"Sending SMS to {self.phone_number}")
        return f"SMS to {self.phone_number}: {self.message}"


class PushNotification(BaseNotification):
    """Push notification with priority level."""

    PRIORITIES = ("low", "normal", "high", "urgent")

    def __init__(self, message: str, priority: str = "normal") -> None:
        """Initialize push notification.
        
        Args:
            message: Push notification content
            priority: One of "low", "normal", "high", "urgent"
            
        Raises:
            ValueError: If priority is not in PRIORITIES
        """
        if priority not in self.PRIORITIES:
            raise ValueError(f"Priority must be one of {self.PRIORITIES}")
        super().__init__(message)
        self.priority = priority

    def send(self) -> str:
        """Send push notification.
        
        Calls parent _log() method and returns formatted string.
        """
        self._log(f"Sending push notification [{self.priority}]")
        return f"Push [{self.priority}]: {self.message}"
