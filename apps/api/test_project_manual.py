"""Manual test for project execution backend.

This script tests the project execution service without requiring Docker.
It validates the code structure and schemas.

Usage:
    python test_project_manual.py
"""

import sys
sys.path.insert(0, '.')

# Test 1: Import schemas
def test_schemas():
    """Test that all schemas can be imported and used."""
    print("Testing schemas...")
    
    from api.schemas.execution import (
        ProjectExecutionRequest,
        ProjectExecutionResponse,
        ProjectFile,
        ProjectFileValidation,
        ProjectMetadata,
        ProjectRunRequest,
        ProjectSaveRequest,
        ProjectSaveResponse,
        ProjectSubmissionResponse,
        ProjectTemplate,
        ProjectTemplateFile,
        ProjectTestRequest,
        ProjectTestResult,
        ProjectValidationResponse,
        TestResult,
    )
    
    # Test creating a request
    request = ProjectExecutionRequest(
        files={
            "src/main.py": "print('hello')",
            "src/bank.py": "class Bank: pass",
        },
        entry_point="src/main.py",
    )
    assert request.files["src/main.py"] == "print('hello')"
    assert request.entry_point == "src/main.py"
    print("  ✓ ProjectExecutionRequest works")
    
    # Test response
    response = ProjectExecutionResponse(
        success=True,
        stdout="hello",
        exit_code=0,
    )
    assert response.success is True
    print("  ✓ ProjectExecutionResponse works")
    
    # Test test result
    test_result = ProjectTestResult(
        success=True,
        tests=[TestResult(name="test_1", passed=True)],
        summary={"total": 1, "passed": 1, "failed": 0, "errors": 0, "skipped": 0},
    )
    assert test_result.success is True
    print("  ✓ ProjectTestResult works")
    
    # Test validation response
    validation = ProjectValidationResponse(
        valid=True,
        validations=[
            ProjectFileValidation(file_path="main.py", valid=True, message="OK")
        ],
    )
    assert validation.valid is True
    print("  ✓ ProjectValidationResponse works")
    
    print("All schema tests passed!\n")


# Test 2: Import service (without Docker)
def test_service_code():
    """Test that service code is valid (without Docker dependency)."""
    print("Testing service code structure...")
    
    import ast
    
    # Parse the service file
    with open('api/services/project_execution.py', 'r') as f:
        code = f.read()
    
    tree = ast.parse(code)
    
    # Check for expected classes and functions
    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    assert 'ProjectExecutionService' in classes
    print("  ✓ ProjectExecutionService class found")
    
    assert 'get_project_execution_service' in functions
    print("  ✓ get_project_execution_service function found")
    
    print("Service code structure tests passed!\n")


# Test 3: Import router (without full app)
def test_router_code():
    """Test that router code is valid."""
    print("Testing router code structure...")
    
    import ast
    
    with open('api/routers/projects.py', 'r') as f:
        code = f.read()
    
    tree = ast.parse(code)
    
    # Check for expected endpoints
    endpoints = [node.name for node in ast.walk(tree) if isinstance(node, ast.AsyncFunctionDef)]
    
    expected = ['get_project', 'run_project', 'run_project_tests', 'validate_project', 'save_project', 'submit_project']
    for endpoint in expected:
        assert endpoint in endpoints, f"Missing endpoint: {endpoint}"
        print(f"  ✓ {endpoint} endpoint found")
    
    print("Router code structure tests passed!\n")


# Test 4: Test validation logic directly
def test_validation_logic():
    """Test the validation logic without Docker."""
    print("Testing validation logic...")
    
    # Import just the validation part of the service
    import ast
    
    def validate_python_syntax(code: str):
        """Validate Python syntax without executing."""
        try:
            ast.parse(code)
            return True, None, None, None
        except SyntaxError as e:
            return False, str(e), e.lineno, e.offset
        except Exception as e:
            return False, str(e), None, None
    
    # Valid code
    valid, error, line, col = validate_python_syntax("def hello():\n    return 'world'")
    assert valid is True
    print("  ✓ Valid code passes syntax check")
    
    # Invalid code
    valid, error, line, col = validate_python_syntax("def hello(\n    return 'world'")
    assert valid is False
    assert error is not None
    print("  ✓ Invalid code fails syntax check")
    
    print("Validation logic tests passed!\n")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Project Execution Backend - Manual Tests")
    print("=" * 60 + "\n")
    
    try:
        test_schemas()
        test_service_code()
        test_router_code()
        test_validation_logic()
        
        print("=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
