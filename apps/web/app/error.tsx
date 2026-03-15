'use client';

import { useEffect } from 'react';
import { captureException } from '@/lib/sentry';
import { Button } from '@/components/ui/button';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';
import Link from 'next/link';

interface ErrorBoundaryProps {
  error: Error & { digest?: string };
  reset: () => void;
}

/**
 * Root Error Boundary
 * Catches errors at the root layout level
 */
export default function RootErrorBoundary({ error, reset }: ErrorBoundaryProps) {
  useEffect(() => {
    // Log error to Sentry
    captureException(error, {
      boundary: 'root',
      digest: error.digest,
    });

    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('[Root Error Boundary]', error);
    }
  }, [error]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="max-w-md w-full text-center space-y-6">
        {/* Error Icon */}
        <div className="flex justify-center">
          <div className="w-20 h-20 rounded-full bg-destructive/10 flex items-center justify-center">
            <AlertTriangle className="w-10 h-10 text-destructive" aria-hidden="true" />
          </div>
        </div>

        {/* Error Message */}
        <div className="space-y-2">
          <h1 className="text-2xl font-bold text-foreground">
            Something went wrong
          </h1>
          <p className="text-muted-foreground">
            We apologize for the inconvenience. Our team has been notified and is working to fix the issue.
          </p>
        </div>

        {/* Error Details (Development Only) */}
        {process.env.NODE_ENV === 'development' && (
          <div className="text-left">
            <details className="bg-muted rounded-lg p-4">
              <summary className="cursor-pointer font-medium text-sm text-foreground">
                Error Details
              </summary>
              <pre className="mt-2 text-xs text-destructive overflow-auto max-h-48">
                {error.message}
                {'\n'}
                {error.stack}
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
            Try Again
          </Button>
          <Button
            asChild
            variant="outline"
            className="gap-2"
          >
            <Link href="/">
              <Home className="w-4 h-4" aria-hidden="true" />
              Go Home
            </Link>
          </Button>
        </div>

        {/* Support Link */}
        <p className="text-sm text-muted-foreground">
          If the problem persists, please{' '}
          <Link href="/support" className="text-primary underline hover:text-primary/80">
            contact support
          </Link>
          .
        </p>
      </div>
    </div>
  );
}
