/**
 * Performance monitoring utilities for Web Vitals and custom metrics
 */

// Types for Web Vitals
export interface WebVitalsMetric {
  name: 'CLS' | 'FCP' | 'FID' | 'INP' | 'LCP' | 'TTFB';
  value: number;
  rating: 'good' | 'needs-improvement' | 'poor';
  delta?: number;
  id: string;
  navigationType?: string;
}

// Performance thresholds based on Core Web Vitals
const THRESHOLDS = {
  CLS: { good: 0.1, poor: 0.25 },
  FCP: { good: 1800, poor: 3000 },
  FID: { good: 100, poor: 300 },
  INP: { good: 200, poor: 500 },
  LCP: { good: 2500, poor: 4000 },
  TTFB: { good: 800, poor: 1800 },
};

/**
 * Get rating based on metric value and thresholds
 */
function getRating(
  name: WebVitalsMetric['name'],
  value: number
): WebVitalsMetric['rating'] {
  const threshold = THRESHOLDS[name];
  if (!threshold) return 'good';
  
  if (value <= threshold.good) return 'good';
  if (value <= threshold.poor) return 'needs-improvement';
  return 'poor';
}

/**
 * Report Web Vitals metric
 */
export function reportWebVitals(metric: WebVitalsMetric): void {
  // Add rating if not present
  if (!metric.rating) {
    metric.rating = getRating(metric.name, metric.value);
  }
  
  // Log in development
  if (process.env.NODE_ENV === 'development') {
    console.log(`[Web Vitals] ${metric.name}:`, {
      value: metric.value,
      rating: metric.rating,
      id: metric.id,
    });
  }
  
  // Send to analytics in production
  if (process.env.NODE_ENV === 'production' && typeof window !== 'undefined') {
    // Send to your analytics endpoint
    const analyticsData = {
      event: 'web_vitals',
      metric: metric.name,
      value: Math.round(metric.value * 1000) / 1000,
      rating: metric.rating,
      id: metric.id,
      page: window.location.pathname,
      timestamp: Date.now(),
    };
    
    // Use sendBeacon for reliability
    if (navigator.sendBeacon) {
      navigator.sendBeacon(
        '/api/analytics/vitals',
        JSON.stringify(analyticsData)
      );
    } else {
      // Fallback to fetch
      fetch('/api/analytics/vitals', {
        method: 'POST',
        body: JSON.stringify(analyticsData),
        keepalive: true,
      }).catch(() => {
        // Silently fail - don't impact user experience
      });
    }
    
    // Also send to Google Analytics if available
    if (typeof window.gtag !== 'undefined') {
      window.gtag('event', metric.name, {
        value: metric.value,
        metric_id: metric.id,
        metric_value: metric.value,
        metric_rating: metric.rating,
      });
    }
  }
}

/**
 * Measure custom performance metric
 */
export function measurePerformance(
  name: string,
  startMark?: string,
  endMark?: string
): number | null {
  if (typeof window === 'undefined' || !window.performance) {
    return null;
  }
  
  try {
    if (startMark && endMark) {
      // Measure between two marks
      performance.measure(name, startMark, endMark);
    }
    
    const entries = performance.getEntriesByName(name, 'measure');
    if (entries.length > 0) {
      const duration = entries[entries.length - 1].duration;
      
      if (process.env.NODE_ENV === 'development') {
        console.log(`[Performance] ${name}: ${duration.toFixed(2)}ms`);
      }
      
      return duration;
    }
  } catch (e) {
    console.warn(`[Performance] Error measuring ${name}:`, e);
  }
  
  return null;
}

/**
 * Create a performance mark
 */
export function mark(name: string): void {
  if (typeof window !== 'undefined' && window.performance) {
    performance.mark(name);
  }
}

/**
 * Clear performance marks and measures
 */
export function clearMarks(name?: string): void {
  if (typeof window !== 'undefined' && window.performance) {
    if (name) {
      performance.clearMarks(name);
      performance.clearMeasures(name);
    } else {
      performance.clearMarks();
      performance.clearMeasures();
    }
  }
}

/**
 * Track component render time
 */
export function trackRenderTime(componentName: string): () => void {
  const startMark = `${componentName}-render-start`;
  const endMark = `${componentName}-render-end`;
  const measureName = `${componentName}-render-time`;
  
  mark(startMark);
  
  return () => {
    mark(endMark);
    const duration = measurePerformance(measureName, startMark, endMark);
    
    if (duration && duration > 16) { // Log if render takes longer than one frame
      console.warn(`[Performance] ${componentName} render took ${duration.toFixed(2)}ms`);
    }
  };
}

/**
 * Lazy load observer for images and iframes
 */
export function createLazyObserver(
  callback: (entries: IntersectionObserverEntry[]) => void,
  options?: IntersectionObserverInit
): IntersectionObserver | null {
  if (typeof window === 'undefined' || !('IntersectionObserver' in window)) {
    return null;
  }
  
  return new IntersectionObserver(callback, {
    root: null,
    rootMargin: '50px',
    threshold: 0.01,
    ...options,
  });
}

/**
 * Prefetch a route
 */
export function prefetchRoute(href: string): void {
  if (typeof window === 'undefined' || !href) return;
  
  // Check if already prefetched
  const linkId = `prefetch-${href.replace(/[^a-z0-9]/gi, '-')}`;
  if (document.getElementById(linkId)) return;
  
  const link = document.createElement('link');
  link.id = linkId;
  link.rel = 'prefetch';
  link.href = href;
  link.as = 'document';
  document.head.appendChild(link);
}

/**
 * Preload critical resources
 */
export function preloadResource(
  href: string,
  as: 'script' | 'style' | 'font' | 'image' | 'fetch',
  type?: string
): void {
  if (typeof window === 'undefined') return;
  
  const linkId = `preload-${href.replace(/[^a-z0-9]/gi, '-')}`;
  if (document.getElementById(linkId)) return;
  
  const link = document.createElement('link');
  link.id = linkId;
  link.rel = 'preload';
  link.href = href;
  link.as = as;
  if (type) link.type = type;
  if (as === 'font') link.crossOrigin = 'anonymous';
  
  document.head.appendChild(link);
}

/**
 * Measure Time to First Byte (TTFB)
 */
export function measureTTFB(): number | null {
  if (typeof window === 'undefined' || !window.performance) {
    return null;
  }
  
  const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
  if (navigation) {
    return navigation.responseStart - navigation.startTime;
  }
  
  return null;
}

/**
 * Measure First Contentful Paint (FCP)
 */
export function measureFCP(): Promise<number | null> {
  return new Promise((resolve) => {
    if (typeof window === 'undefined' || !window.performance) {
      resolve(null);
      return;
    }
    
    const observer = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      const fcpEntry = entries.find(
        (entry) => entry.name === 'first-contentful-paint'
      );
      
      if (fcpEntry) {
        observer.disconnect();
        resolve(fcpEntry.startTime);
      }
    });
    
    try {
      observer.observe({ entryTypes: ['paint'] });
    } catch (e) {
      resolve(null);
    }
    
    // Timeout after 10 seconds
    setTimeout(() => {
      observer.disconnect();
      resolve(null);
    }, 10000);
  });
}

/**
 * Initialize performance monitoring
 */
export function initPerformanceMonitoring(): void {
  if (typeof window === 'undefined') return;
  
  // Mark when app becomes interactive
  if (document.readyState === 'complete') {
    mark('app-interactive');
  } else {
    window.addEventListener('load', () => {
      mark('app-interactive');
    });
  }
  
  // Monitor long tasks
  if ('PerformanceObserver' in window) {
    try {
      const longTaskObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          // Log long tasks (> 50ms) in development
          if (entry.duration > 50 && process.env.NODE_ENV === 'development') {
            console.warn('[Performance] Long task detected:', {
              duration: entry.duration,
              startTime: entry.startTime,
            });
          }
        }
      });
      
      longTaskObserver.observe({ entryTypes: ['longtask'] });
    } catch (e) {
      // Long task observer not supported
    }
  }
  
  // Log navigation timing in development
  if (process.env.NODE_ENV === 'development') {
    window.addEventListener('load', () => {
      setTimeout(() => {
        const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
        if (navigation) {
          console.log('[Performance] Navigation Timing:', {
            dns: Math.round(navigation.domainLookupEnd - navigation.domainLookupStart),
            tcp: Math.round(navigation.connectEnd - navigation.connectStart),
            ttfb: Math.round(navigation.responseStart - navigation.startTime),
            domInteractive: Math.round(navigation.domInteractive),
            domComplete: Math.round(navigation.domComplete),
            loadComplete: Math.round(navigation.loadEventEnd),
          });
        }
      }, 0);
    });
  }
}

// Type declarations for global gtag
declare global {
  interface Window {
    gtag?: (
      command: string,
      eventName: string,
      params?: Record<string, unknown>
    ) => void;
  }
}

export default {
  reportWebVitals,
  measurePerformance,
  mark,
  clearMarks,
  trackRenderTime,
  createLazyObserver,
  prefetchRoute,
  preloadResource,
  measureTTFB,
  measureFCP,
  initPerformanceMonitoring,
};
