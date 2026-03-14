/**
 * Smoke Tests - Health Checks
 * 
 * These tests verify that the production environment is healthy and
 * all critical services are responding.
 */

import { test, expect } from '@playwright/test';

const BASE_URL = process.env.TEST_BASE_URL || 'https://oopjourney.com';
const API_URL = process.env.TEST_API_URL || 'https://api.oopjourney.com';

test.describe('Health Checks', () => {
  test('web server should be accessible', async ({ request }) => {
    const response = await request.get(BASE_URL);
    expect(response.status()).toBe(200);
  });

  test('API health endpoint should return healthy', async ({ request }) => {
    const response = await request.get(`${API_URL}/health`);
    expect(response.status()).toBe(200);
    
    const body = await response.json();
    expect(body.status).toBe('healthy');
  });

  test('nginx health endpoint should respond', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/nginx-health`);
    expect(response.status()).toBe(200);
    
    const body = await response.text();
    expect(body).toContain('healthy');
  });

  test('static assets should be served', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/favicon.ico`);
    expect(response.status()).toBe(200);
  });
});

test.describe('SSL/TLS', () => {
  test('should redirect HTTP to HTTPS', async ({ request }) => {
    // This test assumes we're hitting an HTTP endpoint
    const httpUrl = BASE_URL.replace('https://', 'http://');
    const response = await request.get(httpUrl, { maxRedirects: 0 });
    
    // Should get a redirect
    expect(response.status()).toBe(301);
    expect(response.headers()['location']).toMatch(/^https:/);
  });

  test('API should enforce HTTPS', async ({ request }) => {
    const httpUrl = API_URL.replace('https://', 'http://');
    const response = await request.get(`${httpUrl}/health`, { maxRedirects: 0 });
    
    expect(response.status()).toBe(301);
  });
});

test.describe('Security Headers', () => {
  test('should have security headers', async ({ request }) => {
    const response = await request.get(BASE_URL);
    const headers = response.headers();
    
    expect(headers['x-frame-options']).toBeTruthy();
    expect(headers['x-content-type-options']).toBe('nosniff');
    expect(headers['x-xss-protection']).toBeTruthy();
    expect(headers['referrer-policy']).toBeTruthy();
  });
});

test.describe('API Endpoints', () => {
  test('curriculum endpoint should return data', async ({ request }) => {
    const response = await request.get(`${API_URL}/api/v1/curriculum/weeks`);
    expect(response.status()).toBe(200);
    
    const body = await response.json();
    expect(Array.isArray(body.weeks)).toBe(true);
    expect(body.weeks.length).toBeGreaterThan(0);
  });

  test('rate limiting should be enabled', async ({ request }) => {
    // Make multiple rapid requests
    const requests = Array(15).fill(null).map(() => 
      request.get(`${API_URL}/api/v1/curriculum/weeks`)
    );
    
    const responses = await Promise.all(requests);
    
    // Some should be rate limited
    const rateLimitedCount = responses.filter(r => r.status() === 429).length;
    expect(rateLimitedCount).toBeGreaterThan(0);
  });
});
