"""Final API Testing - Verify All Endpoints Work"""
import requests
import json
import sys

BASE_URL = 'http://localhost:8000'
results = []

def test_endpoint(name, method, path, payload=None, expected_status=200):
    """Test an endpoint and record result."""
    url = f'{BASE_URL}{path}'
    try:
        if method == 'GET':
            response = requests.get(url, timeout=10)
        elif method == 'POST':
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
        else:
            response = requests.request(method, url, json=payload, timeout=10)
        
        success = response.status_code == expected_status
        status = 'PASS' if success else 'FAIL'
        
        try:
            response_data = response.json()
        except:
            response_data = response.text[:200]
        
        results.append({
            'name': name,
            'method': method,
            'path': path,
            'expected': expected_status,
            'actual': response.status_code,
            'status': status,
            'response': response_data
        })
        print(f'  [{status}] {method} {path} -> {response.status_code}')
        return response, success
    except Exception as e:
        results.append({
            'name': name,
            'method': method,
            'path': path,
            'expected': expected_status,
            'actual': 'ERROR',
            'status': 'ERROR',
            'response': str(e)
        })
        print(f'  [ERROR] {method} {path} -> {e}')
        return None, False

def main():
    print('='*70)
    print('API FINAL TESTING REPORT - API Tester Agent')
    print('='*70)
    print(f'Base URL: {BASE_URL}')
    print()
    
    # Health Checks
    print('--- Health Checks ---')
    test_endpoint('Health Check', 'GET', '/health')
    test_endpoint('Health DB Check', 'GET', '/health/db')
    
    # Code Execution
    print()
    print('--- Code Execution ---')
    test_endpoint('Execute Code', 'POST', '/api/v1/execute/run', {
        'code': 'print("Hello World")',
        'language': 'python'
    })
    test_endpoint('Syntax Check Valid', 'POST', '/api/v1/execute/syntax-check', {
        'code': 'print("Hello World")',
        'language': 'python'
    })
    test_endpoint('Syntax Check Invalid', 'POST', '/api/v1/execute/syntax-check', {
        'code': 'print("Hello World"',
        'language': 'python'
    })
    
    # Verification
    print()
    print('--- Verification ---')
    test_endpoint('Validate Syntax', 'POST', '/api/v1/validate-syntax', {
        'code': 'def add(a, b): return a + b'
    })
    
    # Curriculum
    print()
    print('--- Curriculum ---')
    test_endpoint('Get Curriculum', 'GET', '/api/v1/curriculum')
    test_endpoint('List Problems', 'GET', '/api/v1/curriculum/problems')
    
    # Summary
    print()
    print('='*70)
    print('TEST SUMMARY')
    print('='*70)
    
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    errors = sum(1 for r in results if r['status'] == 'ERROR')
    total = len(results)
    
    print(f'Total Tests:  {total}')
    print(f'Passed:       {passed}')
    print(f'Failed:       {failed}')
    print(f'Errors:       {errors}')
    print(f'Success Rate: {passed/total*100:.1f}%')
    print()
    
    # Print detailed results for failures
    if failed > 0 or errors > 0:
        print('FAILED/ERROR DETAILS:')
        print('-'*70)
        for r in results:
            if r['status'] != 'PASS':
                print(f"  Endpoint: {r['name']}")
                print(f"  Method:   {r['method']} {r['path']}")
                print(f"  Expected: {r['expected']}, Got: {r['actual']}")
                print(f"  Response: {r['response']}")
                print()
    
    # Show sample successful responses
    print()
    print('SAMPLE SUCCESSFUL RESPONSES:')
    print('-'*70)
    for r in results:
        if r['status'] == 'PASS':
            print(f"\n{r['name']} ({r['method']} {r['path']}):")
            print(json.dumps(r['response'], indent=2)[:500])
            break  # Just show first one
    
    print()
    print('='*70)
    if failed == 0 and errors == 0:
        print('STATUS: ALL TESTS PASSED')
        print('='*70)
        return 0
    else:
        print(f'STATUS: {failed + errors} TEST(S) FAILED')
        print('='*70)
        return 1

if __name__ == '__main__':
    sys.exit(main())
