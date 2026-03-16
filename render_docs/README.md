# Render Documentation

This folder contains Render platform documentation for troubleshooting deployment issues.

## Files

| File | Description | Source |
|------|-------------|--------|
| [environment-variables.md](environment-variables.md) | How to configure env vars, secret files, and environment groups | https://render.com/docs/configure-environment-variables |
| [deploys.md](deploys.md) | Auto-deploys, manual deploys, deploy steps, zero-downtime deploys | https://render.com/docs/deploys |
| [language-support.md](language-support.md) | Supported languages, version management, runtime configuration | https://render.com/docs/language-support |
| [TROUBLESHOOTING_DEPLOYS.md](../TROUBLESHOOTING_DEPLOYS.md) | Main troubleshooting guide with common errors and solutions | Original |

## Quick Reference

### Setting Environment Variables
```
Key: DATABASE_URL
Value: postgresql+asyncpg://user:pass@host:26257/db?sslmode=require
```

### Python Version
Set `PYTHON_VERSION=3.11.0` in environment variables.

### Deploy Failure?
1. Check logs in Render Dashboard
2. Verify all environment variables are set
3. Check that start command is correct
4. Ensure app binds to `0.0.0.0` and uses `$PORT`

### Common Errors
- **ModuleNotFoundError** - Missing dependency in requirements.txt
- **Exit status 1** - Check logs for specific error
- **Timeout** - App didn't start within 60 seconds
