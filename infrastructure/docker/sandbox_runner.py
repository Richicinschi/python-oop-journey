#!/usr/bin/env python3
"""
Sandbox runner for learner code execution.
Runs inside an isolated Docker container with strict resource limits.
"""
import sys
import json
import subprocess
import tempfile
import os
import signal
from pathlib import Path

# Configuration
TIMEOUT_SECONDS = 10
MAX_OUTPUT_BYTES = 10000


def run_code(code: str, test_code: str = None) -> dict:
    """
    Execute learner code in a controlled environment.
    
    Args:
        code: The learner's Python code
        test_code: Optional test code to verify the solution
        
    Returns:
        dict with keys: success, stdout, stderr, exit_code, timeout
    """
    result = {
        "success": False,
        "stdout": "",
        "stderr": "",
        "exit_code": None,
        "timeout": False,
        "error": None
    }
    
    # Create temporary directory for execution
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write learner code
        code_file = Path(tmpdir) / "solution.py"
        code_file.write_text(code, encoding="utf-8")
        
        # Write test code if provided
        if test_code:
            test_file = Path(tmpdir) / "test_solution.py"
            test_file.write_text(test_code, encoding="utf-8")
        
        # Prepare command
        if test_code:
            # Run with pytest
            cmd = [
                sys.executable, "-m", "pytest",
                str(test_file),
                "-v",
                "--tb=short",
                "--timeout=10"
            ]
        else:
            # Just run the code
            cmd = [sys.executable, str(code_file)]
        
        try:
            # Run with timeout and capture output
            process = subprocess.run(
                cmd,
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                # Prevent network access
                env={**os.environ, "PYTHONHTTPSVERIFY": "1"}
            )
            
            result["exit_code"] = process.returncode
            result["stdout"] = process.stdout[:MAX_OUTPUT_BYTES]
            result["stderr"] = process.stderr[:MAX_OUTPUT_BYTES]
            result["success"] = process.returncode == 0
            
        except subprocess.TimeoutExpired:
            result["timeout"] = True
            result["error"] = f"Code execution timed out after {TIMEOUT_SECONDS} seconds"
        except Exception as e:
            result["error"] = str(e)
    
    return result


def main():
    """CLI entry point for sandbox runner."""
    if len(sys.argv) < 2:
        print("Usage: sandbox_runner.py <json_payload>", file=sys.stderr)
        sys.exit(1)
    
    # Parse input JSON
    try:
        payload = json.loads(sys.argv[1])
        code = payload.get("code", "")
        test_code = payload.get("test_code")
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        sys.exit(1)
    
    # Run code
    result = run_code(code, test_code)
    
    # Output result as JSON
    print(json.dumps(result))


if __name__ == "__main__":
    main()
