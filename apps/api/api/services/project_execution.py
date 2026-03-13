"""Project execution service for multi-file project support."""

import ast
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

from api.schemas.execution import (
    ProjectExecutionRequest,
    ProjectExecutionResponse,
    ProjectFileValidation,
    ProjectSubmissionResponse,
    ProjectTemplate,
    ProjectTestResult,
    ProjectValidationResponse,
    TestResult,
)
from api.services.monitoring import get_monitor

logger = logging.getLogger(__name__)

# Project execution resource limits (higher than single-file)
PROJECT_MEMORY_LIMIT = "512m"  # 512MB RAM
PROJECT_CPU_LIMIT = 1.0  # 1 CPU core
PROJECT_TIMEOUT = 30  # 30 seconds
MAX_OUTPUT_SIZE = 2 * 1024 * 1024  # 2MB max output

# Security options
SECURITY_OPTS = ["no-new-privileges:true"]
CAP_DROP = ["ALL"]
CAP_ADD = []
NETWORK_MODE = "none"


@dataclass
class ProjectExecutionResult:
    """Result of project execution."""

    success: bool
    stdout: str
    stderr: str
    exit_code: int
    timeout: bool
    error: str | None
    duration_ms: int
    memory_usage_mb: float | None = None
    file_results: dict[str, Any] | None = None


class ProjectExecutionService:
    """Service for executing multi-file projects in Docker sandbox."""

    def __init__(
        self,
        sandbox_image: str | None = None,
        memory_limit: str = PROJECT_MEMORY_LIMIT,
        cpu_limit: float = PROJECT_CPU_LIMIT,
    ):
        """Initialize project execution service.

        Args:
            sandbox_image: Docker image to use for sandbox
            memory_limit: Memory limit for container
            cpu_limit: CPU limit for container
        """
        self.sandbox_image = sandbox_image or os.getenv(
            "SANDBOX_IMAGE", "oop-journey-sandbox:latest"
        )
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit
        self._client = None
        self._init_docker_client()
        self.monitor = get_monitor()

    def _init_docker_client(self) -> None:
        """Initialize Docker client."""
        try:
            docker_host = os.getenv("DOCKER_HOST")
            if docker_host:
                self._client = docker.DockerClient(base_url=docker_host)
            else:
                self._client = docker.from_env()
            self._client.ping()
            logger.info("Docker client initialized for project execution")
        except DockerException as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            self._client = None

    def _ensure_image(self) -> bool:
        """Ensure sandbox image exists."""
        if not self._client:
            return False
        try:
            self._client.images.get(self.sandbox_image)
            return True
        except ImageNotFound:
            logger.error(f"Sandbox image '{self.sandbox_image}' not found")
            return False
        except DockerException as e:
            logger.error(f"Docker error: {e}")
            return False

    async def execute_project(
        self,
        files: dict[str, str],
        entry_point: str,
        timeout: int = PROJECT_TIMEOUT,
    ) -> ProjectExecutionResult:
        """Execute a multi-file project.

        Args:
            files: Dictionary mapping file paths to content
            entry_point: Path to the entry point file (e.g., "src/main.py")
            timeout: Maximum execution time in seconds

        Returns:
            ProjectExecutionResult with output and metadata
        """
        if not self._client:
            return ProjectExecutionResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                timeout=False,
                error="Docker not available",
                duration_ms=0,
            )

        if not self._ensure_image():
            return ProjectExecutionResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                timeout=False,
                error=f"Sandbox image '{self.sandbox_image}' not available",
                duration_ms=0,
            )

        temp_dir = tempfile.mkdtemp(prefix="project_sandbox_")
        container_name = f"project_sandbox_{uuid.uuid4().hex[:12]}"
        start_time = time.time()
        container = None

        try:
            # Write all project files
            project_root = Path(temp_dir) / "project"
            project_root.mkdir(parents=True, exist_ok=True)

            for file_path, content in files.items():
                # Sanitize path to prevent directory traversal
                safe_path = self._sanitize_path(file_path)
                full_path = project_root / safe_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")

            # Validate entry point exists
            entry_path = project_root / self._sanitize_path(entry_point)
            if not entry_path.exists():
                return ProjectExecutionResult(
                    success=False,
                    stdout="",
                    stderr="",
                    exit_code=-1,
                    timeout=False,
                    error=f"Entry point '{entry_point}' not found",
                    duration_ms=int((time.time() - start_time) * 1000),
                )

            # Create runner script
            runner_script = self._create_runner_script(entry_point)
            runner_path = project_root / "__runner__.py"
            runner_path.write_text(runner_script, encoding="utf-8")

            # Prepare container configuration
            container_config = {
                "image": self.sandbox_image,
                "command": ["/project/__runner__.py"],
                "name": container_name,
                "detach": True,
                "network_mode": NETWORK_MODE,
                "mem_limit": self.memory_limit,
                "cpu_quota": int(self.cpu_limit * 100000),
                "cpu_period": 100000,
                "read_only": False,  # Allow writing for temp files
                "volumes": {
                    str(project_root): {
                        "bind": "/project",
                        "mode": "rw",
                    }
                },
                "security_opt": SECURITY_OPTS,
                "cap_drop": CAP_DROP,
                "cap_add": CAP_ADD,
                "environment": {
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "PYTHONUNBUFFERED": "1",
                    "PYTHONHASHSEED": "random",
                    "PYTHONPATH": "/project:/project/src",
                },
                "stdout": True,
                "stderr": True,
                "remove": False,
            }

            logger.debug(f"Running project container with config: {container_config}")

            # Run container
            container = self._client.containers.run(**container_config)

            # Wait for container to finish with timeout
            try:
                result = container.wait(timeout=timeout)
                exit_code = result.get("StatusCode", -1)
                timed_out = False
            except Exception as wait_error:
                logger.warning(f"Container wait error: {wait_error}")
                exit_code = -1
                timed_out = True
                error_msg = f"Execution timed out after {timeout}s"

                # Force stop the container
                try:
                    container.stop(timeout=1)
                except Exception:
                    try:
                        container.kill()
                    except Exception as kill_error:
                        logger.error(f"Failed to kill container: {kill_error}")

            # Get logs
            try:
                stdout = container.logs(stdout=True, stderr=False).decode(
                    "utf-8", errors="replace"
                )
                stderr = container.logs(stdout=False, stderr=True).decode(
                    "utf-8", errors="replace"
                )

                # Truncate if too large
                if len(stdout) > MAX_OUTPUT_SIZE:
                    stdout = stdout[:MAX_OUTPUT_SIZE] + "\n[Output truncated...]"
                if len(stderr) > MAX_OUTPUT_SIZE:
                    stderr = stderr[:MAX_OUTPUT_SIZE] + "\n[Error output truncated...]"

            except Exception as log_error:
                logger.error(f"Failed to get container logs: {log_error}")
                stdout = ""
                stderr = f"Failed to retrieve output: {log_error}"

            duration_ms = int((time.time() - start_time) * 1000)

            # Get memory stats
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
                if stderr:
                    final_error = stderr.strip()[:500]
                else:
                    final_error = f"Execution failed with exit code {exit_code}"

            return ProjectExecutionResult(
                success=success,
                stdout=stdout,
                stderr=stderr if not success else "",
                exit_code=exit_code,
                timeout=timed_out,
                error=final_error,
                duration_ms=duration_ms,
                memory_usage_mb=memory_usage_mb,
            )

        except ContainerError as e:
            logger.error(f"Container error: {e}")
            return ProjectExecutionResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                timeout=False,
                error=f"Container error: {e}",
                duration_ms=int((time.time() - start_time) * 1000),
            )

        except Exception as e:
            logger.exception("Unexpected error during project execution")
            return ProjectExecutionResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                timeout=False,
                error=f"Execution error: {str(e)}",
                duration_ms=int((time.time() - start_time) * 1000),
            )

        finally:
            # Cleanup
            if container:
                try:
                    container.remove(force=True, v=True)
                except Exception as e:
                    logger.warning(f"Failed to remove container: {e}")

            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as e:
                logger.warning(f"Failed to remove temp directory: {e}")

    async def run_project_tests(
        self,
        files: dict[str, str],
        test_path: str = "tests",
        timeout: int = PROJECT_TIMEOUT,
    ) -> ProjectTestResult:
        """Run pytest on project tests.

        Args:
            files: Dictionary mapping file paths to content
            test_path: Path to tests directory or specific test file
            timeout: Maximum execution time

        Returns:
            ProjectTestResult with test results
        """
        temp_dir = tempfile.mkdtemp(prefix="project_test_")
        start_time = time.time()

        try:
            # Write all project files
            project_root = Path(temp_dir) / "project"
            project_root.mkdir(parents=True, exist_ok=True)

            for file_path, content in files.items():
                safe_path = self._sanitize_path(file_path)
                full_path = project_root / safe_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")

            # Create pytest runner script
            pytest_runner = self._create_pytest_runner(test_path)
            runner_path = project_root / "__pytest_runner__.py"
            runner_path.write_text(pytest_runner, encoding="utf-8")

            # Execute pytest
            result = await self.execute_project(
                files={**files, "__pytest_runner__.py": pytest_runner},
                entry_point="__pytest_runner__.py",
                timeout=timeout,
            )

            # Parse test results
            tests = []
            summary = {"total": 0, "passed": 0, "failed": 0, "errors": 0, "skipped": 0}

            if result.success:
                tests, summary = self._parse_pytest_output(result.stdout)

            duration_ms = int((time.time() - start_time) * 1000)

            return ProjectTestResult(
                success=result.success and summary["failed"] == 0 and summary["errors"] == 0,
                tests=tests,
                summary=summary,
                stdout=result.stdout,
                stderr=result.stderr,
                execution_time_ms=duration_ms,
                error=result.error,
            )

        finally:
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as e:
                logger.warning(f"Failed to remove temp directory: {e}")

    async def validate_project(
        self, files: dict[str, str], required_files: list[str] | None = None
    ) -> ProjectValidationResponse:
        """Validate project files.

        Args:
            files: Dictionary mapping file paths to content
            required_files: List of required file paths

        Returns:
            ProjectValidationResponse with validation results
        """
        validations = []
        all_valid = True

        # Check required files
        if required_files:
            for required in required_files:
                found = required in files
                validations.append(
                    ProjectFileValidation(
                        file_path=required,
                        valid=found,
                        message="File found" if found else "Required file missing",
                    )
                )
                if not found:
                    all_valid = False

        # Validate Python syntax for each file
        for file_path, content in files.items():
            if not file_path.endswith(".py"):
                continue

            is_valid, error, line, col = self._validate_python_syntax(content)
            validations.append(
                ProjectFileValidation(
                    file_path=file_path,
                    valid=is_valid,
                    message=error or "Syntax valid",
                    line=line,
                    column=col,
                )
            )
            if not is_valid:
                all_valid = False

        # Check imports resolve
        import_errors = self._check_imports(files)
        for error in import_errors:
            validations.append(error)
            all_valid = False

        return ProjectValidationResponse(
            valid=all_valid,
            validations=validations,
            message="Project is valid" if all_valid else "Validation failed",
        )

    def _validate_python_syntax(
        self, code: str
    ) -> tuple[bool, str | None, int | None, int | None]:
        """Validate Python syntax without executing."""
        try:
            ast.parse(code)
            return True, None, None, None
        except SyntaxError as e:
            return False, str(e), e.lineno, e.offset
        except Exception as e:
            return False, str(e), None, None

    def _check_imports(self, files: dict[str, str]) -> list[ProjectFileValidation]:
        """Check if imports in files can be resolved."""
        errors = []
        file_set = set(files.keys())

        for file_path, content in files.items():
            if not file_path.endswith(".py"):
                continue

            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            # Check if module exists in project
                            module_path = alias.name.replace(".", "/") + ".py"
                            if module_path not in file_set:
                                # Could be a stdlib module - skip for now
                                pass

                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            # Check relative imports
                            if node.level > 0:
                                # Relative import - check if target exists
                                base_path = Path(file_path).parent
                                module_parts = node.module.split(".")
                                target_path = (
                                    base_path
                                    / "/".join([".."] * (node.level - 1) + module_parts)
                                )
                                target_str = str(target_path).replace("\\", "/") + ".py"
                                if target_str not in file_set:
                                    errors.append(
                                        ProjectFileValidation(
                                            file_path=file_path,
                                            valid=False,
                                            message=f"Cannot resolve import: {node.module}",
                                            line=node.lineno,
                                        )
                                    )

            except SyntaxError:
                # Already reported in syntax validation
                pass

        return errors

    def _create_runner_script(self, entry_point: str) -> str:
        """Create a runner script for executing the project."""
        return f'''#!/usr/bin/env python3
import sys
import os
import traceback

# Add project directories to Python path
sys.path.insert(0, '/project')
sys.path.insert(0, '/project/src')

# Change to project directory
os.chdir('/project')

# Import and run the entry point
try:
    # Import the entry module
    entry_module = "{entry_point.replace('/', '.').replace('.py', '')}"
    if entry_module.startswith('src.'):
        entry_module = entry_module[4:]  # Remove src. prefix for import
    
    __import__(entry_module)
except Exception as e:
    print(f"Error executing {{entry_module}}: {{e}}", file=sys.stderr)
    traceback.print_exc()
    sys.exit(1)
'''

    def _create_pytest_runner(self, test_path: str) -> str:
        """Create a pytest runner script."""
        return f'''#!/usr/bin/env python3
import sys
import os
import subprocess

# Add project directories to Python path
sys.path.insert(0, '/project')
sys.path.insert(0, '/project/src')

os.chdir('/project')

# Run pytest with JSON output
result = subprocess.run(
    [
        'python', '-m', 'pytest',
        '{test_path}',
        '-v',
        '--tb=short',
        '--no-header',
        '-p', 'no:cacheprovider',
        '--color=no',
    ],
    capture_output=True,
    text=True,
)

print(result.stdout)
if result.stderr:
    print(result.stderr, file=sys.stderr)

sys.exit(result.returncode)
'''

    def _parse_pytest_output(
        self, output: str
    ) -> tuple[list[TestResult], dict[str, int]]:
        """Parse pytest output to extract test results."""
        import re

        tests = []
        summary = {"total": 0, "passed": 0, "failed": 0, "errors": 0, "skipped": 0}

        # Parse individual test results
        # Pattern: test_file.py::test_name PASSED/FAILED/ERROR/SKIPPED
        pattern = r"(\S+)::(test_\S+)\s+(PASSED|FAILED|ERROR|SKIPPED)"

        for match in re.finditer(pattern, output, re.MULTILINE):
            file_path = match.group(1)
            test_name = match.group(2)
            status = match.group(3).lower()

            test_result = TestResult(
                name=f"{file_path}::{test_name}",
                passed=status == "passed",
                output=output,
            )
            tests.append(test_result)

            summary["total"] += 1
            if status == "passed":
                summary["passed"] += 1
            elif status == "failed":
                summary["failed"] += 1
            elif status == "error":
                summary["errors"] += 1
            elif status == "skipped":
                summary["skipped"] += 1

        # Try to extract summary from end of output
        summary_patterns = [
            r"(\d+) passed",
            r"(\d+) failed",
            r"(\d+) error",
            r"(\d+) skipped",
        ]

        for pattern in summary_patterns:
            match = re.search(pattern, output)
            if match:
                # Override summary with pytest's summary if available
                pass

        return tests, summary

    def _sanitize_path(self, path: str) -> str:
        """Sanitize file path to prevent directory traversal."""
        # Normalize path
        path = os.path.normpath(path)
        # Remove leading slashes and parent directory references
        path = path.lstrip("/\\")
        path = path.replace("..", "_")
        return path

    async def get_project_template(self, slug: str) -> ProjectTemplate | None:
        """Get project template from curriculum.

        Args:
            slug: Project slug (e.g., "week-01-project")

        Returns:
            ProjectTemplate or None if not found
        """
        # This will be implemented to load from curriculum
        # For now, return a default structure
        return None


# Singleton instance
_project_execution_service: ProjectExecutionService | None = None


def get_project_execution_service() -> ProjectExecutionService:
    """Get or create project execution service singleton."""
    global _project_execution_service
    if _project_execution_service is None:
        _project_execution_service = ProjectExecutionService()
    return _project_execution_service


def reset_project_execution_service() -> None:
    """Reset project execution service (for testing)."""
    global _project_execution_service
    _project_execution_service = None
