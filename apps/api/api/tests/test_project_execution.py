"""Tests for project execution service."""

import pytest

from api.schemas.execution import (
    ProjectExecutionRequest,
    ProjectRunRequest,
    ProjectTestRequest,
)
from api.services.project_execution import (
    ProjectExecutionService,
    get_project_execution_service,
    reset_project_execution_service,
)


class TestProjectExecutionService:
    """Test project execution service."""

    @pytest.fixture(autouse=True)
    def reset_service(self):
        """Reset service singleton before each test."""
        reset_project_execution_service()
        yield
        reset_project_execution_service()

    @pytest.fixture
    def service(self):
        """Get project execution service."""
        return get_project_execution_service()

    @pytest.fixture
    def sample_project(self):
        """Sample multi-file project."""
        return {
            "src/__init__.py": "",
            "src/main.py": """from bank import Bank

def main():
    b = Bank()
    print(f"Initial balance: {b.balance}")
    b.deposit(100)
    print(f"After deposit: {b.balance}")

if __name__ == "__main__":
    main()
""",
            "src/bank.py": """class Bank:
    def __init__(self):
        self.balance = 0
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False
""",
            "tests/__init__.py": "",
            "tests/test_bank.py": """from bank import Bank

def test_bank_initial_balance():
    b = Bank()
    assert b.balance == 0

def test_bank_deposit():
    b = Bank()
    b.deposit(100)
    assert b.balance == 100

def test_bank_withdraw():
    b = Bank()
    b.deposit(100)
    assert b.withdraw(50) == True
    assert b.balance == 50

def test_bank_withdraw_insufficient():
    b = Bank()
    assert b.withdraw(50) == False
""",
        }

    def test_validate_python_syntax_valid(self, service):
        """Test syntax validation with valid code."""
        code = "def hello():\n    return 'world'"
        is_valid, error, line, col = service._validate_python_syntax(code)
        assert is_valid is True
        assert error is None

    def test_validate_python_syntax_invalid(self, service):
        """Test syntax validation with invalid code."""
        code = "def hello(\n    return 'world'"
        is_valid, error, line, col = service._validate_python_syntax(code)
        assert is_valid is False
        assert error is not None
        assert line is not None

    def test_sanitize_path(self, service):
        """Test path sanitization."""
        assert service._sanitize_path("src/main.py") == "src/main.py"
        assert service._sanitize_path("/etc/passwd") == "etc/passwd"
        assert service._sanitize_path("../../secret") == "_/_/_secret"
        assert service._sanitize_path("normal/file.py") == "normal/file.py"

    @pytest.mark.asyncio
    async def test_validate_project_valid(self, service, sample_project):
        """Test project validation with valid project."""
        result = await service.validate_project(
            files=sample_project,
            required_files=["src/main.py", "src/bank.py"],
        )

        assert result.valid is True
        assert len(result.validations) > 0

    @pytest.mark.asyncio
    async def test_validate_project_missing_file(self, service, sample_project):
        """Test project validation with missing required file."""
        result = await service.validate_project(
            files=sample_project,
            required_files=["src/missing.py"],
        )

        assert result.valid is False
        missing_validations = [v for v in result.validations if not v.valid]
        assert len(missing_validations) > 0

    @pytest.mark.asyncio
    async def test_validate_project_syntax_error(self, service):
        """Test project validation with syntax error."""
        files = {
            "bad.py": "def broken(\n  pass",
        }
        result = await service.validate_project(files=files)

        assert result.valid is False
        syntax_errors = [v for v in result.validations if not v.valid and "syntax" in v.message.lower()]
        assert len(syntax_errors) > 0

    def test_create_runner_script(self, service):
        """Test runner script creation."""
        script = service._create_runner_script("src/main.py")
        assert "src/main.py" in script or "src.main" in script
        assert "/project" in script
        assert "PYTHONPATH" in script or "sys.path" in script

    def test_create_pytest_runner(self, service):
        """Test pytest runner script creation."""
        script = service._create_pytest_runner("tests")
        assert "pytest" in script
        assert "tests" in script
        assert "/project" in script

    def test_parse_pytest_output(self, service):
        """Test pytest output parsing."""
        output = """
test_bank.py::test_bank_initial_balance PASSED
test_bank.py::test_bank_deposit PASSED
test_bank.py::test_bank_withdraw FAILED
test_bank.py::test_bank_withdraw_insufficient PASSED
"""
        tests, summary = service._parse_pytest_output(output)

        assert summary["total"] == 4
        assert summary["passed"] == 3
        assert summary["failed"] == 1
        assert len(tests) == 4


class TestProjectSchemas:
    """Test project execution schemas."""

    def test_project_execution_request_valid(self):
        """Test valid project execution request."""
        request = ProjectExecutionRequest(
            files={"main.py": "print('hello')"},
            entry_point="main.py",
        )
        assert request.files == {"main.py": "print('hello')"}
        assert request.entry_point == "main.py"
        assert request.timeout == 30  # default

    def test_project_execution_request_invalid_entry_point(self):
        """Test project execution request with invalid entry point."""
        with pytest.raises(ValueError):
            ProjectExecutionRequest(
                files={"main.txt": "hello"},
                entry_point="main.txt",  # Not a .py file
            )

    def test_project_execution_request_empty_files(self):
        """Test project execution request with empty files."""
        with pytest.raises(ValueError):
            ProjectExecutionRequest(
                files={},
                entry_point="main.py",
            )

    def test_project_run_request(self):
        """Test project run request."""
        request = ProjectRunRequest(
            files={"src/main.py": "print('hello')"},
            entry_point="src/main.py",
        )
        assert request.files["src/main.py"] == "print('hello')"
        assert request.entry_point == "src/main.py"

    def test_project_test_request(self):
        """Test project test request."""
        request = ProjectTestRequest(
            files={"tests/test.py": "def test(): pass"},
            test_path="tests/test_specific.py",
        )
        assert request.test_path == "tests/test_specific.py"


class TestProjectEndpoints:
    """Test project API endpoints (integration tests)."""

    @pytest.mark.asyncio
    async def test_get_project_not_found(self, client):
        """Test getting non-existent project."""
        # This test requires FastAPI test client
        pass

    @pytest.mark.asyncio
    async def test_validate_project_endpoint(self, client):
        """Test project validation endpoint."""
        # This test requires FastAPI test client
        pass
