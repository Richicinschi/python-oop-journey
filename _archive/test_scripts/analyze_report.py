#!/usr/bin/env python3
import json

with open('api_test_report.json', 'r') as f:
    data = json.load(f)

print('=' * 70)
print('DETAILED API TEST FAILURES ANALYSIS')
print('=' * 70)

for test in data['tests']:
    if not test['passed']:
        print(f"\n[FAIL] {test['method']} {test['endpoint']}")
        print(f"  Category: {test['category']}")
        print(f"  Status Code: {test['status_code']}")
        print(f"  Response Time: {test['response_time_ms']}ms")
        if test['error']:
            print(f"  Error: {test['error'][:200]}")
        if test['response']:
            resp = test['response']
            if isinstance(resp, dict):
                if 'detail' in resp:
                    print(f"  Response Detail: {resp['detail']}")
                if 'message' in resp:
                    print(f"  Response Message: {resp['message']}")
                if 'error' in resp:
                    print(f"  Response Error: {resp['error']}")
            elif isinstance(resp, str):
                print(f"  Response: {resp[:200]}")

print("\n" + "=" * 70)
print("SUMMARY BY STATUS CODE")
print("=" * 70)

status_codes = {}
for test in data['tests']:
    code = test['status_code']
    if code not in status_codes:
        status_codes[code] = []
    status_codes[code].append(test['endpoint'])

for code in sorted(status_codes.keys()):
    print(f"\nStatus {code}: {len(status_codes[code])} endpoints")
    for ep in status_codes[code][:5]:
        print(f"  - {ep}")
    if len(status_codes[code]) > 5:
        print(f"  ... and {len(status_codes[code]) - 5} more")
