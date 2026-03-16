"""Reference solution for Problem 01: Factory Method Notifications.

WHY FACTORY METHOD?
The Factory Method pattern lets us defer instantiation to subclasses. This is
useful when:
- A class can't anticipate the class of objects it must create
- A class wants its subclasses to specify the objects it creates
- Classes delegate responsibility to helper subclasses

KEY BENEFIT: Adding new notification types (e.g., WhatsAppNotification) only
requires creating a new concrete product and factory, without modifying any
existing code (Open/Closed Principle).
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Notification(ABC):
    """Product interface for notifications."""
    
    def __init__(self, recipient: str) -> None:
        self.recipient = recipient
    
    @abstractmethod
    def send(self, message: str) -> str:
        """Send the notification with the given message."""
        pass
    
    @abstractmethod
    def get_channel(self) -> str:
        """Return the notification channel name."""
        pass


class EmailNotification(Notification):
    """Concrete product: Email notification."""
    
    def __init__(self, recipient: str) -> None:
        super().__init__(recipient)
    
    def send(self, message: str) -> str:
        return f"[EMAIL] To: {self.recipient} | Message: {message}"
    
    def get_channel(self) -> str:
        return "email"


class SMSNotification(Notification):
    """Concrete product: SMS notification."""
    
    def __init__(self, recipient: str) -> None:
        super().__init__(recipient)
    
    def send(self, message: str) -> str:
        return f"[SMS] To: {self.recipient} | Message: {message}"
    
    def get_channel(self) -> str:
        return "sms"


class PushNotification(Notification):
    """Concrete product: Push notification."""
    
    def __init__(self, recipient: str) -> None:
        super().__init__(recipient)
    
    def send(self, message: str) -> str:
        return f"[PUSH] To: {self.recipient} | Message: {message}"
    
    def get_channel(self) -> str:
        return "push"


class NotificationFactory(ABC):
    """Creator abstract class.
    
    The creator contains the business logic that uses the product (Notification).
    The factory method allows subclasses to decide which concrete product to
    instantiate, keeping the business logic decoupled from specific notification
    implementations.
    """
    
    @abstractmethod
    def create_notification(self, recipient: str) -> Notification:
        """Factory method to create a notification.
        
        This is the 'hook' that subclasses override to provide specific
        notification types. The creator doesn't know or care which concrete
        notification class is instantiated.
        """
        pass
    
    def send_notification(self, recipient: str, message: str) -> str:
        """Business logic that uses the factory method.
        
        This method demonstrates how the creator works with any product
        implementation without knowing its concrete type.
        """
        notification = self.create_notification(recipient)
        return notification.send(message)


class EmailNotificationFactory(NotificationFactory):
    """Concrete creator for email notifications."""
    
    def create_notification(self, recipient: str) -> Notification:
        return EmailNotification(recipient)


class SMSNotificationFactory(NotificationFactory):
    """Concrete creator for SMS notifications."""
    
    def create_notification(self, recipient: str) -> Notification:
        return SMSNotification(recipient)


class PushNotificationFactory(NotificationFactory):
    """Concrete creator for push notifications."""
    
    def create_notification(self, recipient: str) -> Notification:
        return PushNotification(recipient)
