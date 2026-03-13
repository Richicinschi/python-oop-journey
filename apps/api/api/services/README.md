# Verification Service

The verification service provides test execution and learner-friendly feedback for the Python OOP Journey platform.

## Features

- **Test Loading**: Automatically loads test code from curriculum data
- **Safe Execution**: Runs code in a subprocess with timeouts and resource limits
- **Result Parsing**: Parses pytest output (JUnit XML) for detailed results
- **Error Categorization**: Classifies errors into learner-friendly categories
- **Hint Integration**: Suggests hints based on failure patterns
- **Progress Tracking**: Updates user progress when tests pass

## Usage

### Basic Verification

```python
from api.schemas.verification import VerificationRequest
from api.services.verification import VerificationService

service = VerificationService()

request = VerificationRequest(
    code="def add(a, b): return a + b",
    problem_slug="w01d01-hello-object"
)

result = await service.verify_solution(request)

print(f"Passed: {result.summary.passed}/{result.summary.total}")
for test in result.tests:
    print(f"  {test.name}: {test.status}")
```

### With Progress Update

```python
response = await service.verify_and_update_progress(
    request,
    user_id="user-123"
)

if response.progress_updated:
    print("Progress saved!")
```

## Error Categories

| Category | Description | Example Hint |
|----------|-------------|--------------|
| `wrong_return_value` | Function returns wrong value | "Double-check your logic and calculations" |
| `unexpected_exception` | Unhandled exception raised | "Check for edge cases like empty inputs" |
| `missing_implementation` | NotImplementedError present | "Remove 'raise NotImplementedError' and implement" |
| `timeout` | Execution timed out | "Check for infinite loops" |
| `syntax_error` | Python syntax error | "Check for missing colons or parentheses" |
| `import_error` | Module import failed | "Check module names are spelled correctly" |
| `assertion_error` | Test assertion failed | "Review test requirements" |

## API Endpoints

### POST /api/v1/verify

Verify solution against tests.

**Request:**
```json
{
  "code": "def add(a, b): return a + b",
  "problem_slug": "w01d01-hello-object",
  "test_code": "optional override"
}
```

**Response:**
```json
{
  "success": true,
  "summary": {
    "total": 3,
    "passed": 3,
    "failed": 0,
    "errors": 0
  },
  "tests": [
    {
      "name": "test_add_positive",
      "status": "passed",
      "duration_ms": 12.5
    }
  ],
  "suggested_hints": [
    {"hint_index": 0, "reason": "...", "confidence": "high"}
  ],
  "progress_updated": true,
  "attempts": 5
}
```

### POST /api/v1/validate-syntax

Validate code syntax without running tests.

### GET /api/v1/test-info/{problem_slug}

Get test metadata for a problem.

## Frontend Components

### VerificationPanel

Main panel displaying test results:

```tsx
import { VerificationPanel } from "@/components/verification";

<VerificationPanel
  verification={verificationData}
  isLoading={isLoading}
  onRetry={handleRetry}
  onGetHelp={handleGetHelp}
/>
```

### ProblemVerificationWrapper

Complete integration for problem pages:

```tsx
import { ProblemVerificationWrapper } from "@/components/verification";

<ProblemVerificationWrapper
  problemSlug="w01d01-hello-object"
  code={editorCode}
  onGetHint={(index) => showHint(index)}
/>
```

## Testing

Run verification service tests:

```bash
cd website-playground/apps/api
python -m pytest api/tests/test_verification.py -v
```

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Frontend       │────▶│  API Endpoint    │────▶│  Verification   │
│  Components     │     │  /api/v1/verify  │     │  Service        │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                         │
                              ┌─────────────────────────┼─────────────────────────┐
                              │                         │                         │
                              ▼                         ▼                         ▼
                    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
                    │  Curriculum      │    │  Execution       │    │  Result          │
                    │  Service         │    │  Service         │    │  Parser          │
                    │  (get tests)     │    │  (run pytest)    │    │  (parse output)  │
                    └──────────────────┘    └──────────────────┘    └──────────────────┘
```

## Security Considerations

1. **Subprocess Sandboxing**: Code runs in subprocess with timeouts
2. **Resource Limits**: Memory and CPU limits should be enforced
3. **No Network Access**: Code should not have network access
4. **Restricted Imports**: Dangerous modules are restricted
5. **Temporary Files**: All files are created in temp directories

## Future Improvements

- [ ] Docker-based sandboxing for better isolation
- [ ] Async job queue for long-running tests
- [ ] Caching of test results
- [ ] More sophisticated hint suggestion ML
- [ ] Code similarity detection for plagiarism
