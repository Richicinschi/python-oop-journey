"""Tests for Problem 05: Admin Power User (Diamond Inheritance)."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day04.problem_05_admin_power_user import (
    Admin,
    PowerUser,
    SuperAdmin,
    User,
)


class TestUser:
    """Tests for the User base class."""
    
    def test_user_init(self) -> None:
        """Test User initialization."""
        user = User("alice", "alice@example.com")
        
        assert user.name == "alice"
        assert user.email == "alice@example.com"
        assert user.get_permissions() == ["read"]
    
    def test_user_has_permission(self) -> None:
        """Test checking permissions."""
        user = User("alice", "alice@example.com")
        
        assert user.has_permission("read") is True
        assert user.has_permission("write") is False
        assert user.has_permission("admin") is False
    
    def test_user_describe(self) -> None:
        """Test user description."""
        user = User("alice", "alice@example.com")
        
        assert user.describe() == "User(alice, alice@example.com)"
    
    def test_user_get_permissions_returns_copy(self) -> None:
        """Test that get_permissions returns a copy."""
        user = User("alice", "alice@example.com")
        perms = user.get_permissions()
        perms.append("hacked")
        
        assert user.get_permissions() == ["read"]


class TestAdmin:
    """Tests for the Admin class."""
    
    def test_admin_init(self) -> None:
        """Test Admin initialization."""
        admin = Admin("bob", "bob@example.com")
        
        assert admin.name == "bob"
        assert admin.email == "bob@example.com"
        assert admin.admin_level == 1
        assert "read" in admin.get_permissions()
        assert "write" in admin.get_permissions()
        assert "admin" in admin.get_permissions()
    
    def test_admin_is_user(self) -> None:
        """Test that Admin is a User."""
        admin = Admin("bob", "bob@example.com")
        assert isinstance(admin, User)
    
    def test_admin_can_administer(self) -> None:
        """Test admin can administer."""
        admin = Admin("bob", "bob@example.com")
        assert admin.can_administer() is True
    
    def test_admin_get_admin_info(self) -> None:
        """Test getting admin info."""
        admin = Admin("bob", "bob@example.com", admin_level=3)
        
        info = admin.get_admin_info()
        assert info == {"level": 3, "can_administer": True}
    
    def test_admin_custom_level(self) -> None:
        """Test admin with custom level."""
        admin = Admin("bob", "bob@example.com", admin_level=5)
        assert admin.admin_level == 5


class TestPowerUser:
    """Tests for the PowerUser class."""
    
    def test_power_user_init(self) -> None:
        """Test PowerUser initialization."""
        pu = PowerUser("charlie", "charlie@example.com")
        
        assert pu.name == "charlie"
        assert pu.email == "charlie@example.com"
        assert pu.power_level == 1
        assert "read" in pu.get_permissions()
        assert "write" in pu.get_permissions()
        assert "power" in pu.get_permissions()
    
    def test_power_user_is_user(self) -> None:
        """Test that PowerUser is a User."""
        pu = PowerUser("charlie", "charlie@example.com")
        assert isinstance(pu, User)
    
    def test_power_user_can_access_power_features(self) -> None:
        """Test power user can access power features."""
        pu = PowerUser("charlie", "charlie@example.com")
        assert pu.can_access_power_features() is True
    
    def test_power_user_get_power_info(self) -> None:
        """Test getting power user info."""
        pu = PowerUser("charlie", "charlie@example.com", power_level=3)
        
        info = pu.get_power_info()
        assert info == {"level": 3, "can_access_power": True}
    
    def test_power_user_custom_level(self) -> None:
        """Test power user with custom level."""
        pu = PowerUser("charlie", "charlie@example.com", power_level=5)
        assert pu.power_level == 5


class TestSuperAdmin:
    """Tests for the SuperAdmin class (diamond inheritance)."""
    
    def test_super_admin_init(self) -> None:
        """Test SuperAdmin initialization."""
        sa = SuperAdmin("dave", "dave@example.com")
        
        assert sa.name == "dave"
        assert sa.email == "dave@example.com"
        assert sa.admin_level == 2
        assert sa.power_level == 2
    
    def test_super_admin_is_user(self) -> None:
        """Test that SuperAdmin is a User."""
        sa = SuperAdmin("dave", "dave@example.com")
        assert isinstance(sa, User)
    
    def test_super_admin_is_admin(self) -> None:
        """Test that SuperAdmin is an Admin."""
        sa = SuperAdmin("dave", "dave@example.com")
        assert isinstance(sa, Admin)
    
    def test_super_admin_is_power_user(self) -> None:
        """Test that SuperAdmin is a PowerUser."""
        sa = SuperAdmin("dave", "dave@example.com")
        assert isinstance(sa, PowerUser)
    
    def test_super_admin_has_all_permissions(self) -> None:
        """Test SuperAdmin has all permissions."""
        sa = SuperAdmin("dave", "dave@example.com")
        
        perms = sa.get_permissions()
        assert "read" in perms
        assert "write" in perms
        assert "admin" in perms
        assert "power" in perms
    
    def test_super_admin_can_administer(self) -> None:
        """Test SuperAdmin can administer."""
        sa = SuperAdmin("dave", "dave@example.com")
        assert sa.can_administer() is True
    
    def test_super_admin_can_access_power_features(self) -> None:
        """Test SuperAdmin can access power features."""
        sa = SuperAdmin("dave", "dave@example.com")
        assert sa.can_access_power_features() is True
    
    def test_super_admin_is_super_admin(self) -> None:
        """Test SuperAdmin is identified as super admin."""
        sa = SuperAdmin("dave", "dave@example.com")
        assert sa.is_super_admin() is True
    
    def test_super_admin_get_all_capabilities(self) -> None:
        """Test getting all capabilities."""
        sa = SuperAdmin("dave", "dave@example.com", admin_level=3, power_level=4)
        
        caps = sa.get_all_capabilities()
        assert caps["name"] == "dave"
        assert caps["email"] == "dave@example.com"
        assert caps["admin_level"] == 3
        assert caps["power_level"] == 4
        assert "read" in caps["permissions"]
        assert "admin" in caps["permissions"]
        assert "power" in caps["permissions"]
    
    def test_super_admin_mro(self) -> None:
        """Test SuperAdmin's MRO (demonstrates diamond inheritance)."""
        # Expected MRO: SuperAdmin -> Admin -> PowerUser -> User -> object
        mro = SuperAdmin.__mro__
        
        assert mro[0] == SuperAdmin
        assert mro[1] == Admin
        assert mro[2] == PowerUser
        assert mro[3] == User
        assert mro[4] == object
        
        # Verify the diamond: User should appear only once
        user_count = sum(1 for cls in mro if cls == User)
        assert user_count == 1
    
    def test_super_admin_custom_levels(self) -> None:
        """Test SuperAdmin with custom levels."""
        sa = SuperAdmin("eve", "eve@example.com", admin_level=5, power_level=10)
        
        assert sa.admin_level == 5
        assert sa.power_level == 10
