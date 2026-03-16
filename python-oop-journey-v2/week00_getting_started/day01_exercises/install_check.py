"""Installation Check Script for Python Setup.

This script verifies that Python is installed correctly and can run basic code.
Run this after installing Python to confirm everything is working.

Usage:
    Windows: python install_check.py
    Mac/Linux: python3 install_check.py
"""

from __future__ import annotations

import sys


def check_python_version() -> bool:
    """Check if Python version is 3.8 or higher."""
    version_info = sys.version_info
    print(f"Python version: {version_info.major}.{version_info.minor}.{version_info.micro}")
    
    if version_info.major == 3 and version_info.minor >= 8:
        print("✓ Python version is 3.8 or higher - GOOD!")
        return True
    else:
        print("✗ Python version should be 3.8 or higher")
        print("  Please download the latest version from python.org")
        return False


def check_basic_operations() -> bool:
    """Test basic Python operations."""
    print("\nTesting basic operations...")
    
    try:
        # Test arithmetic
        result = 2 + 2
        assert result == 4, f"Expected 4, got {result}"
        print("✓ Arithmetic works")
        
        # Test variables
        message = "Hello, Python!"
        assert message == "Hello, Python!"
        print("✓ Variables work")
        
        # Test print function
        print("✓ Print function works")
        
        return True
    except Exception as e:
        print(f"✗ Basic operations failed: {e}")
        return False


def check_string_operations() -> bool:
    """Test basic string operations."""
    print("\nTesting string operations...")
    
    try:
        # Test string creation
        name = "Python"
        assert name == "Python"
        
        # Test string concatenation
        greeting = "Hello, " + name + "!"
        assert greeting == "Hello, Python!"
        print("✓ String operations work")
        
        # Test f-strings (Python 3.6+)
        version = 3
        f_string = f"Python {version}"
        assert f_string == "Python 3"
        print("✓ F-strings work")
        
        return True
    except Exception as e:
        print(f"✗ String operations failed: {e}")
        return False


def check_list_operations() -> bool:
    """Test basic list operations."""
    print("\nTesting list operations...")
    
    try:
        # Test list creation
        numbers = [1, 2, 3, 4, 5]
        assert len(numbers) == 5
        print("✓ List creation works")
        
        # Test list access
        first = numbers[0]
        assert first == 1
        print("✓ List indexing works")
        
        # Test list append
        numbers.append(6)
        assert numbers[-1] == 6
        print("✓ List append works")
        
        return True
    except Exception as e:
        print(f"✗ List operations failed: {e}")
        return False


def main() -> int:
    """Run all installation checks.
    
    Returns:
        0 if all checks pass, 1 otherwise.
    """
    print("=" * 50)
    print("PYTHON INSTALLATION CHECK")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Basic Operations", check_basic_operations),
        ("String Operations", check_string_operations),
        ("List Operations", check_list_operations),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"\n✗ {name} check crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print("🎉 ALL CHECKS PASSED!")
        print(f"   {passed}/{total} tests passed")
        print("\nYour Python installation is working correctly.")
        print("You're ready for Day 02: Setting Up Your Environment!")
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED")
        print(f"   {passed}/{total} tests passed")
        print("\nPlease review the errors above and:")
        print("1. Make sure Python is installed correctly")
        print("2. Try reinstalling from python.org")
        print("3. Check that you're using Python 3.8 or higher")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
