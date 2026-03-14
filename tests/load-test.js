/**
 * k6 Load Test Configuration
 * 
 * Run with: k6 run --vus 100 --duration 5m load-test.js
 */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const apiLatency = new Trend('api_latency');
const cacheHitRate = new Rate('cache_hits');

// Test configuration
export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Ramp up to 50 users
    { duration: '5m', target: 50 },   // Stay at 50 users
    { duration: '2m', target: 100 },  // Ramp up to 100 users
    { duration: '5m', target: 100 },  // Stay at 100 users
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests under 500ms
    http_req_failed: ['rate<0.1'],     // Error rate under 10%
    errors: ['rate<0.05'],              // Custom error rate under 5%
  },
};

const BASE_URL = __ENV.API_URL || 'http://localhost:8000';

// Test scenarios
export default function () {
  // Health check
  testHealth();
  
  // Curriculum endpoints
  testCurriculum();
  
  // User endpoints (with auth)
  // testUserEndpoints();
  
  sleep(1);
}

function testHealth() {
  const res = http.get(`${BASE_URL}/health`);
  
  const success = check(res, {
    'health status is 200': (r) => r.status === 200,
    'health response is healthy': (r) => r.json('status') === 'healthy',
  });
  
  errorRate.add(!success);
  apiLatency.add(res.timings.duration);
}

function testCurriculum() {
  // Get curriculum
  const res = http.get(`${BASE_URL}/api/v1/curriculum`);
  
  const success = check(res, {
    'curriculum status is 200': (r) => r.status === 200,
    'curriculum has weeks': (r) => r.json('weeks') !== undefined,
  });
  
  errorRate.add(!success);
  apiLatency.add(res.timings.duration);
  
  // Check cache header
  if (res.headers['X-Cache'] === 'HIT') {
    cacheHitRate.add(true);
  } else {
    cacheHitRate.add(false);
  }
  
  // Get specific week
  const weekRes = http.get(`${BASE_URL}/api/v1/curriculum/week/week-01`);
  
  check(weekRes, {
    'week status is 200': (r) => r.status === 200,
  });
  
  apiLatency.add(weekRes.timings.duration);
}

function testUserEndpoints() {
  // These require authentication
  const headers = {
    'Authorization': `Bearer ${__ENV.API_TOKEN || ''}`,
  };
  
  // Get user progress
  const res = http.get(`${BASE_URL}/api/v1/progress`, { headers });
  
  check(res, {
    'progress status is 200': (r) => r.status === 200,
  });
  
  apiLatency.add(res.timings.duration);
  
  // Get bookmarks
  const bookmarksRes = http.get(`${BASE_URL}/api/v1/bookmarks`, { headers });
  
  check(bookmarksRes, {
    'bookmarks status is 200': (r) => r.status === 200,
  });
  
  apiLatency.add(bookmarksRes.timings.duration);
}

// Setup function
export function setup() {
  console.log(`Starting load test against: ${BASE_URL}`);
  
  // Verify API is up
  const res = http.get(`${BASE_URL}/health`);
  if (res.status !== 200) {
    throw new Error('API is not healthy');
  }
  
  return { baseUrl: BASE_URL };
}

// Teardown function
export function teardown(data) {
  console.log('Load test completed');
}
