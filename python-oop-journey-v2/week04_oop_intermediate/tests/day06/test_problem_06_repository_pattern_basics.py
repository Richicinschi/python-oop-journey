"""Tests for Problem 06: Repository Pattern Basics."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day06.problem_06_repository_pattern_basics import (
    Entity,
    InMemoryRepository,
    Repository,
    User,
    UserRepository,
)


class TestEntity:
    """Tests for the Entity base class."""
    
    def test_entity_init(self) -> None:
        """Test Entity initialization."""
        # Need a concrete subclass to test
        user = User(1, "alice", "alice@example.com")
        assert user.id == 1
    
    def test_entity_is_abstract(self) -> None:
        """Test that Entity cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Entity(1)


class TestUser:
    """Tests for the User entity."""
    
    def test_user_init(self) -> None:
        """Test User initialization."""
        user = User(1, "alice", "alice@example.com")
        assert user.id == 1
        assert user.name == "alice"
        assert user.email == "alice@example.com"
    
    def test_user_name_setter(self) -> None:
        """Test setting user name."""
        user = User(1, "alice", "alice@example.com")
        user.name = "bob"
        assert user.name == "bob"
    
    def test_user_email_setter(self) -> None:
        """Test setting user email."""
        user = User(1, "alice", "alice@example.com")
        user.email = "bob@example.com"
        assert user.email == "bob@example.com"
    
    def test_user_str(self) -> None:
        """Test User string representation."""
        user = User(1, "alice", "alice@example.com")
        assert str(user) == "alice"
    
    def test_user_repr(self) -> None:
        """Test User repr."""
        user = User(1, "alice", "alice@example.com")
        result = repr(user)
        assert "User" in result
        assert "id=1" in result
        assert "alice" in result
    
    def test_user_is_entity(self) -> None:
        """Test that User is an Entity."""
        user = User(1, "alice", "alice@example.com")
        assert isinstance(user, Entity)
    
    def test_user_equality(self) -> None:
        """Test User equality based on ID."""
        user1 = User(1, "alice", "alice@example.com")
        user2 = User(1, "bob", "bob@example.com")  # Same ID, different data
        user3 = User(2, "alice", "alice@example.com")  # Different ID
        
        assert user1 == user2  # Same ID
        assert user1 != user3  # Different ID
    
    def test_user_hash(self) -> None:
        """Test User hashing."""
        user1 = User(1, "alice", "alice@example.com")
        user2 = User(1, "bob", "bob@example.com")
        
        assert hash(user1) == hash(user2)  # Same ID = same hash


class TestRepository:
    """Tests for the Repository abstract class."""
    
    def test_repository_is_abstract(self) -> None:
        """Test that Repository cannot be instantiated."""
        with pytest.raises(TypeError):
            Repository()  # type: ignore


class TestInMemoryRepository:
    """Tests for the InMemoryRepository."""
    
    def test_repo_init(self) -> None:
        """Test repository initialization."""
        repo = InMemoryRepository()
        assert repo.count() == 0
    
    def test_repo_save_and_get(self) -> None:
        """Test saving and retrieving an entity."""
        repo = InMemoryRepository()
        user = User(1, "alice", "alice@example.com")
        repo.save(user)
        
        retrieved = repo.get(1)
        assert retrieved == user
        assert retrieved.name == "alice"
    
    def test_repo_get_nonexistent(self) -> None:
        """Test getting non-existent entity."""
        repo = InMemoryRepository()
        assert repo.get(999) is None
    
    def test_repo_exists(self) -> None:
        """Test checking entity existence."""
        repo = InMemoryRepository()
        user = User(1, "alice", "alice@example.com")
        repo.save(user)
        
        assert repo.exists(1) is True
        assert repo.exists(999) is False
    
    def test_repo_delete(self) -> None:
        """Test deleting an entity."""
        repo = InMemoryRepository()
        user = User(1, "alice", "alice@example.com")
        repo.save(user)
        
        result = repo.delete(1)
        assert result is True
        assert repo.get(1) is None
        assert repo.count() == 0
    
    def test_repo_delete_nonexistent(self) -> None:
        """Test deleting non-existent entity."""
        repo = InMemoryRepository()
        result = repo.delete(999)
        assert result is False
    
    def test_repo_get_all(self) -> None:
        """Test getting all entities."""
        repo = InMemoryRepository()
        repo.save(User(1, "alice", "alice@example.com"))
        repo.save(User(2, "bob", "bob@example.com"))
        
        all_users = repo.get_all()
        assert len(all_users) == 2
        assert all(isinstance(u, User) for u in all_users)
    
    def test_repo_count(self) -> None:
        """Test counting entities."""
        repo = InMemoryRepository()
        assert repo.count() == 0
        
        repo.save(User(1, "alice", "alice@example.com"))
        assert repo.count() == 1
        
        repo.save(User(2, "bob", "bob@example.com"))
        assert repo.count() == 2
    
    def test_repo_clear(self) -> None:
        """Test clearing all entities."""
        repo = InMemoryRepository()
        repo.save(User(1, "alice", "alice@example.com"))
        repo.save(User(2, "bob", "bob@example.com"))
        
        repo.clear()
        assert repo.count() == 0
        assert repo.get_all() == []
    
    def test_repo_update_existing(self) -> None:
        """Test updating an existing entity."""
        repo = InMemoryRepository()
        user = User(1, "alice", "alice@example.com")
        repo.save(user)
        
        updated_user = User(1, "alison", "alison@example.com")
        repo.save(updated_user)
        
        retrieved = repo.get(1)
        assert retrieved.name == "alison"


class TestUserRepository:
    """Tests for the UserRepository."""
    
    def test_user_repo_inherits_from_in_memory_repo(self) -> None:
        """Test that UserRepository inherits CRUD operations."""
        repo = UserRepository()
        user = User(1, "alice", "alice@example.com")
        repo.save(user)
        assert repo.get(1) == user
    
    def test_user_repo_find_by_name(self) -> None:
        """Test finding users by name."""
        repo = UserRepository()
        repo.save(User(1, "alice", "alice@example.com"))
        repo.save(User(2, "bob", "bob@example.com"))
        repo.save(User(3, "alice", "alice2@example.com"))
        
        results = repo.find_by_name("alice")
        assert len(results) == 2
        assert all(u.name == "alice" for u in results)
    
    def test_user_repo_find_by_name_no_match(self) -> None:
        """Test finding by name with no matches."""
        repo = UserRepository()
        repo.save(User(1, "alice", "alice@example.com"))
        
        results = repo.find_by_name("charlie")
        assert results == []
    
    def test_user_repo_find_by_email(self) -> None:
        """Test finding user by email."""
        repo = UserRepository()
        repo.save(User(1, "alice", "alice@example.com"))
        repo.save(User(2, "bob", "bob@example.com"))
        
        result = repo.find_by_email("bob@example.com")
        assert result is not None
        assert result.name == "bob"
    
    def test_user_repo_find_by_email_no_match(self) -> None:
        """Test finding by email with no match."""
        repo = UserRepository()
        repo.save(User(1, "alice", "alice@example.com"))
        
        result = repo.find_by_email("unknown@example.com")
        assert result is None
    
    def test_user_repo_search_by_name(self) -> None:
        """Test searching by name."""
        repo = UserRepository()
        repo.save(User(1, "Alice Johnson", "alice@example.com"))
        repo.save(User(2, "Bob Smith", "bob@example.com"))
        
        results = repo.search("alice")
        assert len(results) == 1
        assert results[0].name == "Alice Johnson"
    
    def test_user_repo_search_by_email(self) -> None:
        """Test searching by email."""
        repo = UserRepository()
        repo.save(User(1, "Alice", "alice.johnson@example.com"))
        repo.save(User(2, "Bob", "bob@example.com"))
        
        results = repo.search("johnson")
        assert len(results) == 1
        assert results[0].name == "Alice"
    
    def test_user_repo_search_case_insensitive(self) -> None:
        """Test that search is case-insensitive."""
        repo = UserRepository()
        repo.save(User(1, "Alice", "alice@example.com"))
        
        results_lower = repo.search("alice")
        results_upper = repo.search("ALICE")
        
        assert len(results_lower) == 1
        assert len(results_upper) == 1
    
    def test_user_repo_search_multiple_matches(self) -> None:
        """Test search with multiple matches."""
        repo = UserRepository()
        repo.save(User(1, "Alice", "alice@example.com"))
        repo.save(User(2, "Alicia", "alicia@example.com"))
        
        results = repo.search("ali")
        assert len(results) == 2
    
    def test_user_repo_search_no_matches(self) -> None:
        """Test search with no matches."""
        repo = UserRepository()
        repo.save(User(1, "Alice", "alice@example.com"))
        
        results = repo.search("xyz")
        assert results == []
