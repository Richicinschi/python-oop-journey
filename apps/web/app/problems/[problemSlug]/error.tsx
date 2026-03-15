'use client';

import { useEffect } from 'react';
import { captureException } from '@/lib/sentry';
import { Button } from '@/components/ui/button';
import { AlertTriangle, RefreshCw, ChevronLeft, SkipForward } from 'lucide-react';
import Link from 'next/link';

interface ProblemErrorBoundaryProps {
  error: Error & { digest?: string };
  reset: () => void;
}

/**
 * Problem Page Error Boundary
 * Catches errors within individual problem pages
 * Provides problem-specific recovery and navigation options
 */
export default function ProblemErrorBoundary({ 
  error, 
  reset 
}: ProblemErrorBoundaryProps) {
  useEffect(() => {
    // Log error to Sentry with problem context
    captureException(error, {
      boundary: 'problem_page',
      digest: error.digest,
      location: 'problem_detail',
    });

    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('[Problem Error Boundary]', error);
    }
  }, [error]);

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center bg-background p-4">
      <div className="max-w-lg w-full">
        {/* Back Navigation */}
        <Button
          variant="ghost"
          size="sm"
          asChild
          className="mb-6 -ml-2 text-muted-foreground"
        >
          <Link href="/problems">
            <ChevronLeft className="w-4 h-4 mr-1" aria-hidden="true" />
            Back to Problems
          </Link>
        </Button>

        <div className="text-center space-y-6">
          {/* Error Icon */}
          <div className="flex justify-center">
            <div className="w-16 h-16 rounded-full bg-destructive/10 flex items-center justify-center">
              <AlertTriangle className="w-8 h-8 text-destructive" aria-hidden="true" />
            </div>
          </div>

          {/* Error Message */}
          <div className="space-y-2">
            <h1 className="text-xl font-bold text-foreground">
              Problem Loading Error
            </h1>
            <p className="text-muted-foreground">
              We couldn&apos;t load this problem. This might be a temporary issue or the problem may have been moved.
            </p>
          </div>

          {/* Troubleshooting Tips */}
          <div className="text-left bg-muted rounded-lg p-4">
            <h2 className="font-medium text-sm text-foreground mb-2">
              Try these steps:
            </h2>
            <ul className="text-sm text-muted-foreground space-y-1 list-disc list-inside">
              <li>Refresh the page to reload the problem</li>
              <li>Check your internet connection</li>
              <li>Return to the problems list and try again</li>
              <li>Skip to the next problem if this persists</li>
            </ul>
          </div>

          {/* Error Details (Development Only) */}
          {process.env.NODE_ENV === 'development' && (
            <div className="text-left">
              <details className="bg-muted rounded-lg p-3 border border-destructive/20">
                <summary className="cursor-pointer font-medium text-sm text-destructive">
                  Debug Information
                </summary>
                <pre className="mt-2 text-xs text-destructive overflow-auto max-h-32">
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
              Retry Loading
            </Button>
            <Button
              asChild
              variant="outline"
              className="gap-2"
            >
              <Link href="/problems">
                <SkipForward className="w-4 h-4" aria-hidden="true" />
                Browse Problems
              </Link>
            </Button>
          </div>

          {/* Support Link */}
          <p className="text-sm text-muted-foreground">
            Still having trouble?{' '}
            <Link href="/support" className="text-primary underline hover:text-primary/80">
              Report this issue
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
