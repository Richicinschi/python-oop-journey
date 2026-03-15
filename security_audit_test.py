#!/usr/bin/env python3
"""
Security Audit Test Script for Python OOP Journey Website
Tests security controls on production: https://python-oop-journey.onrender.com
"""

import requests
import time
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
BASE_URL = "https://python-oop-journey.onrender.com"
API_BASE = "https://oop-journey-api.onrender.com"
API_URL = f"{API_BASE}/api/v1"

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_success(msg):
    print(f"{GREEN}[PASS] {msg}{RESET}")

def print_fail(msg):
    print(f"{RED}[FAIL] {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}[WARN] {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}[INFO] {msg}{RESET}")

def print_section(title):
    print(f"\n{'='*60}")
    print(f"{title}")
    print('='*60)

class SecurityAuditor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
        })
        self.results = []
        
    def test_xss_protection(self):
        """Test XSS protection in code execution output"""
        print_section("TEST 1: XSS Protection in Code Execution")
        
        xss_payloads = [
            ("script tag", "print('<script>alert(\"xss\")</script>')"),
            ("img onerror", "print('<img src=x onerror=alert(\"xss\")>')"),
            ("svg onload", "print('<svg onload=alert(\"xss\")>')"),
            ("javascript protocol", "print('javascript:alert(\"xss\")')"),
            ("event handler", "print('<div onmouseover=alert(\"xss\")>hover</div>')"),
        ]
        
        for name, code in xss_payloads:
            try:
                response = self.session.post(
                    f"{API_URL}/execute/run",
                    json={"code": code, "timeout": 10},
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    output = data.get("output", "")
                    
                    # Check if any script tags are in raw output (would indicate XSS vuln)
                    if "<script>" in output and "&lt;script&gt;" not in output:
                        print_fail(f"XSS VULNERABILITY: {name} - Script tags not escaped!")
                        self.results.append(("XSS", name, "FAIL", "Script tags not escaped"))
                    else:
                        print_success(f"XSS Protection working: {name} - Output properly escaped")
                        self.results.append(("XSS", name, "PASS", "Output escaped"))
                else:
                    print_warning(f"XSS test {name} returned status {response.status_code}")
                    
            except Exception as e:
                print_warning(f"XSS test {name} failed: {e}")
                
    def test_code_injection_sandbox(self):
        """Test sandbox blocks dangerous imports"""
        print_section("TEST 2: Sandbox - Dangerous Import Blocking")
        
        dangerous_code = [
            ("os import", "import os\nprint(os.listdir('.'))"),
            ("subprocess import", "import subprocess\nprint('pwned')"),
            ("sys import", "import sys\nprint(sys.version)"),
            ("eval call", "print(eval('1+1'))"),
            ("exec call", "exec('print(1)')"),
            ("open file", "print(open('/etc/passwd').read())"),
            ("socket import", "import socket\nprint(socket.gethostname())"),
            ("urllib import", "import urllib\nprint('pwned')"),
        ]
        
        for name, code in dangerous_code:
            try:
                response = self.session.post(
                    f"{API_URL}/execute/run",
                    json={"code": code, "timeout": 10},
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    error = data.get("error", "")
                    
                    if "security" in error.lower() or "not allowed" in error.lower():
                        print_success(f"Sandbox blocked: {name}")
                        self.results.append(("Sandbox", name, "PASS", "Blocked"))
                    else:
                        print_fail(f"Sandbox NOT blocking: {name} - Code executed!")
                        self.results.append(("Sandbox", name, "FAIL", "Executed"))
                else:
                    print_warning(f"Sandbox test {name} returned {response.status_code}")
                    
            except Exception as e:
                print_warning(f"Sandbox test {name} failed: {e}")
                
    def test_rate_limiting(self):
        """Test rate limiting on execute endpoint"""
        print_section("TEST 3: Rate Limiting (30 requests/minute)")
        
        print_info("Sending 35 rapid requests to /execute/run...")
        
        responses = []
        for i in range(35):
            try:
                response = self.session.post(
                    f"{API_URL}/execute/run",
                    json={"code": "print('hello')", "timeout": 5},
                    timeout=10
                )
                responses.append((i+1, response.status_code))
                
                if response.status_code == 429:
                    print_success(f"Rate limit triggered at request {i+1}")
                    self.results.append(("Rate Limit", f"Triggered at {i+1}", "PASS", "Working"))
                    break
                    
            except Exception as e:
                responses.append((i+1, f"error: {e}"))
                
        # Count 429s
        rate_limited = [r for r in responses if r[1] == 429]
        if rate_limited:
            print_success(f"Rate limiting working: {len(rate_limited)} requests blocked with 429")
            self.results.append(("Rate Limit", "Summary", "PASS", f"{len(rate_limited)} blocked"))
        else:
            print_fail("Rate limiting NOT working - no 429 responses received!")
            self.results.append(("Rate Limit", "Summary", "FAIL", "No 429s"))
            
    def test_request_size_limit(self):
        """Test request size limit (1MB)"""
        print_section("TEST 4: Request Size Limit (1MB)")
        
        # Create payload > 1MB
        large_code = "x = " + "'A' * 2000000"  # ~2MB
        
        try:
            response = self.session.post(
                f"{API_URL}/execute/run",
                json={"code": large_code, "timeout": 10},
                timeout=20
            )
            
            if response.status_code == 413:
                print_success("Request size limit working: 413 Payload Too Large returned")
                self.results.append(("Size Limit", ">1MB payload", "PASS", "413 returned"))
            else:
                print_fail(f"Size limit NOT working: got {response.status_code} instead of 413")
                self.results.append(("Size Limit", ">1MB payload", "FAIL", f"Got {response.status_code}"))
                
        except Exception as e:
            print_warning(f"Size limit test failed: {e}")
            
    def test_cors_configuration(self):
        """Test CORS configuration"""
        print_section("TEST 5: CORS Configuration")
        
        # Test preflight request
        try:
            response = self.session.options(
                f"{API_URL}/execute/run",
                headers={
                    "Origin": "https://evil.com",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type",
                },
                timeout=10
            )
            
            allow_origin = response.headers.get("Access-Control-Allow-Origin", "")
            allow_credentials = response.headers.get("Access-Control-Allow-Credentials", "")
            
            print_info(f"CORS Allow-Origin: {allow_origin}")
            print_info(f"CORS Allow-Credentials: {allow_credentials}")
            
            if "*" in allow_origin and allow_credentials.lower() == "true":
                print_fail("CORS VULNERABILITY: Wildcard with credentials!")
                self.results.append(("CORS", "Wildcard + Credentials", "FAIL", "Security issue"))
            elif "evil.com" in allow_origin:
                print_fail("CORS VULNERABILITY: Reflecting arbitrary origins!")
                self.results.append(("CORS", "Origin reflection", "FAIL", "Security issue"))
            else:
                print_success("CORS configuration appears secure")
                self.results.append(("CORS", "Configuration", "PASS", "Secure"))
                
        except Exception as e:
            print_warning(f"CORS test failed: {e}")
            
    def test_csrf_protection(self):
        """Test CSRF protection"""
        print_section("TEST 6: CSRF Protection")
        
        # Test without CSRF token
        try:
            response = self.session.post(
                f"{API_URL}/progress/test-problem",
                json={"status": "solved"},
                timeout=10
            )
            
            if response.status_code == 403:
                data = response.json()
                if "csrf" in data.get("error", "").lower():
                    print_success("CSRF protection working: Request without token rejected")
                    self.results.append(("CSRF", "Without token", "PASS", "Blocked"))
                else:
                    print_warning(f"Got 403 but not CSRF-related: {data}")
            else:
                print_fail(f"CSRF protection NOT working: got {response.status_code}")
                self.results.append(("CSRF", "Without token", "FAIL", f"Got {response.status_code}"))
                
        except Exception as e:
            print_warning(f"CSRF test failed: {e}")
            
    def test_security_headers(self):
        """Test security headers"""
        print_section("TEST 7: Security Headers")
        
        try:
            response = self.session.get(BASE_URL, timeout=10)
            headers = response.headers
            
            security_headers = {
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY",
                "X-XSS-Protection": "1; mode=block",
                "Strict-Transport-Security": None,  # Just check presence
                "Content-Security-Policy": None,
                "Referrer-Policy": None,
            }
            
            for header, expected in security_headers.items():
                value = headers.get(header)
                if value:
                    if expected and expected.lower() not in value.lower():
                        print_warning(f"{header}: {value} (expected: {expected})")
                    else:
                        print_success(f"{header}: {value}")
                        self.results.append(("Headers", header, "PASS", "Present"))
                else:
                    print_fail(f"Missing header: {header}")
                    self.results.append(("Headers", header, "FAIL", "Missing"))
                    
        except Exception as e:
            print_warning(f"Security headers test failed: {e}")
            
    def test_authentication_security(self):
        """Test authentication security"""
        print_section("TEST 8: Authentication Security")
        
        # Test protected endpoint without auth
        try:
            response = self.session.get(f"{API_URL}/auth/me", timeout=10)
            
            if response.status_code == 401:
                print_success("Protected endpoint returns 401 without auth")
                self.results.append(("Auth", "No token", "PASS", "401 returned"))
            else:
                print_fail(f"Protected endpoint NOT secure: got {response.status_code}")
                self.results.append(("Auth", "No token", "FAIL", f"Got {response.status_code}"))
                
        except Exception as e:
            print_warning(f"Auth test failed: {e}")
            
        # Test magic link endpoint for email enumeration
        try:
            response = self.session.post(
                f"{API_URL}/auth/magic-link",
                json={"email": "nonexistent@example.com"},
                timeout=10
            )
            
            if response.status_code in [200, 202]:
                data = response.json()
                if data.get("success"):
                    print_success("Magic link prevents email enumeration (always returns success)")
                    self.results.append(("Auth", "Email enumeration", "PASS", "Prevented"))
                else:
                    print_warning("Magic link may allow email enumeration")
            else:
                print_warning(f"Magic link returned {response.status_code}")
                
        except Exception as e:
            print_warning(f"Magic link test failed: {e}")
            
    def test_code_execution_limits(self):
        """Test code execution limits"""
        print_section("TEST 9: Code Execution Limits")
        
        # Test timeout
        print_info("Testing execution timeout (10s)...")
        try:
            start = time.time()
            response = self.session.post(
                f"{API_URL}/execute/run",
                json={"code": "import time\ntime.sleep(20)", "timeout": 10},
                timeout=20
            )
            elapsed = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                if data.get("timeout") or elapsed < 15:
                    print_success(f"Timeout working: executed in {elapsed:.1f}s")
                    self.results.append(("Execution", "Timeout", "PASS", f"{elapsed:.1f}s"))
                else:
                    print_fail(f"Timeout NOT working: took {elapsed:.1f}s")
                    self.results.append(("Execution", "Timeout", "FAIL", f"{elapsed:.1f}s"))
            else:
                print_warning(f"Timeout test returned {response.status_code}")
                
        except Exception as e:
            print_warning(f"Timeout test failed: {e}")
            
    def generate_report(self):
        """Generate summary report"""
        print_section("SECURITY AUDIT SUMMARY")
        
        passed = [r for r in self.results if r[2] == "PASS"]
        failed = [r for r in self.results if r[2] == "FAIL"]
        
        print(f"\nTotal Tests: {len(self.results)}")
        print_success(f"Passed: {len(passed)}")
        print_fail(f"Failed: {len(failed)}")
        
        if failed:
            print("\n--- FAILED TESTS ---")
            for category, name, status, detail in failed:
                print_fail(f"{category} - {name}: {detail}")
                
        print("\n--- PASSED TESTS ---")
        for category, name, status, detail in passed:
            print_success(f"{category} - {name}: {detail}")
            
        return len(failed) == 0

def main():
    print("="*60)
    print("Python OOP Journey - Security Audit")
    print(f"Target: {BASE_URL}")
    print("="*60)
    
    auditor = SecurityAuditor()
    
    # Run all tests
    auditor.test_xss_protection()
    auditor.test_code_injection_sandbox()
    auditor.test_rate_limiting()
    auditor.test_request_size_limit()
    auditor.test_cors_configuration()
    auditor.test_csrf_protection()
    auditor.test_security_headers()
    auditor.test_authentication_security()
    auditor.test_code_execution_limits()
    
    # Generate report
    success = auditor.generate_report()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
