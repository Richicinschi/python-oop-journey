'use client';

import { useEffect } from 'react';
import { captureException } from '@/lib/sentry';
import { Button } from '@/components/ui/button';
import { AlertTriangle, RefreshCw, BookOpen } from 'lucide-react';
import Link from 'next/link';

interface DashboardErrorBoundaryProps {
  error: Error & { digest?: string };
  reset: () => void;
}

/**
 * Dashboard Error Boundary
 * Catches errors within the dashboard layout
 * Provides dashboard-specific recovery options
 */
export default function DashboardErrorBoundary({ 
  error, 
  reset 
}: DashboardErrorBoundaryProps) {
  useEffect(() => {
    // Log error to Sentry with dashboard context
    captureException(error, {
      boundary: 'dashboard',
      digest: error.digest,
      location: 'dashboard_layout',
    });

    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('[Dashboard Error Boundary]', error);
    }
  }, [error]);

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center bg-background p-4">
      <div className="max-w-md w-full text-center space-y-6">
        {/* Error Icon */}
        <div className="flex justify-center">
          <div className="w-16 h-16 rounded-full bg-destructive/10 flex items-center justify-center">
            <AlertTriangle className="w-8 h-8 text-destructive" aria-hidden="true" />
          </div>
        </div>

        {/* Error Message */}
        <div className="space-y-2">
          <h1 className="text-xl font-bold text-foreground">
            Dashboard Error
          </h1>
          <p className="text-muted-foreground">
            We encountered an error loading your dashboard. Your progress is safe.
          </p>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-2 gap-3 text-sm">
          <Link 
            href="/problems"
            className="p-3 rounded-lg bg-muted hover:bg-muted/80 transition-colors text-left"
          >
            <BookOpen className="w-4 h-4 mb-1 text-primary" aria-hidden="true" />
            <span className="font-medium">Continue Learning</span>
          </Link>
          <Link 
            href="/profile"
            className="p-3 rounded-lg bg-muted hover:bg-muted/80 transition-colors text-left"
          >
            <span className="font-medium">View Profile</span>
          </Link>
        </div>

        {/* Error Details (Development Only) */}
        {process.env.NODE_ENV === 'development' && (
          <div className="text-left">
            <details className="bg-muted rounded-lg p-3">
              <summary className="cursor-pointer font-medium text-sm text-foreground">
                Error Details
              </summary>
              <pre className="mt-2 text-xs text-destructive overflow-auto max-h-32">
                {error.message}
              </pre>
            </details>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Button
            onClick={reset}
            variant="default"
            className="gap-2"
          >
            <RefreshCw className="w-4 h-4" aria-hidden="true" />
            Retry Loading
          </Button>
          <Button
            asChild
            variant="outline"
          >
            <Link href="/">Exit Dashboard</Link>
          </Button>
        </div>
      </div>
    </div>
  );
}
