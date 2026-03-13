"""Automated code review service for analyzing code quality."""

import ast
import logging
import re
import subprocess
import tempfile
import os
from typing import Any

from api.schemas.submission import CodeMetrics, TestResults, TestResult

logger = logging.getLogger(__name__)


class CodeReviewService:
    """Service for automated code review and quality analysis."""

    def __init__(self):
        """Initialize code review service."""
        pass

    async def analyze_code(self, files: dict[str, str]) -> CodeMetrics:
        """Analyze code quality metrics.
        
        Args:
            files: Dictionary of file paths to content
            
        Returns:
            CodeMetrics with analysis results
        """
        all_code = "\n".join(files.values())
        
        # Calculate basic metrics
        lines_of_code = self._count_lines_of_code(all_code)
        total_lines = len(all_code.split("\n"))
        blank_lines = self._count_blank_lines(all_code)
        comment_lines = self._count_comment_lines(all_code)
        
        # Analyze structure
        function_count = self._count_functions(all_code)
        class_count = self._count_classes(all_code)
        average_function_length = self._calculate_avg_function_length(all_code)
        docstring_coverage = self._calculate_docstring_coverage(all_code)
        
        # Run linting
        lint_errors, lint_warnings = await self._run_linter(files)
        
        # Calculate complexity (simple version)
        complexity_score = self._calculate_complexity(all_code)
        
        return CodeMetrics(
            lines_of_code=lines_of_code,
            total_lines=total_lines,
            blank_lines=blank_lines,
            comment_lines=comment_lines,
            function_count=function_count,
            class_count=class_count,
            average_function_length=average_function_length,
            docstring_coverage=docstring_coverage,
            complexity_score=complexity_score,
            lint_errors=lint_errors,
            lint_warnings=lint_warnings,
        )

    async def run_tests(
        self,
        files: dict[str, str],
        test_code: str | None = None,
        timeout: int = 30
    ) -> TestResults:
        """Run tests on submitted code.
        
        Args:
            files: Dictionary of file paths to content
            test_code: Optional test code to run
            timeout: Execution timeout in seconds
            
        Returns:
            TestResults with test outcomes
        """
        import time
        from api.services.docker_runner import get_docker_runner
        
        runner = get_docker_runner()
        
        # Build test script
        test_script = self._build_test_script(files, test_code)
        
        start_time = time.time()
        result = runner.execute(test_script, timeout=timeout)
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Parse test results
        test_results = []
        passed = 0
        failed = 0
        
        if result.success:
            # Parse pytest output or unittest output
            test_results, passed, failed = self._parse_test_output(result.stdout)
        
        total = passed + failed
        success_rate = (passed / total * 100) if total > 0 else 0
        
        return TestResults(
            total=total,
            passed=passed,
            failed=failed,
            success_rate=success_rate,
            tests=test_results,
            stdout=result.stdout if len(result.stdout) < 10000 else result.stdout[:10000] + "...",
            stderr=result.stderr if len(result.stderr) < 5000 else result.stderr[:5000] + "...",
            execution_time_ms=execution_time_ms,
        )

    def check_required_patterns(
        self,
        files: dict[str, str],
        required_patterns: list[str] | None = None
    ) -> dict[str, Any]:
        """Check if code contains required patterns.
        
        Args:
            files: Dictionary of file paths to content
            required_patterns: List of regex patterns to check for
            
        Returns:
            Dict with pattern check results
        """
        all_code = "\n".join(files.values())
        
        default_patterns = [
            r"class\s+\w+",  # Class definition
            r"def\s+\w+\s*\(",  # Function definition
            r"\"\"\"|'''",  # Docstrings
        ]
        
        patterns = required_patterns or default_patterns
        results = {}
        
        for pattern in patterns:
            matches = re.findall(pattern, all_code)
            results[pattern] = len(matches)
        
        return {
            "patterns_found": results,
            "all_patterns_present": all(count > 0 for count in results.values()),
        }

    def check_required_files(
        self,
        files: dict[str, str],
        required_files: list[str]
    ) -> dict[str, bool]:
        """Check if required files are present.
        
        Args:
            files: Dictionary of file paths to content
            required_files: List of required file names/patterns
            
        Returns:
            Dict mapping required files to presence status
        """
        file_paths = set(files.keys())
        results = {}
        
        for required in required_files:
            # Check for exact match or basename match
            found = any(
                path == required or 
                os.path.basename(path) == required or
                path.endswith(required)
                for path in file_paths
            )
            results[required] = found
        
        return results

    def _count_lines_of_code(self, code: str) -> int:
        """Count non-blank, non-comment lines of code."""
        lines = code.split("\n")
        count = 0
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                count += 1
        return count

    def _count_blank_lines(self, code: str) -> int:
        """Count blank lines."""
        lines = code.split("\n")
        return sum(1 for line in lines if not line.strip())

    def _count_comment_lines(self, code: str) -> int:
        """Count comment lines."""
        lines = code.split("\n")
        return sum(1 for line in lines if line.strip().startswith("#"))

    def _count_functions(self, code: str) -> int:
        """Count function definitions."""
        try:
            tree = ast.parse(code)
            count = 0
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    count += 1
            return count
        except SyntaxError:
            return 0

    def _count_classes(self, code: str) -> int:
        """Count class definitions."""
        try:
            tree = ast.parse(code)
            count = 0
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    count += 1
            return count
        except SyntaxError:
            return 0

    def _calculate_avg_function_length(self, code: str) -> float:
        """Calculate average function length in lines."""
        try:
            tree = ast.parse(code)
            function_lengths = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    length = node.end_lineno - node.lineno + 1 if node.end_lineno else 10
                    function_lengths.append(length)
            
            if function_lengths:
                return round(sum(function_lengths) / len(function_lengths), 1)
            return 0.0
        except SyntaxError:
            return 0.0

    def _calculate_docstring_coverage(self, code: str) -> float:
        """Calculate docstring coverage percentage."""
        try:
            tree = ast.parse(code)
            
            # Count functions and classes
            functions_and_classes = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    functions_and_classes.append(node)
            
            if not functions_and_classes:
                return 100.0
            
            # Count those with docstrings
            with_docstrings = 0
            for node in functions_and_classes:
                if (
                    node.body and 
                    isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, (ast.Str, ast.Constant))
                ):
                    with_docstrings += 1
            
            return round(with_docstrings / len(functions_and_classes) * 100, 1)
        except SyntaxError:
            return 0.0

    async def _run_linter(self, files: dict[str, str]) -> tuple[int, int]:
        """Run flake8 linter on code.
        
        Returns:
            Tuple of (error_count, warning_count)
        """
        try:
            # Create temporary directory with files
            with tempfile.TemporaryDirectory() as tmpdir:
                for path, content in files.items():
                    # Sanitize path to prevent directory traversal
                    safe_path = os.path.basename(path)
                    if not safe_path.endswith('.py'):
                        safe_path += '.py'
                    
                    file_path = os.path.join(tmpdir, safe_path)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                
                # Run flake8
                result = subprocess.run(
                    ['flake8', '--max-line-length=100', '--count', tmpdir],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # Parse output for error/warning counts
                output = result.stdout + result.stderr
                
                # Count E (errors) and W (warnings)
                errors = len(re.findall(r':\s*E\d+', output))
                warnings = len(re.findall(r':\s*W\d+', output))
                
                return errors, warnings
                
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            logger.warning(f"Linter execution failed: {e}")
            return 0, 0

    def _calculate_complexity(self, code: str) -> float | None:
        """Calculate cyclomatic complexity score."""
        try:
            tree = ast.parse(code)
            
            complexity = 0
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.While, ast.For, 
                                     ast.ExceptHandler, ast.With,
                                     ast.Assert, ast.comprehension)):
                    complexity += 1
                elif isinstance(node, ast.BoolOp):
                    complexity += len(node.values) - 1
            
            return float(complexity) if complexity > 0 else None
        except SyntaxError:
            return None

    def _build_test_script(self, files: dict[str, str], test_code: str | None) -> str:
        """Build executable test script from files."""
        lines = []
        
        # Add all user files
        for path, content in files.items():
            lines.append(f"# File: {path}")
            lines.append(content)
            lines.append("")
        
        # Add test code if provided
        if test_code:
            lines.append("# Test code")
            lines.append(test_code)
        else:
            # Add a default test runner
            lines.append(self._get_default_test_runner())
        
        return "\n".join(lines)

    def _get_default_test_runner(self) -> str:
        """Get default test runner code."""
        return '''
import unittest
import sys

# Run all tests
loader = unittest.TestLoader()
suite = loader.loadTestsFromModule(sys.modules[__name__])
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# Exit with appropriate code
sys.exit(0 if result.wasSuccessful() else 1)
'''

    def _parse_test_output(self, output: str) -> tuple[list[TestResult], int, int]:
        """Parse test output to extract results."""
        test_results = []
        passed = 0
        failed = 0
        
        lines = output.split("\n")
        
        for line in lines:
            # Parse unittest output
            if line.startswith("test_"):
                parts = line.split()
                test_name = parts[0]
                
                if "... ok" in line or "OK" in line.upper():
                    test_results.append(TestResult(
                        name=test_name,
                        passed=True,
                        duration_ms=0,
                        output=line
                    ))
                    passed += 1
                elif "FAIL" in line or "ERROR" in line:
                    test_results.append(TestResult(
                        name=test_name,
                        passed=False,
                        duration_ms=0,
                        output=line,
                        error="Test failed"
                    ))
                    failed += 1
            
            # Parse pytest-style output
            elif "PASSED" in line:
                test_name = line.split()[0] if line.split() else "unknown"
                test_results.append(TestResult(
                    name=test_name,
                    passed=True,
                    duration_ms=0,
                    output=line
                ))
                passed += 1
            elif "FAILED" in line:
                test_name = line.split()[0] if line.split() else "unknown"
                test_results.append(TestResult(
                    name=test_name,
                    passed=False,
                    duration_ms=0,
                    output=line,
                    error="Test failed"
                ))
                failed += 1
        
        return test_results, passed, failed


# Service singleton
_code_review_service: CodeReviewService | None = None


def get_code_review_service() -> CodeReviewService:
    """Get or create code review service singleton."""
    global _code_review_service
    if _code_review_service is None:
        _code_review_service = CodeReviewService()
    return _code_review_service
