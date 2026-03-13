# Code Execution Backend

This directory contains the secure Python code execution system for the website playground.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Client    │────▶│  FastAPI     │────▶│  Execution      │
│  (Browser)  │     │  Endpoints   │     │  Service        │
└─────────────┘     └──────────────┘     └────────┬────────┘
                           │                       │
                           ▼                       ▼
                    ┌──────────────┐     ┌─────────────────┐
                    │   Celery     │     │  Docker Runner  │
                    │   (Async)    │     │                 │
                    └──────────────┘     └────────┬────────┘
                           │                       │
                           └───────────────────────┘
                                                   │
                                                   ▼
                                          ┌─────────────────┐
                                          │  Docker Sandbox │
                                          │  (Restricted)   │
                                          └─────────────────┘
```

## Security Features

### Docker Sandbox
- **No Network Access**: Containers run with `network_mode=none`
- **Read-Only Filesystem**: Root filesystem is mounted read-only
- **No Privileges**: All Linux capabilities are dropped
- **Resource Limits**: 
  - 256MB RAM limit
  - 0.5 CPU cores limit
  - 10 second default timeout (configurable up to 60s)
- **Non-Root User**: Code runs as unprivileged `sandbox` user
- **Container Isolation**: Fresh container per execution, destroyed after

### Rate Limiting
- 10 executions per minute per user/IP
- Automatic tracking and enforcement

### Input Validation
- Maximum code length: 10,000 characters
- Syntax validation before execution
- Empty code rejection

## API Endpoints

### Execute Code (Synchronous)
```http
POST /api/v1/execute/run
Content-Type: application/json

{
  "code": "print('Hello, World!')",
  "timeout": 10
}
```

Response:
```json
{
  "success": true,
  "output": "Hello, World!\n",
  "error": null,
  "execution_time_ms": 150,
  "exit_code": 0,
  "timeout": false
}
```

### Execute Code (Asynchronous)
```http
POST /api/v1/execute/async
Content-Type: application/json

{
  "code": "print('Hello, World!')",
  "timeout": 10
}
```

Response:
```json
{
  "job_id": "abc-123",
  "status": "pending",
  "message": "Job submitted successfully",
  "result_url": "/api/v1/execute/jobs/abc-123"
}
```

### Check Job Result
```http
GET /api/v1/execute/jobs/abc-123
```

### Execute with Tests
```http
POST /api/v1/execute/validate
Content-Type: application/json

{
  "code": "def add(a, b): return a + b",
  "test_code": "print(add(2, 3))",
  "timeout": 10
}
```

### Check Syntax
```http
POST /api/v1/execute/syntax-check
Content-Type: application/json

{
  "code": "print('hello')"
}
```

### Get Metrics
```http
GET /api/v1/execute/metrics?hours=24
```

### Health Check
```http
GET /api/v1/execute/health
```

## Setup

### 1. Build Sandbox Image

```bash
cd website-playground/apps/api
docker build -f sandbox.Dockerfile -t oop-journey-sandbox:latest .
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Infrastructure (Optional)

```bash
# Start Redis and PostgreSQL
docker-compose up -d redis db

# Start Celery worker
celery -A api.celery_app worker --loglevel=info

# Start Celery beat (for scheduled tasks)
celery -A api.celery_app beat --loglevel=info
```

### 4. Start API Server

```bash
# Development
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## Testing

### Run Unit Tests
```bash
pytest api/tests/test_execution.py -v
```

### Run Integration Tests (Requires Docker)
```bash
pytest api/tests/test_execution.py -v -m integration
```

### Run Security Tests
```bash
pytest api/tests/test_execution.py::TestSecurity -v
```

### Manual Testing with curl
```bash
# Simple execution
curl -X POST http://localhost:8000/api/v1/execute/run \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello\")"}'

# Timeout test
curl -X POST http://localhost:8000/api/v1/execute/run \
  -H "Content-Type: application/json" \
  -d '{"code": "import time; time.sleep(20)", "timeout": 5}'

# Syntax error
curl -X POST http://localhost:8000/api/v1/execute/run \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"hello"}'

# Network access test (should fail)
curl -X POST http://localhost:8000/api/v1/execute/run \
  -H "Content-Type: application/json" \
  -d '{"code": "import urllib.request; print(urllib.request.urlopen(\"http://example.com\").read())"}'
```

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `SANDBOX_IMAGE` | `oop-journey-sandbox:latest` | Docker image for sandbox |
| `DOCKER_HOST` | - | Docker daemon socket |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection URL |
| `MAX_CODE_LENGTH` | `10000` | Maximum code length |
| `DOCKER_TIMEOUT` | `30` | Default timeout seconds |

## Monitoring

### View Metrics
```python
from api.services.monitoring import get_monitor

monitor = get_monitor()
metrics = monitor.get_metrics(hours=24)
print(f"Total executions: {metrics.total_executions}")
print(f"Failure rate: {metrics.failure_rate}%")
```

### View Error Breakdown
```python
errors = monitor.get_error_breakdown(hours=24)
for error_type, count in errors.items():
    print(f"{error_type}: {count}")
```

### Flower (Celery Monitoring)
Access at http://localhost:5555 when running with docker-compose.

## Troubleshooting

### "Sandbox image not available"
Build the sandbox image:
```bash
docker build -f sandbox.Dockerfile -t oop-journey-sandbox:latest .
```

### "Docker not available"
- Ensure Docker is running
- Check `DOCKER_HOST` environment variable
- Verify Docker socket permissions

### High memory usage
- Reduce concurrent Celery workers
- Lower container memory limits
- Enable container cleanup

### Rate limit exceeded
Default is 10 executions per minute. Adjust in `monitoring.py`:
```python
MAX_EXECUTIONS_PER_WINDOW = 10
```

## Security Considerations

1. **Never expose Docker socket directly** - Use docker-socket-proxy or TLS
2. **Keep sandbox image minimal** - Reduce attack surface
3. **Monitor for abuse** - Check metrics regularly
4. **Update regularly** - Keep Docker and base images updated
5. **Use production Docker settings** - Enable user namespaces, seccomp, apparmor

## License

MIT
