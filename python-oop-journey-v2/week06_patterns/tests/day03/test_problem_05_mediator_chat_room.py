"""Tests for Problem 05: Mediator Chat Room."""

from __future__ import annotations

import pytest
from abc import ABC

from week06_patterns.solutions.day03.problem_05_mediator_chat_room import (
    ChatMediator,
    User,
    ChatRoom,
    ChatUser,
)


class TestChatMediator:
    """Test ChatMediator abstract base class."""
    
    def test_chat_mediator_is_abstract(self) -> None:
        """Test that ChatMediator cannot be instantiated."""
        assert issubclass(ChatMediator, ABC)
        with pytest.raises(TypeError, match="abstract"):
            ChatMediator()
    
    def test_chat_mediator_has_required_methods(self) -> None:
        """Test that ChatMediator defines required methods."""
        assert hasattr(ChatMediator, 'send_message')
        assert hasattr(ChatMediator, 'register_user')
        assert hasattr(ChatMediator, 'get_user')


class TestUser:
    """Test User abstract base class."""
    
    def test_user_is_abstract(self) -> None:
        """Test that User cannot be instantiated directly."""
        assert issubclass(User, ABC)
    
    def test_user_init_requires_name_and_mediator(self) -> None:
        """Test User initialization requires name and mediator."""
        # Need concrete implementation to test
        chat_room = ChatRoom("Test")
        user = ChatUser("Alice", chat_room)
        
        assert user.name == "Alice"


class TestChatRoom:
    """Test ChatRoom mediator."""
    
    def test_initialization(self) -> None:
        """Test chat room initialization."""
        room = ChatRoom("General")
        assert room.name == "General"
        assert room.get_users() == []
        assert room.get_history() == []
    
    def test_register_user(self) -> None:
        """Test registering users."""
        room = ChatRoom("General")
        alice = ChatUser("Alice", room)
        bob = ChatUser("Bob", room)
        
        room.register_user(alice)
        room.register_user(bob)
        
        assert room.get_users() == ["Alice", "Bob"]
    
    def test_get_user(self) -> None:
        """Test getting user by name."""
        room = ChatRoom("General")
        alice = ChatUser("Alice", room)
        
        room.register_user(alice)
        
        assert room.get_user("Alice") == alice
        assert room.get_user("Bob") is None
    
    def test_broadcast_message(self) -> None:
        """Test broadcasting message to all users."""
        room = ChatRoom("General")
        alice = ChatUser("Alice", room)
        bob = ChatUser("Bob", room)
        charlie = ChatUser("Charlie", room)
        
        room.register_user(alice)
        room.register_user(bob)
        room.register_user(charlie)
        
        alice.send("Hello everyone!")
        
        # Bob and Charlie should receive
        assert len(bob.get_inbox()) == 1
        assert bob.get_inbox()[0]["message"] == "Hello everyone!"
        assert bob.get_inbox()[0]["sender"] == "Alice"
        
        assert len(charlie.get_inbox()) == 1
        
        # Alice should not receive her own message
        assert len(alice.get_inbox()) == 0
    
    def test_direct_message(self) -> None:
        """Test sending direct message."""
        room = ChatRoom("General")
        alice = ChatUser("Alice", room)
        bob = ChatUser("Bob", room)
        charlie = ChatUser("Charlie", room)
        
        room.register_user(alice)
        room.register_user(bob)
        room.register_user(charlie)
        
        alice.send("Hi Bob!", recipient="Bob")
        
        # Only Bob should receive
        assert len(bob.get_inbox()) == 1
        assert bob.get_inbox()[0]["message"] == "Hi Bob!"
        
        # Charlie should not receive
        assert len(charlie.get_inbox()) == 0
        
        # Alice should not receive
        assert len(alice.get_inbox()) == 0
    
    def test_dm_to_nonexistent_user(self) -> None:
        """Test DM to non-existent user is handled gracefully."""
        room = ChatRoom("General")
        alice = ChatUser("Alice", room)
        bob = ChatUser("Bob", room)
        
        room.register_user(alice)
        room.register_user(bob)
        
        # DM to non-existent user
        alice.send("Hello?", recipient="Charlie")
        
        # Bob should not receive
        assert len(bob.get_inbox()) == 0
    
    def test_dm_to_self_not_received(self) -> None:
        """Test DM to self is not received."""
        room = ChatRoom("General")
        alice = ChatUser("Alice", room)
        
        room.register_user(alice)
        
        alice.send("Note to self", recipient="Alice")
        
        # Alice should not receive her own DM
        assert len(alice.get_inbox()) == 0
    
    def test_message_history(self) -> None:
        """Test message history is recorded."""
        room = ChatRoom("General")
        alice = ChatUser("Alice", room)
        bob = ChatUser("Bob", room)
        
        room.register_user(alice)
        room.register_user(bob)
        
        alice.send("Hello!")
        bob.send("Hi there!", recipient="Alice")
        
        history = room.get_history()
        assert len(history) == 2
        
        # Check broadcast record
        assert history[0]["type"] == "broadcast"
        assert history[0]["from"] == "Alice"
        assert history[0]["message"] == "Hello!"
        assert "timestamp" in history[0]
        
        # Check DM record
        assert history[1]["type"] == "dm"
        assert history[1]["from"] == "Bob"
        assert history[1]["to"] == "Alice"
        assert history[1]["message"] == "Hi there!"
    
    def test_get_history_returns_copy(self) -> None:
        """Test get_history returns a copy."""
        room = ChatRoom("General")
        alice = ChatUser("Alice", room)
        
        room.register_user(alice)
        alice.send("Hello!")
        
        history = room.get_history()
        history.append({"fake": "record"})
        
        # Original should be unchanged
        assert len(room.get_history()) == 1


class TestChatUser:
    """Test ChatUser colleague."""
    
    def test_initialization(self) -> None:
        """Test user initialization."""
        room = ChatRoom("General")
        alice = ChatUser("Alice", room)
        
        assert alice.name == "Alice"
        assert alice.get_inbox() == []
    
    def test_send_delegates_to_mediator(self) -> None:
        """Test send delegates to mediator."""
        room = ChatRoom("General")
        alice = ChatUser("Alice", room)
        bob = ChatUser("Bob", room)
        
        room.register_user(alice)
        room.register_user(bob)
        
        alice.send("Hello Bob!", recipient="Bob")
        
        # Message should be delivered
        assert len(bob.get_inbox()) == 1
        assert bob.get_inbox()[0]["message"] == "Hello Bob!"
    
    def test_receive_stores_message(self) -> None:
        """Test receive stores message in inbox."""
        room = ChatRoom("General")
        alice = ChatUser("Alice", room)
        
        room.register_user(alice)
        
        # Manually receive a message (simulating delivery)
        alice.receive("Test message", "Sender")
        
        inbox = alice.get_inbox()
        assert len(inbox) == 1
        assert inbox[0]["message"] == "Test message"
        assert inbox[0]["sender"] == "Sender"
        assert "timestamp" in inbox[0]
    
    def test_get_inbox_returns_copy(self) -> None:
        """Test get_inbox returns a copy."""
        room = ChatRoom("General")
        alice = ChatUser("Alice", room)
        
        room.register_user(alice)
        alice.receive("Message", "Sender")
        
        inbox = alice.get_inbox()
        inbox.append({"fake": "message"})
        
        # Original should be unchanged
        assert len(alice.get_inbox()) == 1
    
    def test_multiple_messages_in_inbox(self) -> None:
        """Test inbox with multiple messages."""
        room = ChatRoom("General")
        alice = ChatUser("Alice", room)
        bob = ChatUser("Bob", room)
        charlie = ChatUser("Charlie", room)
        
        room.register_user(alice)
        room.register_user(bob)
        room.register_user(charlie)
        
        bob.send("Message 1", recipient="Alice")
        charlie.send("Message 2", recipient="Alice")
        bob.send("Message 3", recipient="Alice")
        
        inbox = alice.get_inbox()
        assert len(inbox) == 3
        assert inbox[0]["message"] == "Message 1"
        assert inbox[1]["message"] == "Message 2"
        assert inbox[2]["message"] == "Message 3"


class TestIntegration:
    """Integration tests for the complete system."""
    
    def test_full_chat_scenario(self) -> None:
        """Test a full chat scenario."""
        room = ChatRoom("Tech Discussion")
        
        alice = ChatUser("Alice", room)
        bob = ChatUser("Bob", room)
        charlie = ChatUser("Charlie", room)
        dave = ChatUser("Dave", room)
        
        for user in [alice, bob, charlie, dave]:
            room.register_user(user)
        
        # Alice broadcasts to everyone
        alice.send("Hey team! Ready for the meeting?")
        
        # Bob DMs Alice
        bob.send("Yes, I'll join in 5", recipient="Alice")
        
        # Charlie broadcasts
        charlie.send("Running a bit late, start without me")
        
        # Dave DMs Alice about Charlie
        dave.send("Should we wait?", recipient="Alice")
        
        # Check inboxes
        # Alice receives: Bob's DM, Charlie's broadcast, Dave's DM = 3
        assert len(alice.get_inbox()) == 3
        # Bob receives: Alice's broadcast, Charlie's broadcast = 2
        assert len(bob.get_inbox()) == 2
        # Charlie receives: Alice's broadcast (not his own) = 1
        assert len(charlie.get_inbox()) == 1
        # Dave receives: Alice's broadcast, Charlie's broadcast = 2
        assert len(dave.get_inbox()) == 2
        
        # Check history
        history = room.get_history()
        assert len(history) == 4
        assert history[0]["type"] == "broadcast"
        assert history[1]["type"] == "dm"
        assert history[2]["type"] == "broadcast"
        assert history[3]["type"] == "dm"
    
    def test_users_in_multiple_rooms(self) -> None:
        """Test that users are isolated to their rooms."""
        room1 = ChatRoom("Room 1")
        room2 = ChatRoom("Room 2")
        
        alice1 = ChatUser("Alice", room1)
        bob1 = ChatUser("Bob", room1)
        alice2 = ChatUser("Alice", room2)  # Same name, different room
        bob2 = ChatUser("Bob", room2)
        
        room1.register_user(alice1)
        room1.register_user(bob1)
        room2.register_user(alice2)
        room2.register_user(bob2)
        
        # Message in room 1
        alice1.send("Hello Room 1!")
        
        # Only room 1 users receive
        assert len(bob1.get_inbox()) == 1
        assert len(bob2.get_inbox()) == 0
        
        # Message in room 2
        alice2.send("Hello Room 2!")
        
        assert len(bob2.get_inbox()) == 1
        assert "Room 2" in bob2.get_inbox()[0]["message"]
