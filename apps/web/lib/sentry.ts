/**
 * Sentry Integration for Error Tracking and Performance Monitoring
 * 
 * This module configures Sentry for the Next.js frontend.
 * Sentry captures errors and performance data to help identify and fix issues.
 */

import * as Sentry from '@sentry/nextjs';
import type { Event, Scope } from '@sentry/nextjs';

const SENTRY_DSN = process.env.NEXT_PUBLIC_SENTRY_DSN;
const ENVIRONMENT = process.env.NEXT_PUBLIC_ENVIRONMENT || 'development';

/**
 * Initialize Sentry for the application
 * This should be called once at app startup
 */
export function initSentry(): void {
  if (!SENTRY_DSN) {
    console.warn('Sentry DSN not configured - error tracking disabled');
    return;
  }

  Sentry.init({
    dsn: SENTRY_DSN,
    environment: ENVIRONMENT,
    
    // Adjust sampling rates based on environment
    tracesSampleRate: ENVIRONMENT === 'production' ? 0.1 : 1.0,
    profilesSampleRate: ENVIRONMENT === 'production' ? 0.01 : 1.0,
    
    // Replay sampling
    replaysSessionSampleRate: 0.1,
    replaysOnErrorSampleRate: 1.0,
    
    // Don't send errors in development
    beforeSend(event: Event): Event | null {
      if (ENVIRONMENT === 'development') {
        return null;
      }
      return event;
    },
    
    // Ignore common browser errors
    ignoreErrors: [
      // Network errors
      'Network Error',
      'Failed to fetch',
      'NetworkError when attempting to fetch resource.',
      
      // Browser extension errors
      /chrome-extension/,
      /moz-extension/,
      
      // Third-party script errors
      'Non-Error exception captured',
      'Non-Error promise rejection captured',
      
      // ResizeObserver loop errors (common but harmless)
      'ResizeObserver loop limit exceeded',
      'ResizeObserver loop completed with undelivered notifications.',
    ],
    
    // Deny URLs from browser extensions
    denyUrls: [
      /^chrome:\/\//i,
      /^chrome-extension:\/\//i,
      /^moz-extension:\/\//i,
    ],
    
    // Set release version
    release: process.env.NEXT_PUBLIC_APP_VERSION || 'development',
    
    // Enable debug in non-production
    debug: ENVIRONMENT !== 'production',
  });
}

/**
 * Set user context for Sentry
 * Call this when user logs in
 */
export function setSentryUser(userId: string, email?: string, username?: string): void {
  Sentry.setUser({
    id: userId,
    email,
    username,
  });
}

/**
 * Clear user context from Sentry
 * Call this when user logs out
 */
export function clearSentryUser(): void {
  Sentry.setUser(null);
}

/**
 * Capture an exception manually
 * Use this for caught errors that should still be reported
 */
export function captureException(error: Error, context?: Record<string, unknown>): void {
  if (context) {
    Sentry.withScope((scope: Scope) => {
      scope.setContext('additional', context);
      Sentry.captureException(error);
    });
  } else {
    Sentry.captureException(error);
  }
}

/**
 * Capture a message manually
 * Use this for important events that aren't errors
 */
export function captureMessage(message: string, level: Sentry.SeverityLevel = 'info'): void {
  Sentry.captureMessage(message, level);
}

/**
 * Add breadcrumbs for debugging
 * Breadcrumbs help trace the steps leading to an error
 */
export function addBreadcrumb(
  message: string,
  category?: string,
  data?: Record<string, unknown>
): void {
  Sentry.addBreadcrumb({
    message,
    category,
    data,
    level: 'info',
  });
}

/**
 * Set tags for filtering in Sentry
 */
export function setTag(key: string, value: string): void {
  Sentry.setTag(key, value);
}

// Re-export Sentry for direct access if needed
export { Sentry };
