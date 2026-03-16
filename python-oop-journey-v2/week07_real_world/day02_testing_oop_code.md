# Day 2: Testing OOP Code

## Learning Objectives

By the end of this day, you will:

1. Understand how to effectively test classes and object interactions
2. Master mocking techniques for isolating units under test
3. Learn to use pytest fixtures for object setup and teardown
4. Write regression tests for stateful objects
5. Apply contract-style testing for interfaces

## Why Testing OOP Code is Different

Testing object-oriented code presents unique challenges:

- **Objects have state**: Tests must account for state changes and lifecycle
- **Objects collaborate**: Dependencies need isolation through mocking
- **Inheritance hierarchies**: Tests must verify behavior at multiple levels
- **Encapsulation**: Tests should verify behavior, not internal implementation

## Key Concepts

### 1. Unit Testing Classes

Test classes by verifying their public behavior:

```python
class TestBankAccount:
    def test_deposit_increases_balance(self) -> None:
        account = BankAccount("Alice", 100.0)
        account.deposit(50.0)
        assert account.balance == 150.0
    
    def test_withdraw_insufficient_funds_raises(self) -> None:
        account = BankAccount("Alice", 100.0)
        with pytest.raises(InsufficientFundsError):
            account.withdraw(200.0)
```

### 2. Mocking Dependencies

Use `unittest.mock` or `pytest-mock` to isolate the unit under test:

```python
def test_order_service_processes_payment(mock_payment_gateway):
    # Arrange
    gateway = mock_payment_gateway.return_value
    gateway.charge.return_value = PaymentResult(success=True)
    service = OrderService(gateway)
    
    # Act
    result = service.process_order(order)
    
    # Assert
    assert result.is_success
    gateway.charge.assert_called_once_with(order.total)
```

### 3. Test Doubles

Different types of test doubles serve different purposes:

| Type | Purpose | Example |
|------|---------|---------|
| **Dummy** | Fills parameter lists | `NullLogger()` |
| **Fake** | Working simplified implementation | `InMemoryRepository()` |
| **Stub** | Returns canned responses | `StubPaymentGateway(always_approve=True)` |
| **Mock** | Verifies interactions | `MockEmailService` with `assert_called` |
| **Spy** | Records calls for later verification | `SpyNotificationService.sent_messages` |

### 4. Pytest Fixtures for Objects

Use fixtures to create reusable object configurations:

```python
@pytest.fixture
def empty_cart() -> ShoppingCart:
    return ShoppingCart()

@pytest.fixture
def cart_with_items() -> ShoppingCart:
    cart = ShoppingCart()
    cart.add_item(Product("Book", 29.99), quantity=2)
    cart.add_item(Product("Pen", 5.99), quantity=5)
    return cart

@pytest.fixture
def mock_repository() -> Mock:
    repo = Mock(spec=UserRepository)
    repo.find_by_id.return_value = User(id=1, name="Test")
    return repo
```

### 5. Testing Stateful Objects

State machines require tests for valid and invalid transitions:

```python
class TestOrderStateMachine:
    def test_pending_to_confirmed_on_payment(self) -> None:
        order = Order(status=OrderStatus.PENDING)
        order.confirm_payment()
        assert order.status == OrderStatus.CONFIRMED
    
    def test_cannot_ship_unconfirmed_order(self) -> None:
        order = Order(status=OrderStatus.PENDING)
        with pytest.raises(InvalidStateTransition):
            order.ship()
```

### 6. Interface Contract Testing

Verify that implementations satisfy interface contracts:

```python
class TestPaymentProcessorContract:
    """Contract tests that must pass for ALL implementations."""
    
    @pytest.fixture(params=[StripeProcessor, PayPalProcessor])
    def processor(self, request) -> PaymentProcessor:
        return request.param()
    
    def test_process_payment_returns_result(self, processor) -> None:
        result = processor.process(Payment(amount=100.0))
        assert isinstance(result, PaymentResult)
```

## Common Patterns

### The Test Pyramid for OOP

```
       /\
      /  \      E2E Tests (few)
     /----\
    /      \    Integration Tests
   /--------\
  /          \  Unit Tests (many)
 /------------\
```

### Arrange-Act-Assert (AAA)

Structure every test clearly:

```python
def test_withdraw_reduces_balance() -> None:
    # Arrange
    account = BankAccount(balance=100.0)
    
    # Act
    account.withdraw(30.0)
    
    # Assert
    assert account.balance == 70.0
```

### Given-When-Then (BDD Style)

Alternative structure for behavior-focused tests:

```python
def test_insufficient_funds_rejection() -> None:
    # Given an account with $100
    account = BankAccount(balance=100.0)
    
    # When attempting to withdraw $150
    with pytest.raises(InsufficientFunds):
        account.withdraw(150.0)
    
    # Then the balance remains unchanged
    assert account.balance == 100.0
```

## Best Practices

1. **Test behavior, not implementation**: Avoid testing private methods or internal state
2. **One concept per test**: Each test should verify one specific behavior
3. **Descriptive names**: Test names should explain the expected behavior
4. **Fast tests**: Use mocks to avoid slow external dependencies
5. **Deterministic tests**: Tests should produce the same results every time
6. **Independent tests**: Tests should not depend on execution order

## Common Mistakes

| Mistake | Why It's Wrong | Solution |
|---------|---------------|----------|
| Testing private methods | Breaks encapsulation | Test through public interface |
| Over-mocking | Tests become brittle | Only mock external dependencies |
| Shared mutable state | Tests become interdependent | Use fixtures, reset state |
| Missing edge cases | Bugs slip through | Test boundaries and invalid inputs |
| Testing getters/setters | Wastes effort | Test behavior that uses them |

## Connection to Weekly Project

The Personal Finance Tracker project will use these testing techniques:

- **Mock repositories** for database isolation
- **Fixture suites** for account/transaction setup
- **State machine tests** for transaction status flows
- **Contract tests** for pluggable categorization engines

## Exercises

Today's exercises cover:

1. **Mocking dependencies** - Creating testable service layers
2. **Fake implementations** - Building in-memory test doubles
3. **Fixture patterns** - Reusable test object setup
4. **State-based testing** - Testing stateful objects and transitions
5. **Interface contracts** - Ensuring implementation consistency

Each exercise includes starter code, a reference solution, and comprehensive tests.

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [unittest.mock guide](https://docs.python.org/3/library/unittest.mock.html)
- Martin Fowler: "Mocks Aren't Stubs"
