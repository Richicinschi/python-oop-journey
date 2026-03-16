# Day 6: Testing with pytest

Learn to write comprehensive, maintainable tests using pytest, Python's most popular testing framework.

## Learning Objectives

By the end of this day, you will be able to:
- Write test functions with clear assertions
- Use fixtures for reusable test setup
- Parametrize tests to run with multiple inputs
- Mock external dependencies
- Test exception handling
- Practice Test-Driven Development (TDD)

## Why Testing Matters

Testing is not about finding bugs after code is written—it's about:
- **Confidence**: Knowing your code works as expected
- **Documentation**: Tests show how code should be used
- **Refactoring safety**: Tests catch regressions when you change code
- **Design feedback**: Testable code is often better-designed code

## pytest Basics

### Test Functions

pytest discovers and runs functions starting with `test_`:

```python
# Simple test function
def test_addition():
    assert 2 + 2 == 4

# Test with setup
def test_string_uppercase():
    result = "hello".upper()
    assert result == "HELLO"
```

### Assertions

pytest provides rich assertion introspection:

```python
def test_list_containment():
    numbers = [1, 2, 3]
    assert 2 in numbers  # Clear, readable assertion

def test_dictionary_access():
    data = {"name": "Alice", "age": 30}
    assert data["name"] == "Alice"
    assert "email" not in data
```

### Testing Exceptions

Use `pytest.raises` to test that code raises expected exceptions:

```python
import pytest

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_value_error_with_message():
    with pytest.raises(ValueError, match="must be positive"):
        raise ValueError("value must be positive")
```

## Fixtures

Fixtures provide reusable test setup and teardown:

```python
import pytest

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {"name": "Test", "value": 42}

def test_data_has_name(sample_data):
    assert "name" in sample_data
    assert sample_data["name"] == "Test"
```

### Fixture Scopes

Control how often fixtures run:

```python
@pytest.fixture(scope="function")  # Default: runs for each test
@pytest.fixture(scope="class")     # Once per test class
@pytest.fixture(scope="module")    # Once per module
@pytest.fixture(scope="session")   # Once per test session
```

### Fixture Dependencies

Fixtures can depend on other fixtures:

```python
@pytest.fixture
def database():
    return Database()

@pytest.fixture
def user(database):  # Depends on database fixture
    return database.create_user("test@example.com")
```

### Built-in Fixtures

pytest includes useful built-in fixtures:

```python
def test_file_operations(tmp_path):
    """tmp_path provides a temporary directory."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello, World!")
    assert file_path.read_text() == "Hello, World!"

def test_environment_variable(monkeypatch):
    """monkeypatch modifies environment and objects."""
    monkeypatch.setenv("API_KEY", "secret123")
    assert os.getenv("API_KEY") == "secret123"
```

## Parametrized Tests

Run the same test with different inputs:

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("world", 5),
    ("", 0),
    ("pytest", 6),
])
def test_string_length(input, expected):
    assert len(input) == expected

# Multiple parameters
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (10, 20, 30),
])
def test_addition(a, b, expected):
    assert a + b == expected
```

## Mocking

Mock external dependencies with `unittest.mock`:

```python
from unittest.mock import Mock, patch

def test_with_mock():
    """Create a mock object."""
    mock_api = Mock()
    mock_api.get_user.return_value = {"name": "Alice"}
    
    result = mock_api.get_user(123)
    assert result["name"] == "Alice"
    mock_api.get_user.assert_called_once_with(123)

# Patch external calls
@patch("requests.get")
def test_api_client(mock_get):
    """Patch external library calls."""
    mock_get.return_value.json.return_value = {"status": "ok"}
    
    response = requests.get("https://api.example.com")
    assert response.json()["status"] == "ok"
```

## Test Organization

### Test Classes

Group related tests in classes:

```python
class TestCalculator:
    """Tests for Calculator class."""
    
    def test_add(self):
        assert Calculator.add(2, 3) == 5
    
    def test_divide_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            Calculator.divide(1, 0)
```

### Markers

Tag tests for selective running:

```python
import pytest

@pytest.mark.slow
def test_long_running_operation():
    pass

@pytest.mark.integration
def test_database_connection():
    pass
```

Run marked tests:
```bash
pytest -m slow          # Only slow tests
pytest -m "not slow"    # Exclude slow tests
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific file
pytest test_calculator.py

# Run specific test
pytest test_calculator.py::test_addition

# Run with coverage
pytest --cov=my_module --cov-report=html

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l
```

## Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|---------------|------------------|
| Testing implementation details | Tests break when refactoring | Test behavior, not internals |
| No assertions | Tests pass even if code is broken | Every test needs at least one assertion |
| One giant test | Hard to identify what failed | Split into focused tests |
| Testing multiple things | Confusing failures | One concept per test |
| Ignoring edge cases | Bugs hide in boundaries | Test empty inputs, limits, errors |
| Mutable default fixtures | Tests interfere with each other | Return new objects from fixtures |

## TDD Workflow

Test-Driven Development cycle:

1. **Red**: Write a failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code while keeping tests green

Example:

```python
# Step 1: Write failing test
def test_calculator_adds_numbers():
    calc = Calculator()
    assert calc.add(2, 3) == 5  # Fails - Calculator doesn't exist

# Step 2: Minimal implementation
class Calculator:
    def add(self, a, b):
        return a + b  # Test passes

# Step 3: Refactor if needed
# Add type hints, docstrings, edge cases
```

## Exercise Connections

| Exercise | pytest Feature | Focus |
|----------|---------------|-------|
| calculator_test_suite | Basic assertions | Testing existing code |
| fixture_driven_user_factory | Fixtures | Reusable test data |
| parametrized_palindrome_tests | @pytest.mark.parametrize | Multiple test cases |
| file_processor_with_tmp_path | tmp_path fixture | File operations |
| mock_api_client | unittest.mock | Isolating dependencies |
| exception_assertion_suite | pytest.raises | Error handling |
| mini_tdd_refactor | TDD workflow | Red-green-refactor |

## Weekly Project Connection

The Week 2 project (Procedural Library System) will use:
- **Fixtures** for test data setup
- **tmp_path** for testing file operations
- **Parametrized tests** for multiple book/user scenarios
- **Mocks** for simulating external catalog APIs

## Key Takeaways

1. **Start simple**: Basic test functions with clear assertions
2. **Use fixtures**: For setup code that's reused across tests
3. **Parametrize**: To test many cases without duplication
4. **Mock wisely**: Isolate tests from external dependencies
5. **Test behavior**: Not implementation details
6. **Run often**: Tests are only useful if you run them

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Guide](https://docs.python.org/3/library/unittest.mock.html)
- [pytest Fixtures Best Practices](https://docs.pytest.org/en/latest/explanation/fixtures.html)
