# Day 5: Service-Oriented OOP Design

## Learning Objectives

By the end of this day, you will:

- Understand the Service Layer pattern and its role in application architecture
- Learn how to design service classes that encapsulate business logic
- Practice dependency injection for testable services
- Implement session management and request-scoped contexts
- Build permission and policy systems using OOP principles

## Key Concepts

### The Service Layer Pattern

The Service Layer pattern introduces a layer between controllers/HTTP handlers and the data access layer. Services encapsulate business logic, orchestrate domain objects, and provide a clean API for the rest of the application.

```python
# Without Service Layer - Business logic scattered
class OrderController:
    def create_order(self, user_id: int, items: list) -> dict:
        user = db.get_user(user_id)
        if not user.is_active:
            return {"error": "User inactive"}
        order = Order(user_id=user_id)
        for item in items:
            product = db.get_product(item["product_id"])
            if product.stock < item["quantity"]:
                return {"error": "Insufficient stock"}
            order.add_item(product, item["quantity"])
        db.save_order(order)
        return {"order_id": order.id}

# With Service Layer - Clean separation
class OrderService:
    def __init__(self, user_repo, product_repo, order_repo):
        self._user_repo = user_repo
        self._product_repo = product_repo
        self._order_repo = order_repo
    
    def create_order(self, user_id: int, items: list[OrderItem]) -> OrderResult:
        user = self._user_repo.get(user_id)
        self._validate_user_active(user)
        order = self._build_order(user_id, items)
        self._order_repo.save(order)
        return OrderResult.success(order.id)
```

### Benefits of the Service Layer

1. **Separation of Concerns**: Business logic is isolated from transport and data layers
2. **Testability**: Services can be unit tested with mock dependencies
3. **Reusability**: Same service methods can be used by CLI, API, or background jobs
4. **Transaction Boundaries**: Services define clear units of work

### Dependency Injection

Services receive their dependencies through the constructor rather than creating them:

```python
class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        email_service: EmailService,
        password_hasher: PasswordHasher
    ) -> None:
        self._user_repo = user_repository
        self._email = email_service
        self._hasher = password_hasher
```

This enables:
- Easy testing with mock implementations
- Swapping implementations without changing service code
- Clear visibility of service dependencies

### Session Management

Sessions track user state across requests. A session manager service:

```python
class SessionManager:
    def __init__(self, store: SessionStore, ttl: int = 3600) -> None:
        self._store = store
        self._ttl = ttl
    
    def create_session(self, user_id: int) -> Session:
        session = Session(user_id=user_id, expires_at=now() + self._ttl)
        self._store.save(session.id, session, ttl=self._ttl)
        return session
    
    def get_session(self, session_id: str) -> Session | None:
        return self._store.get(session_id)
    
    def invalidate_session(self, session_id: str) -> None:
        self._store.delete(session_id)
```

### Request Context

Request-scoped data (user, request ID, timestamps) can be encapsulated:

```python
class RequestContext:
    def __init__(self, request_id: str, user_id: int | None = None) -> None:
        self.request_id = request_id
        self.user_id = user_id
        self.started_at = datetime.now()
    
    @property
    def is_authenticated(self) -> bool:
        return self.user_id is not None
```

### Permission Policies

Policy-based authorization separates "can do X" from "how to check":

```python
class PermissionPolicy(ABC):
    @abstractmethod
    def check(self, user: User, resource: Any) -> bool:
        ...

class OwnerPermission(PermissionPolicy):
    def check(self, user: User, resource: Owned) -> bool:
        return resource.owner_id == user.id

class RolePermission(PermissionPolicy):
    def __init__(self, allowed_roles: set[str]) -> None:
        self._allowed_roles = allowed_roles
    
    def check(self, user: User, resource: Any = None) -> bool:
        return user.role in self._allowed_roles
```

## Common Mistakes

1. **Anemic Services**: Services that are just proxies to repositories add no value
2. **Leaky Abstractions**: Services exposing internal details to callers
3. **God Services**: Single service handling too many unrelated responsibilities
4. **Hidden Dependencies**: Creating repositories inside methods instead of injecting them
5. **Missing Transaction Boundaries**: Partial failures leaving data inconsistent

## Design Guidelines

### Service Naming

- Name services after the domain concept they manage: `UserService`, `OrderService`
- Method names describe the operation: `create`, `update`, `delete`, `find_by_id`
- Return result objects, not raw data structures

### Error Handling

```python
@dataclass
class ServiceResult:
    success: bool
    data: Any | None = None
    error: str | None = None

class UserService:
    def register(self, email: str, password: str) -> ServiceResult:
        if self._user_repo.exists(email):
            return ServiceResult(success=False, error="Email exists")
        user = self._create_user(email, password)
        return ServiceResult(success=True, data=user)
```

### Testing Services

```python
def test_user_service_registers_new_user():
    # Arrange
    mock_repo = MockUserRepository()
    mock_email = MockEmailService()
    service = UserService(mock_repo, mock_email)
    
    # Act
    result = service.register("test@example.com", "password123")
    
    # Assert
    assert result.success
    assert mock_repo.saved_user is not None
    assert mock_email.welcome_sent
```

## Connection to Weekly Project

The Personal Finance Tracker project uses services extensively:

- `TransactionService`: Handles categorization, validation, and balance updates
- `AccountService`: Manages account creation and balance inquiries
- `ReportService`: Generates spending reports and analytics
- `BudgetService`: Tracks budget limits and alerts

These services work with repositories for persistence while keeping business rules testable and organized.

## Additional Resources

- Martin Fowler: "Service Layer" pattern (martinfowler.com)
- Repository Pattern and Unit of Work
- Ports and Adapters (Hexagonal Architecture)
