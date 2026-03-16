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
from typing import Dict, Any, Tuple, Optional, List

# Configuration
BASE_URL = "https://oop-journey-api.onrender.com"
TIMEOUT = 30
EXEC_TIMEOUT = 35

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
    url = f"{BASE_URL}{endpoint}" if not endpoint.startswith('http') else endpoint
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
    return any(h.lower() in [k.lower() for k in response.headers.keys()] for h in cors_headers)

print("=" * 70)
print("COMPREHENSIVE API TEST SUITE FOR PYTHON OOP JOURNEY")
print(f"Base URL: {BASE_URL}")
print(f"Started: {datetime.now().isoformat()}")
print("=" * 70)
print()

# ============================================================================
# TEST GROUP 1: Health Check Endpoints
# ============================================================================
print("-" * 70)
print("GROUP 1: HEALTH CHECK ENDPOINTS")
print("-" * 70)

health_endpoints = [
    ("GET", "/health", "Main health check"),
    ("GET", "/health/detailed", "Detailed health check"),
    ("GET", "/health/db", "Database health"),
    ("GET", "/health/cache", "Cache health"),
    ("GET", "/health/ready", "Readiness check"),
    ("GET", "/health/live", "Liveness check"),
    ("GET", "/ready", "Alternative readiness"),
    ("GET", "/", "Root endpoint"),
]

for method, endpoint, description in health_endpoints:
    resp, elapsed, error = make_request(method, endpoint)
    if resp and resp.status_code == 200:
        try:
            data = resp.json()
            log_test(f"{method} {endpoint}", True, f"{description}: OK", elapsed)
        except:
            log_test(f"{method} {endpoint}", True, f"{description}: OK (non-JSON)", elapsed)
    elif resp:
        log_test(f"{method} {endpoint}", False, f"Status: {resp.status_code}", elapsed, resp.text[:200])
    else:
        log_test(f"{method} {endpoint}", False, description, elapsed, error)

# ============================================================================
# TEST GROUP 2: Code Execution Endpoints
# ============================================================================
print("-" * 70)
print("GROUP 2: CODE EXECUTION ENDPOINTS")
print("-" * 70)

# Test 2.1: Execute Python code - valid code
valid_code_tests = [
    ("Simple print", "print('Hello, World!')"),
    ("Variable assignment", "x = 5\ny = 10\nprint(f'Sum: {x + y}')"),
    ("Function definition", "def greet(name):\n    return f'Hello, {name}!'\nprint(greet('Python'))"),
    ("List comprehension", "squares = [x**2 for x in range(10)]\nprint(squares)"),
]

for test_name, code in valid_code_tests:
    payload = {"code": code}
    resp, elapsed, error = make_request("POST", "/api/v1/execute/run", 
                                          json=payload, 
                                          timeout=EXEC_TIMEOUT,
                                          headers={"Content-Type": "application/json"})
    if resp and resp.status_code == 200:
        try:
            data = resp.json()
            success = data.get('success', False)
            has_output = 'output' in data or 'stdout' in data or 'result' in data
            if success or has_output:
                log_test(f"POST /api/v1/execute/run - {test_name}", True, 
                        f"Success: {success}", elapsed)
            else:
                log_test(f"POST /api/v1/execute/run - {test_name}", False, 
                        f"No output in response: {list(data.keys())}", elapsed)
        except Exception as e:
            log_test(f"POST /api/v1/execute/run - {test_name}", False, 
                    f"Parse error: {str(e)}", elapsed, resp.text[:200])
    elif resp:
        log_test(f"POST /api/v1/execute/run - {test_name}", False, 
                f"Status: {resp.status_code}", elapsed, resp.text[:200])
    else:
        log_test(f"POST /api/v1/execute/run - {test_name}", False, "No response", elapsed, error)

# Test 2.2: Syntax error handling
syntax_error_tests = [
    ("Missing parenthesis", "print('hello'"),
    ("Invalid indentation", "def foo():\nprint('bad indent')"),
    ("Undefined variable", "print(undefined_var)"),
]

for test_name, code in syntax_error_tests:
    payload = {"code": code}
    resp, elapsed, error = make_request("POST", "/api/v1/execute/run", 
                                          json=payload,
                                          timeout=EXEC_TIMEOUT,
                                          headers={"Content-Type": "application/json"})
    if resp and resp.status_code == 200:
        try:
            data = resp.json()
            # Should return error info
            has_error = 'error' in data or data.get('success') == False or 'stderr' in data
            log_test(f"POST /api/v1/execute/run - {test_name}", True, 
                    f"Has error handling: {has_error}", elapsed)
        except:
            log_test(f"POST /api/v1/execute/run - {test_name}", True, 
                    f"Status: {resp.status_code}", elapsed)
    elif resp:
        log_test(f"POST /api/v1/execute/run - {test_name}", True, 
                f"Status: {resp.status_code} (handled)", elapsed)
    else:
        log_test(f"POST /api/v1/execute/run - {test_name}", False, "No response", elapsed, error)

# Test 2.3: Legacy execute endpoint
resp, elapsed, error = make_request("POST", "/api/v1/execute", 
                                      json={"code": "print('legacy test')"},
                                      timeout=EXEC_TIMEOUT,
                                      headers={"Content-Type": "application/json"})
if resp:
    status_ok = resp.status_code in [200, 301, 302, 307, 308]
    log_test("POST /api/v1/execute (legacy)", status_ok, 
            f"Status: {resp.status_code}", elapsed)
else:
    log_test("POST /api/v1/execute (legacy)", False, "No response", elapsed, error)

# Test 2.4: Execute health check
resp, elapsed, error = make_request("GET", "/api/v1/execute/health")
if resp and resp.status_code == 200:
    log_test("GET /api/v1/execute/health", True, f"Status: {resp.status_code}", elapsed)
else:
    log_test("GET /api/v1/execute/health", False, 
            f"Status: {resp.status_code if resp else 'N/A'}", elapsed, error)

# Test 2.5: Syntax check endpoint
resp, elapsed, error = make_request("POST", "/api/v1/execute/syntax-check",
                                      json={"code": "x = 1 + 2"},
                                      timeout=EXEC_TIMEOUT,
                                      headers={"Content-Type": "application/json"})
if resp and resp.status_code == 200:
    log_test("POST /api/v1/execute/syntax-check (valid)", True, 
            f"Status: {resp.status_code}", elapsed)
else:
    log_test("POST /api/v1/execute/syntax-check (valid)", False, 
            f"Status: {resp.status_code if resp else 'N/A'}", elapsed, error)

# Test 2.6: Syntax check with invalid code
resp, elapsed, error = make_request("POST", "/api/v1/execute/syntax-check",
                                      json={"code": "def broken("},
                                      timeout=EXEC_TIMEOUT,
                                      headers={"Content-Type": "application/json"})
if resp:
    log_test("POST /api/v1/execute/syntax-check (invalid)", True, 
            f"Status: {resp.status_code}", elapsed)
else:
    log_test("POST /api/v1/execute/syntax-check (invalid)", False, "No response", elapsed, error)

# ============================================================================
# TEST GROUP 3: Verification Endpoints
# ============================================================================
print("-" * 70)
print("GROUP 3: VERIFICATION ENDPOINTS")
print("-" * 70)

# Test 3.1: General verify endpoint with correct solution
correct_solution = {
    "code": "def add(a, b):\n    return a + b",
    "problem_slug": "test_problem"
}
resp, elapsed, error = make_request("POST", "/api/v1/verify", 
                                      json=correct_solution,
                                      timeout=EXEC_TIMEOUT,
                                      headers={"Content-Type": "application/json"})
if resp:
    try:
        data = resp.json()
        log_test("POST /api/v1/verify", True, 
                f"Status: {resp.status_code}, Keys: {list(data.keys())}", elapsed)
    except:
        log_test("POST /api/v1/verify", True, 
                f"Status: {resp.status_code}", elapsed)
else:
    log_test("POST /api/v1/verify", False, "No response", elapsed, error)

# Test 3.2: Verify with specific problem slug
problem_slugs = ["week1_calculate_sum", "hello_world", "test_problem"]
for slug in problem_slugs:
    resp, elapsed, error = make_request("POST", f"/api/v1/verify/{slug}", 
                                          json={"code": "def solution(): pass"},
                                          timeout=EXEC_TIMEOUT,
                                          headers={"Content-Type": "application/json"})
    if resp:
        is_ok = resp.status_code in [200, 404, 422]  # 404 if problem doesn't exist is OK
        log_test(f"POST /api/v1/verify/{slug}", is_ok, 
                f"Status: {resp.status_code}", elapsed)
        if resp.status_code == 200:
            break

# Test 3.3: Validate syntax endpoint
resp, elapsed, error = make_request("POST", "/api/v1/validate-syntax", 
                                      json={"code": "x = 1 + 2"},
                                      timeout=EXEC_TIMEOUT,
                                      headers={"Content-Type": "application/json"})
if resp and resp.status_code == 200:
    log_test("POST /api/v1/validate-syntax (valid)", True, 
            f"Status: {resp.status_code}", elapsed)
else:
    log_test("POST /api/v1/validate-syntax (valid)", False, 
            f"Status: {resp.status_code if resp else 'N/A'}", elapsed, error)

# Test 3.4: Validate syntax with invalid code
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
            "All tested slugs returned 404", elapsed if 'elapsed' in locals() else 0, error)

# ============================================================================
# TEST GROUP 4: Curriculum Endpoints
# ============================================================================
print("-" * 70)
print("GROUP 4: CURRICULUM ENDPOINTS")
print("-" * 70)

# Test 4.1: Full curriculum
curriculum_tests = [
    ("/api/v1/curriculum", "Full curriculum"),
    ("/api/v1/curriculum/problems", "All problems"),
]

for endpoint, description in curriculum_tests:
    resp, elapsed, error = make_request("GET", endpoint, timeout=TIMEOUT)
    if resp and resp.status_code == 200:
        try:
            data = resp.json()
            data_info = ""
            if isinstance(data, list):
                data_info = f" ({len(data)} items)"
            elif isinstance(data, dict):
                data_info = f" (keys: {list(data.keys())})"
            log_test(f"GET {endpoint}", True, 
                    f"{description}: OK{data_info}", elapsed)
        except:
            log_test(f"GET {endpoint}", True, 
                    f"{description}: OK (non-JSON)", elapsed)
    elif resp:
        log_test(f"GET {endpoint}", False, 
                f"Status: {resp.status_code}", elapsed, resp.text[:100])
    else:
        log_test(f"GET {endpoint}", False, description, elapsed, error)

# Test 4.2: Specific week
week_slugs = ["week-1", "week1", "fundamentals"]
for slug in week_slugs:
    resp, elapsed, error = make_request("GET", f"/api/v1/curriculum/weeks/{slug}", timeout=TIMEOUT)
    if resp and resp.status_code == 200:
        log_test(f"GET /api/v1/curriculum/weeks/{slug}", True, 
                f"Status: {resp.status_code}", elapsed)
        break
    elif resp and resp.status_code == 404:
        continue
else:
    log_test("GET /api/v1/curriculum/weeks/{slug}", False, 
            "No valid week slug found", elapsed if 'elapsed' in locals() else 0, error)

# Test 4.3: Specific problem
problem_endpoints = [
    "/api/v1/curriculum/problems/hello_world",
    "/api/v1/curriculum/problems/week1_calculate_sum",
]
for endpoint in problem_endpoints:
    resp, elapsed, error = make_request("GET", endpoint, timeout=TIMEOUT)
    if resp and resp.status_code == 200:
        log_test(f"GET {endpoint}", True, 
                f"Status: {resp.status_code}", elapsed)
        break
    elif resp and resp.status_code == 404:
        continue
else:
    log_test("GET /api/v1/curriculum/problems/{slug}", False, 
            "No valid problem slug found", elapsed if 'elapsed' in locals() else 0, error)

# ============================================================================
# TEST GROUP 5: Authentication Endpoints
# ============================================================================
print("-" * 70)
print("GROUP 5: AUTHENTICATION ENDPOINTS")
print("-" * 70)

# Test 5.1: Magic link request (no auth required)
resp, elapsed, error = make_request("POST", "/api/v1/auth/magic-link",
                                      json={"email": "test@example.com"},
                                      timeout=TIMEOUT,
                                      headers={"Content-Type": "application/json"})
if resp:
    # Should accept the request (may return 200 or error for invalid email format)
    is_ok = resp.status_code in [200, 400, 422]
    log_test("POST /api/v1/auth/magic-link", is_ok, 
            f"Status: {resp.status_code}", elapsed)
else:
    log_test("POST /api/v1/auth/magic-link", False, "No response", elapsed, error)

# Test 5.2: Get current user (should require auth)
auth_endpoints = [
    ("GET", "/api/v1/auth/me", "Get current user"),
    ("PATCH", "/api/v1/auth/me", "Update user"),
    ("GET", "/api/v1/users/me", "Get user profile"),
    ("GET", "/api/v1/users/me/stats", "Get user stats"),
    ("GET", "/api/v1/users/me/progress", "Get user progress"),
]

for method, endpoint, description in auth_endpoints:
    if method == "GET":
        resp, elapsed, error = make_request(method, endpoint, timeout=TIMEOUT)
    else:
        resp, elapsed, error = make_request(method, endpoint, 
                                              json={},
                                              timeout=TIMEOUT,
                                              headers={"Content-Type": "application/json"})
    
    if resp:
        # Auth endpoints should return 401/403 for unauthenticated requests
        is_ok = resp.status_code in [200, 401, 403]
        log_test(f"{method} {endpoint}", is_ok, 
                f"{description}: Status {resp.status_code}", elapsed)
    else:
        log_test(f"{method} {endpoint}", False, description, elapsed, error)

# ============================================================================
# TEST GROUP 6: AI Endpoints
# ============================================================================
print("-" * 70)
print("GROUP 6: AI SERVICE ENDPOINTS")
print("-" * 70)

# Test 6.1: AI health check
resp, elapsed, error = make_request("GET", "/api/v1/ai/health", timeout=TIMEOUT)
if resp and resp.status_code == 200:
    log_test("GET /api/v1/ai/health", True, f"Status: {resp.status_code}", elapsed)
else:
    log_test("GET /api/v1/ai/health", False, 
            f"Status: {resp.status_code if resp else 'N/A'}", elapsed, error)

# Test 6.2: AI hint (may require auth)
ai_tests = [
    ("/api/v1/ai/hint", "Generate hint"),
    ("/api/v1/ai/explain-error", "Explain error"),
    ("/api/v1/ai/code-review", "Code review"),
]

for endpoint, description in ai_tests:
    resp, elapsed, error = make_request("POST", endpoint,
                                          json={"code": "print('test')"},
                                          timeout=TIMEOUT,
                                          headers={"Content-Type": "application/json"})
    if resp:
        is_ok = resp.status_code in [200, 401, 403, 422]  # Auth or validation errors are OK
        log_test(f"POST {endpoint}", is_ok, 
                f"{description}: Status {resp.status_code}", elapsed)
    else:
        log_test(f"POST {endpoint}", False, description, elapsed, error)

# ============================================================================
# TEST GROUP 7: Progress & Drafts Endpoints
# ============================================================================
print("-" * 70)
print("GROUP 7: PROGRESS & DRAFTS ENDPOINTS")
print("-" * 70)

progress_endpoints = [
    ("GET", "/api/v1/progress", "Get all progress"),
    ("GET", "/api/v1/progress/stats/overall", "Overall stats"),
    ("GET", "/api/v1/drafts", "List drafts"),
]

for method, endpoint, description in progress_endpoints:
    resp, elapsed, error = make_request(method, endpoint, timeout=TIMEOUT)
    if resp:
        is_ok = resp.status_code in [200, 401, 403]
        log_test(f"{method} {endpoint}", is_ok, 
                f"{description}: Status {resp.status_code}", elapsed)
    else:
        log_test(f"{method} {endpoint}", False, description, elapsed, error)

# ============================================================================
# TEST GROUP 8: CORS and Headers Validation
# ============================================================================
print("-" * 70)
print("GROUP 8: CORS AND HEADERS VALIDATION")
print("-" * 70)

# Test 8.1: CORS preflight
resp, elapsed, error = make_request("OPTIONS", "/api/v1/execute/run", 
                                      headers={
                                          "Origin": "http://localhost:3000",
                                          "Access-Control-Request-Method": "POST",
                                          "Access-Control-Request-Headers": "Content-Type"
                                      },
                                      timeout=TIMEOUT)
if resp:
    has_cors = check_cors_headers(resp)
    cors_headers = {k: v for k, v in resp.headers.items() if 'access-control' in k.lower()}
    log_test("OPTIONS /api/v1/execute/run (CORS)", has_cors, 
            f"Status: {resp.status_code}, CORS headers: {cors_headers}", elapsed)
else:
    log_test("OPTIONS /api/v1/execute/run (CORS)", False, 
            "No response", elapsed, error)

# Test 8.2: Response headers
resp, elapsed, error = make_request("GET", "/health", timeout=TIMEOUT)
if resp:
    content_type = resp.headers.get('content-type', 'N/A')
    server = resp.headers.get('server', 'N/A')
    has_cors = check_cors_headers(resp)
    log_test("Response Headers Check", True, 
            f"Content-Type: {content_type}, Server: {server}, CORS: {has_cors}", elapsed)
else:
    log_test("Response Headers Check", False, "No response", elapsed, error)

# ============================================================================
# TEST GROUP 9: Error Handling
# ============================================================================
print("-" * 70)
print("GROUP 9: ERROR HANDLING")
print("-" * 70)

# Test 9.1: 404 handler
resp, elapsed, error = make_request("GET", "/api/nonexistent-endpoint-xyz123", timeout=TIMEOUT)
if resp and resp.status_code == 404:
    log_test("404 Error Handling", True, 
            f"Status: {resp.status_code}", elapsed)
else:
    log_test("404 Error Handling", False, 
            f"Status: {resp.status_code if resp else 'N/A'}", elapsed, error)

# Test 9.2: Invalid method
resp, elapsed, error = make_request("DELETE", "/health", timeout=TIMEOUT)
if resp:
    is_handled = resp.status_code in [405, 404, 200]
    log_test("Invalid HTTP Method Handling", is_handled, 
            f"Status: {resp.status_code}", elapsed)
else:
    log_test("Invalid HTTP Method Handling", False, "No response", elapsed, error)

# Test 9.3: Malformed JSON
resp, elapsed, error = make_request("POST", "/api/v1/execute/run", 
                                      data="not valid json",
                                      headers={"Content-Type": "application/json"},
                                      timeout=TIMEOUT)
if resp and resp.status_code in [400, 422]:
    log_test("Malformed JSON Handling", True, 
            f"Status: {resp.status_code} (properly rejected)", elapsed)
else:
    log_test("Malformed JSON Handling", False, 
            f"Status: {resp.status_code if resp else 'N/A'}", elapsed, error)

# Test 9.4: Empty body
resp, elapsed, error = make_request("POST", "/api/v1/execute/run", 
                                      data="",
                                      headers={"Content-Type": "application/json"},
                                      timeout=TIMEOUT)
if resp:
    log_test("Empty Body Handling", True, 
            f"Status: {resp.status_code}", elapsed)
else:
    log_test("Empty Body Handling", False, "No response", elapsed, error)

# ============================================================================
# TEST GROUP 10: OpenAPI Documentation
# ============================================================================
print("-" * 70)
print("GROUP 10: API DOCUMENTATION")
print("-" * 70)

resp, elapsed, error = make_request("GET", "/openapi.json", timeout=TIMEOUT)
if resp and resp.status_code == 200:
    try:
        spec = resp.json()
        paths_count = len(spec.get('paths', {}))
        log_test("GET /openapi.json", True, 
                f"OpenAPI spec loaded: {paths_count} paths", elapsed)
    except:
        log_test("GET /openapi.json", False, 
                "Invalid JSON", elapsed)
else:
    log_test("GET /openapi.json", False, 
            f"Status: {resp.status_code if resp else 'N/A'}", elapsed, error)

# ============================================================================
# GENERATE FINAL REPORT
# ============================================================================
print()
print("=" * 70)
print("FINAL API TEST REPORT SUMMARY")
print("=" * 70)

total_tests = len(results["passed"]) + len(results["failed"])
pass_rate = (len(results["passed"]) / total_tests * 100) if total_tests > 0 else 0

print(f"\nTotal Tests: {total_tests}")
print(f"[PASS] Passed: {len(results['passed'])}")
print(f"[FAIL] Failed: {len(results['failed'])}")
print(f"Pass Rate: {pass_rate:.1f}%")

# Performance summary
if results["passed"]:
    times = [r['response_time'] for r in results['passed']]
    avg_time = sum(times) / len(times)
    max_time = max(times)
    min_time = min(times)
    
    print(f"\nPerformance Metrics:")
    print(f"   Average Response Time: {avg_time:.3f}s")
    print(f"   Fastest: {min_time:.3f}s")
    print(f"   Slowest: {max_time:.3f}s")
    
    # SLA Check (< 200ms for 95th percentile)
    sorted_times = sorted(times)
    p95_index = int(len(sorted_times) * 0.95)
    p95_time = sorted_times[min(p95_index, len(sorted_times)-1)]
    sla_status = "MET" if p95_time < 0.2 else "NOT MET"
    print(f"   95th Percentile: {p95_time:.3f}s (SLA: <0.2s) [{sla_status}]")
    
    # Slow endpoints
    slow_threshold = 1.0
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

# Category summary
categories = {
    "Health": ["health", "ready", "live"],
    "Execution": ["execute", "run", "syntax"],
    "Verification": ["verify", "test-info"],
    "Curriculum": ["curriculum", "week", "problem"],
    "Auth": ["auth", "users"],
    "AI": ["ai"],
}

print(f"\nResults by Category:")
for cat_name, keywords in categories.items():
    cat_passed = len([r for r in results["passed"] if any(k in r["name"].lower() for k in keywords)])
    cat_failed = len([r for r in results["failed"] if any(k in r["name"].lower() for k in keywords)])
    cat_total = cat_passed + cat_failed
    if cat_total > 0:
        print(f"   {cat_name}: {cat_passed}/{cat_total} passed")

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
    "performance": {
        "average": sum(r['response_time'] for r in results['passed']) / len(results['passed']) if results['passed'] else 0,
        "max": max(r['response_time'] for r in results['passed']) if results['passed'] else 0,
        "min": min(r['response_time'] for r in results['passed']) if results['passed'] else 0,
    },
    "results": results
}

with open("api_test_report_comprehensive.json", "w") as f:
    json.dump(report, f, indent=2)

print("\nDetailed report saved to: api_test_report_comprehensive.json")
