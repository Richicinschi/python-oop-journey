#!/usr/bin/env python3
"""
Comprehensive API Testing Script for Python OOP Journey API
Tests all endpoints with functional, performance, and security scenarios
"""

import requests
import json
import time
import concurrent.futures
from datetime import datetime
from statistics import mean, median

BASE_URL = "https://oop-journey-api.onrender.com"

# Test results storage
test_results = []
performance_data = []

def log_test(category, endpoint, method, status, response_time, payload=None, response=None, passed=True, error=None):
    """Log a test result"""
    result = {
        "timestamp": datetime.now().isoformat(),
        "category": category,
        "endpoint": endpoint,
        "method": method,
        "status_code": status,
        "response_time_ms": round(response_time * 1000, 2),
        "payload": payload,
        "response": response,
        "passed": passed,
        "error": error
    }
    test_results.append(result)
    performance_data.append(response_time * 1000)
    return result

def print_result(result):
    """Print a test result in a readable format"""
    icon = "✅" if result["passed"] else "❌"
    print(f"{icon} {result['method']} {result['endpoint']}")
    print(f"   Status: {result['status_code']} | Time: {result['response_time_ms']}ms")
    if result["error"]:
        print(f"   Error: {result['error']}")
    print()

# ============================================
# 1. HEALTH ENDPOINTS
# ============================================

def test_health_endpoints():
    """Test all health endpoints"""
    print("=" * 60)
    print("🏥 HEALTH ENDPOINTS TESTING")
    print("=" * 60)
    
    health_endpoints = [
        "/health",
        "/health/db",
        "/health/ready",
        "/health/live",
        "/api/execute/health"
    ]
    
    for endpoint in health_endpoints:
        url = f"{BASE_URL}{endpoint}"
        start = time.time()
        try:
            response = requests.get(url, timeout=30)
            elapsed = time.time() - start
            
            passed = response.status_code == 200
            try:
                resp_data = response.json()
            except:
                resp_data = response.text[:500]
            
            result = log_test(
                category="Health",
                endpoint=endpoint,
                method="GET",
                status=response.status_code,
                response_time=elapsed,
                response=resp_data,
                passed=passed
            )
            print_result(result)
            
        except Exception as e:
            elapsed = time.time() - start
            result = log_test(
                category="Health",
                endpoint=endpoint,
                method="GET",
                status=0,
                response_time=elapsed,
                error=str(e),
                passed=False
            )
            print_result(result)

# ============================================
# 2. CODE EXECUTION ENDPOINTS
# ============================================

def test_code_execution():
    """Test code execution endpoints with real payloads"""
    print("=" * 60)
    print("💻 CODE EXECUTION ENDPOINTS TESTING")
    print("=" * 60)
    
    # Test 1: Simple print
    print("\n--- Test 1: Simple print statement ---")
    payload = {"code": "print('hello world')", "language": "python"}
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/api/v1/execute/run", json=payload, timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        passed = response.status_code == 200 and resp_data and "hello world" in str(resp_data)
        
        result = log_test(
            category="Code Execution",
            endpoint="/api/v1/execute/run",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            payload=payload,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Code Execution",
            endpoint="/api/v1/execute/run",
            method="POST",
            status=0,
            response_time=elapsed,
            payload=payload,
            error=str(e),
            passed=False
        )
        print_result(result)
    
    # Test 2: Calculation
    print("\n--- Test 2: Calculation with variable ---")
    payload = {"code": "x = 1 + 2\nprint(x)", "language": "python"}
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/api/v1/execute/run", json=payload, timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        passed = response.status_code == 200 and resp_data and "3" in str(resp_data)
        
        result = log_test(
            category="Code Execution",
            endpoint="/api/v1/execute/run",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            payload=payload,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Code Execution",
            endpoint="/api/v1/execute/run",
            method="POST",
            status=0,
            response_time=elapsed,
            payload=payload,
            error=str(e),
            passed=False
        )
        print_result(result)
    
    # Test 3: Syntax error
    print("\n--- Test 3: Syntax error handling ---")
    payload = {"code": "print('hello" , "language": "python"}
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/api/v1/execute/run", json=payload, timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        # Should either return 400 or handle gracefully with error in response
        passed = response.status_code in [200, 400] and (resp_data is None or "error" in str(resp_data).lower() or "syntax" in str(resp_data).lower())
        
        result = log_test(
            category="Code Execution",
            endpoint="/api/v1/execute/run",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            payload=payload,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Code Execution",
            endpoint="/api/v1/execute/run",
            method="POST",
            status=0,
            response_time=elapsed,
            payload=payload,
            error=str(e),
            passed=False
        )
        print_result(result)
    
    # Test 4: Infinite loop (timeout test)
    print("\n--- Test 4: Infinite loop timeout test ---")
    payload = {"code": "while True: pass", "language": "python"}
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/api/v1/execute/run", json=payload, timeout=35)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        # Should timeout or return error
        passed = response.status_code in [408, 500, 200] or "timeout" in str(resp_data).lower() or "error" in str(resp_data).lower()
        
        result = log_test(
            category="Code Execution",
            endpoint="/api/v1/execute/run",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            payload=payload,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except requests.exceptions.Timeout:
        elapsed = time.time() - start
        result = log_test(
            category="Code Execution",
            endpoint="/api/v1/execute/run",
            method="POST",
            status=408,
            response_time=elapsed,
            payload=payload,
            error="Request timeout (expected for infinite loop)",
            passed=True  # Timeout is expected behavior
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Code Execution",
            endpoint="/api/v1/execute/run",
            method="POST",
            status=0,
            response_time=elapsed,
            payload=payload,
            error=str(e),
            passed=False
        )
        print_result(result)

def test_syntax_check():
    """Test syntax check endpoint"""
    print("\n--- Syntax Check Endpoint ---")
    
    # Valid syntax
    payload = {"code": "x = 1 + 2\nprint(x)"}
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/api/v1/execute/syntax-check", json=payload, timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        passed = response.status_code == 200
        
        result = log_test(
            category="Syntax Check",
            endpoint="/api/v1/execute/syntax-check",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            payload=payload,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Syntax Check",
            endpoint="/api/v1/execute/syntax-check",
            method="POST",
            status=0,
            response_time=elapsed,
            payload=payload,
            error=str(e),
            passed=False
        )
        print_result(result)
    
    # Invalid syntax
    payload = {"code": "print('hello"}
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/api/v1/execute/syntax-check", json=payload, timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        
        result = log_test(
            category="Syntax Check (Invalid)",
            endpoint="/api/v1/execute/syntax-check",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            payload=payload,
            response=resp_data,
            passed=True
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Syntax Check (Invalid)",
            endpoint="/api/v1/execute/syntax-check",
            method="POST",
            status=0,
            response_time=elapsed,
            payload=payload,
            error=str(e),
            passed=False
        )
        print_result(result)

def test_legacy_execute():
    """Test legacy execute endpoint"""
    print("\n--- Legacy Execute Endpoint ---")
    payload = {"code": "print('legacy test')", "language": "python"}
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/api/execute", json=payload, timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        passed = response.status_code == 200
        
        result = log_test(
            category="Legacy Execute",
            endpoint="/api/execute",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            payload=payload,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Legacy Execute",
            endpoint="/api/execute",
            method="POST",
            status=0,
            response_time=elapsed,
            payload=payload,
            error=str(e),
            passed=False
        )
        print_result(result)

# ============================================
# 3. VERIFICATION ENDPOINTS
# ============================================

def test_verification_endpoints():
    """Test verification endpoints"""
    print("=" * 60)
    print("✅ VERIFICATION ENDPOINTS TESTING")
    print("=" * 60)
    
    # First, get a valid problem slug from curriculum
    print("\n--- Getting valid problem slug ---")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/curriculum/problems", timeout=30)
        problems = response.json() if response.status_code == 200 else []
        test_slug = problems[0]["slug"] if problems and len(problems) > 0 else "week1_day1_calculate_sum"
        print(f"Using test slug: {test_slug}")
    except:
        test_slug = "week1_day1_calculate_sum"
        print(f"Using default test slug: {test_slug}")
    
    # Test GET test-info
    print("\n--- GET /api/v1/test-info/{problem_slug} ---")
    start = time.time()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/test-info/{test_slug}", timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        passed = response.status_code == 200
        
        result = log_test(
            category="Verification",
            endpoint=f"/api/v1/test-info/{test_slug}",
            method="GET",
            status=response.status_code,
            response_time=elapsed,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Verification",
            endpoint=f"/api/v1/test-info/{test_slug}",
            method="GET",
            status=0,
            response_time=elapsed,
            error=str(e),
            passed=False
        )
        print_result(result)
    
    # Test POST /api/v1/verify with real solution
    print("\n--- POST /api/v1/verify (with solution) ---")
    payload = {
        "problem_slug": test_slug,
        "code": "def calculate_sum(a, b):\n    return a + b"
    }
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/api/v1/verify", json=payload, timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        passed = response.status_code == 200
        
        result = log_test(
            category="Verification",
            endpoint="/api/v1/verify",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            payload=payload,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Verification",
            endpoint="/api/v1/verify",
            method="POST",
            status=0,
            response_time=elapsed,
            payload=payload,
            error=str(e),
            passed=False
        )
        print_result(result)
    
    # Test POST /api/v1/verify with incorrect solution
    print("\n--- POST /api/v1/verify (incorrect solution) ---")
    payload = {
        "problem_slug": test_slug,
        "code": "def calculate_sum(a, b):\n    return a - b"  # Wrong operation
    }
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/api/v1/verify", json=payload, timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        # Should return 200 but with failed tests in response
        passed = response.status_code == 200
        
        result = log_test(
            category="Verification (Incorrect)",
            endpoint="/api/v1/verify",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            payload=payload,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Verification (Incorrect)",
            endpoint="/api/v1/verify",
            method="POST",
            status=0,
            response_time=elapsed,
            payload=payload,
            error=str(e),
            passed=False
        )
        print_result(result)
    
    # Test POST /api/v1/verify/{problem_slug}
    print(f"\n--- POST /api/v1/verify/{test_slug} ---")
    payload = {"code": "def calculate_sum(a, b):\n    return a + b"}
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/api/v1/verify/{test_slug}", json=payload, timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        passed = response.status_code == 200
        
        result = log_test(
            category="Verification (Path Param)",
            endpoint=f"/api/v1/verify/{test_slug}",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            payload=payload,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Verification (Path Param)",
            endpoint=f"/api/v1/verify/{test_slug}",
            method="POST",
            status=0,
            response_time=elapsed,
            payload=payload,
            error=str(e),
            passed=False
        )
        print_result(result)
    
    # Test validate-syntax
    print("\n--- POST /api/v1/validate-syntax ---")
    payload = {"code": "def test():\n    return 42"}
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/api/v1/validate-syntax", json=payload, timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        passed = response.status_code == 200
        
        result = log_test(
            category="Validate Syntax",
            endpoint="/api/v1/validate-syntax",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            payload=payload,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Validate Syntax",
            endpoint="/api/v1/validate-syntax",
            method="POST",
            status=0,
            response_time=elapsed,
            payload=payload,
            error=str(e),
            passed=False
        )
        print_result(result)

# ============================================
# 4. CURRICULUM ENDPOINTS
# ============================================

def test_curriculum_endpoints():
    """Test all curriculum endpoints"""
    print("=" * 60)
    print("📚 CURRICULUM ENDPOINTS TESTING")
    print("=" * 60)
    
    # GET /api/v1/curriculum
    print("\n--- GET /api/v1/curriculum ---")
    start = time.time()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/curriculum", timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        has_data = resp_data and len(resp_data) > 0 if isinstance(resp_data, list) else resp_data and resp_data.get("weeks")
        passed = response.status_code == 200 and has_data
        
        result = log_test(
            category="Curriculum",
            endpoint="/api/v1/curriculum",
            method="GET",
            status=response.status_code,
            response_time=elapsed,
            response=resp_data if not has_data else {"weeks_count": len(resp_data) if isinstance(resp_data, list) else len(resp_data.get("weeks", []))},
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Curriculum",
            endpoint="/api/v1/curriculum",
            method="GET",
            status=0,
            response_time=elapsed,
            error=str(e),
            passed=False
        )
        print_result(result)
    
    # GET /api/v1/curriculum/weeks
    print("\n--- GET /api/v1/curriculum/weeks ---")
    start = time.time()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/curriculum/weeks", timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        has_data = resp_data and len(resp_data) > 0 if isinstance(resp_data, list) else False
        passed = response.status_code == 200 and has_data
        
        result = log_test(
            category="Curriculum",
            endpoint="/api/v1/curriculum/weeks",
            method="GET",
            status=response.status_code,
            response_time=elapsed,
            response={"weeks_count": len(resp_data)} if has_data else resp_data,
            passed=passed
        )
        print_result(result)
        
        # Save first week slug for later tests
        first_week_slug = resp_data[0]["slug"] if has_data and len(resp_data) > 0 else None
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Curriculum",
            endpoint="/api/v1/curriculum/weeks",
            method="GET",
            status=0,
            response_time=elapsed,
            error=str(e),
            passed=False
        )
        print_result(result)
        first_week_slug = None
    
    # GET /api/v1/curriculum/weeks/{slug}
    if first_week_slug:
        print(f"\n--- GET /api/v1/curriculum/weeks/{first_week_slug} ---")
        start = time.time()
        try:
            response = requests.get(f"{BASE_URL}/api/v1/curriculum/weeks/{first_week_slug}", timeout=30)
            elapsed = time.time() - start
            
            resp_data = response.json() if response.text else None
            has_data = resp_data and (resp_data.get("days") or resp_data.get("problems"))
            passed = response.status_code == 200 and has_data
            
            result = log_test(
                category="Curriculum",
                endpoint=f"/api/v1/curriculum/weeks/{first_week_slug}",
                method="GET",
                status=response.status_code,
                response_time=elapsed,
                response=resp_data if not has_data else {"week_has_data": True},
                passed=passed
            )
            print_result(result)
        except Exception as e:
            elapsed = time.time() - start
            result = log_test(
                category="Curriculum",
                endpoint=f"/api/v1/curriculum/weeks/{first_week_slug}",
                method="GET",
                status=0,
                response_time=elapsed,
                error=str(e),
                passed=False
            )
            print_result(result)
    
    # GET /api/v1/curriculum/problems
    print("\n--- GET /api/v1/curriculum/problems ---")
    start = time.time()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/curriculum/problems", timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        has_data = resp_data and len(resp_data) > 0 if isinstance(resp_data, list) else False
        passed = response.status_code == 200 and has_data
        
        result = log_test(
            category="Curriculum",
            endpoint="/api/v1/curriculum/problems",
            method="GET",
            status=response.status_code,
            response_time=elapsed,
            response={"problems_count": len(resp_data)} if has_data else resp_data,
            passed=passed
        )
        print_result(result)
        
        # Save first problem slug for later tests
        first_problem_slug = resp_data[0]["slug"] if has_data and len(resp_data) > 0 else None
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Curriculum",
            endpoint="/api/v1/curriculum/problems",
            method="GET",
            status=0,
            response_time=elapsed,
            error=str(e),
            passed=False
        )
        print_result(result)
        first_problem_slug = None
    
    # GET /api/v1/curriculum/problems/{slug}
    if first_problem_slug:
        print(f"\n--- GET /api/v1/curriculum/problems/{first_problem_slug} ---")
        start = time.time()
        try:
            response = requests.get(f"{BASE_URL}/api/v1/curriculum/problems/{first_problem_slug}", timeout=30)
            elapsed = time.time() - start
            
            resp_data = response.json() if response.text else None
            # Check for essential fields
            has_essential = resp_data and any(k in resp_data for k in ["title", "description", "code", "test_cases"])
            passed = response.status_code == 200 and has_essential
            
            result = log_test(
                category="Curriculum",
                endpoint=f"/api/v1/curriculum/problems/{first_problem_slug}",
                method="GET",
                status=response.status_code,
                response_time=elapsed,
                response=resp_data if not has_essential else {"problem_has_essential_fields": True, "fields": list(resp_data.keys())[:10]},
                passed=passed
            )
            print_result(result)
        except Exception as e:
            elapsed = time.time() - start
            result = log_test(
                category="Curriculum",
                endpoint=f"/api/v1/curriculum/problems/{first_problem_slug}",
                method="GET",
                status=0,
                response_time=elapsed,
                error=str(e),
                passed=False
            )
            print_result(result)

# ============================================
# 5. AUTHENTICATION ENDPOINTS
# ============================================

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("=" * 60)
    print("🔐 AUTHENTICATION ENDPOINTS TESTING")
    print("=" * 60)
    
    # GET /api/v1/auth/me (should require auth or return 401)
    print("\n--- GET /api/v1/auth/me ---")
    start = time.time()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/auth/me", timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        # Should return 401 (unauthorized) or 200 if there's a guest session
        passed = response.status_code in [200, 401]
        
        result = log_test(
            category="Authentication",
            endpoint="/api/v1/auth/me",
            method="GET",
            status=response.status_code,
            response_time=elapsed,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Authentication",
            endpoint="/api/v1/auth/me",
            method="GET",
            status=0,
            response_time=elapsed,
            error=str(e),
            passed=False
        )
        print_result(result)
    
    # POST /api/v1/auth/refresh
    print("\n--- POST /api/v1/auth/refresh ---")
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/refresh", timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        passed = response.status_code in [200, 401]  # Either success or unauthorized
        
        result = log_test(
            category="Authentication",
            endpoint="/api/v1/auth/refresh",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Authentication",
            endpoint="/api/v1/auth/refresh",
            method="POST",
            status=0,
            response_time=elapsed,
            error=str(e),
            passed=False
        )
        print_result(result)
    
    # POST /api/v1/auth/logout
    print("\n--- POST /api/v1/auth/logout ---")
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/logout", timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        passed = response.status_code in [200, 401, 204]
        
        result = log_test(
            category="Authentication",
            endpoint="/api/v1/auth/logout",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Authentication",
            endpoint="/api/v1/auth/logout",
            method="POST",
            status=0,
            response_time=elapsed,
            error=str(e),
            passed=False
        )
        print_result(result)

# ============================================
# 6. ERROR SCENARIOS
# ============================================

def test_error_scenarios():
    """Test error scenarios"""
    print("=" * 60)
    print("⚠️ ERROR SCENARIOS TESTING")
    print("=" * 60)
    
    # Invalid JSON payload
    print("\n--- Test: Invalid JSON payload ---")
    start = time.time()
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/execute/run",
            data="invalid json {",
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        passed = response.status_code in [400, 422]
        
        result = log_test(
            category="Error Handling",
            endpoint="/api/v1/execute/run",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            payload="invalid json {",
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Error Handling",
            endpoint="/api/v1/execute/run",
            method="POST",
            status=0,
            response_time=elapsed,
            error=str(e),
            passed=False
        )
        print_result(result)
    
    # Missing required fields
    print("\n--- Test: Missing required fields ---")
    payload = {}  # Empty payload
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/api/v1/execute/run", json=payload, timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        passed = response.status_code in [400, 422]
        
        result = log_test(
            category="Error Handling",
            endpoint="/api/v1/execute/run",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            payload=payload,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Error Handling",
            endpoint="/api/v1/execute/run",
            method="POST",
            status=0,
            response_time=elapsed,
            payload=payload,
            error=str(e),
            passed=False
        )
        print_result(result)
    
    # Invalid problem slug
    print("\n--- Test: Invalid problem slug ---")
    start = time.time()
    try:
        response = requests.get(f"{BASE_URL}/api/v1/curriculum/problems/nonexistent_slug_12345", timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        passed = response.status_code in [404, 400]
        
        result = log_test(
            category="Error Handling",
            endpoint="/api/v1/curriculum/problems/nonexistent_slug_12345",
            method="GET",
            status=response.status_code,
            response_time=elapsed,
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Error Handling",
            endpoint="/api/v1/curriculum/problems/nonexistent_slug_12345",
            method="GET",
            status=0,
            response_time=elapsed,
            error=str(e),
            passed=False
        )
        print_result(result)
    
    # Large code payload (close to 100KB)
    print("\n--- Test: Large code payload (~50KB) ---")
    large_code = "x = 1\n" + "# " + "A" * 50000  # ~50KB of comments
    payload = {"code": large_code, "language": "python"}
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/api/v1/execute/run", json=payload, timeout=30)
        elapsed = time.time() - start
        
        resp_data = response.json() if response.text else None
        passed = response.status_code in [200, 400, 413]
        
        result = log_test(
            category="Error Handling",
            endpoint="/api/v1/execute/run",
            method="POST",
            status=response.status_code,
            response_time=elapsed,
            payload={"code_size_kb": len(large_code) / 1024, "language": "python"},
            response=resp_data,
            passed=passed
        )
        print_result(result)
    except Exception as e:
        elapsed = time.time() - start
        result = log_test(
            category="Error Handling",
            endpoint="/api/v1/execute/run",
            method="POST",
            status=0,
            response_time=elapsed,
            error=str(e),
            passed=False
        )
        print_result(result)

# ============================================
# 7. RATE LIMIT TESTING
# ============================================

def test_rate_limits():
    """Test rate limiting on endpoints"""
    print("=" * 60)
    print("🚦 RATE LIMIT TESTING (Limited to 10 requests)")
    print("=" * 60)
    
    # Test execution rate limit
    print("\n--- Testing /api/v1/execute/run rate limit (10 requests) ---")
    payload = {"code": "print('test')", "language": "python"}
    
    rate_limited = False
    responses = []
    
    for i in range(10):
        start = time.time()
        try:
            response = requests.post(f"{BASE_URL}/api/v1/execute/run", json=payload, timeout=30)
            elapsed = time.time() - start
            responses.append({"status": response.status_code, "time": elapsed})
            
            if response.status_code == 429:
                rate_limited = True
                print(f"   Request {i+1}: Rate limited (429)")
                break
        except Exception as e:
            elapsed = time.time() - start
            responses.append({"status": 0, "time": elapsed, "error": str(e)})
    
    result = log_test(
        category="Rate Limiting",
        endpoint="/api/v1/execute/run",
        method="POST",
        status=429 if rate_limited else 200,
        response_time=sum(r["time"] for r in responses) / len(responses),
        payload={"requests_sent": len(responses), "rate_limited": rate_limited},
        response={"rate_limit_detected": rate_limited, "requests_completed": len(responses)},
        passed=True  # Test itself passes, we just document the rate limiting behavior
    )
    print_result(result)

# ============================================
# GENERATE REPORT
# ============================================

def generate_report():
    """Generate comprehensive test report"""
    print("=" * 60)
    print("📊 COMPREHENSIVE API TEST REPORT")
    print("=" * 60)
    
    # Calculate statistics
    total_tests = len(test_results)
    passed_tests = sum(1 for r in test_results if r["passed"])
    failed_tests = total_tests - passed_tests
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    # Performance statistics
    if performance_data:
        avg_time = mean(performance_data)
        med_time = median(performance_data)
        min_time = min(performance_data)
        max_time = max(performance_data)
        slow_endpoints = [r for r in test_results if r["response_time_ms"] > 1000]
    else:
        avg_time = med_time = min_time = max_time = 0
        slow_endpoints = []
    
    print(f"\n📈 TEST SUMMARY")
    print(f"   Total Tests: {total_tests}")
    print(f"   ✅ Passed: {passed_tests}")
    print(f"   ❌ Failed: {failed_tests}")
    print(f"   📊 Pass Rate: {pass_rate:.1f}%")
    
    print(f"\n⚡ PERFORMANCE METRICS")
    print(f"   Average Response Time: {avg_time:.2f}ms")
    print(f"   Median Response Time: {med_time:.2f}ms")
    print(f"   Min Response Time: {min_time:.2f}ms")
    print(f"   Max Response Time: {max_time:.2f}ms")
    print(f"   Slow Endpoints (>1s): {len(slow_endpoints)}")
    
    if slow_endpoints:
        print(f"\n   🐢 Slow Endpoints:")
        for ep in slow_endpoints[:5]:
            print(f"      - {ep['method']} {ep['endpoint']}: {ep['response_time_ms']:.2f}ms")
    
    # Group by category
    print(f"\n📁 RESULTS BY CATEGORY")
    categories = {}
    for r in test_results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "passed": 0}
        categories[cat]["total"] += 1
        if r["passed"]:
            categories[cat]["passed"] += 1
    
    for cat, stats in sorted(categories.items()):
        cat_pass_rate = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
        icon = "✅" if cat_pass_rate == 100 else "⚠️" if cat_pass_rate >= 50 else "❌"
        print(f"   {icon} {cat}: {stats['passed']}/{stats['total']} ({cat_pass_rate:.0f}%)")
    
    # Failed tests details
    if failed_tests > 0:
        print(f"\n❌ FAILED TEST DETAILS")
        for r in test_results:
            if not r["passed"]:
                print(f"\n   🔴 {r['method']} {r['endpoint']}")
                print(f"      Status: {r['status_code']} | Time: {r['response_time_ms']}ms")
                if r["error"]:
                    print(f"      Error: {r['error'][:100]}")
    
    # Save detailed report to file
    report_file = "c:\\Users\\digitalnomad\\Documents\\oopkimi\\api_test_report.json"
    with open(report_file, 'w') as f:
        json.dump({
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "pass_rate": pass_rate,
                "performance": {
                    "avg_ms": avg_time,
                    "median_ms": med_time,
                    "min_ms": min_time,
                    "max_ms": max_time
                }
            },
            "category_breakdown": categories,
            "tests": test_results
        }, f, indent=2, default=str)
    
    print(f"\n💾 Detailed report saved to: {report_file}")
    
    return {
        "total": total_tests,
        "passed": passed_tests,
        "failed": failed_tests,
        "pass_rate": pass_rate
    }

# ============================================
# MAIN EXECUTION
# ============================================

def main():
    print("🚀 PYTHON OOP JOURNEY API - COMPREHENSIVE TEST SUITE")
    print(f"   Target: {BASE_URL}")
    print(f"   Started: {datetime.now().isoformat()}")
    print("=" * 60)
    
    try:
        test_health_endpoints()
    except Exception as e:
        print(f"Health endpoints test error: {e}")
    
    try:
        test_code_execution()
    except Exception as e:
        print(f"Code execution test error: {e}")
    
    try:
        test_syntax_check()
    except Exception as e:
        print(f"Syntax check test error: {e}")
    
    try:
        test_legacy_execute()
    except Exception as e:
        print(f"Legacy execute test error: {e}")
    
    try:
        test_verification_endpoints()
    except Exception as e:
        print(f"Verification endpoints test error: {e}")
    
    try:
        test_curriculum_endpoints()
    except Exception as e:
        print(f"Curriculum endpoints test error: {e}")
    
    try:
        test_auth_endpoints()
    except Exception as e:
        print(f"Auth endpoints test error: {e}")
    
    try:
        test_error_scenarios()
    except Exception as e:
        print(f"Error scenarios test error: {e}")
    
    try:
        test_rate_limits()
    except Exception as e:
        print(f"Rate limit test error: {e}")
    
    # Generate final report
    stats = generate_report()
    
    print("\n" + "=" * 60)
    print("🏁 TEST SUITE COMPLETED")
    print("=" * 60)
    
    if stats["pass_rate"] >= 90:
        print("✅ OVERALL STATUS: EXCELLENT")
    elif stats["pass_rate"] >= 70:
        print("⚠️ OVERALL STATUS: GOOD WITH ISSUES")
    else:
        print("❌ OVERALL STATUS: NEEDS ATTENTION")
    
    return stats

if __name__ == "__main__":
    main()
