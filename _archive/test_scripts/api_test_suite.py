#!/usr/bin/env python3
"""
Comprehensive API Test Suite for Python OOP Journey API
Backend URL: https://oop-journey-api.onrender.com
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, Any, Tuple, Optional

# Fix encoding for Windows
sys.stdout.reconfigure(encoding='utf-8')

# Configuration
BASE_URL = "https://oop-journey-api.onrender.com"
TIMEOUT = 30  # seconds for normal requests
EXEC_TIMEOUT = 35  # seconds for execution endpoints

# Test results storage
results = {
    "passed": [],
    "failed": [],
    "warnings": [],
    "performance": {}
}

def log_test(name: str, passed: bool, details: str = "", response_time: float = 0, error: str = None):
    """Log test result"""
    status = "[PASS]" if passed else "[FAIL]"
    entry = {
        "name": name,
        "status": passed,
        "details": details,
        "response_time": response_time,
        "error": error,
        "timestamp": datetime.now().isoformat()
    }
    
    if passed:
        results["passed"].append(entry)
    else:
        results["failed"].append(entry)
    
    perf_indicator = f" ({response_time:.2f}s)" if response_time > 0 else ""
    print(f"{status} {name}{perf_indicator}")
    if details:
        print(f"    -> {details}")
    if error:
        print(f"    ERROR: {error}")
    print()

def make_request(method: str, endpoint: str, **kwargs) -> Tuple[Optional[requests.Response], float, str]:
    """Make HTTP request and return response, time taken, and error"""
    url = f"{BASE_URL}{endpoint}"
    start_time = time.time()
    
    try:
        timeout = kwargs.pop('timeout', TIMEOUT)
        response = requests.request(method, url, timeout=timeout, **kwargs)
        elapsed = time.time() - start_time
        return response, elapsed, None
    except requests.exceptions.Timeout:
        elapsed = time.time() - start_time
        return None, elapsed, "Request timeout"
    except requests.exceptions.ConnectionError as e:
        elapsed = time.time() - start_time
        return None, elapsed, f"Connection error: {str(e)}"
    except Exception as e:
        elapsed = time.time() - start_time
        return None, elapsed, f"Exception: {str(e)}"

def check_cors_headers(response: requests.Response) -> bool:
    """Check if CORS headers are present"""
    cors_headers = [
        'access-control-allow-origin',
        'access-control-allow-methods',
        'access-control-allow-headers'
    ]
    return any(h in response.headers for h in cors_headers)

print("=" * 70)
print("API TEST SUITE FOR PYTHON OOP JOURNEY")
print(f"Base URL: {BASE_URL}")
print(f"Started: {datetime.now().isoformat()}")
print("=" * 70)
print()

# ============================================================================
# TEST 1: Health Check Endpoints
# ============================================================================
print("-" * 70)
print("HEALTH CHECK ENDPOINTS")
print("-" * 70)

# Test main health endpoint
resp, elapsed, error = make_request("GET", "/health")
if resp and resp.status_code == 200:
    try:
        data = resp.json()
        log_test("GET /health", True, f"Status: {resp.status_code}, Response: {data}", elapsed)
    except:
        log_test("GET /health", True, f"Status: {resp.status_code}, Body: {resp.text[:100]}", elapsed)
elif resp:
    log_test("GET /health", False, f"Status: {resp.status_code}", elapsed, resp.text[:200])
else:
    log_test("GET /health", False, "No response", elapsed, error)

# Test execute health endpoint
resp, elapsed, error = make_request("GET", "/api/execute/health")
if resp and resp.status_code == 200:
    try:
        data = resp.json()
        log_test("GET /api/execute/health", True, f"Status: {resp.status_code}, Response: {data}", elapsed)
    except:
        log_test("GET /api/execute/health", True, f"Status: {resp.status_code}", elapsed)
elif resp:
    log_test("GET /api/execute/health", False, f"Status: {resp.status_code}", elapsed, resp.text[:200])
else:
    log_test("GET /api/execute/health", False, "No response", elapsed, error)

# ============================================================================
# TEST 2: Code Execution Endpoints
# ============================================================================
print("-" * 70)
print("CODE EXECUTION ENDPOINTS")
print("-" * 70)

# Test 2.1: Valid Python code execution
valid_code = {
    "code": "x = 5\ny = 10\nprint(f'Sum: {x + y}')\nprint('Hello from Python!')"
}
resp, elapsed, error = make_request("POST", "/api/execute/run", 
                                      json=valid_code, 
                                      timeout=EXEC_TIMEOUT,
                                      headers={"Content-Type": "application/json"})
if resp and resp.status_code == 200:
    try:
        data = resp.json()
        success = data.get('success', False)
        has_output = 'output' in data or 'stdout' in data
        if success or has_output:
            log_test("POST /api/execute/run (valid code)", True, 
                    f"Status: {resp.status_code}, Success: {success}", elapsed)
        else:
            log_test("POST /api/execute/run (valid code)", False, 
                    f"Unexpected response: {data}", elapsed)
    except Exception as e:
        log_test("POST /api/execute/run (valid code)", False, 
                f"Parse error: {str(e)}", elapsed, resp.text[:200])
elif resp:
    log_test("POST /api/execute/run (valid code)", False, 
            f"Status: {resp.status_code}", elapsed, resp.text[:200])
else:
    log_test("POST /api/execute/run (valid code)", False, "No response", elapsed, error)

# Test 2.2: Invalid syntax code
invalid_code = {
    "code": "def broken(\n    print('missing parenthesis'"
}
resp, elapsed, error = make_request("POST", "/api/execute/run", 
                                      json=invalid_code,
                                      timeout=EXEC_TIMEOUT,
                                      headers={"Content-Type": "application/json"})
if resp:
    try:
        data = resp.json()
        has_error = 'error' in data or data.get('success') == False
        log_test("POST /api/execute/run (syntax error)", True, 
                f"Status: {resp.status_code}, Has error handling: {has_error}", elapsed)
    except:
        log_test("POST /api/execute/run (syntax error)", True, 
                f"Status: {resp.status_code}", elapsed)
else:
    log_test("POST /api/execute/run (syntax error)", False, "No response", elapsed, error)

# Test 2.3: Legacy execute endpoint
resp, elapsed, error = make_request("POST", "/api/execute", 
                                      json=valid_code,
                                      timeout=EXEC_TIMEOUT,
                                      headers={"Content-Type": "application/json"})
if resp:
    status_ok = resp.status_code in [200, 301, 302, 308]
    log_test("POST /api/execute (legacy)", status_ok, 
            f"Status: {resp.status_code}", elapsed)
else:
    log_test("POST /api/execute (legacy)", False, "No response", elapsed, error)

# Test 2.4: Code with large output
large_output_code = {
    "code": "for i in range(100):\n    print(f'Line {i}: ' + 'A' * 50)"
}
resp, elapsed, error = make_request("POST", "/api/execute/run", 
                                      json=large_output_code,
                                      timeout=EXEC_TIMEOUT,
                                      headers={"Content-Type": "application/json"})
if resp and resp.status_code == 200:
    log_test("POST /api/execute/run (large output)", True, 
            f"Status: {resp.status_code}", elapsed)
else:
    log_test("POST /api/execute/run (large output)", False, 
            f"Status: {resp.status_code if resp else 'N/A'}", elapsed, error)

# Test 2.5: Code that might timeout (infinite loop protection)
timeout_code = {
    "code": "import time\nwhile True:\n    time.sleep(1)",
    "timeout": 2
}
resp, elapsed, error = make_request("POST", "/api/execute/run", 
                                      json=timeout_code,
                                      timeout=10,
                                      headers={"Content-Type": "application/json"})
if resp:
    log_test("POST /api/execute/run (timeout protection)", True, 
            f"Status: {resp.status_code}, Has timeout handling", elapsed)
elif error and "timeout" in error.lower():
    log_test("POST /api/execute/run (timeout protection)", True, 
            f"Request timeout as expected: {error}", elapsed)
else:
    log_test("POST /api/execute/run (timeout protection)", False, 
            "Unexpected behavior", elapsed, error)

# ============================================================================
# TEST 3: Verification Endpoints
# ============================================================================
print("-" * 70)
print("VERIFICATION ENDPOINTS")
print("-" * 70)

# Test 3.1: General verify endpoint
correct_solution = {
    "code": "def add(a, b):\n    return a + b",
    "problem_id": "test_add"
}
resp, elapsed, error = make_request("POST", "/api/v1/verify", 
                                      json=correct_solution,
                                      timeout=EXEC_TIMEOUT,
                                      headers={"Content-Type": "application/json"})
if resp:
    try:
        data = resp.json()
        log_test("POST /api/v1/verify", True, 
                f"Status: {resp.status_code}, Response keys: {list(data.keys())}", elapsed)
    except:
        log_test("POST /api/v1/verify", True, 
                f"Status: {resp.status_code}", elapsed)
else:
    log_test("POST /api/v1/verify", False, "No response", elapsed, error)

# Test 3.2: Verify with problem slug
problem_slugs = ["week1_day1_hello_world", "week1_calculate_sum", "test_problem"]
for slug in problem_slugs:
    resp, elapsed, error = make_request("POST", f"/api/v1/verify/{slug}", 
                                          json={"code": "print('test')"},
                                          timeout=EXEC_TIMEOUT,
                                          headers={"Content-Type": "application/json"})
    if resp:
        log_test(f"POST /api/v1/verify/{slug}", resp.status_code != 500, 
                f"Status: {resp.status_code}", elapsed)
        if resp.status_code in [200, 404]:
            break

# Test 3.3: Syntax validation endpoint - valid code
resp, elapsed, error = make_request("POST", "/api/v1/validate-syntax", 
                                      json={"code": "x = 1 + 2"},
                                      timeout=EXEC_TIMEOUT,
                                      headers={"Content-Type": "application/json"})
if resp:
    log_test("POST /api/v1/validate-syntax (valid)", resp.status_code == 200, 
            f"Status: {resp.status_code}", elapsed)
else:
    log_test("POST /api/v1/validate-syntax (valid)", False, "No response", elapsed, error)

# Test 3.4: Syntax validation with invalid code
resp, elapsed, error = make_request("POST", "/api/v1/validate-syntax", 
                                      json={"code": "def broken("},
                                      timeout=EXEC_TIMEOUT,
                                      headers={"Content-Type": "application/json"})
if resp:
    log_test("POST /api/v1/validate-syntax (invalid)", True, 
            f"Status: {resp.status_code}", elapsed)
else:
    log_test("POST /api/v1/validate-syntax (invalid)", False, "No response", elapsed, error)

# Test 3.5: Test info endpoint
found_test_info = False
for slug in problem_slugs:
    resp, elapsed, error = make_request("GET", f"/api/v1/test-info/{slug}", 
                                          timeout=TIMEOUT)
    if resp and resp.status_code == 200:
        log_test(f"GET /api/v1/test-info/{slug}", True, 
                f"Status: {resp.status_code}", elapsed)
        found_test_info = True
        break
    elif resp and resp.status_code == 404:
        continue
if not found_test_info:
    log_test("GET /api/v1/test-info/{problem_slug}", False, 
            "All tested slugs returned 404 or error", elapsed if 'elapsed' in locals() else 0, error)

# ============================================================================
# TEST 4: Curriculum Endpoints
# ============================================================================
print("-" * 70)
print("CURRICULUM ENDPOINTS")
print("-" * 70)

# Test curriculum endpoints
curriculum_endpoints = [
    "/api/curriculum",
    "/api/curriculum/weeks",
    "/api/curriculum/week/1",
    "/api/curriculum/week/1/day/1",
    "/api/curriculum/problems",
    "/api/curriculum/problem/hello_world",
]

for endpoint in curriculum_endpoints:
    resp, elapsed, error = make_request("GET", endpoint, timeout=TIMEOUT)
    if resp and resp.status_code == 200:
        try:
            data = resp.json()
            log_test(f"GET {endpoint}", True, 
                    f"Status: {resp.status_code}, Data type: {type(data).__name__}", elapsed)
        except:
            log_test(f"GET {endpoint}", True, 
                    f"Status: {resp.status_code} (non-JSON)", elapsed)
    elif resp:
        log_test(f"GET {endpoint}", resp.status_code == 404, 
                f"Status: {resp.status_code}", elapsed)
    else:
        log_test(f"GET {endpoint}", False, "No response", elapsed, error)

# ============================================================================
# TEST 5: Authentication Endpoints
# ============================================================================
print("-" * 70)
print("AUTHENTICATION ENDPOINTS")
print("-" * 70)

auth_endpoints = [
    ("GET", "/api/auth/me"),
    ("POST", "/api/auth/login"),
    ("POST", "/api/auth/register"),
    ("POST", "/api/auth/logout"),
    ("POST", "/api/auth/refresh"),
]

for method, endpoint in auth_endpoints:
    if method == "GET":
        resp, elapsed, error = make_request(method, endpoint, timeout=TIMEOUT)
    else:
        resp, elapsed, error = make_request(method, endpoint, 
                                              json={"test": "data"},
                                              timeout=TIMEOUT,
                                              headers={"Content-Type": "application/json"})
    
    if resp:
        is_ok = resp.status_code in [200, 401, 403, 404, 422]
        log_test(f"{method} {endpoint}", is_ok, 
                f"Status: {resp.status_code}", elapsed)
    else:
        log_test(f"{method} {endpoint}", False, "No response", elapsed, error)

# ============================================================================
# TEST 6: CORS and Headers
# ============================================================================
print("-" * 70)
print("CORS AND HEADERS VALIDATION")
print("-" * 70)

# Test CORS preflight
resp, elapsed, error = make_request("OPTIONS", "/api/execute/run", 
                                      headers={
                                          "Origin": "http://localhost:3000",
                                          "Access-Control-Request-Method": "POST",
                                          "Access-Control-Request-Headers": "Content-Type"
                                      },
                                      timeout=TIMEOUT)
if resp:
    has_cors = check_cors_headers(resp)
    log_test("OPTIONS /api/execute/run (CORS preflight)", has_cors, 
            f"Status: {resp.status_code}, CORS headers: {has_cors}", elapsed)
else:
    log_test("OPTIONS /api/execute/run (CORS preflight)", False, 
            "No response", elapsed, error)

# Test response headers on regular request
resp, elapsed, error = make_request("GET", "/health", timeout=TIMEOUT)
if resp:
    content_type = resp.headers.get('content-type', 'N/A')
    has_cors = check_cors_headers(resp)
    log_test("Response Headers Check", True, 
            f"Content-Type: {content_type}, CORS: {has_cors}", elapsed)
else:
    log_test("Response Headers Check", False, "No response", elapsed, error)

# ============================================================================
# TEST 7: Error Handling
# ============================================================================
print("-" * 70)
print("ERROR HANDLING")
print("-" * 70)

# Test 404 handler
resp, elapsed, error = make_request("GET", "/api/nonexistent-endpoint-12345", timeout=TIMEOUT)
if resp:
    returns_404 = resp.status_code == 404
    log_test("404 Error Handling", returns_404, 
            f"Status: {resp.status_code}", elapsed)
else:
    log_test("404 Error Handling", False, "No response", elapsed, error)

# Test invalid method
resp, elapsed, error = make_request("DELETE", "/api/execute/health", timeout=TIMEOUT)
if resp:
    is_handled = resp.status_code in [405, 404, 200]
    log_test("Invalid HTTP Method Handling", is_handled, 
            f"Status: {resp.status_code}", elapsed)
else:
    log_test("Invalid HTTP Method Handling", False, "No response", elapsed, error)

# Test malformed JSON
resp, elapsed, error = make_request("POST", "/api/execute/run", 
                                      data="not valid json",
                                      headers={"Content-Type": "application/json"},
                                      timeout=TIMEOUT)
if resp:
    log_test("Malformed JSON Handling", True, 
            f"Status: {resp.status_code}", elapsed)
else:
    log_test("Malformed JSON Handling", False, "No response", elapsed, error)

# ============================================================================
# GENERATE REPORT
# ============================================================================
print()
print("=" * 70)
print("API TEST REPORT SUMMARY")
print("=" * 70)

total_tests = len(results["passed"]) + len(results["failed"])
pass_rate = (len(results["passed"]) / total_tests * 100) if total_tests > 0 else 0

print(f"\nTotal Tests: {total_tests}")
print(f"[PASS] Passed: {len(results['passed'])}")
print(f"[FAIL] Failed: {len(results['failed'])}")
print(f"Pass Rate: {pass_rate:.1f}%")

# Performance summary
if results["passed"]:
    avg_time = sum(r['response_time'] for r in results['passed']) / len(results['passed'])
    max_time = max(r['response_time'] for r in results['passed'])
    min_time = min(r['response_time'] for r in results['passed'])
    
    print(f"\nPerformance Metrics:")
    print(f"   Average Response Time: {avg_time:.3f}s")
    print(f"   Fastest: {min_time:.3f}s")
    print(f"   Slowest: {max_time:.3f}s")
    
    # Find slow endpoints
    slow_threshold = 2.0
    slow_endpoints = [r for r in results['passed'] if r['response_time'] > slow_threshold]
    if slow_endpoints:
        print(f"\n   Slow Endpoints (>{slow_threshold}s):")
        for r in sorted(slow_endpoints, key=lambda x: x['response_time'], reverse=True)[:5]:
            print(f"      - {r['name']}: {r['response_time']:.2f}s")

# Failed tests detail
if results["failed"]:
    print(f"\nFAILED TESTS DETAIL:")
    for r in results["failed"]:
        print(f"\n   {r['name']}")
        print(f"   Time: {r['response_time']:.3f}s")
        if r['details']:
            print(f"   Details: {r['details']}")
        if r['error']:
            print(f"   Error: {r['error']}")

print("\n" + "=" * 70)
print(f"Test Run Completed: {datetime.now().isoformat()}")
print("=" * 70)

# Save detailed report
report = {
    "timestamp": datetime.now().isoformat(),
    "base_url": BASE_URL,
    "summary": {
        "total": total_tests,
        "passed": len(results["passed"]),
        "failed": len(results["failed"]),
        "pass_rate": pass_rate
    },
    "results": results
}

with open("api_test_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("\nDetailed report saved to: api_test_report.json")
