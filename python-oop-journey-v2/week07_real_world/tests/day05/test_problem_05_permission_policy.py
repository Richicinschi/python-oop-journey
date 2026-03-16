"""Tests for Problem 05: Permission Policy."""

from __future__ import annotations

import pytest

from week07_real_world.solutions.day05.problem_05_permission_policy import (
    AdminPolicy,
    AllowedUserPolicy,
    AndPolicy,
    NotPolicy,
    OrPolicy,
    OwnerPolicy,
    Permission,
    PermissionChecker,
    PermissionPolicyConcrete,
    PublicResourcePolicy,
    Resource,
    RolePolicy,
    User,
)


@pytest.fixture
def admin_user() -> User:
    """Create an admin user."""
    return User(
        user_id=1,
        username="admin",
        roles=frozenset({"admin"}),
        permissions=frozenset(),
    )


@pytest.fixture
def regular_user() -> User:
    """Create a regular user."""
    return User(
        user_id=2,
        username="user",
        roles=frozenset({"user"}),
        permissions=frozenset({Permission.READ, Permission.WRITE}),
    )


@pytest.fixture
def owner_user() -> User:
    """Create a user who owns resources."""
    return User(
        user_id=3,
        username="owner",
        roles=frozenset({"user"}),
        permissions=frozenset({Permission.READ, Permission.WRITE, Permission.DELETE}),
    )


@pytest.fixture
def private_resource(owner_user: User) -> Resource:
    """Create a private resource."""
    return Resource(
        resource_id="res-1",
        resource_type="document",
        owner_id=owner_user.user_id,
        is_public=False,
    )


@pytest.fixture
def public_resource(owner_user: User) -> Resource:
    """Create a public resource."""
    return Resource(
        resource_id="res-2",
        resource_type="document",
        owner_id=owner_user.user_id,
        is_public=True,
    )


@pytest.fixture
def shared_resource(owner_user: User, regular_user: User) -> Resource:
    """Create a resource shared with specific users."""
    return Resource(
        resource_id="res-3",
        resource_type="document",
        owner_id=owner_user.user_id,
        is_public=False,
        allowed_users=frozenset({regular_user.user_id}),
    )


class TestUser:
    """Tests for User class."""
    
    def test_is_admin_true(self) -> None:
        """Test is_admin with admin role."""
        user = User(user_id=1, username="admin", roles=frozenset({"admin"}))
        assert user.is_admin
    
    def test_is_admin_via_permission(self) -> None:
        """Test is_admin via ADMIN permission."""
        user = User(
            user_id=1,
            username="admin",
            permissions=frozenset({Permission.ADMIN}),
        )
        assert user.is_admin
    
    def test_is_admin_false(self) -> None:
        """Test is_admin returns False for regular user."""
        user = User(user_id=2, username="user", roles=frozenset({"user"}))
        assert not user.is_admin
    
    def test_has_role_true(self) -> None:
        """Test has_role with existing role."""
        user = User(user_id=1, username="test", roles=frozenset({"admin", "user"}))
        assert user.has_role("admin")
    
    def test_has_role_false(self) -> None:
        """Test has_role with non-existent role."""
        user = User(user_id=1, username="test", roles=frozenset({"user"}))
        assert not user.has_role("admin")
    
    def test_has_permission_true(self) -> None:
        """Test has_permission with existing permission."""
        user = User(
            user_id=1,
            username="test",
            permissions=frozenset({Permission.READ}),
        )
        assert user.has_permission(Permission.READ)
    
    def test_has_permission_false(self) -> None:
        """Test has_permission with non-existent permission."""
        user = User(user_id=1, username="test")
        assert not user.has_permission(Permission.WRITE)


class TestResource:
    """Tests for Resource class."""
    
    def test_is_owner_true(self) -> None:
        """Test is_owner when user is owner."""
        resource = Resource(
            resource_id="r1",
            resource_type="doc",
            owner_id=123,
        )
        assert resource.is_owner(123)
    
    def test_is_owner_false(self) -> None:
        """Test is_owner when user is not owner."""
        resource = Resource(
            resource_id="r1",
            resource_type="doc",
            owner_id=123,
        )
        assert not resource.is_owner(456)
    
    def test_is_allowed_true(self) -> None:
        """Test is_allowed when user is in allowed list."""
        resource = Resource(
            resource_id="r1",
            resource_type="doc",
            owner_id=123,
            allowed_users=frozenset({456, 789}),
        )
        assert resource.is_allowed(456)
    
    def test_is_allowed_false(self) -> None:
        """Test is_allowed when user is not in allowed list."""
        resource = Resource(
            resource_id="r1",
            resource_type="doc",
            owner_id=123,
            allowed_users=frozenset({456}),
        )
        assert not resource.is_allowed(789)


class TestOwnerPolicy:
    """Tests for OwnerPolicy."""
    
    def test_owner_passes(self, owner_user: User, private_resource: Resource) -> None:
        """Test that owner passes policy."""
        policy = OwnerPolicy()
        assert policy.check(owner_user, private_resource)
    
    def test_non_owner_fails(
        self, regular_user: User, private_resource: Resource
    ) -> None:
        """Test that non-owner fails policy."""
        policy = OwnerPolicy()
        assert not policy.check(regular_user, private_resource)
    
    def test_no_resource_fails(self, owner_user: User) -> None:
        """Test that missing resource fails policy."""
        policy = OwnerPolicy()
        assert not policy.check(owner_user, None)


class TestRolePolicy:
    """Tests for RolePolicy."""
    
    def test_matching_role_passes(self, admin_user: User) -> None:
        """Test that matching role passes."""
        policy = RolePolicy({"admin"})
        assert policy.check(admin_user)
    
    def test_non_matching_role_fails(self, regular_user: User) -> None:
        """Test that non-matching role fails."""
        policy = RolePolicy({"admin"})
        assert not policy.check(regular_user)
    
    def test_any_matching_role_passes(self) -> None:
        """Test that any matching role passes."""
        user = User(user_id=1, username="test", roles=frozenset({"user", "editor"}))
        policy = RolePolicy({"admin", "editor"})
        assert policy.check(user)


class TestPermissionPolicy:
    """Tests for PermissionPolicyConcrete."""
    
    def test_matching_permission_passes(self, regular_user: User) -> None:
        """Test that matching permission passes."""
        policy = PermissionPolicyConcrete({Permission.READ})
        assert policy.check(regular_user)
    
    def test_non_matching_permission_fails(self, admin_user: User) -> None:
        """Test that non-matching permission fails."""
        policy = PermissionPolicyConcrete({Permission.READ})
        assert not policy.check(admin_user)
    
    def test_any_matching_permission_passes(self) -> None:
        """Test that any matching permission passes."""
        user = User(
            user_id=1,
            username="test",
            permissions=frozenset({Permission.READ, Permission.WRITE}),
        )
        policy = PermissionPolicyConcrete({Permission.DELETE, Permission.WRITE})
        assert policy.check(user)


class TestPublicResourcePolicy:
    """Tests for PublicResourcePolicy."""
    
    def test_public_resource_passes(
        self, regular_user: User, public_resource: Resource
    ) -> None:
        """Test that public resource passes for any user."""
        policy = PublicResourcePolicy()
        assert policy.check(regular_user, public_resource)
    
    def test_private_resource_fails(
        self, regular_user: User, private_resource: Resource
    ) -> None:
        """Test that private resource fails."""
        policy = PublicResourcePolicy()
        assert not policy.check(regular_user, private_resource)
    
    def test_no_resource_fails(self, regular_user: User) -> None:
        """Test that missing resource fails."""
        policy = PublicResourcePolicy()
        assert not policy.check(regular_user, None)


class TestAllowedUserPolicy:
    """Tests for AllowedUserPolicy."""
    
    def test_allowed_user_passes(
        self, regular_user: User, shared_resource: Resource
    ) -> None:
        """Test that allowed user passes."""
        policy = AllowedUserPolicy()
        assert policy.check(regular_user, shared_resource)
    
    def test_non_allowed_user_fails(
        self, admin_user: User, shared_resource: Resource
    ) -> None:
        """Test that non-allowed user fails."""
        policy = AllowedUserPolicy()
        assert not policy.check(admin_user, shared_resource)
    
    def test_no_resource_fails(self, regular_user: User) -> None:
        """Test that missing resource fails."""
        policy = AllowedUserPolicy()
        assert not policy.check(regular_user, None)


class TestAdminPolicy:
    """Tests for AdminPolicy."""
    
    def test_admin_passes(self, admin_user: User, private_resource: Resource) -> None:
        """Test that admin passes."""
        policy = AdminPolicy()
        assert policy.check(admin_user, private_resource)
    
    def test_non_admin_fails(
        self, regular_user: User, private_resource: Resource
    ) -> None:
        """Test that non-admin fails."""
        policy = AdminPolicy()
        assert not policy.check(regular_user, private_resource)


class TestCompositePolicies:
    """Tests for AndPolicy, OrPolicy, NotPolicy."""
    
    def test_and_policy_both_true(self, owner_user: User, private_resource: Resource) -> None:
        """Test AND policy when both pass."""
        policy = OwnerPolicy() & PermissionPolicyConcrete({Permission.DELETE})
        assert policy.check(owner_user, private_resource)
    
    def test_and_policy_one_false(self, owner_user: User, private_resource: Resource) -> None:
        """Test AND policy when one fails."""
        policy = OwnerPolicy() & AdminPolicy()
        assert not policy.check(owner_user, private_resource)
    
    def test_or_policy_first_true(
        self, owner_user: User, private_resource: Resource
    ) -> None:
        """Test OR policy when first passes."""
        policy = OwnerPolicy() | AdminPolicy()
        assert policy.check(owner_user, private_resource)
    
    def test_or_policy_second_true(
        self, admin_user: User, private_resource: Resource
    ) -> None:
        """Test OR policy when second passes."""
        policy = OwnerPolicy() | AdminPolicy()
        assert policy.check(admin_user, private_resource)
    
    def test_or_policy_both_false(
        self, regular_user: User, private_resource: Resource
    ) -> None:
        """Test OR policy when both fail."""
        policy = OwnerPolicy() | AdminPolicy()
        assert not policy.check(regular_user, private_resource)
    
    def test_not_policy_inverts(self, regular_user: User, private_resource: Resource) -> None:
        """Test NOT policy inverts result."""
        policy = ~OwnerPolicy()
        # User is not the owner, so OwnerPolicy returns False, NotPolicy returns True
        assert policy.check(regular_user, private_resource)
        # With no resource, OwnerPolicy returns False (not owner), NotPolicy returns True
        assert policy.check(regular_user, None)


class TestPermissionChecker:
    """Tests for PermissionChecker class."""
    
    def test_authorized_with_policy(
        self, owner_user: User, private_resource: Resource
    ) -> None:
        """Test authorized with passing policy."""
        checker = PermissionChecker()
        assert checker.authorized(
            owner_user, private_resource, OwnerPolicy()
        )
    
    def test_not_authorized_with_policy(
        self, regular_user: User, private_resource: Resource
    ) -> None:
        """Test authorized with failing policy."""
        checker = PermissionChecker()
        assert not checker.authorized(
            regular_user, private_resource, OwnerPolicy()
        )
    
    def test_has_permission_true(self, regular_user: User) -> None:
        """Test has_permission when user has permission."""
        checker = PermissionChecker()
        assert checker.has_permission(regular_user, Permission.READ)
    
    def test_has_permission_false(self, admin_user: User) -> None:
        """Test has_permission when user lacks permission."""
        checker = PermissionChecker()
        assert not checker.has_permission(admin_user, Permission.READ)
    
    def test_is_owner_true(self, owner_user: User, private_resource: Resource) -> None:
        """Test is_owner when user is owner."""
        checker = PermissionChecker()
        assert checker.is_owner(owner_user, private_resource)
    
    def test_is_owner_false(
        self, regular_user: User, private_resource: Resource
    ) -> None:
        """Test is_owner when user is not owner."""
        checker = PermissionChecker()
        assert not checker.is_owner(regular_user, private_resource)
    
    def test_owner_or_admin_policy(self) -> None:
        """Test owner_or_admin returns correct policy type."""
        checker = PermissionChecker()
        policy = checker.owner_or_admin()
        
        owner_user = User(user_id=1, username="owner")
        admin_user = User(user_id=2, username="admin", roles=frozenset({"admin"}))
        regular_user = User(user_id=3, username="user")
        
        resource = Resource(resource_id="r1", resource_type="doc", owner_id=1)
        
        assert policy.check(owner_user, resource)
        assert policy.check(admin_user, resource)
        assert not policy.check(regular_user, resource)
    
    def test_can_read_as_owner(
        self, owner_user: User, private_resource: Resource
    ) -> None:
        """Test can_read for owner."""
        checker = PermissionChecker()
        assert checker.can_read(owner_user, private_resource)
    
    def test_can_read_as_admin(
        self, admin_user: User, private_resource: Resource
    ) -> None:
        """Test can_read for admin."""
        checker = PermissionChecker()
        assert checker.can_read(admin_user, private_resource)
    
    def test_can_read_public_resource(
        self, regular_user: User, public_resource: Resource
    ) -> None:
        """Test can_read for public resource."""
        checker = PermissionChecker()
        assert checker.can_read(regular_user, public_resource)
    
    def test_can_read_allowed_user_with_permission(
        self, regular_user: User, shared_resource: Resource
    ) -> None:
        """Test can_read for allowed user with READ permission."""
        checker = PermissionChecker()
        assert checker.can_read(regular_user, shared_resource)
    
    def test_can_read_denied_for_unauthorized(
        self, admin_user: User, private_resource: Resource
    ) -> None:
        """Test can_read denies unauthorized user."""
        checker = PermissionChecker()
        # Admin can read anyway, so use a user without access
        user = User(user_id=999, username="intruder")
        assert not checker.can_read(user, private_resource)
    
    def test_can_write_as_owner_with_permission(
        self, owner_user: User, private_resource: Resource
    ) -> None:
        """Test can_write for owner with WRITE permission."""
        checker = PermissionChecker()
        assert checker.can_write(owner_user, private_resource)
    
    def test_can_write_as_admin(
        self, admin_user: User, private_resource: Resource
    ) -> None:
        """Test can_write for admin."""
        checker = PermissionChecker()
        assert checker.can_write(admin_user, private_resource)
    
    def test_can_write_denied_without_write_permission(
        self, private_resource: Resource
    ) -> None:
        """Test can_write denied without WRITE permission."""
        checker = PermissionChecker()
        # Owner user without WRITE permission
        user = User(
            user_id=private_resource.owner_id,
            username="owner",
            permissions=frozenset({Permission.READ}),  # No WRITE
        )
        assert not checker.can_write(user, private_resource)
    
    def test_can_write_denied_for_non_owner(
        self, regular_user: User, private_resource: Resource
    ) -> None:
        """Test can_write denied for non-owner."""
        checker = PermissionChecker()
        assert not checker.can_write(regular_user, private_resource)
    
    def test_can_delete_as_owner_with_permission(
        self, owner_user: User, private_resource: Resource
    ) -> None:
        """Test can_delete for owner with DELETE permission."""
        checker = PermissionChecker()
        assert checker.can_delete(owner_user, private_resource)
    
    def test_can_delete_as_admin(
        self, admin_user: User, private_resource: Resource
    ) -> None:
        """Test can_delete for admin."""
        checker = PermissionChecker()
        assert checker.can_delete(admin_user, private_resource)
    
    def test_can_delete_denied_without_delete_permission(
        self, private_resource: Resource
    ) -> None:
        """Test can_delete denied without DELETE permission."""
        checker = PermissionChecker()
        user = User(
            user_id=private_resource.owner_id,
            username="owner",
            permissions=frozenset({Permission.READ, Permission.WRITE}),
        )
        assert not checker.can_delete(user, private_resource)
