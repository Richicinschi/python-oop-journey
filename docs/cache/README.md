# Upstash Redis Documentation

## Quick Reference

### Connection URL
```
rediss://default:<token>@<host>:6379
```

**Note:** Use `rediss://` (double s) for SSL/TLS encryption.

### Our Connection
```
rediss://default:<token>@refined-gibbon-70439.upstash.io:6379
```

## Free Tier Limits

| Metric | Limit |
|--------|-------|
| **Commands** | 10,000/day |
| **Bandwidth** | 50 GB/month |
| **Storage** | 256 MB |
| **Cost** | $0 |

## Use Cases

1. **Session Storage** - User login sessions
2. **Caching** - API response caching
3. **Rate Limiting** - API rate limit counters
4. **Background Jobs** - Celery task queue
5. **Real-time Features** - WebSocket state

## Dashboard

URL: https://console.upstash.com/redis

### Key Sections
- **Details:** Connection info, token
- **Usage:** Command counts, bandwidth
- **CLI:** Test commands
- **Data Browser:** View stored data

## Common Commands

```bash
# Test connection (local)
redis-cli --tls -u rediss://default:<token>@host:6379 ping

# Set a key
SET user:123 "data"

# Get a key
GET user:123

# Set with expiry (1 hour)
SET session:abc "data" EX 3600

# Delete key
DEL user:123
```

## Python Usage (redis-py)

```python
import redis

# Connect
r = redis.from_url("rediss://default:<token>@host:6379")

# Set value
r.set("key", "value")

# Get value
value = r.get("key")

# Set with expiry
r.setex("session", 3600, "user_data")
```

## Troubleshooting

### "Connection refused"
- Check if using `rediss://` (SSL)
- Verify token is correct
- Check if port is 6379

### "Max connections reached"
- Use connection pooling
- Close connections when done
- Check for connection leaks

### "Out of memory"
- Free tier limited to 256MB
- Set TTL on keys
- Use LRU eviction policy

## Best Practices

1. **Always use SSL** (`rediss://`)
2. **Set TTL on keys** - Prevents memory issues
3. **Use connection pooling** - Better performance
4. **Handle connection errors** - Graceful degradation
5. **Monitor usage** - Stay within free tier
