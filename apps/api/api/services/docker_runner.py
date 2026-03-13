"""Docker runner for secure code execution."""

import json
import logging
import os
import shutil
import tempfile
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import docker
    from docker.errors import ContainerError, DockerException, ImageNotFound
    DOCKER_AVAILABLE = True
except ImportError:
    docker = None
    ContainerError = DockerException = ImageNotFound = Exception
    DOCKER_AVAILABLE = False

logger = logging.getLogger(__name__)

# Resource limits
DEFAULT_MEMORY_LIMIT = "256m"  # 256MB RAM
DEFAULT_CPU_LIMIT = 0.5  # 0.5 CPU cores
DEFAULT_TIMEOUT = 10  # 10 seconds
MAX_OUTPUT_SIZE = 1024 * 1024  # 1MB max output

# Security options
SECURITY_OPTS = [
    "no-new-privileges:true",
]

CAP_DROP = [
    "ALL",  # Drop all capabilities
]

CAP_ADD = []  # Don't add any capabilities

NETWORK_MODE = "none"  # No network access


@dataclass
class ExecutionResult:
    """Result of code execution."""
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    timeout: bool
    error: str | None
    duration_ms: int
    memory_usage_mb: float | None = None


class DockerRunner:
    """Docker-based secure code execution runner."""

    def __init__(self, 
                 sandbox_image: str = None,
                 memory_limit: str = DEFAULT_MEMORY_LIMIT,
                 cpu_limit: float = DEFAULT_CPU_LIMIT):
        """Initialize Docker runner.
        
        Args:
            sandbox_image: Docker image to use for sandbox (default from env)
            memory_limit: Memory limit for container (e.g., "256m")
            cpu_limit: CPU limit for container (e.g., 0.5)
        """
        self.sandbox_image = sandbox_image or os.getenv(
            "SANDBOX_IMAGE", 
            "oop-journey-sandbox:latest"
        )
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit
        self._client = None
        self._init_docker_client()

    def _init_docker_client(self) -> None:
        """Initialize Docker client with proper configuration."""
        try:
            # Try environment-based connection first
            docker_host = os.getenv("DOCKER_HOST")
            if docker_host:
                self._client = docker.DockerClient(base_url=docker_host)
            else:
                self._client = docker.from_env()
            
            # Test connection
            self._client.ping()
            logger.info("Docker client initialized successfully")
            
        except DockerException as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            self._client = None

    def _ensure_image(self) -> bool:
        """Ensure sandbox image exists.
        
        Returns:
            True if image is available, False otherwise
        """
        if not self._client:
            return False
            
        try:
            self._client.images.get(self.sandbox_image)
            return True
        except ImageNotFound:
            logger.error(f"Sandbox image '{self.sandbox_image}' not found")
            logger.info("Please build the sandbox image: docker build -f sandbox.Dockerfile -t oop-journey-sandbox .")
            return False
        except DockerException as e:
            logger.error(f"Docker error checking image: {e}")
            return False

    def execute(self, 
                code: str, 
                timeout: int = DEFAULT_TIMEOUT) -> ExecutionResult:
        """Execute Python code in a secure Docker container.
        
        Args:
            code: Python code to execute
            timeout: Maximum execution time in seconds
            
        Returns:
            ExecutionResult with output and metadata
        """
        if not self._client:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                timeout=False,
                error="Docker not available",
                duration_ms=0
            )

        if not self._ensure_image():
            return ExecutionResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                timeout=False,
                error=f"Sandbox image '{self.sandbox_image}' not available",
                duration_ms=0
            )

        # Create temporary directory for code
        temp_dir = tempfile.mkdtemp(prefix="sandbox_")
        container_name = f"sandbox_{uuid.uuid4().hex[:12]}"
        
        start_time = time.time()
        container = None
        
        try:
            # Write code to file
            code_file = Path(temp_dir) / "code.py"
            code_file.write_text(code, encoding="utf-8")
            
            # Prepare container configuration
            container_config = {
                "image": self.sandbox_image,
                "command": ["/workspace/code.py"],
                "name": container_name,
                "detach": True,
                "network_mode": NETWORK_MODE,
                "mem_limit": self.memory_limit,
                "cpu_quota": int(self.cpu_limit * 100000),  # Docker uses microseconds
                "cpu_period": 100000,
                "read_only": True,  # Read-only root filesystem
                "volumes": {
                    temp_dir: {
                        "bind": "/workspace",
                        "mode": "ro",  # Read-only mount
                    }
                },
                "security_opt": SECURITY_OPTS,
                "cap_drop": CAP_DROP,
                "cap_add": CAP_ADD,
                "environment": {
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "PYTHONUNBUFFERED": "1",
                    "PYTHONHASHSEED": "random",
                },
                "stdout": True,
                "stderr": True,
                "remove": False,  # We'll remove manually for cleanup
            }
            
            logger.debug(f"Running container with config: {container_config}")
            
            # Run container
            container = self._client.containers.run(**container_config)
            
            # Wait for container to finish with timeout
            try:
                result = container.wait(timeout=timeout)
                exit_code = result.get("StatusCode", -1)
                error_msg = result.get("Error", None)
                timed_out = False
            except Exception as wait_error:
                # Timeout or other error
                logger.warning(f"Container wait error: {wait_error}")
                exit_code = -1
                timed_out = True
                error_msg = f"Execution timed out after {timeout}s"
                
                # Force stop the container
                try:
                    container.stop(timeout=1)
                except Exception as stop_error:
                    logger.warning(f"Failed to stop container: {stop_error}")
                    try:
                        container.kill()
                    except Exception as kill_error:
                        logger.error(f"Failed to kill container: {kill_error}")
            
            # Get logs
            try:
                stdout = container.logs(stdout=True, stderr=False).decode("utf-8", errors="replace")
                stderr = container.logs(stdout=False, stderr=True).decode("utf-8", errors="replace")
                
                # Truncate if too large
                if len(stdout) > MAX_OUTPUT_SIZE:
                    stdout = stdout[:MAX_OUTPUT_SIZE] + "\n[Output truncated...]"
                if len(stderr) > MAX_OUTPUT_SIZE:
                    stderr = stderr[:MAX_OUTPUT_SIZE] + "\n[Error output truncated...]"
                    
            except Exception as log_error:
                logger.error(f"Failed to get container logs: {log_error}")
                stdout = ""
                stderr = f"Failed to retrieve output: {log_error}"
            
            # Calculate duration
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Get memory stats if available
            memory_usage_mb = None
            try:
                stats = container.stats(stream=False)
                memory_stats = stats.get("memory_stats", {})
                if memory_stats and "usage" in memory_stats:
                    memory_usage_mb = memory_stats["usage"] / (1024 * 1024)
            except Exception as stats_error:
                logger.debug(f"Failed to get memory stats: {stats_error}")
            
            # Determine success
            success = exit_code == 0 and not timed_out
            
            # Set error message
            final_error = None
            if timed_out:
                final_error = f"Execution timed out after {timeout} seconds"
            elif exit_code != 0:
                if error_msg:
                    final_error = f"Execution failed: {error_msg}"
                elif stderr:
                    final_error = stderr.strip()[:500]  # Limit error message length
                else:
                    final_error = f"Execution failed with exit code {exit_code}"
            
            return ExecutionResult(
                success=success,
                stdout=stdout,
                stderr=stderr if not success else "",
                exit_code=exit_code,
                timeout=timed_out,
                error=final_error,
                duration_ms=duration_ms,
                memory_usage_mb=memory_usage_mb
            )
            
        except ContainerError as e:
            logger.error(f"Container error: {e}")
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                timeout=False,
                error=f"Container error: {e}",
                duration_ms=int((time.time() - start_time) * 1000)
            )
            
        except Exception as e:
            logger.exception("Unexpected error during execution")
            return ExecutionResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                timeout=False,
                error=f"Execution error: {str(e)}",
                duration_ms=int((time.time() - start_time) * 1000)
            )
            
        finally:
            # Cleanup
            if container:
                try:
                    container.remove(force=True, v=True)
                    logger.debug(f"Removed container: {container_name}")
                except Exception as e:
                    logger.warning(f"Failed to remove container {container_name}: {e}")
            
            # Clean up temp directory
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as e:
                logger.warning(f"Failed to remove temp directory {temp_dir}: {e}")

    def validate_syntax(self, code: str) -> tuple[bool, str | None, int | None, int | None]:
        """Validate Python syntax without executing.
        
        Args:
            code: Python code to validate
            
        Returns:
            Tuple of (is_valid, error_message, error_line, error_column)
        """
        import ast
        
        try:
            ast.parse(code)
            return True, None, None, None
        except SyntaxError as e:
            return False, str(e), e.lineno, e.offset
        except Exception as e:
            return False, str(e), None, None

    def health_check(self) -> dict[str, Any]:
        """Check Docker runner health.
        
        Returns:
            Health status dictionary
        """
        status = {
            "docker_available": False,
            "image_available": False,
            "can_run_containers": False,
            "error": None,
        }
        
        try:
            if not self._client:
                status["error"] = "Docker client not initialized"
                return status
            
            # Check Docker connection
            self._client.ping()
            status["docker_available"] = True
            
            # Check image availability
            status["image_available"] = self._ensure_image()
            
            # Test container execution with simple code
            if status["image_available"]:
                test_result = self.execute("print('health_check')", timeout=5)
                status["can_run_containers"] = test_result.success
                if not test_result.success:
                    status["error"] = test_result.error
                    
        except Exception as e:
            status["error"] = str(e)
            
        return status


# Singleton instance
_docker_runner: DockerRunner | None = None


def get_docker_runner() -> DockerRunner:
    """Get or create Docker runner singleton."""
    global _docker_runner
    if _docker_runner is None:
        _docker_runner = DockerRunner()
    return _docker_runner


def reset_docker_runner() -> None:
    """Reset Docker runner (for testing)."""
    global _docker_runner
    _docker_runner = None
