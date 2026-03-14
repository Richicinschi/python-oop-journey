import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import Script from "next/script";
import { Suspense } from "react";
import { PerformanceMonitor, PreconnectHints } from "@/components/performance-monitor";

const inter = Inter({ 
  subsets: ["latin"],
  display: "swap", // Optimize font loading
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Python OOP Journey - Learn Object-Oriented Programming",
  description:
    "Master Python OOP through hands-on exercises, projects, and comprehensive curriculum covering fundamentals to advanced design patterns.",
  manifest: "/manifest.json",
  icons: {
    icon: "/favicon.ico",
    apple: "/icon-192x192.png",
  },
  // Performance optimizations
  other: {
    "theme-color": "#000000",
  },
};

export const viewport: Viewport = {
  themeColor: "#000000",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning className={inter.variable}>
      <head>
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content="#000000" />
        
        {/* Preconnect to critical domains for performance */}
        <PreconnectHints />
        
        {/* Resource hints */}
        <link rel="dns-prefetch" href="https://cdn.jsdelivr.net" />
        
        {/* Preload critical resources */}
        <link
          rel="preload"
          href="/_next/static/css/app.css"
          as="style"
        />
      </head>
      <body className={inter.className}>
        <ThemeProvider defaultTheme="system">
          {children}
        </ThemeProvider>
        
        {/* Performance monitoring */}
        <Suspense fallback={null}>
          <PerformanceMonitor />
        </Suspense>
        
        {/* Service Worker Registration */}
        <Script id="service-worker-registration" strategy="afterInteractive">
          {`
            if ('serviceWorker' in navigator) {
              window.addEventListener('load', function() {
                navigator.serviceWorker.register('/sw.js')
                  .then(function(registration) {
                    console.log('[SW] Registered:', registration.scope);
                    
                    // Listen for messages from service worker
                    navigator.serviceWorker.addEventListener('message', function(event) {
                      if (event.data && event.data.type === 'SYNC_PENDING_OPERATIONS') {
                        // Trigger sync when service worker requests it
                        if (window.__syncEngine) {
                          window.__syncEngine.syncPendingOperations();
                        }
                      }
                    });
                  })
                  .catch(function(error) {
                    console.log('[SW] Registration failed:', error);
                  });
              });
            }
          `}
        </Script>
      </body>
    </html>
  );
}
