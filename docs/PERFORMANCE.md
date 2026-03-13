# Performance Optimization Guide

This document outlines the performance optimizations implemented in the Python OOP Journey platform and provides guidance for maintaining and monitoring performance.

## Table of Contents

1. [Performance Targets](#performance-targets)
2. [Frontend Optimizations](#frontend-optimizations)
3. [Backend Optimizations](#backend-optimizations)
4. [Caching Strategy](#caching-strategy)
5. [Database Optimization](#database-optimization)
6. [Monitoring & Metrics](#monitoring--metrics)
7. [Production Checklist](#production-checklist)
8. [Troubleshooting](#troubleshooting)

## Performance Targets

### Core Web Vitals

| Metric | Target | Maximum |
|--------|--------|---------|
| LCP (Largest Contentful Paint) | < 2.0s | < 2.5s |
| FID (First Input Delay) | < 50ms | < 100ms |
| CLS (Cumulative Layout Shift) | < 0.05 | < 0.1 |
| FCP (First Contentful Paint) | < 1.0s | < 1.8s |
| TTFB (Time to First Byte) | < 400ms | < 800ms |
| INP (Interaction to Next Paint) | < 150ms | < 200ms |

### API Performance

| Endpoint Type | Target Response Time | P95 |
|--------------|---------------------|-----|
| Health Check | < 50ms | < 100ms |
| Curriculum Data | < 100ms | < 200ms |
| User Progress | < 100ms | < 300ms |
| Code Execution | < 5s | < 10s |
| Authentication | < 200ms | < 500ms |

## Frontend Optimizations

### Code Splitting & Lazy Loading

Components are dynamically loaded to reduce initial bundle size:

```typescript
// Lazy-loaded editor components
import { LazyCodeEditor, LazyPlayground, LazyMultiFileEditor } from '@/components/editor/lazy-editor';

// Lazy-loaded feature components
import { LazyDashboard, LazySearchDialog } from '@/components/lazy-components';
```

Key lazy-loaded components:
- Monaco Editor (500KB+ saved from initial bundle)
- Multi-file project editor
- Search dialog
- Dashboard components
- Verification panel

### Bundle Optimization

The Next.js configuration includes:

```javascript
// next.config.js optimizations
{
  output: 'standalone',
  experimental: {
    optimizePackageImports: ['lucide-react', '@radix-ui/*', 'date-fns'],
    optimizeCss: true,
  },
  webpack: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        monaco: { name: 'monaco-editor', test: /monaco-editor/ },
        vendor: { name: 'vendors', test: /node_modules/ },
        ui: { name: 'ui-components', test: /packages\/ui/ },
      }
    }
  }
}
```

### Image Optimization

- WebP format with AVIF fallback
- Responsive images with `sizes` attribute
- Lazy loading for below-fold images
- Blur placeholders for progressive loading

### Caching Headers

Static assets are cached for 1 year with immutable flag:
```
Cache-Control: public, max-age=31536000, immutable
```

## Backend Optimizations

### Response Compression

API responses are compressed using gzip or brotli:
- gzip level 6 (balanced compression/speed)
- brotli quality 4 (preferred if client supports)
- Minimum size: 500 bytes

### Rate Limiting

Configured per endpoint type:
- Public endpoints: 100 requests/minute
- Authenticated endpoints: 1000 requests/minute
- Code execution: 30 requests/minute
- Login attempts: 5 requests/minute

### Connection Pooling

Database connection pool settings:
- Pool size: 10 connections
- Max overflow: 20 connections
- Pool pre-ping: enabled
- Connection timeout: 30 seconds

## Caching Strategy

### Redis Cache

Cache configuration by data type:

| Data Type | TTL | Invalidation |
|-----------|-----|--------------|
| Curriculum | 1 hour | Manual on update |
| User Progress | 5 minutes | On update |
| Bookmarks | 5 minutes | On update |
| Activity | 1 minute | Real-time |
| Drafts | 1 minute | Real-time |
| Submissions | 1 minute | On update |
| Verification | 1 hour | Manual |

### CDN Caching

| Asset Type | Cache Duration |
|------------|----------------|
| Static files (JS, CSS) | 1 year |
| Images | 1 year |
| Curriculum JSON | 1 hour |
| API responses | Vary by endpoint |

### Cache Invalidation

Programmatic invalidation via tags:

```python
from api.middleware.cache import invalidate_user_cache, invalidate_curriculum_cache

# Invalidate all user data
await invalidate_user_cache(user_id)

# Invalidate curriculum cache
await invalidate_curriculum_cache()
```

## Database Optimization

### Indexes

Performance indexes created on frequently queried fields:

**Progress Table:**
- `idx_progress_user_problem` (user_id, problem_slug)
- `idx_progress_user_status` (user_id, status)
- `idx_progress_solved_at` (solved_at) - partial index

**Activity Table:**
- `idx_activity_user_created` (user_id, created_at)
- `idx_activity_type_created` (activity_type, created_at)

**Bookmarks Table:**
- `idx_bookmarks_user_type` (user_id, item_type)
- `idx_bookmarks_user_created` (user_id, created_at)

### Query Optimization

- Use `selectinload` for relationship loading
- Implement cursor pagination for large datasets
- Cache frequent query results
- Use database connection pooling

## Monitoring & Metrics

### Web Vitals Tracking

```typescript
import { reportWebVitals, initPerformanceMonitoring } from '@/lib/performance';

// Initialize monitoring
initPerformanceMonitoring();

// Report metrics
reportWebVitals({
  name: 'LCP',
  value: 1500,
  id: 'metric-id',
  rating: 'good'
});
```

### API Metrics

Health check endpoints:
- `GET /health` - Basic health status
- `GET /health/detailed` - Component health
- `GET /health/db` - Database connectivity
- `GET /health/cache` - Redis cache status
- `GET /health/ready` - Kubernetes readiness probe
- `GET /health/live` - Kubernetes liveness probe

### Logging

Performance-related logs:
- Cache hit/miss rates
- Database query times
- API response times
- Error rates by endpoint

## Production Checklist

### Environment Variables

```bash
# Required
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=redis://...

# Optional but recommended
NEXT_PUBLIC_API_URL=https://api.oopjourney.com
ANALYZE_BUNDLE=true  # For bundle analysis
```

### Build Verification

1. Run production build:
   ```bash
   cd apps/web
   npm run build
   ```

2. Analyze bundle size:
   ```bash
   npx @next/bundle-analyzer
   ```

3. Run Lighthouse CI:
   ```bash
   npm run lighthouse
   ```

### Pre-deployment Checks

- [ ] All Web Vitals meet targets
- [ ] API response times < 500ms (p95)
- [ ] No JavaScript errors in console
- [ ] Images optimized and lazy loading
- [ ] Service worker registered
- [ ] Redis cache connected
- [ ] Database migrations applied
- [ ] Health checks passing

## Troubleshooting

### Slow Page Load

1. Check bundle size:
   ```bash
   cd apps/web
   npm run build 2>&1 | grep -E "(First Load JS|chunks)"
   ```

2. Analyze with Lighthouse:
   - Run Chrome DevTools > Lighthouse
   - Check "Performance" tab
   - Look for long tasks in main thread

3. Common causes:
   - Large initial JS bundle → Enable code splitting
   - Unoptimized images → Use Next.js Image component
   - Blocking resources → Add resource hints

### High API Latency

1. Check database performance:
   ```python
   # Add query logging in config
   echo=True  # Log all SQL queries
   ```

2. Review slow query log in PostgreSQL

3. Check Redis cache hit rate:
   ```bash
   redis-cli INFO stats
   ```

4. Common causes:
   - Missing indexes → Check migration files
   - N+1 queries → Use `selectinload`
   - Cache misses → Review cache keys

### Memory Issues

1. Monitor container memory:
   ```bash
   docker stats
   ```

2. Check for memory leaks:
   - Node.js heap snapshots
   - Python tracemalloc

3. Common causes:
   - Unclosed database connections → Use context managers
   - Large cache entries → Set appropriate TTLs
   - Memory-intensive operations → Use streaming

### Cache Issues

1. Verify Redis connectivity:
   ```bash
   redis-cli ping
   ```

2. Check cache stats:
   ```bash
   redis-cli INFO keyspace
   ```

3. Clear cache if needed:
   ```bash
   redis-cli FLUSHDB
   ```

## Performance Budgets

| Resource | Budget | Warning |
|----------|--------|---------|
| Initial JS | 500KB | 400KB |
| Initial CSS | 100KB | 80KB |
| Images (total) | 2MB | 1.5MB |
| API response | 500ms | 300ms |
| Page load | 3s | 2s |

## Additional Resources

- [Next.js Performance Optimization](https://nextjs.org/docs/advanced-features/measuring-performance)
- [Web Vitals](https://web.dev/vitals/)
- [Redis Best Practices](https://redis.io/docs/manual/performance/)
- [PostgreSQL Performance](https://www.postgresql.org/docs/current/performance-tips.html)
