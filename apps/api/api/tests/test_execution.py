"""Tests for code execution service."""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock

from api.schemas.execution import (
    CodeExecutionRequest,
    CodeValidationExecutionRequest,
    ExecutionStatus,
)
from api.services.docker_runner import ExecutionResult, DockerRunner
from api.services.execution import ExecutionService
from api.services.monitoring import ExecutionMonitor, get_monitor


class TestDockerRunner:
    """Tests for DockerRunner."""

    @pytest.fixture
    def mock_docker_client(self):
        """Create a mock Docker client."""
        mock_client = MagicMock()
        mock_client.ping.return_value = True
        
        # Mock container
        mock_container = MagicMock()
        mock_container.wait.return_value = {"StatusCode": 0}
        mock_container.logs.return_value = b"Hello, World!"
        mock_container.stats.return_value = {"memory_stats": {"usage": 1024 * 1024 * 50}}
        
        mock_client.containers.run.return_value = mock_container
        mock_client.images.get.return_value = MagicMock()
        
        return mock_client, mock_container

    def test_execute_simple_code(self, mock_docker_client):
        """Test executing simple code."""
        mock_client, mock_container = mock_docker_client
        
        with patch("docker.from_env", return_value=mock_client):
            runner = DockerRunner()
            result = runner.execute('print("Hello, World!")', timeout=10)
        
        assert result.success is True
        assert "Hello, World!" in result.stdout
        assert result.exit_code == 0
        assert result.timeout is False

    def test_execute_timeout(self, mock_docker_client):
        """Test execution timeout handling."""
        mock_client, mock_container = mock_docker_client
        mock_container.wait.side_effect = Exception("Timeout")
        
        with patch("docker.from_env", return_value=mock_client):
            runner = DockerRunner()
            result = runner.execute("import time; time.sleep(100)", timeout=1)
        
        assert result.success is False
        assert result.timeout is True
        assert "timed out" in result.error.lower()

    def test_execute_error_code(self, mock_docker_client):
        """Test execution with error exit code."""
        mock_client, mock_container = mock_docker_client
        mock_container.wait.return_value = {"StatusCode": 1}
        mock_container.logs.return_value = b"Error message"
        
        with patch("docker.from_env", return_value=mock_client):
            runner = DockerRunner()
            result = runner.execute("raise Exception('test')", timeout=10)
        
        assert result.success is False
        assert result.exit_code == 1
        assert result.error is not None

    def test_execute_docker_not_available(self):
        """Test handling when Docker is not available."""
        with patch("docker.from_env", side_effect=Exception("Docker not found")):
            runner = DockerRunner()
            result = runner.execute("print('test')", timeout=10)
        
        assert result.success is False
        assert "Docker not available" in result.error

    def test_validate_syntax_valid(self):
        """Test syntax validation with valid code."""
        runner = DockerRunner()
        is_valid, error, line, col = runner.validate_syntax("print('hello')")
        
        assert is_valid is True
        assert error is None
        assert line is None
        assert col is None

    def test_validate_syntax_invalid(self):
        """Test syntax validation with invalid code."""
        runner = DockerRunner()
        is_valid, error, line, col = runner.validate_syntax("print('hello'")
        
        assert is_valid is False
        assert error is not None
        assert line is not None

    def test_health_check_healthy(self, mock_docker_client):
        """Test health check when all systems are healthy."""
        mock_client, _ = mock_docker_client
        
        with patch("docker.from_env", return_value=mock_client):
            runner = DockerRunner()
            health = runner.health_check()
        
        assert health["docker_available"] is True
        assert health["image_available"] is True
        assert health["can_run_containers"] is True

    def test_health_check_docker_unavailable(self):
        """Test health check when Docker is unavailable."""
        with patch("docker.from_env", side_effect=Exception("Connection refused")):
            runner = DockerRunner()
            health = runner.health_check()
        
        assert health["docker_available"] is False
        assert health["error"] is not None


class TestExecutionService:
    """Tests for ExecutionService."""

    @pytest.fixture
    def service(self):
        """Create execution service with mocked dependencies."""
        with patch("api.services.execution.get_docker_runner") as mock_runner:
            with patch("api.services.execution.get_monitor") as mock_monitor:
                service = ExecutionService()
                service.runner = mock_runner.return_value
                service.monitor = mock_monitor.return_value
                yield service

    @pytest.mark.asyncio
    async def test_execute_simple_code(self, service):
        """Test executing simple code."""
        # Setup mock
        service.runner.execute.return_value = ExecutionResult(
            success=True,
            stdout="Hello, World!",
            stderr="",
            exit_code=0,
            timeout=False,
            error=None,
            duration_ms=100
        )
        
        request = CodeExecutionRequest(code="print('Hello, World!')")
        result = await service.execute(request)
        
        assert result.success is True
        assert result.output == "Hello, World!"
        assert result.error is None
        assert result.execution_time_ms == 100

    @pytest.mark.asyncio
    async def test_execute_with_timeout(self, service):
        """Test execution timeout."""
        service.runner.execute.return_value = ExecutionResult(
            success=False,
            stdout="",
            stderr="",
            exit_code=-1,
            timeout=True,
            error="Execution timed out after 10 seconds",
            duration_ms=10000
        )
        
        request = CodeExecutionRequest(code="import time; time.sleep(100)", timeout=10)
        result = await service.execute(request)
        
        assert result.success is False
        assert result.timeout is True
        assert "timed out" in result.error.lower()

    @pytest.mark.asyncio
    async def test_execute_with_test_code(self, service):
        """Test executing code with test code."""
        service.runner.execute.return_value = ExecutionResult(
            success=True,
            stdout="Test passed",
            stderr="",
            exit_code=0,
            timeout=False,
            error=None,
            duration_ms=200
        )
        
        request = CodeExecutionRequest(
            code="def add(a, b): return a + b",
            test_code="print(add(2, 3))"
        )
        result = await service.execute(request)
        
        # Verify combined code was passed to runner
        call_args = service.runner.execute.call_args
        combined_code = call_args[0][0]
        assert "def add(a, b)" in combined_code
        assert "print(add(2, 3))" in combined_code

    @pytest.mark.asyncio
    async def test_validate_syntax_valid(self, service):
        """Test syntax validation with valid code."""
        service.runner.validate_syntax.return_value = (True, None, None, None)
        
        result = await service.validate_syntax("print('hello')")
        
        assert result.valid is True
        assert result.error is None

    @pytest.mark.asyncio
    async def test_validate_syntax_invalid(self, service):
        """Test syntax validation with invalid code."""
        service.runner.validate_syntax.return_value = (
            False, "unexpected EOF", 1, 15
        )
        
        result = await service.validate_syntax("print('hello'")
        
        assert result.valid is False
        assert "EOF" in result.error
        assert result.syntax_error_line == 1

    @pytest.mark.asyncio
    async def test_check_rate_limit(self, service):
        """Test rate limit checking."""
        service.monitor.check_rate_limit.return_value = (True, 5, 10)
        
        allowed, current, limit = await service.check_rate_limit("user123", "127.0.0.1")
        
        assert allowed is True
        assert current == 5
        assert limit == 10


class TestExecutionMonitor:
    """Tests for ExecutionMonitor."""

    @pytest.fixture
    def monitor(self):
        """Create fresh monitor instance."""
        return ExecutionMonitor()

    def test_log_execution_success(self, monitor):
        """Test logging successful execution."""
        record = monitor.log_execution(
            execution_id="test-123",
            user_id="user-456",
            code="print('hello')",
            status=ExecutionStatus.COMPLETED,
            duration_ms=100,
            exit_code=0,
            error=None
        )
        
        assert record.id == "test-123"
        assert record.user_id == "user-456"
        assert record.status == ExecutionStatus.COMPLETED
        assert record.error_type is None

    def test_log_execution_timeout(self, monitor):
        """Test logging timeout execution."""
        record = monitor.log_execution(
            execution_id="test-123",
            user_id=None,
            code="time.sleep(100)",
            status=ExecutionStatus.TIMEOUT,
            duration_ms=10000,
            exit_code=-1,
            error="Execution timed out"
        )
        
        assert record.status == ExecutionStatus.TIMEOUT
        assert record.error_type.value == "timeout"

    def test_rate_limit_tracking(self, monitor):
        """Test rate limit tracking."""
        user_id = "test-user"
        
        # Add executions up to limit
        for i in range(5):
            monitor._track_user_execution(user_id)
        
        # Check rate limit
        allowed, count, limit = monitor.check_rate_limit(user_id, None)
        assert count == 5
        assert limit == 10
        assert allowed is True

    def test_rate_limit_exceeded(self, monitor):
        """Test rate limit exceeded."""
        user_id = "test-user"
        
        # Add executions beyond limit
        for i in range(15):
            monitor._track_user_execution(user_id)
        
        # Check rate limit
        allowed, count, limit = monitor.check_rate_limit(user_id, None)
        assert count >= 10
        assert allowed is False

    def test_get_metrics_empty(self, monitor):
        """Test getting metrics with no executions."""
        metrics = monitor.get_metrics(hours=24)
        
        assert metrics.total_executions == 0
        assert metrics.successful_executions == 0
        assert metrics.failure_rate == 0.0

    def test_get_metrics_with_data(self, monitor):
        """Test getting metrics with execution data."""
        # Log some executions
        for i in range(10):
            monitor.log_execution(
                execution_id=f"test-{i}",
                user_id="user-1",
                code="print('hello')",
                status=ExecutionStatus.COMPLETED if i < 7 else ExecutionStatus.FAILED,
                duration_ms=100,
                exit_code=0 if i < 7 else 1,
                error=None if i < 7 else "Error"
            )
        
        metrics = monitor.get_metrics(hours=24)
        
        assert metrics.total_executions == 10
        assert metrics.successful_executions == 7
        assert metrics.failed_executions == 3
        assert metrics.failure_rate == 30.0

    def test_error_breakdown(self, monitor):
        """Test error type breakdown."""
        # Log different error types
        monitor.log_execution(
            "test-1", None, "code",
            ExecutionStatus.TIMEOUT, 10000, -1, "timed out"
        )
        monitor.log_execution(
            "test-2", None, "code",
            ExecutionStatus.FAILED, 100, 1, "Syntax error"
        )
        monitor.log_execution(
            "test-3", None, "code",
            ExecutionStatus.TIMEOUT, 10000, -1, "timed out"
        )
        
        breakdown = monitor.get_error_breakdown(hours=24)
        
        assert breakdown.get("timeout") == 2
        assert breakdown.get("syntax_error") == 1


class TestSecurity:
    """Security tests for code execution."""

    @pytest.fixture
    def runner(self):
        """Create DockerRunner with mocked Docker."""
        mock_client = MagicMock()
        mock_client.ping.return_value = True
        mock_client.images.get.return_value = MagicMock()
        
        mock_container = MagicMock()
        mock_container.wait.return_value = {"StatusCode": 0}
        mock_container.logs.return_value = b"output"
        mock_container.stats.return_value = {}
        mock_client.containers.run.return_value = mock_container
        
        with patch("docker.from_env", return_value=mock_client):
            runner = DockerRunner()
            yield runner, mock_client

    def test_network_isolation(self, runner):
        """Test that containers run with no network access."""
        docker_runner, mock_client = runner
        
        docker_runner.execute("print('test')")
        
        # Verify network_mode is set to 'none'
        call_kwargs = mock_client.containers.run.call_args[1]
        assert call_kwargs["network_mode"] == "none"

    def test_read_only_filesystem(self, runner):
        """Test that containers run with read-only filesystem."""
        docker_runner, mock_client = runner
        
        docker_runner.execute("print('test')")
        
        # Verify read_only is True
        call_kwargs = mock_client.containers.run.call_args[1]
        assert call_kwargs["read_only"] is True

    def test_capabilities_dropped(self, runner):
        """Test that all capabilities are dropped."""
        docker_runner, mock_client = runner
        
        docker_runner.execute("print('test')")
        
        # Verify capabilities are dropped
        call_kwargs = mock_client.containers.run.call_args[1]
        assert "ALL" in call_kwargs["cap_drop"]

    def test_memory_limit(self, runner):
        """Test memory limit configuration."""
        docker_runner, mock_client = runner
        
        docker_runner.execute("print('test')")
        
        # Verify memory limit
        call_kwargs = mock_client.containers.run.call_args[1]
        assert call_kwargs["mem_limit"] == "256m"

    def test_cpu_limit(self, runner):
        """Test CPU limit configuration."""
        docker_runner, mock_client = runner
        
        docker_runner.execute("print('test')")
        
        # Verify CPU quota
        call_kwargs = mock_client.containers.run.call_args[1]
        assert call_kwargs["cpu_quota"] == 50000  # 0.5 * 100000


class TestIntegration:
    """Integration tests requiring real Docker."""
    
    @pytest.mark.integration
    def test_real_docker_execution(self):
        """Test with real Docker (requires Docker to be running)."""
        # Skip if Docker is not available
        try:
            import docker
            client = docker.from_env()
            client.ping()
        except Exception:
            pytest.skip("Docker not available")
        
        runner = DockerRunner()
        result = runner.execute("print('Hello from Docker!')", timeout=10)
        
        # Should succeed if sandbox image is built
        if "not available" in (result.error or ""):
            pytest.skip("Sandbox image not built")
        
        assert result.success is True
        assert "Hello from Docker!" in result.stdout


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
