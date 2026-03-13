'use client';

import { Component, ErrorInfo, ReactNode } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { 
  AlertCircle, 
  RefreshCw, 
  Home, 
  Bug,
  FileWarning,
  FolderX
} from 'lucide-react';
import Link from 'next/link';
import { cn } from '@/lib/utils';

interface ProjectErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
  onReset?: () => void;
}

interface ProjectErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export class ProjectErrorBoundary extends Component<ProjectErrorBoundaryProps, ProjectErrorBoundaryState> {
  constructor(props: ProjectErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error: Error): ProjectErrorBoundaryState {
    return { hasError: true, error, errorInfo: null };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log to console in development
    console.error('Project Error Boundary caught an error:', error, errorInfo);
    
    // In production, you might want to log to an error tracking service
    this.setState({ error, errorInfo });
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
    this.props.onReset?.();
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <ProjectErrorFallback 
          error={this.state.error}
          onReset={this.handleReset}
        />
      );
    }

    return this.props.children;
  }
}

interface ProjectErrorFallbackProps {
  error: Error | null;
  onReset: () => void;
  variant?: 'full' | 'compact';
}

export function ProjectErrorFallback({ 
  error, 
  onReset,
  variant = 'full'
}: ProjectErrorFallbackProps) {
  const errorMessage = error?.message || 'An unexpected error occurred';

  if (variant === 'compact') {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Something went wrong</AlertTitle>
        <AlertDescription className="flex items-center gap-2 mt-2">
          <span className="flex-1 truncate">{errorMessage}</span>
          <Button size="sm" variant="outline" onClick={onReset}>
            <RefreshCw className="h-3 w-3 mr-1" />
            Retry
          </Button>
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="flex items-center justify-center min-h-[400px] p-6">
      <Card className="max-w-lg w-full">
        <CardHeader className="text-center">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-destructive/10 mb-4">
            <Bug className="h-8 w-8 text-destructive" />
          </div>
          <CardTitle className="text-xl">Project Error</CardTitle>
          <CardDescription>
            We encountered an issue while loading your project
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Alert variant="destructive" className="bg-destructive/5">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error Details</AlertTitle>
            <AlertDescription className="font-mono text-xs mt-2 break-all">
              {errorMessage}
            </AlertDescription>
          </Alert>

          <div className="text-sm text-muted-foreground space-y-1">
            <p>Try these steps to resolve the issue:</p>
            <ul className="list-disc list-inside space-y-1 ml-2">
              <li>Refresh the page</li>
              <li>Clear your browser cache</li>
              <li>Check your internet connection</li>
              <li>Try again in a few minutes</li>
            </ul>
          </div>
        </CardContent>
        <CardFooter className="flex gap-2">
          <Button onClick={onReset} className="flex-1 gap-2">
            <RefreshCw className="h-4 w-4" />
            Try Again
          </Button>
          <Button variant="outline" asChild className="flex-1 gap-2">
            <Link href="/weeks">
              <Home className="h-4 w-4" />
              Go Home
            </Link>
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}

// File tree specific error boundary
export function FileTreeError({ onRetry }: { onRetry: () => void }) {
  return (
    <div className="p-4 text-center">
      <div className="inline-flex h-10 w-10 items-center justify-center rounded-lg bg-destructive/10 mb-3">
        <FolderX className="h-5 w-5 text-destructive" />
      </div>
      <p className="text-sm text-muted-foreground mb-3">
        Failed to load file tree
      </p>
      <Button size="sm" variant="outline" onClick={onRetry}>
        <RefreshCw className="h-3.5 w-3.5 mr-1.5" />
        Retry
      </Button>
    </div>
  );
}

// Editor specific error boundary
export function EditorError({ onRetry, onReset }: { onRetry: () => void; onReset?: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center h-full p-6 text-center">
      <div className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-destructive/10 mb-4">
        <FileWarning className="h-6 w-6 text-destructive" />
      </div>
      <h3 className="font-medium mb-2">Editor Error</h3>
      <p className="text-sm text-muted-foreground mb-4 max-w-xs">
        There was a problem loading the code editor. Your work is saved.
      </p>
      <div className="flex gap-2">
        <Button size="sm" variant="outline" onClick={onRetry}>
          <RefreshCw className="h-4 w-4 mr-1.5" />
          Retry
        </Button>
        {onReset && (
          <Button size="sm" variant="ghost" onClick={onReset}>
            Reset Editor
          </Button>
        )}
      </div>
    </div>
  );
}

// Graceful degradation wrapper
interface GracefulDegradationProps {
  children: ReactNode;
  degradedChildren: ReactNode;
  isDegraded: boolean;
}

export function GracefulDegradation({ 
  children, 
  degradedChildren, 
  isDegraded 
}: GracefulDegradationProps) {
  if (isDegraded) {
    return (
      <div className="relative">
        <Alert className="mb-4 border-amber-500/50 bg-amber-500/10">
          <AlertCircle className="h-4 w-4 text-amber-600" />
          <AlertTitle className="text-amber-800">Limited Functionality</AlertTitle>
          <AlertDescription className="text-amber-700">
            Some features are unavailable. Basic editing still works.
          </AlertDescription>
        </Alert>
        {degradedChildren}
      </div>
    );
  }

  return children;
}

// Hook for error tracking
export function useErrorTracker() {
  const trackError = (error: Error, context?: Record<string, unknown>) => {
    console.error('Tracked Error:', error, context);
    
    // Store recent errors for debugging
    const errors = JSON.parse(localStorage.getItem('oop-journey-errors') || '[]');
    errors.push({
      message: error.message,
      stack: error.stack,
      context,
      timestamp: Date.now(),
    });
    
    // Keep only last 10 errors
    localStorage.setItem('oop-journey-errors', JSON.stringify(errors.slice(-10)));
  };

  const getRecentErrors = () => {
    return JSON.parse(localStorage.getItem('oop-journey-errors') || '[]');
  };

  const clearErrors = () => {
    localStorage.removeItem('oop-journey-errors');
  };

  return { trackError, getRecentErrors, clearErrors };
}
