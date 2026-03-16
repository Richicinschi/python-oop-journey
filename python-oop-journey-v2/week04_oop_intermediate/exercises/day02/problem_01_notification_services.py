"""Problem 01: Notification Services

Topic: Method overriding with super()
Difficulty: Easy

Create a notification service hierarchy where different notification types
override the base send() method while sharing common logging functionality.

Classes to implement:
- BaseNotification: Base class with send() and _log() methods
- EmailNotification: Sends email notifications with subject
- SMSNotification: Sends SMS notifications with phone validation
- PushNotification: Sends push notifications with priority levels

Example:
    >>> base = BaseNotification("Welcome!")
    >>> base.send()
    'Notification sent: Welcome!'
    
    >>> email = EmailNotification("Hello", "user@example.com", "Greeting")
    >>> email.send()
    'Email to user@example.com [Greeting]: Hello'
    
    >>> sms = SMSNotification("Code: 1234", "+1234567890")
    >>> sms.send()
    'SMS to +1234567890: Code: 1234'

Requirements:
    - BaseNotification: message attribute, send() method, _log() helper
    - EmailNotification: extends BaseNotification, adds recipient and subject
    - SMSNotification: extends BaseNotification, adds phone number
    - PushNotification: extends BaseNotification, adds priority
    - Use super() to call parent methods where appropriate
    - All classes must have proper type hints
"""

from __future__ import annotations


class BaseNotification:
    """Base notification class with common functionality."""

    def __init__(self, message: str) -> None:
        """Initialize with a message."""
        raise NotImplementedError("Initialize message attribute")

    def _log(self, action: str) -> None:
        """Log the notification action (print to stdout)."""
        raise NotImplementedError("Implement logging")

    def send(self) -> str:
        """Send the notification. Returns confirmation message."""
        raise NotImplementedError("Implement send()")


class EmailNotification(BaseNotification):
    """Email notification with recipient and subject."""

    def __init__(self, message: str, recipient: str, subject: str) -> None:
        """Initialize email notification.
        
        Args:
            message: The email body content
            recipient: Email address of recipient
            subject: Email subject line
        """
        raise NotImplementedError("Initialize with super() and add email-specific attributes")

    def send(self) -> str:
        """Send email notification.
        
        Should call parent _log() method and return formatted string.
        Format: 'Email to {recipient} [{subject}]: {message}'
        """
        raise NotImplementedError("Override send() using super()")


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
        raise NotImplementedError("Initialize with super() and validate phone")

    def send(self) -> str:
        """Send SMS notification.
        
        Should call parent _log() method and return formatted string.
        Format: 'SMS to {phone_number}: {message}'
        """
        raise NotImplementedError("Override send() using super()")


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
        raise NotImplementedError("Initialize with super() and validate priority")

    def send(self) -> str:
        """Send push notification.
        
        Should call parent _log() method and return formatted string.
        Format: 'Push [{priority}]: {message}'
        """
        raise NotImplementedError("Override send() using super()")
