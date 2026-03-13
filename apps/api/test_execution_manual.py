"""Manual test script for code execution system."""

import asyncio
import json
import sys

from api.schemas.execution import CodeExecutionRequest, CodeValidationExecutionRequest
from api.services.execution import get_execution_service
from api.services.docker_runner import get_docker_runner


async def test_docker_available():
    """Test if Docker is available."""
    print("=" * 60)
    print("TEST 1: Docker Availability")
    print("=" * 60)
    
    runner = get_docker_runner()
    health = runner.health_check()
    
    print(f"Docker available: {health['docker_available']}")
    print(f"Image available: {health['image_available']}")
    print(f"Can run containers: {health['can_run_containers']}")
    
    if health['error']:
        print(f"Error: {health['error']}")
    
    return health['docker_available'] and health['image_available']


async def test_simple_execution():
    """Test simple code execution."""
    print("\n" + "=" * 60)
    print("TEST 2: Simple Code Execution")
    print("=" * 60)
    
    service = get_execution_service()
    
    test_cases = [
        ("Hello World", "print('Hello, World!')"),
        ("Math", "print(2 + 2)"),
        ("Variables", "x = 10\nprint(f'x = {x}')"),
    ]
    
    for name, code in test_cases:
        print(f"\n{name}:")
        print(f"  Code: {code[:50]}...")
        
        request = CodeExecutionRequest(code=code, timeout=10)
        result = await service.execute(request)
        
        print(f"  Success: {result.success}")
        print(f"  Output: {result.output[:100]}")
        print(f"  Duration: {result.execution_time_ms}ms")
        
        if not result.success:
            print(f"  Error: {result.error}")


async def test_timeout():
    """Test timeout handling."""
    print("\n" + "=" * 60)
    print("TEST 3: Timeout Handling")
    print("=" * 60)
    
    service = get_execution_service()
    
    code = "import time; time.sleep(20)"
    print(f"Code: {code}")
    print("Timeout: 3 seconds")
    
    request = CodeExecutionRequest(code=code, timeout=3)
    result = await service.execute(request)
    
    print(f"Success: {result.success}")
    print(f"Timeout: {result.timeout}")
    print(f"Error: {result.error}")


async def test_syntax_error():
    """Test syntax error handling."""
    print("\n" + "=" * 60)
    print("TEST 4: Syntax Error Handling")
    print("=" * 60)
    
    service = get_execution_service()
    
    code = "print('hello"  # Missing closing quote
    print(f"Code: {code}")
    
    request = CodeExecutionRequest(code=code, timeout=10)
    result = await service.execute(request)
    
    print(f"Success: {result.success}")
    print(f"Error: {result.error}")


async def test_security_network():
    """Test network access is blocked."""
    print("\n" + "=" * 60)
    print("TEST 5: Security - Network Access")
    print("=" * 60)
    
    service = get_execution_service()
    
    code = "import urllib.request; urllib.request.urlopen('http://example.com')"
    print(f"Code: {code}")
    
    request = CodeExecutionRequest(code=code, timeout=10)
    result = await service.execute(request)
    
    print(f"Success: {result.success}")
    print(f"Error: {result.error}")
    
    if not result.success:
        print("✓ Network access correctly blocked")


async def test_security_filesystem():
    """Test filesystem access is restricted."""
    print("\n" + "=" * 60)
    print("TEST 6: Security - Filesystem Access")
    print("=" * 60)
    
    service = get_execution_service()
    
    code = "open('/etc/passwd').read()"
    print(f"Code: {code}")
    
    request = CodeExecutionRequest(code=code, timeout=10)
    result = await service.execute(request)
    
    print(f"Success: {result.success}")
    print(f"Error: {result.error}")
    
    if not result.success:
        print("✓ Filesystem access correctly restricted")


async def test_memory_limit():
    """Test memory limit enforcement."""
    print("\n" + "=" * 60)
    print("TEST 7: Memory Limit")
    print("=" * 60)
    
    service = get_execution_service()
    
    # Try to allocate a large list
    code = "big_list = [0] * 100_000_000"  # ~800MB
    print(f"Code: {code}")
    print("Expected: Should hit 256MB memory limit")
    
    request = CodeExecutionRequest(code=code, timeout=10)
    result = await service.execute(request)
    
    print(f"Success: {result.success}")
    print(f"Error: {result.error}")


async def test_validation():
    """Test code validation with tests."""
    print("\n" + "=" * 60)
    print("TEST 8: Code Validation with Tests")
    print("=" * 60)
    
    service = get_execution_service()
    
    code = """
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
"""
    test_code = """
# Run tests
assert add(2, 3) == 5, "add(2, 3) should be 5"
assert add(-1, 1) == 0, "add(-1, 1) should be 0"
assert multiply(3, 4) == 12, "multiply(3, 4) should be 12"
print("All tests passed!")
"""
    
    print("User code:")
    print(code)
    print("Test code:")
    print(test_code)
    
    request = CodeValidationExecutionRequest(
        code=code,
        test_code=test_code,
        timeout=10
    )
    result = await service.validate_and_test(request)
    
    print(f"Success: {result.success}")
    print(f"Passed: {result.passed}")
    print(f"Tests run: {result.tests_run}")
    print(f"Tests passed: {result.tests_passed}")
    print(f"Tests failed: {result.tests_failed}")
    print(f"Output: {result.stdout}")
    if result.stderr:
        print(f"Stderr: {result.stderr}")


async def test_metrics():
    """Test metrics collection."""
    print("\n" + "=" * 60)
    print("TEST 9: Metrics Collection")
    print("=" * 60)
    
    service = get_execution_service()
    
    metrics = await service.get_metrics(hours=24)
    
    print(f"Total executions: {metrics.total_executions}")
    print(f"Successful: {metrics.successful_executions}")
    print(f"Failed: {metrics.failed_executions}")
    print(f"Timeouts: {metrics.timeout_executions}")
    print(f"Average duration: {metrics.average_execution_time_ms}ms")
    print(f"Failure rate: {metrics.failure_rate}%")


async def test_rate_limiting():
    """Test rate limiting."""
    print("\n" + "=" * 60)
    print("TEST 10: Rate Limiting")
    print("=" * 60)
    
    service = get_execution_service()
    
    # Check initial rate limit
    allowed, count, limit = await service.check_rate_limit("test-user", "127.0.0.1")
    print(f"Initial state: allowed={allowed}, count={count}, limit={limit}")
    
    # Simulate some executions
    for i in range(5):
        request = CodeExecutionRequest(code=f"print({i})")
        await service.execute(request, user_id="test-user")
    
    # Check rate limit again
    allowed, count, limit = await service.check_rate_limit("test-user", None)
    print(f"After 5 executions: allowed={allowed}, count={count}, limit={limit}")


async def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("CODE EXECUTION SYSTEM TESTS")
    print("=" * 60)
    
    # Check Docker first
    docker_ready = await test_docker_available()
    
    if not docker_ready:
        print("\n❌ Docker is not available. Please:")
        print("   1. Ensure Docker is running")
        print("   2. Build the sandbox image:")
        print("      docker build -f sandbox.Dockerfile -t oop-journey-sandbox:latest .")
        return
    
    # Run all tests
    try:
        await test_simple_execution()
    except Exception as e:
        print(f"Error in simple execution: {e}")
    
    try:
        await test_timeout()
    except Exception as e:
        print(f"Error in timeout test: {e}")
    
    try:
        await test_syntax_error()
    except Exception as e:
        print(f"Error in syntax error test: {e}")
    
    try:
        await test_security_network()
    except Exception as e:
        print(f"Error in network security test: {e}")
    
    try:
        await test_security_filesystem()
    except Exception as e:
        print(f"Error in filesystem security test: {e}")
    
    try:
        await test_memory_limit()
    except Exception as e:
        print(f"Error in memory limit test: {e}")
    
    try:
        await test_validation()
    except Exception as e:
        print(f"Error in validation test: {e}")
    
    try:
        await test_metrics()
    except Exception as e:
        print(f"Error in metrics test: {e}")
    
    try:
        await test_rate_limiting()
    except Exception as e:
        print(f"Error in rate limiting test: {e}")
    
    print("\n" + "=" * 60)
    print("TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
