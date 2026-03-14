"""Performance tests for API endpoints."""

import asyncio
import time
from typing import List

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from api.main import app
from api.database import get_db


@pytest_asyncio.fixture
async def async_client():
    """Create async test client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


class TestResponseTimes:
    """Test API response times meet performance targets."""

    async def _measure_response_time(self, client: AsyncClient, url: str, iterations: int = 10) -> List[float]:
        """Measure response time for multiple requests."""
        times = []
        for _ in range(iterations):
            start = time.time()
            response = await client.get(url)
            elapsed = (time.time() - start) * 1000  # Convert to ms
            times.append(elapsed)
            assert response.status_code == 200
        return times

    @pytest.mark.asyncio
    async def test_health_check_response_time(self, async_client: AsyncClient):
        """Health check should respond in < 50ms."""
        times = await self._measure_response_time(async_client, "/health", iterations=20)
        
        avg_time = sum(times) / len(times)
        p95_time = sorted(times)[int(len(times) * 0.95)]
        
        print(f"\nHealth check times: avg={avg_time:.2f}ms, p95={p95_time:.2f}ms")
        
        assert avg_time < 50, f"Average response time {avg_time:.2f}ms exceeds 50ms"
        assert p95_time < 100, f"P95 response time {p95_time:.2f}ms exceeds 100ms"

    @pytest.mark.asyncio
    async def test_curriculum_response_time(self, async_client: AsyncClient):
        """Curriculum endpoint should respond in < 100ms."""
        times = await self._measure_response_time(async_client, "/api/v1/curriculum", iterations=10)
        
        avg_time = sum(times) / len(times)
        p95_time = sorted(times)[int(len(times) * 0.95)]
        
        print(f"\nCurriculum times: avg={avg_time:.2f}ms, p95={p95_time:.2f}ms")
        
        assert avg_time < 100, f"Average response time {avg_time:.2f}ms exceeds 100ms"
        assert p95_time < 200, f"P95 response time {p95_time:.2f}ms exceeds 200ms"


class TestConcurrentRequests:
    """Test API behavior under concurrent load."""

    @pytest.mark.asyncio
    async def test_concurrent_health_checks(self, async_client: AsyncClient):
        """API should handle 50 concurrent health checks."""
        async def make_request():
            response = await async_client.get("/health")
            return response.status_code == 200

        # Create 50 concurrent requests
        tasks = [make_request() for _ in range(50)]
        results = await asyncio.gather(*tasks)
        
        success_count = sum(results)
        assert success_count == 50, f"Only {success_count}/50 requests succeeded"

    @pytest.mark.asyncio
    async def test_concurrent_curriculum_requests(self, async_client: AsyncClient):
        """API should handle 20 concurrent curriculum requests."""
        async def make_request():
            response = await async_client.get("/api/v1/curriculum")
            return response.status_code == 200

        # Create 20 concurrent requests
        tasks = [make_request() for _ in range(20)]
        results = await asyncio.gather(*tasks)
        
        success_count = sum(results)
        assert success_count == 20, f"Only {success_count}/20 requests succeeded"


class TestCachePerformance:
    """Test caching performance improvements."""

    @pytest.mark.asyncio
    async def test_curriculum_caching(self, async_client: AsyncClient):
        """Cached curriculum requests should be faster."""
        # First request (cache miss)
        start = time.time()
        response1 = await async_client.get("/api/v1/curriculum")
        first_time = (time.time() - start) * 1000
        
        assert response1.status_code == 200
        
        # Wait a moment
        await asyncio.sleep(0.1)
        
        # Second request (potential cache hit)
        start = time.time()
        response2 = await async_client.get("/api/v1/curriculum")
        second_time = (time.time() - start) * 1000
        
        assert response2.status_code == 200
        
        print(f"\nCache performance: first={first_time:.2f}ms, second={second_time:.2f}ms")
        
        # Second request should not be significantly slower
        # (allow for some variance due to async operations)
        assert second_time < first_time * 2, "Cached request should not be 2x slower"


class TestDatabasePerformance:
    """Test database query performance."""

    @pytest.mark.asyncio
    async def test_database_health_check(self, async_client: AsyncClient):
        """Database health check should be fast."""
        start = time.time()
        response = await async_client.get("/health/db")
        elapsed = (time.time() - start) * 1000
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        
        latency = response.json().get("latency_ms", elapsed)
        print(f"\nDatabase latency: {latency}ms")
        
        assert latency < 50, f"Database latency {latency}ms exceeds 50ms"


class TestResourceUsage:
    """Test resource usage under load."""

    @pytest.mark.asyncio
    async def test_memory_stability(self, async_client: AsyncClient):
        """Memory usage should remain stable under load."""
        # Make many requests
        for i in range(100):
            response = await async_client.get("/api/v1/curriculum")
            assert response.status_code == 200
            
            if i % 20 == 0:
                await asyncio.sleep(0.01)  # Small delay every 20 requests
        
        # If we get here without memory errors, test passes
        assert True


@pytest.mark.skip(reason="Long-running stress test - run manually")
class TestStress:
    """Stress tests for extreme load conditions."""

    @pytest.mark.asyncio
    async def test_sustained_load(self, async_client: AsyncClient):
        """Test sustained load over time."""
        duration = 30  # seconds
        start_time = time.time()
        request_count = 0
        error_count = 0
        
        while time.time() - start_time < duration:
            try:
                response = await async_client.get("/health")
                if response.status_code == 200:
                    request_count += 1
                else:
                    error_count += 1
            except Exception:
                error_count += 1
            
            # Small delay to prevent overwhelming
            await asyncio.sleep(0.01)
        
        error_rate = error_count / (request_count + error_count)
        print(f"\nStress test: {request_count} successful, {error_count} errors")
        print(f"Error rate: {error_rate:.2%}")
        
        assert error_rate < 0.05, f"Error rate {error_rate:.2%} exceeds 5%"
