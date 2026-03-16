# Kimi Claw Configuration

This folder contains configuration for Kimi Claw development environment.

## Files

- `soul.yaml` - Project configuration and service definitions

## Usage

When opening this project in Kimi Claw, it will automatically:
1. Detect the project structure
2. Install required dependencies
3. Set up development environment
4. Start backend and frontend services

## Development

```bash
# Start all services
claw dev

# Build for production
claw build

# Run tests
claw test

# View logs
claw logs
```

## Ports

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
