#!/usr/bin/env python3
"""
Test script for the verification system.
Run this to verify the verification service is working correctly.
"""

import asyncio
import sys
from pathlib import Path

# Add the API path
sys.path.insert(0, str(Path(__file__).parent / "apps" / "api"))

from api.schemas.verification import VerificationRequest
from api.services.verification import VerificationService


async def test_case_1_all_pass():
    """Test case: All tests pass."""
    print("\n" + "="*60)
    print("Test Case 1: All tests pass")
    print("="*60)
    
    service = VerificationService()
    request = VerificationRequest(
        code="""def add(a, b):
    return a + b
""",
        problem_slug="test",
        test_code="""def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -4) == -5

def test_add_zero():
    assert add(0, 0) == 0
""",
    )
    
    result = await service.verify_solution(request)
    
    print(f"Success: {result.success}")
    print(f"All passed: {result.all_tests_passed}")
    print(f"Summary: {result.summary.passed}/{result.summary.total} passed")
    print(f"Execution time: {result.execution_time_ms}ms")
    print("\nTest results:")
    for test in result.tests:
        status_icon = "✅" if test.status == "passed" else "❌"
        print(f"  {status_icon} {test.name}: {test.status}")
    
    print("\nNext steps:")
    for step in result.next_steps:
        print(f"  • {step}")
    
    assert result.success is True
    assert result.all_tests_passed is True
    assert result.summary.passed == 3
    print("\n✓ Test case 1 PASSED")


async def test_case_2_wrong_return():
    """Test case: Wrong return value."""
    print("\n" + "="*60)
    print("Test Case 2: Wrong return value")
    print("="*60)
    
    service = VerificationService()
    request = VerificationRequest(
        code="""def add(a, b):
    return a - b  # Wrong operation
""",
        problem_slug="test",
        test_code="""def test_add_positive():
    assert add(2, 3) == 5
""",
    )
    
    result = await service.verify_solution(request)
    
    print(f"Success: {result.success}")
    print(f"All passed: {result.all_tests_passed}")
    print(f"Summary: {result.summary.passed}/{result.summary.total} passed")
    
    print("\nTest results:")
    for test in result.tests:
        status_icon = "✅" if test.status == "passed" else "❌"
        print(f"  {status_icon} {test.name}: {test.status}")
        if test.hint:
            print(f"     Hint: {test.hint}")
        if test.expected:
            print(f"     Expected: {test.expected}")
        if test.actual:
            print(f"     Actual: {test.actual}")
    
    assert result.success is False
    assert result.all_tests_passed is False
    assert result.summary.failed == 1
    print("\n✓ Test case 2 PASSED")


async def test_case_3_not_implemented():
    """Test case: Not implemented."""
    print("\n" + "="*60)
    print("Test Case 3: Not implemented")
    print("="*60)
    
    service = VerificationService()
    request = VerificationRequest(
        code="""def add(a, b):
    raise NotImplementedError("TODO: implement this function")
""",
        problem_slug="test",
        test_code="""def test_add():
    assert add(2, 3) == 5
""",
    )
    
    result = await service.verify_solution(request)
    
    print(f"Success: {result.success}")
    print(f"Summary: {result.summary}")
    
    print("\nTest results:")
    for test in result.tests:
        print(f"  {test.name}: {test.status}")
        if test.error_category:
            print(f"     Category: {test.error_category}")
        if test.hint:
            print(f"     Hint: {test.hint}")
    
    assert result.success is False
    print("\n✓ Test case 3 PASSED")


async def test_case_4_syntax_error():
    """Test case: Syntax error."""
    print("\n" + "="*60)
    print("Test Case 4: Syntax error")
    print("="*60)
    
    service = VerificationService()
    request = VerificationRequest(
        code="""def add(a, b)  # Missing colon
    return a + b
""",
        problem_slug="test",
        test_code="",
    )
    
    result = await service.verify_solution(request)
    
    print(f"Success: {result.success}")
    print(f"Summary: {result.summary}")
    print(f"Stderr: {result.stderr[:100]}...")
    
    assert result.success is False
    print("\n✓ Test case 4 PASSED")


async def main():
    """Run all test cases."""
    print("\n" + "="*60)
    print("VERIFICATION SYSTEM TEST SUITE")
    print("="*60)
    
    try:
        await test_case_1_all_pass()
        await test_case_2_wrong_return()
        await test_case_3_not_implemented()
        await test_case_4_syntax_error()
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED! ✅")
        print("="*60)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
