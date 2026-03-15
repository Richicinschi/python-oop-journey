# Piston Code Execution Setup

This directory contains the configuration for deploying Piston - a self-hosted code execution engine - to Render.

## What is Piston?

Piston is a high-performance code execution engine that runs code in isolated environments via Docker containers. It provides a REST API for executing code in various languages.

- GitHub: https://github.com/engineer-man/piston
- API Docs: https://piston.readthedocs.io/

## Why Piston?

Render's free web services don't support running Docker containers inside them (Docker-in-Docker). Piston solves this by:

1. Running as a separate Docker service on Render
2. Providing a REST API for code execution
3. Supporting multiple language runtimes (Python, JavaScript, etc.)

## Deployment Steps

### 1. Deploy Piston to Render

Option A: Using Render Dashboard (Manual)
1. Go to Render Dashboard → New → Web Service
2. Connect your GitHub repo
3. Select "Docker" runtime
4. Set root directory: `./piston`
5. Set Docker build context: `./piston`
6. Deploy

Option B: Using Blueprint (render-piston.yaml)
```bash
# In Render dashboard, use the blueprint to auto-deploy
curl -X POST \
  https://api.render.com/v1/services \
  -H "Authorization: Bearer <RENDER_API_KEY>" \
  -H "Content-Type: application/json" \
  -d @render-piston.yaml
```

### 2. Install Python Runtime

After Piston is deployed, you need to install the Python runtime:

```bash
# SSH into the Piston container (via Render dashboard)
# Then run:
ppman install python 3.12.0
```

Or via API:
```bash
curl -X POST https://your-piston-service.onrender.com/api/v2/packages \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "version": "3.12.0"
  }'
```

### 3. Configure Backend

Set environment variable in your backend service:

```bash
USE_PISTON=true
PISTON_API_URL=https://your-piston-service.onrender.com
```

### 4. Test

```bash
curl -X POST https://your-piston-service.onrender.com/api/v2/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "version": "3.12.0",
    "files": [{"content": "print(\"Hello from Piston!\")"}]
  }'
```

## Local Development

Run Piston locally with Docker:

```bash
cd piston
docker-compose up -d

# Install Python runtime
docker exec -it piston-api ppman install python 3.12.0

# Test
curl -X POST http://localhost:2000/api/v2/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "version": "3.12.0",
    "files": [{"content": "print(1+1)"}]
  }'
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/v2/runtimes` | List installed runtimes |
| `POST /api/v2/execute` | Execute code |
| `GET /api/v2/packages` | List available packages |

## Troubleshooting

### Piston container fails to start
- Check logs in Render dashboard
- Ensure port 2000 is exposed
- Verify Docker build succeeds

### Python runtime not found
- Run `ppman install python 3.12.0` in container
- Check with `GET /api/v2/runtimes`

### Execution timeout
- Adjust `PISTON_RUN_TIMEOUT` in environment variables
- Default is 10 seconds

## Costs

- Render Docker service: Free tier available
- Piston runs efficiently on 512MB RAM / 0.5 CPU
- Multiple concurrent executions supported

## Security

Piston runs code in isolated containers with:
- Network isolation
- Resource limits (CPU, memory)
- Time limits
- No persistent storage

For production, consider:
- Rate limiting
- Authentication
- Input validation
