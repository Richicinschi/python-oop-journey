"""Solution: Mediator Chat Room.

Implements the Mediator pattern for chat room communication.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import datetime


class ChatMediator(ABC):
    """Abstract mediator for chat communication."""
    
    @abstractmethod
    def send_message(self, message: str, sender: User, recipient: str | None = None) -> None:
        """Send a message through the mediator.
        
        Args:
            message: The message content.
            sender: The user sending the message.
            recipient: Specific recipient name for DM, None for broadcast.
        """
        pass
    
    @abstractmethod
    def register_user(self, user: User) -> None:
        """Register a user with the mediator.
        
        Args:
            user: User to register.
        """
        pass
    
    @abstractmethod
    def get_user(self, name: str) -> User | None:
        """Get a user by name.
        
        Args:
            name: User name to look up.
        
        Returns:
            User if found, None otherwise.
        """
        pass


class User(ABC):
    """Abstract colleague (user) in the chat system."""
    
    def __init__(self, name: str, mediator: ChatMediator) -> None:
        """Initialize user.
        
        Args:
            name: User's display name.
            mediator: The chat mediator.
        """
        self._name = name
        self._mediator = mediator
        self._inbox: List[dict] = []
    
    @property
    def name(self) -> str:
        """Get user name."""
        return self._name
    
    def send(self, message: str, recipient: str | None = None) -> None:
        """Send a message through the mediator.
        
        Args:
            message: Message content.
            recipient: Recipient name for DM, None for broadcast.
        """
        self._mediator.send_message(message, self, recipient)
    
    @abstractmethod
    def receive(self, message: str, sender: str) -> None:
        """Receive a message.
        
        Args:
            message: Message content.
            sender: Name of the sender.
        """
        pass
    
    def get_inbox(self) -> List[dict]:
        """Get received messages.
        
        Returns:
            List of message dictionaries.
        """
        return self._inbox.copy()


class ChatRoom(ChatMediator):
    """Concrete mediator implementing a chat room."""
    
    def __init__(self, name: str) -> None:
        """Initialize chat room.
        
        Args:
            name: Chat room name.
        """
        self._name = name
        self._users: Dict[str, User] = {}
        self._history: List[dict] = []
    
    @property
    def name(self) -> str:
        """Get chat room name."""
        return self._name
    
    def register_user(self, user: User) -> None:
        """Register a user.
        
        Args:
            user: User to register.
        """
        self._users[user.name] = user
    
    def get_user(self, name: str) -> User | None:
        """Get user by name.
        
        Args:
            name: User name.
        
        Returns:
            User or None.
        """
        return self._users.get(name)
    
    def send_message(self, message: str, sender: User, recipient: str | None = None) -> None:
        """Send message to recipient(s).
        
        Args:
            message: Message content.
            sender: Sending user.
            recipient: Recipient name for DM, None for broadcast.
        """
        timestamp = datetime.now().isoformat()
        
        if recipient:
            # Direct message
            target_user = self._users.get(recipient)
            if target_user and target_user != sender:
                target_user.receive(message, sender.name)
                self._history.append({
                    "type": "dm",
                    "from": sender.name,
                    "to": recipient,
                    "message": message,
                    "timestamp": timestamp,
                })
        else:
            # Broadcast to all except sender
            for user in self._users.values():
                if user != sender:
                    user.receive(message, sender.name)
            self._history.append({
                "type": "broadcast",
                "from": sender.name,
                "message": message,
                "timestamp": timestamp,
            })
    
    def get_users(self) -> List[str]:
        """Get list of registered user names.
        
        Returns:
            List of user names.
        """
        return list(self._users.keys())
    
    def get_history(self) -> List[dict]:
        """Get message history.
        
        Returns:
            List of message records.
        """
        return self._history.copy()


class ChatUser(User):
    """Concrete colleague implementing a chat user."""
    
    def __init__(self, name: str, mediator: ChatMediator) -> None:
        """Initialize chat user.
        
        Args:
            name: User name.
            mediator: Chat mediator.
        """
        super().__init__(name, mediator)
    
    def receive(self, message: str, sender: str) -> None:
        """Receive a message.
        
        Args:
            message: Message content.
            sender: Sender name.
        """
        self._inbox.append({
            "message": message,
            "sender": sender,
            "timestamp": datetime.now().isoformat(),
        })
