"""Verification service for test execution and result parsing."""

import json
import logging
import re
import subprocess
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from api.schemas.verification import (
    ErrorCategory,
    HintSuggestion,
    TestResult,
    TestStatus,
    VerificationRequest,
    VerificationResponse,
    VerificationResult,
    VerificationSummary,
)
from api.services.curriculum import CurriculumService
from api.services.execution import ExecutionService

logger = logging.getLogger(__name__)


class VerificationService:
    """Service for verifying learner solutions against tests."""

    def __init__(self):
        self.execution_service = ExecutionService()
        self.curriculum_service = CurriculumService()
        self.timeout = 30  # seconds for test execution

    async def verify_solution(
        self, request: VerificationRequest
    ) -> VerificationResult:
        """Verify a learner's solution against tests.

        Args:
            request: Verification request with code and problem slug

        Returns:
            VerificationResult with detailed test results
        """
        start_time = time.time()

        try:
            # Get test code from curriculum or use provided test code
            test_code = await self._get_test_code(request)
            if not test_code:
                return self._create_error_result(
                    "No test code found for this problem",
                    execution_time_ms=self._get_elapsed_ms(start_time),
                )

            # Validate learner code syntax first
            valid, error = await self.execution_service.validate_syntax(request.code)
            if not valid:
                return self._create_syntax_error_result(
                    error, execution_time_ms=self._get_elapsed_ms(start_time)
                )

            # Combine learner code with test code and run pytest
            combined_code = self._combine_code(request.code, test_code)
            pytest_result = await self._run_pytest(combined_code, request.problem_slug)

            execution_time_ms = self._get_elapsed_ms(start_time)

            return VerificationResult(
                success=pytest_result["success"],
                summary=pytest_result["summary"],
                tests=pytest_result["tests"],
                stdout=pytest_result.get("stdout", ""),
                stderr=pytest_result.get("stderr", ""),
                execution_time_ms=execution_time_ms,
                all_tests_passed=pytest_result["summary"].passed
                == pytest_result["summary"].total
                and pytest_result["summary"].total > 0,
                next_steps=self._generate_next_steps(pytest_result),
            )

        except Exception as e:
            logger.exception("Verification failed")
            return self._create_error_result(
                f"Verification error: {str(e)}",
                execution_time_ms=self._get_elapsed_ms(start_time),
            )

    async def verify_and_update_progress(
        self, request: VerificationRequest, user_id: str | None = None
    ) -> VerificationResponse:
        """Verify solution and update user progress.

        Args:
            request: Verification request
            user_id: Optional user ID for progress tracking

        Returns:
            VerificationResponse with suggestions and progress info
        """
        result = await self.verify_solution(request)

        # Generate hint suggestions based on failures
        suggested_hints = self._suggest_hints(result)

        # Update progress if user is logged in and tests passed
        progress_updated = False
        attempts = None
        if user_id and result.all_tests_passed:
            progress_updated = await self._update_progress(
                user_id, request.problem_slug, result
            )
            attempts = await self._get_attempt_count(user_id, request.problem_slug)

        return VerificationResponse(
            success=result.success,
            summary=result.summary,
            tests=result.tests,
            stdout=result.stdout,
            stderr=result.stderr,
            execution_time_ms=result.execution_time_ms,
            suggested_hints=suggested_hints,
            progress_updated=progress_updated,
            attempts=attempts,
        )

    async def _get_test_code(self, request: VerificationRequest) -> str | None:
        """Get test code from curriculum or request."""
        if request.test_code:
            return request.test_code

        problem_data = self.curriculum_service.get_problem(request.problem_slug)
        if problem_data:
            return problem_data["problem"].test_code

        return None

    def _combine_code(self, learner_code: str, test_code: str) -> str:
        """Combine learner code with test code."""
        return f"""# Learner code
{learner_code}

# Test code
{test_code}
"""

    async def _run_pytest(
        self, combined_code: str, problem_slug: str
    ) -> dict[str, Any]:
        """Run pytest on the combined code and parse results."""
        # Create temporary files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Write learner code
            solution_file = temp_path / "solution.py"
            solution_file.write_text(combined_code, encoding="utf-8")

            # Write pytest.ini
            pytest_ini = temp_path / "pytest.ini"
            pytest_ini.write_text(
                """[pytest]
testpaths = .
python_files = solution.py
""",
                encoding="utf-8",
            )

            # Run pytest with JUnit XML output
            junit_file = temp_path / "results.xml"

            try:
                result = subprocess.run(
                    [
                        "python",
                        "-m",
                        "pytest",
                        str(solution_file),
                        "-v",
                        f"--junitxml={junit_file}",
                        "--tb=short",
                        "-p",
                        "no:cacheprovider",
                        "--capture=tee-sys",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=str(temp_path),
                )

                # Parse JUnit XML if it exists
                if junit_file.exists():
                    return self._parse_junit_xml(junit_file, result)

                # Fallback to parsing stdout
                return self._parse_pytest_output(result)

            except subprocess.TimeoutExpired:
                return {
                    "success": False,
                    "summary": VerificationSummary(
                        total=1, passed=0, failed=0, errors=1, skipped=0
                    ),
                    "tests": [
                        TestResult(
                            name="execution",
                            status=TestStatus.TIMEOUT,
                            message=f"Execution timed out after {self.timeout} seconds",
                            error_category=ErrorCategory.TIMEOUT,
                            hint="Your code took too long to run. Check for infinite loops or very slow operations.",
                        )
                    ],
                    "stdout": "",
                    "stderr": f"Timeout after {self.timeout} seconds",
                }

    def _parse_junit_xml(
        self, junit_file: Path, result: subprocess.CompletedProcess
    ) -> dict[str, Any]:
        """Parse JUnit XML output from pytest."""
        try:
            tree = ET.parse(junit_file)
            root = tree.getroot()

            # Get summary from testsuite element
            testsuite = root if root.tag == "testsuite" else root.find("testsuite")
            if testsuite is None:
                return self._parse_pytest_output(result)

            total = int(testsuite.get("tests", 0))
            failures = int(testsuite.get("failures", 0))
            errors = int(testsuite.get("errors", 0))
            skipped = int(testsuite.get("skipped", 0))
            passed = total - failures - errors - skipped

            summary = VerificationSummary(
                total=total,
                passed=passed,
                failed=failures,
                errors=errors,
                skipped=skipped,
            )

            # Parse individual test cases
            tests = []
            for testcase in testsuite.findall("testcase"):
                test_result = self._parse_testcase(testcase)
                tests.append(test_result)

            return {
                "success": failures == 0 and errors == 0 and passed > 0,
                "summary": summary,
                "tests": tests,
                "stdout": result.stdout,
                "stderr": result.stderr if result.returncode != 0 else "",
            }

        except ET.ParseError as e:
            logger.error(f"Failed to parse JUnit XML: {e}")
            return self._parse_pytest_output(result)

    def _parse_testcase(self, testcase: ET.Element) -> TestResult:
        """Parse a single test case from JUnit XML."""
        name = testcase.get("name", "unknown")
        classname = testcase.get("classname", "")
        time_str = testcase.get("time", "0")
        duration_ms = float(time_str) * 1000

        # Check for failure
        failure = testcase.find("failure")
        if failure is not None:
            message = failure.get("message", "")
            traceback = failure.text or ""
            return self._create_failed_test_result(
                name, message, traceback, duration_ms
            )

        # Check for error
        error = testcase.find("error")
        if error is not None:
            message = error.get("message", "")
            traceback = error.text or ""
            return self._create_error_test_result(name, message, traceback, duration_ms)

        # Check for skipped
        skipped = testcase.find("skipped")
        if skipped is not None:
            return TestResult(
                name=name,
                status=TestStatus.SKIPPED,
                message="Test skipped",
                duration_ms=duration_ms,
            )

        # Passed
        return TestResult(
            name=name,
            status=TestStatus.PASSED,
            duration_ms=duration_ms,
        )

    def _parse_pytest_output(
        self, result: subprocess.CompletedProcess
    ) -> dict[str, Any]:
        """Parse pytest output as fallback when XML parsing fails."""
        stdout = result.stdout
        stderr = result.stderr

        # Try to extract test results from output
        tests = []

        # Pattern for passed tests
        passed_pattern = r"(\S+)::(\S+) PASSED"
        for match in re.finditer(passed_pattern, stdout):
            tests.append(
                TestResult(
                    name=match.group(2),
                    status=TestStatus.PASSED,
                )
            )

        # Pattern for failed tests
        failed_pattern = r"(\S+)::(\S+) FAILED"
        for match in re.finditer(failed_pattern, stdout):
            test_name = match.group(2)
            # Try to find failure details
            failure_info = self._extract_failure_info(stdout, test_name)
            tests.append(
                TestResult(
                    name=test_name,
                    status=TestStatus.FAILED,
                    message=failure_info.get("message"),
                    expected=failure_info.get("expected"),
                    actual=failure_info.get("actual"),
                    error_category=failure_info.get("category"),
                    hint=failure_info.get("hint"),
                )
            )

        # Pattern for errors
        error_pattern = r"(\S+)::(\S+) ERROR"
        for match in re.finditer(error_pattern, stdout):
            tests.append(
                TestResult(
                    name=match.group(2),
                    status=TestStatus.ERROR,
                    message="Test encountered an error during execution",
                )
            )

        # Calculate summary
        total = len(tests)
        passed = sum(1 for t in tests if t.status == TestStatus.PASSED)
        failed = sum(1 for t in tests if t.status == TestStatus.FAILED)
        errors = sum(1 for t in tests if t.status == TestStatus.ERROR)

        summary = VerificationSummary(
            total=total, passed=passed, failed=failed, errors=errors
        )

        return {
            "success": failed == 0 and errors == 0 and passed > 0,
            "summary": summary,
            "tests": tests,
            "stdout": stdout,
            "stderr": stderr if result.returncode != 0 else "",
        }

    def _extract_failure_info(self, stdout: str, test_name: str) -> dict[str, Any]:
        """Extract failure details from pytest output."""
        info = {
            "message": "Test failed",
            "category": ErrorCategory.UNKNOWN_ERROR,
        }

        # Look for assertion failure patterns
        assert_pattern = r"assert\s+(.+?)\s*==\s*(.+)"
        assert_match = re.search(assert_pattern, stdout)
        if assert_match:
            info["actual"] = assert_match.group(1).strip()
            info["expected"] = assert_match.group(2).strip()
            info["category"] = ErrorCategory.WRONG_RETURN_VALUE
            info["hint"] = "Your function returned a different value than expected. Check your logic."

        # Look for exception patterns
        exception_patterns = [
            (r"NotImplementedError", ErrorCategory.MISSING_IMPLEMENTATION),
            (r"SyntaxError", ErrorCategory.SYNTAX_ERROR),
            (r"ImportError", ErrorCategory.IMPORT_ERROR),
            (r"ModuleNotFoundError", ErrorCategory.IMPORT_ERROR),
        ]

        for pattern, category in exception_patterns:
            if pattern in stdout:
                info["category"] = category
                if category == ErrorCategory.MISSING_IMPLEMENTATION:
                    info["hint"] = "You need to implement this function. Remove 'raise NotImplementedError' and add your code."
                elif category == ErrorCategory.SYNTAX_ERROR:
                    info["hint"] = "There's a syntax error in your code. Check for missing colons, parentheses, or quotes."
                elif category == ErrorCategory.IMPORT_ERROR:
                    info["hint"] = "There's an issue with importing modules. Make sure all imports are correct."
                break

        return info

    def _create_failed_test_result(
        self, name: str, message: str, traceback: str, duration_ms: float
    ) -> TestResult:
        """Create a TestResult for a failed test with learner-friendly feedback."""
        category = self._categorize_error(message, traceback)
        hint = self._generate_hint(category, message)
        expected, actual = self._extract_expected_actual(message, traceback)

        return TestResult(
            name=name,
            status=TestStatus.FAILED,
            message=self._clean_message(message),
            expected=expected,
            actual=actual,
            hint=hint,
            error_category=category,
            traceback=traceback if category != ErrorCategory.PASSED else None,
            duration_ms=duration_ms,
        )

    def _create_error_test_result(
        self, name: str, message: str, traceback: str, duration_ms: float
    ) -> TestResult:
        """Create a TestResult for a test with an error."""
        category = self._categorize_error(message, traceback)
        hint = self._generate_hint(category, message)

        return TestResult(
            name=name,
            status=TestStatus.ERROR,
            message=self._clean_message(message),
            hint=hint,
            error_category=category,
            traceback=traceback,
            duration_ms=duration_ms,
        )

    def _categorize_error(self, message: str, traceback: str) -> ErrorCategory:
        """Categorize the type of error from message and traceback."""
        combined = f"{message}\n{traceback}".lower()

        if "notimplementederror" in combined:
            return ErrorCategory.MISSING_IMPLEMENTATION
        if "syntaxerror" in combined:
            return ErrorCategory.SYNTAX_ERROR
        if "importerror" in combined or "modulenotfounderror" in combined:
            return ErrorCategory.IMPORT_ERROR
        if "assertionerror" in combined:
            # Check if it's about return values
            if "==" in message or "!=" in message:
                return ErrorCategory.WRONG_RETURN_VALUE
            return ErrorCategory.ASSERTION_ERROR
        if "timeout" in combined:
            return ErrorCategory.TIMEOUT
        if any(x in combined for x in ["exception", "error", "raise"]):
            return ErrorCategory.UNEXPECTED_EXCEPTION

        return ErrorCategory.UNKNOWN_ERROR

    def _generate_hint(self, category: ErrorCategory, message: str) -> str | None:
        """Generate a learner-friendly hint based on error category."""
        hints = {
            ErrorCategory.WRONG_RETURN_VALUE: "Your function returned a different value than expected. Double-check your logic and calculations.",
            ErrorCategory.UNEXPECTED_EXCEPTION: "Your code raised an unexpected error. Check for edge cases and make sure you're handling all inputs correctly.",
            ErrorCategory.MISSING_IMPLEMENTATION: "You need to implement this function. Remove 'raise NotImplementedError' and write your solution.",
            ErrorCategory.TIMEOUT: "Your code took too long to run. Check for infinite loops or very slow operations.",
            ErrorCategory.SYNTAX_ERROR: "There's a syntax error in your code. Check for missing colons, parentheses, quotes, or incorrect indentation.",
            ErrorCategory.IMPORT_ERROR: "There's an issue with importing modules. Make sure all module names are spelled correctly.",
            ErrorCategory.ASSERTION_ERROR: "An assertion failed. Make sure your code meets all the requirements specified in the problem.",
            ErrorCategory.UNKNOWN_ERROR: "Something unexpected happened. Try running your code locally to debug the issue.",
        }
        return hints.get(category)

    def _extract_expected_actual(
        self, message: str, traceback: str
    ) -> tuple[str | None, str | None]:
        """Extract expected and actual values from error message."""
        # Pattern for assertion failures
        patterns = [
            r"assert\s+(.+?)\s*==\s*(.+?)(?:\n|$)",
            r"expected\s*[:=]?\s*(.+?)\s*but\s+got\s*[:=]?\s*(.+?)(?:\n|$)",
            r"assert\s+.*==\s*(.+?)\s*#\s*expected.*?\n.*?assert\s+(.+?)(?:\n|$)",
        ]

        combined = f"{message}\n{traceback}"
        for pattern in patterns:
            match = re.search(pattern, combined, re.IGNORECASE)
            if match:
                return match.group(2).strip(), match.group(1).strip()

        return None, None

    def _clean_message(self, message: str) -> str:
        """Clean up error message for display."""
        # Remove file paths for security
        cleaned = re.sub(r'File\s+"[^"]+"', 'File "..."', message)
        # Limit length
        if len(cleaned) > 500:
            cleaned = cleaned[:497] + "..."
        return cleaned

    def _generate_next_steps(self, pytest_result: dict[str, Any]) -> list[str]:
        """Generate suggested next steps based on results."""
        steps = []
        summary = pytest_result["summary"]

        if summary.passed == summary.total:
            steps.append("🎉 Great job! All tests passed.")
            steps.append("Consider reviewing your solution for potential improvements.")
            steps.append("Move on to the next problem to continue learning!")
        elif summary.failed > 0:
            steps.append("👀 Review the failed tests above to understand what went wrong.")
            steps.append("Try the suggested hints to fix your solution.")
            if summary.passed > 0:
                steps.append(f"Good news: {summary.passed} test(s) already pass!")
            steps.append("Click 'Get Help' if you need more guidance.")
        elif summary.errors > 0:
            steps.append("⚠️ Your code has errors that prevented tests from running.")
            steps.append("Check the error messages and fix any syntax or runtime issues.")

        return steps

    def _suggest_hints(self, result: VerificationResult) -> list[HintSuggestion]:
        """Suggest hints based on test failures."""
        suggestions = []

        # Count error categories
        categories = {}
        for test in result.tests:
            if test.status != TestStatus.PASSED and test.error_category:
                categories[test.error_category] = categories.get(test.error_category, 0) + 1

        # Suggest hints based on most common error types
        if ErrorCategory.MISSING_IMPLEMENTATION in categories:
            suggestions.append(
                HintSuggestion(
                    hint_index=0,
                    reason="You haven't implemented the function yet",
                    confidence="high",
                )
            )

        if ErrorCategory.WRONG_RETURN_VALUE in categories:
            suggestions.append(
                HintSuggestion(
                    hint_index=0,
                    reason="Your return values don't match expected results",
                    confidence="high",
                )
            )

        if ErrorCategory.SYNTAX_ERROR in categories:
            suggestions.append(
                HintSuggestion(
                    hint_index=0,
                    reason="There are syntax errors in your code",
                    confidence="high",
                )
            )

        if ErrorCategory.UNEXPECTED_EXCEPTION in categories:
            suggestions.append(
                HintSuggestion(
                    hint_index=1,
                    reason="Your code raises unexpected exceptions",
                    confidence="medium",
                )
            )

        # If many tests fail, suggest structural hint
        if result.summary.failed > result.summary.total // 2:
            suggestions.append(
                HintSuggestion(
                    hint_index=1,
                    reason="Multiple tests are failing - consider reviewing the problem structure",
                    confidence="medium",
                )
            )

        # If edge cases fail, suggest hint 2
        edge_case_failures = sum(
            1
            for t in result.tests
            if t.status != TestStatus.PASSED
            and any(x in t.name.lower() for x in ["edge", "empty", "none", "negative", "zero"])
        )
        if edge_case_failures > 0:
            suggestions.append(
                HintSuggestion(
                    hint_index=2,
                    reason="Some edge case tests are failing",
                    confidence="high",
                )
            )

        return suggestions

    async def _update_progress(
        self, user_id: str, problem_slug: str, result: VerificationResult
    ) -> bool:
        """Update user progress after verification."""
        # This would integrate with the progress service
        # For now, just return True if all tests passed
        return result.all_tests_passed

    async def _get_attempt_count(self, user_id: str, problem_slug: str) -> int | None:
        """Get the current attempt count for a user and problem."""
        # This would query the database
        return None

    def _create_error_result(
        self, message: str, execution_time_ms: float
    ) -> VerificationResult:
        """Create an error result."""
        return VerificationResult(
            success=False,
            summary=VerificationSummary(total=0, passed=0, failed=0, errors=1),
            tests=[],
            stdout="",
            stderr=message,
            execution_time_ms=execution_time_ms,
            all_tests_passed=False,
            next_steps=["Check your code and try again."],
        )

    def _create_syntax_error_result(
        self, error: str, execution_time_ms: float
    ) -> VerificationResult:
        """Create a result for syntax errors."""
        return VerificationResult(
            success=False,
            summary=VerificationSummary(total=0, passed=0, failed=0, errors=1),
            tests=[
                TestResult(
                    name="syntax_check",
                    status=TestStatus.ERROR,
                    message=error,
                    error_category=ErrorCategory.SYNTAX_ERROR,
                    hint="Fix the syntax error before running tests. Check for missing colons, parentheses, or quotes.",
                )
            ],
            stdout="",
            stderr=error,
            execution_time_ms=execution_time_ms,
            all_tests_passed=False,
            next_steps=[
                "Fix the syntax error in your code.",
                "Common issues: missing colons after if/for/def, unmatched parentheses, or incorrect indentation.",
            ],
        )

    def _get_elapsed_ms(self, start_time: float) -> float:
        """Get elapsed time in milliseconds."""
        return round((time.time() - start_time) * 1000, 2)

# Singleton instance
_verification_service: VerificationService | None = None


def get_verification_service() -> VerificationService:
    """Get or create the verification service singleton."""
    global _verification_service
    if _verification_service is None:
        _verification_service = VerificationService()
    return _verification_service
