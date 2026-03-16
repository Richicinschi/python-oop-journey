"""Problem 05: Mediator Chat Room

Topic: Mediator Pattern
Difficulty: Medium

Implement the Mediator pattern for a chat room system.

HINTS:
- Hint 1 (Conceptual): Users should NOT communicate directly. All messages go 
  through the ChatRoom mediator which decides who receives what.
- Hint 2 (Structural): ChatRoom tracks registered users. Users have a reference 
  to the mediator. When user.send() is called, it delegates to mediator.send().
- Hint 3 (Edge Case): Handle direct messages (recipient specified) vs broadcasts 
  (no recipient). Don't send messages back to the sender in broadcasts.

PATTERN EXPLANATION:
The Mediator pattern defines an object that encapsulates how a set of objects
interact. It promotes loose coupling by preventing objects from referring to
each other explicitly.

STRUCTURE:
- Mediator (ChatMediator): Interface for communication between colleagues
- ConcreteMediator (ChatRoom): Implements cooperative behavior, routes messages
- Colleague (User): Communicates through mediator
- ConcreteColleague (ChatUser): Sends/receives messages via mediator

WHEN TO USE:
- When many objects need to communicate in complex ways
- To reduce coupling between components
- When reusing components is difficult due to many interconnections

EXAMPLE USAGE:
    chat = ChatRoom("General")
    
    alice = ChatUser("Alice", chat)
    bob = ChatUser("Bob", chat)
    
    chat.register_user(alice)
    chat.register_user(bob)
    
    # Broadcast to all
    alice.send("Hello everyone!")  # Bob receives
    
    # Direct message
    alice.send("Hey Bob!", recipient="Bob")  # Only Bob receives

TODO:
1. Create ChatMediator abstract base class with send method
2. Create User (Colleague) abstract base class
3. Implement ChatRoom as concrete mediator
4. Implement ChatUser as concrete colleague
5. Support direct messages and broadcast messages
6. Track message history
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict


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
        # TODO: Implement abstract send_message
        raise NotImplementedError("send_message must be implemented")
    
    @abstractmethod
    def register_user(self, user: User) -> None:
        """Register a user with the mediator.
        
        Args:
            user: User to register.
        """
        # TODO: Implement abstract register_user
        raise NotImplementedError("register_user must be implemented")
    
    @abstractmethod
    def get_user(self, name: str) -> User | None:
        """Get a user by name.
        
        Args:
            name: User name to look up.
        
        Returns:
            User if found, None otherwise.
        """
        # TODO: Implement abstract get_user
        raise NotImplementedError("get_user must be implemented")


class User(ABC):
    """Abstract colleague (user) in the chat system."""
    
    def __init__(self, name: str, mediator: ChatMediator) -> None:
        """Initialize user.
        
        Args:
            name: User's display name.
            mediator: The chat mediator.
        """
        # TODO: Store name, mediator, and initialize inbox
        raise NotImplementedError("Initialize user")
    
    @property
    def name(self) -> str:
        """Get user name."""
        # TODO: Return name
        raise NotImplementedError("Return name")
    
    def send(self, message: str, recipient: str | None = None) -> None:
        """Send a message through the mediator.
        
        Args:
            message: Message content.
            recipient: Recipient name for DM, None for broadcast.
        """
        # TODO: Send message through mediator
        raise NotImplementedError("Send message")
    
    @abstractmethod
    def receive(self, message: str, sender: str) -> None:
        """Receive a message.
        
        Args:
            message: Message content.
            sender: Name of the sender.
        """
        # TODO: Implement abstract receive
        raise NotImplementedError("receive must be implemented")
    
    def get_inbox(self) -> List[dict]:
        """Get received messages.
        
        Returns:
            List of message dictionaries.
        """
        # TODO: Return inbox copy
        raise NotImplementedError("Get inbox")


class ChatRoom(ChatMediator):
    """Concrete mediator implementing a chat room."""
    
    def __init__(self, name: str) -> None:
        """Initialize chat room.
        
        Args:
            name: Chat room name.
        """
        # TODO: Initialize name, users dict, and message history
        raise NotImplementedError("Initialize chat room")
    
    @property
    def name(self) -> str:
        """Get chat room name."""
        # TODO: Return name
        raise NotImplementedError("Return name")
    
    def register_user(self, user: User) -> None:
        """Register a user.
        
        Args:
            user: User to register.
        """
        # TODO: Add user to users dict with name as key
        raise NotImplementedError("Register user")
    
    def get_user(self, name: str) -> User | None:
        """Get user by name.
        
        Args:
            name: User name.
        
        Returns:
            User or None.
        """
        # TODO: Return user from users dict
        raise NotImplementedError("Get user")
    
    def send_message(self, message: str, sender: User, recipient: str | None = None) -> None:
        """Send message to recipient(s).
        
        Args:
            message: Message content.
            sender: Sending user.
            recipient: Recipient name for DM, None for broadcast.
        """
        # TODO: If recipient specified, send DM. Otherwise broadcast to all except sender
        raise NotImplementedError("Send message")
    
    def get_users(self) -> List[str]:
        """Get list of registered user names.
        
        Returns:
            List of user names.
        """
        # TODO: Return list of user names
        raise NotImplementedError("Get users")
    
    def get_history(self) -> List[dict]:
        """Get message history.
        
        Returns:
            List of message records.
        """
        # TODO: Return history copy
        raise NotImplementedError("Get history")


class ChatUser(User):
    """Concrete colleague implementing a chat user."""
    
    def __init__(self, name: str, mediator: ChatMediator) -> None:
        """Initialize chat user.
        
        Args:
            name: User name.
            mediator: Chat mediator.
        """
        # TODO: Call parent __init__
        raise NotImplementedError("Initialize chat user")
    
    def receive(self, message: str, sender: str) -> None:
        """Receive a message.
        
        Args:
            message: Message content.
            sender: Sender name.
        """
        # TODO: Store message in inbox with sender info
        raise NotImplementedError("Receive message")
