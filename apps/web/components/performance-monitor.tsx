"use client";

import { useEffect } from "react";
import { usePathname, useSearchParams } from "next/navigation";
import { initPerformanceMonitoring, reportWebVitals, mark } from "@/lib/performance";

/**
 * Performance monitoring component
 * Tracks Web Vitals and page navigation performance
 */
export function PerformanceMonitor() {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  useEffect(() => {
    // Initialize performance monitoring on mount
    initPerformanceMonitoring();

    // Report Core Web Vitals
    if ("web-vitals" in window) {
      import("web-vitals").then(({ onCLS, onFID, onFCP, onINP, onLCP, onTTFB }) => {
        onCLS((metric) => reportWebVitals({ ...metric, name: "CLS" }));
        onFID((metric) => reportWebVitals({ ...metric, name: "FID" }));
        onFCP((metric) => reportWebVitals({ ...metric, name: "FCP" }));
        onINP((metric) => reportWebVitals({ ...metric, name: "INP" }));
        onLCP((metric) => reportWebVitals({ ...metric, name: "LCP" }));
        onTTFB((metric) => reportWebVitals({ ...metric, name: "TTFB" }));
      });
    }
  }, []);

  // Track page navigation
  useEffect(() => {
    const url = `${pathname}${searchParams.toString() ? `?${searchParams.toString()}` : ""}`;
    
    // Mark navigation start
    mark(`navigation-start-${url}`);

    // Report to analytics in production
    if (process.env.NODE_ENV === "production" && typeof window !== "undefined") {
      // Send page view event
      if (window.gtag) {
        window.gtag("config", process.env.NEXT_PUBLIC_GA_ID || "", {
          page_path: url,
        });
      }
    }

    return () => {
      // Mark navigation end
      mark(`navigation-end-${url}`);
    };
  }, [pathname, searchParams]);

  return null;
}

/**
 * Preconnect to critical domains
 */
export function PreconnectHints() {
  const criticalDomains = [
    "https://cdn.jsdelivr.net", // Monaco editor CDN
    "https://fonts.googleapis.com",
    "https://fonts.gstatic.com",
  ];

  return (
    <>
      {criticalDomains.map((domain) => (
        <link key={domain} rel="preconnect" href={domain} crossOrigin="anonymous" />
      ))}
      <link rel="dns-prefetch" href="https://cdn.jsdelivr.net" />
    </>
  );
}

/**
 * Resource hints for preloading critical assets
 */
export function CriticalResourceHints() {
  return (
    <>
      {/* Preload critical fonts */}
      <link
        rel="preload"
        href="/fonts/inter-var.woff2"
        as="font"
        type="font/woff2"
        crossOrigin="anonymous"
      />
      
      {/* Preload critical CSS */}
      <link rel="preload" href="/_next/static/css/app.css" as="style" />
      
      {/* Prefetch likely navigation targets */}
      <link rel="prefetch" href="/weeks" />
      <link rel="prefetch" href="/dashboard" />
    </>
  );
}

// Type declarations
declare global {
  interface Window {
    gtag?: (command: string, targetId: string, config?: Record<string, unknown>) => void;
  }
}
