"""Tests for Problem 02: Repository Pattern with Service Layer."""

from __future__ import annotations

import pytest

from week07_real_world.solutions.day01.problem_02_repository_service_layer import (
    InMemoryUserRepository,
    Repository,
    User,
    UserService,
)


class TestUser:
    """Tests for User dataclass."""
    
    def test_user_creation(self) -> None:
        """Test creating a User."""
        user = User(email="test@example.com", name="Test User")
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.id == 0
        assert user.is_active is True
    
    def test_user_with_id(self) -> None:
        """Test creating a User with explicit ID."""
        user = User(id=5, email="test@example.com", name="Test User", is_active=False)
        assert user.id == 5
        assert user.is_active is False


class TestInMemoryUserRepository:
    """Tests for InMemoryUserRepository."""
    
    def test_add_user(self) -> None:
        """Test adding a user assigns ID."""
        repo = InMemoryUserRepository()
        user = User(email="test@example.com", name="Test User")
        
        added = repo.add(user)
        
        assert added.id == 1
        assert added.email == "test@example.com"
    
    def test_add_multiple_users_assigns_incrementing_ids(self) -> None:
        """Test that multiple users get sequential IDs."""
        repo = InMemoryUserRepository()
        
        user1 = repo.add(User(email="user1@example.com", name="User 1"))
        user2 = repo.add(User(email="user2@example.com", name="User 2"))
        user3 = repo.add(User(email="user3@example.com", name="User 3"))
        
        assert user1.id == 1
        assert user2.id == 2
        assert user3.id == 3
    
    def test_get_existing_user(self) -> None:
        """Test getting an existing user."""
        repo = InMemoryUserRepository()
        added = repo.add(User(email="test@example.com", name="Test User"))
        
        fetched = repo.get(added.id)
        
        assert fetched is not None
        assert fetched.id == added.id
        assert fetched.email == "test@example.com"
    
    def test_get_nonexistent_user(self) -> None:
        """Test getting a user that doesn't exist."""
        repo = InMemoryUserRepository()
        
        fetched = repo.get(999)
        
        assert fetched is None
    
    def test_get_all_users(self) -> None:
        """Test getting all users."""
        repo = InMemoryUserRepository()
        repo.add(User(email="user1@example.com", name="User 1"))
        repo.add(User(email="user2@example.com", name="User 2"))
        
        all_users = repo.get_all()
        
        assert len(all_users) == 2
    
    def test_update_user(self) -> None:
        """Test updating a user."""
        repo = InMemoryUserRepository()
        added = repo.add(User(email="old@example.com", name="Old Name"))
        
        added.name = "New Name"
        added.email = "new@example.com"
        updated = repo.update(added)
        
        assert updated.name == "New Name"
        assert updated.email == "new@example.com"
        
        # Verify persistence
        fetched = repo.get(added.id)
        assert fetched.name == "New Name"
    
    def test_update_nonexistent_user(self) -> None:
        """Test updating a user that doesn't exist raises error."""
        repo = InMemoryUserRepository()
        user = User(id=999, email="test@example.com", name="Test")
        
        with pytest.raises(ValueError, match="User with id=999 does not exist"):
            repo.update(user)
    
    def test_delete_existing_user(self) -> None:
        """Test deleting an existing user."""
        repo = InMemoryUserRepository()
        added = repo.add(User(email="test@example.com", name="Test User"))
        
        result = repo.delete(added.id)
        
        assert result is True
        assert repo.get(added.id) is None
    
    def test_delete_nonexistent_user(self) -> None:
        """Test deleting a user that doesn't exist."""
        repo = InMemoryUserRepository()
        
        result = repo.delete(999)
        
        assert result is False
    
    def test_find_by_email(self) -> None:
        """Test finding users by email."""
        repo = InMemoryUserRepository()
        repo.add(User(email="user1@example.com", name="User 1"))
        repo.add(User(email="user2@example.com", name="User 2"))
        
        results = repo.find_by(email="user1@example.com")
        
        assert len(results) == 1
        assert results[0].name == "User 1"
    
    def test_find_by_is_active(self) -> None:
        """Test finding users by is_active."""
        repo = InMemoryUserRepository()
        repo.add(User(email="active@example.com", name="Active", is_active=True))
        repo.add(User(email="inactive@example.com", name="Inactive", is_active=False))
        
        results = repo.find_by(is_active=True)
        
        assert len(results) == 1
        assert results[0].email == "active@example.com"
    
    def test_find_by_multiple_criteria(self) -> None:
        """Test finding users by multiple criteria."""
        repo = InMemoryUserRepository()
        repo.add(User(email="test@example.com", name="Test", is_active=True))
        repo.add(User(email="test@example.com", name="Test 2", is_active=False))
        
        results = repo.find_by(email="test@example.com", is_active=True)
        
        assert len(results) == 1
        assert results[0].name == "Test"
    
    def test_find_by_no_matches(self) -> None:
        """Test finding with no matches."""
        repo = InMemoryUserRepository()
        
        results = repo.find_by(email="nonexistent@example.com")
        
        assert results == []
    
    def test_implements_repository_abc(self) -> None:
        """Test that repository implements the ABC."""
        repo = InMemoryUserRepository()
        assert isinstance(repo, Repository)


class TestUserService:
    """Tests for UserService."""
    
    def test_register_user_success(self) -> None:
        """Test successful user registration."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        user = service.register_user("test@example.com", "Test User")
        
        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.is_active is True
    
    def test_register_user_invalid_email(self) -> None:
        """Test registration with invalid email."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        with pytest.raises(ValueError, match="Invalid email format"):
            service.register_user("invalid-email", "Test User")
    
    def test_register_user_empty_name(self) -> None:
        """Test registration with empty name."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        with pytest.raises(ValueError, match="Name cannot be empty"):
            service.register_user("test@example.com", "")
        
        with pytest.raises(ValueError, match="Name cannot be empty"):
            service.register_user("test@example.com", "   ")
    
    def test_register_user_duplicate_email(self) -> None:
        """Test registration with duplicate email."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        service.register_user("test@example.com", "Test User")
        
        with pytest.raises(ValueError, match="Email already registered"):
            service.register_user("test@example.com", "Another User")
    
    def test_activate_user(self) -> None:
        """Test activating a user."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        user = service.register_user("test@example.com", "Test User")
        
        # Deactivate first
        service.deactivate_user(user.id)
        
        # Then activate
        activated = service.activate_user(user.id)
        
        assert activated.is_active is True
    
    def test_activate_nonexistent_user(self) -> None:
        """Test activating a non-existent user."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        with pytest.raises(ValueError, match="User with id=999 not found"):
            service.activate_user(999)
    
    def test_deactivate_user(self) -> None:
        """Test deactivating a user."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        user = service.register_user("test@example.com", "Test User")
        
        deactivated = service.deactivate_user(user.id)
        
        assert deactivated.is_active is False
    
    def test_deactivate_nonexistent_user(self) -> None:
        """Test deactivating a non-existent user."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        with pytest.raises(ValueError, match="User with id=999 not found"):
            service.deactivate_user(999)
    
    def test_get_active_users(self) -> None:
        """Test getting all active users."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        user1 = service.register_user("user1@example.com", "User 1")
        user2 = service.register_user("user2@example.com", "User 2")
        service.deactivate_user(user2.id)
        
        active = service.get_active_users()
        
        assert len(active) == 1
        assert active[0].id == user1.id
    
    def test_search_users_by_name(self) -> None:
        """Test searching users by name."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        service.register_user("alice@example.com", "Alice Smith")
        service.register_user("bob@example.com", "Bob Jones")
        
        results = service.search_users("alice")
        
        assert len(results) == 1
        assert results[0].name == "Alice Smith"
    
    def test_search_users_by_email(self) -> None:
        """Test searching users by email."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        service.register_user("alice.smith@example.com", "Alice")
        service.register_user("bob@example.com", "Bob")
        
        results = service.search_users("alice.smith")
        
        assert len(results) == 1
        assert results[0].email == "alice.smith@example.com"
    
    def test_search_users_case_insensitive(self) -> None:
        """Test that search is case insensitive."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        service.register_user("User@example.com", "Test User")
        
        results_lower = service.search_users("user")
        results_upper = service.search_users("USER")
        
        assert len(results_lower) == 1
        assert len(results_upper) == 1
    
    def test_search_users_no_matches(self) -> None:
        """Test search with no matches."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        service.register_user("user@example.com", "User")
        
        results = service.search_users("nonexistent")
        
        assert results == []


class TestIntegration:
    """Integration tests for repository and service layer."""
    
    def test_full_workflow(self) -> None:
        """Test complete user management workflow."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        # Register users
        user1 = service.register_user("user1@example.com", "User One")
        user2 = service.register_user("user2@example.com", "User Two")
        
        # Deactivate one
        service.deactivate_user(user2.id)
        
        # Get active
        active = service.get_active_users()
        assert len(active) == 1
        assert active[0].id == user1.id
        
        # Search
        results = service.search_users("User")
        assert len(results) == 2
        
        # Verify through repo
        assert len(repo.get_all()) == 2
