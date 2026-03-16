"""Problem 01: Factory Method Notifications

Topic: Factory Method Pattern
Difficulty: Medium

Implement the Factory Method pattern for creating different types of notifications.
The pattern should allow adding new notification types without modifying existing code.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Notification(ABC):
    """Product interface for notifications.
    
    All notification types must implement this interface.
    """
    
    def __init__(self, recipient: str) -> None:
        """Initialize notification with recipient.
        
        Args:
            recipient: The target recipient for this notification
        """
        raise NotImplementedError("Implement Notification.__init__")
    
    @abstractmethod
    def send(self, message: str) -> str:
        """Send the notification with the given message.
        
        Args:
            message: The message content to send
            
        Returns:
            Confirmation string indicating how the message was sent
        """
        raise NotImplementedError("Implement Notification.send")
    
    @abstractmethod
    def get_channel(self) -> str:
        """Return the notification channel name.
        
        Returns:
            String identifying the channel (e.g., 'email', 'sms')
        """
        raise NotImplementedError("Implement Notification.get_channel")


class EmailNotification(Notification):
    """Concrete product: Email notification."""
    
    def __init__(self, recipient: str) -> None:
        """Initialize email notification.
        
        Args:
            recipient: Email address of the recipient
        """
        raise NotImplementedError("Implement EmailNotification.__init__")
    
    def send(self, message: str) -> str:
        """Send email notification.
        
        Returns:
            Format: "[EMAIL] To: {recipient} | Message: {message}"
        """
        raise NotImplementedError("Implement EmailNotification.send")
    
    def get_channel(self) -> str:
        """Return 'email'."""
        raise NotImplementedError("Implement EmailNotification.get_channel")


class SMSNotification(Notification):
    """Concrete product: SMS notification."""
    
    def __init__(self, recipient: str) -> None:
        """Initialize SMS notification.
        
        Args:
            recipient: Phone number of the recipient
        """
        raise NotImplementedError("Implement SMSNotification.__init__")
    
    def send(self, message: str) -> str:
        """Send SMS notification.
        
        Returns:
            Format: "[SMS] To: {recipient} | Message: {message}"
        """
        raise NotImplementedError("Implement SMSNotification.send")
    
    def get_channel(self) -> str:
        """Return 'sms'."""
        raise NotImplementedError("Implement SMSNotification.get_channel")


class PushNotification(Notification):
    """Concrete product: Push notification."""
    
    def __init__(self, recipient: str) -> None:
        """Initialize push notification.
        
        Args:
            recipient: Device token of the recipient
        """
        raise NotImplementedError("Implement PushNotification.__init__")
    
    def send(self, message: str) -> str:
        """Send push notification.
        
        Returns:
            Format: "[PUSH] To: {recipient} | Message: {message}"
        """
        raise NotImplementedError("Implement PushNotification.send")
    
    def get_channel(self) -> str:
        """Return 'push'."""
        raise NotImplementedError("Implement PushNotification.get_channel")


class NotificationFactory(ABC):
    """Creator abstract class.
    
    Declares the factory method that returns Notification objects.
    """
    
    @abstractmethod
    def create_notification(self, recipient: str) -> Notification:
        """Factory method to create a notification.
        
        Args:
            recipient: The recipient for the notification
            
        Returns:
            A Notification instance
        """
        raise NotImplementedError("Implement NotificationFactory.create_notification")
    
    def send_notification(self, recipient: str, message: str) -> str:
        """Business logic that uses the factory method.
        
        Creates a notification and sends the message.
        
        Args:
            recipient: The recipient for the notification
            message: The message to send
            
        Returns:
            The result of sending the notification
        """
        raise NotImplementedError("Implement NotificationFactory.send_notification")


class EmailNotificationFactory(NotificationFactory):
    """Concrete creator for email notifications."""
    
    def create_notification(self, recipient: str) -> Notification:
        """Create an EmailNotification instance."""
        raise NotImplementedError("Implement EmailNotificationFactory.create_notification")


class SMSNotificationFactory(NotificationFactory):
    """Concrete creator for SMS notifications."""
    
    def create_notification(self, recipient: str) -> Notification:
        """Create an SMSNotification instance."""
        raise NotImplementedError("Implement SMSNotificationFactory.create_notification")


class PushNotificationFactory(NotificationFactory):
    """Concrete creator for push notifications."""
    
    def create_notification(self, recipient: str) -> Notification:
        """Create a PushNotification instance."""
        raise NotImplementedError("Implement PushNotificationFactory.create_notification")
