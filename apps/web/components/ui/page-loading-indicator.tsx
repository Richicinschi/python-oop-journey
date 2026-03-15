'use client';

import { useEffect, useState } from 'react';
import { usePathname, useSearchParams } from 'next/navigation';
import { cn } from '@/lib/utils';
import { Skeleton } from './skeleton';

export interface PageLoadingIndicatorProps {
  /** Custom class name */
  className?: string;
  /** Color variant */
  variant?: 'primary' | 'secondary' | 'destructive';
  /** Height of the progress bar */
  height?: 'thin' | 'normal' | 'thick';
  /** Whether to show at top of page (fixed) or relative */
  position?: 'fixed' | 'relative';
  /** Delay before showing (in ms) to prevent flash for fast loads */
  delay?: number;
}

/**
 * Top progress bar that shows during page navigation
 * Automatically detects route changes and shows progress
 * 
 * @example
 * ```tsx
 * // Add to your root layout
 * <PageLoadingIndicator position="fixed" />
 * ```
 */
export function PageLoadingIndicator({
  className,
  variant = 'primary',
  height = 'thin',
  position = 'fixed',
  delay = 100,
}: PageLoadingIndicatorProps) {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    let timeoutId: NodeJS.Timeout;
    let progressInterval: NodeJS.Timeout;

    const startLoading = () => {
      timeoutId = setTimeout(() => {
        setIsLoading(true);
        // Simulate progress
        progressInterval = setInterval(() => {
          setProgress((prev) => {
            if (prev >= 90) return prev;
            return prev + Math.random() * 15;
          });
        }, 200);
      }, delay);
    };

    const stopLoading = () => {
      clearTimeout(timeoutId);
      clearInterval(progressInterval);
      setProgress(100);
      setTimeout(() => {
        setIsLoading(false);
        setProgress(0);
      }, 200);
    };

    startLoading();
    return () => {
      clearTimeout(timeoutId);
      clearInterval(progressInterval);
      stopLoading();
    };
  }, [pathname, searchParams, delay]);

  if (!isLoading && progress === 0) return null;

  const variantClasses = {
    primary: 'bg-primary',
    secondary: 'bg-secondary',
    destructive: 'bg-destructive',
  };

  const heightClasses = {
    thin: 'h-0.5',
    normal: 'h-1',
    thick: 'h-1.5',
  };

  return (
    <div
      className={cn(
        'left-0 right-0 z-[100]',
        position === 'fixed' ? 'fixed top-0' : 'relative',
        className
      )}
    >
      <div
        className={cn(
          'transition-all duration-200 ease-out',
          heightClasses[height],
          variantClasses[variant]
        )}
        style={{
          width: `${progress}%`,
          opacity: isLoading || progress === 100 ? 1 : 0,
        }}
      />
    </div>
  );
}

export interface PageTransitionLoaderProps {
  /** Custom class name */
  className?: string;
  /** Whether the transition is active */
  isLoading?: boolean;
  /** Message to display during loading */
  message?: string;
}

/**
 * Full page transition loader with fade effect
 * Useful for showing loading state during major navigation
 * 
 * @example
 * ```tsx
 * <PageTransitionLoader 
 *   isLoading={isNavigating} 
 *   message="Loading problem..." 
 * />
 * ```
 */
export function PageTransitionLoader({
  className,
  isLoading = false,
  message = 'Loading...',
}: PageTransitionLoaderProps) {
  return (
    <div
      className={cn(
        'fixed inset-0 z-50 flex items-center justify-center',
        'bg-background/80 backdrop-blur-sm',
        'transition-opacity duration-300',
        isLoading ? 'opacity-100' : 'opacity-0 pointer-events-none',
        className
      )}
    >
      <div className="flex flex-col items-center gap-4">
        <div className="relative">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-primary border-t-transparent" />
          <div className="absolute inset-0 h-10 w-10 animate-pulse rounded-full border-4 border-primary/20" />
        </div>
        <p className="text-sm font-medium text-muted-foreground animate-pulse">
          {message}
        </p>
      </div>
    </div>
  );
}

export interface ContentSkeletonProps {
  /** Number of lines to show */
  lines?: number;
  /** Whether to show a title */
  showTitle?: boolean;
  /** Whether to show cards */
  showCards?: boolean;
  /** Number of cards */
  cardCount?: number;
  /** Custom class name */
  className?: string;
}

/**
 * Generic content skeleton for pages
 * Flexible skeleton that can adapt to various content layouts
 */
export function ContentSkeleton({
  lines = 4,
  showTitle = true,
  showCards = false,
  cardCount = 3,
  className,
}: ContentSkeletonProps) {
  return (
    <div className={cn('space-y-6', className)}>
      {showTitle && (
        <div className="space-y-2">
          <Skeleton className="h-8 w-1/3" />
          <Skeleton className="h-4 w-1/2" />
        </div>
      )}

      <div className="space-y-3">
        {Array.from({ length: lines }).map((_, i) => (
          <Skeleton
            key={i}
            className="h-4"
            style={{ width: `${70 + Math.random() * 30}%` }}
          />
        ))}
      </div>

      {showCards && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 mt-6">
          {Array.from({ length: cardCount }).map((_, i) => (
            <div key={i} className="space-y-3">
              <Skeleton className="h-32 w-full" />
              <Skeleton className="h-5 w-3/4" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-2/3" />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default PageLoadingIndicator;
