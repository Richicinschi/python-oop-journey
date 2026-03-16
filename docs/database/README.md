# CockroachDB Documentation

## Quick Reference

### Connection URL Format
```
postgresql://<username>:<password>@<host>:<port>/<database>?<parameters>
```

### Our Connection
```
postgresql+asyncpg://richicinschi_user:<password>@<host>:26257/defaultdb?ssl=require
```

**Note:** Use `ssl=require` not `sslmode=require` for asyncpg driver.

## Connection Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `username` | SQL user | No |
| `password` | User password | No |
| `host` | Hostname or IP | Yes |
| `port` | Port (default: 26257) | Yes |
| `database` | Database name | No (defaults to `defaultdb`) |
| `ssl` | SSL mode for asyncpg | Yes |

## SSL Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `disable` | No encryption | Development only |
| `require` | Force SSL | Production (what we use) |
| `verify-ca` | Verify CA cert | High security |
| `verify-full` | Full verification | Maximum security |

## Common Issues & Solutions

### Issue: "sslmode got unexpected keyword argument"
**Solution:** Use `ssl=require` not `sslmode=require` for asyncpg

### Issue: "Could not determine version from string 'CockroachDB CCL v25.4.1'"
**Solution:** Added version detection patch in `database.py`:
```python
# Returns (14, 0, 0) for CockroachDB compatibility
```

### Issue: "relation 'users' does not exist"
**Solution:** Check migration order - create parent tables before child tables

## Free Tier Limits

- **Storage:** 5GB
- **Request Units:** 50 million/month
- **Connections:** Unlimited
- **Databases:** 1 cluster per account

## Useful Links

- Dashboard: https://cockroachlabs.cloud
- Connection: SQL Shell or connection string
- Region: Frankfurt (eu-central-1)

## Migration Best Practices

1. Always create parent tables first (users before auth_tokens)
2. Use `down_revision` to link migrations in order
3. Test migrations locally before deploying
4. Keep migrations idempotent (can run multiple times safely)
