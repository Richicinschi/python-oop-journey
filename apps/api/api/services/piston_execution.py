"""Piston-based code execution service for Render deployment.

This service replaces the Docker-based execution for environments
where Docker-in-Docker is not available (like Render free tier).
"""

import logging
import os
from typing import Optional

import httpx

from api.schemas.execution import CodeExecutionRequest, ExecutionResult

logger = logging.getLogger(__name__)

PISTON_API_URL = os.getenv("PISTON_API_URL", "https://piston-code-execution.onrender.com")


class PistonExecutionService:
    """Code execution service using Piston API."""

    def __init__(self):
        self.api_url = PISTON_API_URL.rstrip("/")
        self.client = httpx.AsyncClient(timeout=30.0)

    async def execute(self, request: CodeExecutionRequest) -> ExecutionResult:
        """Execute Python code via Piston API.
        
        Args:
            request: Execution request with code and optional input
            
        Returns:
            ExecutionResult with output, errors, and exit code
        """
        try:
            # Prepare Piston API request
            piston_request = {
                "language": "python",
                "version": "3.12.0",
                "files": [
                    {
                        "name": "main.py",
                        "content": request.code
                    }
                ],
                "stdin": request.stdin or "",
                "compile_timeout": 10000,
                "run_timeout": 10000,
            }

            # Call Piston API
            response = await self.client.post(
                f"{self.api_url}/api/v2/execute",
                json=piston_request
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Parse Piston response
            run = result.get("run", {})
            compile_output = result.get("compile", {})
            
            stdout = run.get("stdout", "")
            stderr = run.get("stderr", "")
            exit_code = run.get("code", 1)
            
            # Include compile errors if any
            if compile_output.get("stderr"):
                stderr = compile_output["stderr"] + "\n" + stderr
            
            return ExecutionResult(
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code,
                execution_time_ms=run.get("wallTime", 0) * 1000,
                timeout=exit_code == 124,  # Piston uses 124 for timeout
            )
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Piston API error: {e.response.status_code} - {e.response.text}")
            return ExecutionResult(
                stdout="",
                stderr=f"Execution service error: {e.response.status_code}",
                exit_code=1,
                timeout=False,
            )
        except httpx.RequestError as e:
            logger.error(f"Piston connection error: {e}")
            return ExecutionResult(
                stdout="",
                stderr="Code execution service is temporarily unavailable. Please try again later.",
                exit_code=1,
                timeout=False,
            )
        except Exception as e:
            logger.exception("Unexpected error during code execution")
            return ExecutionResult(
                stdout="",
                stderr=f"Internal error: {str(e)}",
                exit_code=1,
                timeout=False,
            )

    async def validate_syntax(self, code: str) -> tuple[bool, Optional[str]]:
        """Validate Python syntax using Piston.
        
        Args:
            code: Python code to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Try to compile the code using Piston
            validation_code = f"""
import ast
try:
    ast.parse({repr(code)})
    print("SYNTAX_OK")
except SyntaxError as e:
    print(f"SYNTAX_ERROR: {{e}}")
"""
            
            validation_request = CodeExecutionRequest(code=validation_code)
            result = await self.execute(validation_request)
            
            if "SYNTAX_OK" in result.stdout:
                return True, None
            elif "SYNTAX_ERROR:" in result.stdout:
                error = result.stdout.split("SYNTAX_ERROR:", 1)[1].strip()
                return False, error
            else:
                # Fallback to error message from stderr
                return False, result.stderr or "Syntax validation failed"
                
        except Exception as e:
            logger.exception("Syntax validation error")
            return False, str(e)


# Singleton instance
_piston_service: Optional[PistonExecutionService] = None


def get_piston_service() -> PistonExecutionService:
    """Get or create Piston execution service singleton."""
    global _piston_service
    if _piston_service is None:
        _piston_service = PistonExecutionService()
    return _piston_service
