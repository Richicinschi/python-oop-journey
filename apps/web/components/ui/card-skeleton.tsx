'use client';

import { Skeleton } from './skeleton';
import { Card, CardContent, CardHeader, CardFooter } from './card';
import { cn } from '@/lib/utils';

export interface CardSkeletonProps {
  /** Number of cards to show */
  count?: number;
  /** Whether to show header */
  showHeader?: boolean;
  /** Whether to show footer */
  showFooter?: boolean;
  /** Layout direction */
  layout?: 'grid' | 'list';
  /** Number of columns in grid layout */
  columns?: 1 | 2 | 3 | 4;
  /** Custom class name */
  className?: string;
}

/**
 * Card skeleton component for loading states
 * Flexible card skeleton that can adapt to various card layouts
 * 
 * @example
 * ```tsx
 * // Grid layout with 3 columns
 * <CardSkeleton count={6} layout="grid" columns={3} showHeader />
 * 
 * // List layout
 * <CardSkeleton count={4} layout="list" showHeader showFooter />
 * ```
 */
export function CardSkeleton({
  count = 3,
  showHeader = true,
  showFooter = false,
  layout = 'grid',
  columns = 3,
  className,
}: CardSkeletonProps) {
  const gridCols = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-4',
  };

  const containerClasses = layout === 'grid'
    ? cn('grid gap-4', gridCols[columns])
    : 'space-y-4';

  return (
    <div className={cn(containerClasses, className)}>
      {Array.from({ length: count }).map((_, index) => (
        <Card key={index} className="overflow-hidden">
          {showHeader && (
            <CardHeader className="space-y-2">
              <div className="flex items-center justify-between">
                <Skeleton className="h-5 w-20" />
                <Skeleton className="h-4 w-12" />
              </div>
              <Skeleton className="h-6 w-3/4" />
              <Skeleton className="h-4 w-full" />
            </CardHeader>
          )}
          
          <CardContent className={!showHeader ? 'pt-6' : undefined}>
            <div className="space-y-3">
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-5/6" />
              <Skeleton className="h-4 w-4/5" />
            </div>
            
            {/* Optional media area */}
            <Skeleton className="h-32 w-full mt-4 rounded-md" />
            
            {/* Tags/badges area */}
            <div className="flex flex-wrap gap-2 mt-4">
              <Skeleton className="h-5 w-16" />
              <Skeleton className="h-5 w-20" />
              <Skeleton className="h-5 w-14" />
            </div>
          </CardContent>
          
          {showFooter && (
            <CardFooter className="flex justify-between">
              <Skeleton className="h-4 w-24" />
              <Skeleton className="h-9 w-20" />
            </CardFooter>
          )}
        </Card>
      ))}
    </div>
  );
}

export interface CompactCardSkeletonProps {
  /** Number of cards */
  count?: number;
  /** Custom class name */
  className?: string;
}

/**
 * Compact card skeleton for list views
 */
export function CompactCardSkeleton({
  count = 4,
  className,
}: CompactCardSkeletonProps) {
  return (
    <div className={cn('space-y-3', className)}>
      {Array.from({ length: count }).map((_, index) => (
        <Card key={index}>
          <CardContent className="p-4">
            <div className="flex items-center gap-4">
              {/* Icon/avatar placeholder */}
              <Skeleton className="h-10 w-10 rounded-full shrink-0" />
              
              {/* Content */}
              <div className="flex-1 min-w-0 space-y-2">
                <Skeleton className="h-5 w-48" />
                <div className="flex items-center gap-3">
                  <Skeleton className="h-4 w-16" />
                  <Skeleton className="h-4 w-20" />
                </div>
              </div>
              
              {/* Action */}
              <Skeleton className="h-8 w-16 shrink-0" />
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

export interface StatCardSkeletonProps {
  /** Number of stat cards */
  count?: number;
  /** Custom class name */
  className?: string;
}

/**
 * Stat card skeleton for dashboard/stat displays
 */
export function StatCardSkeleton({
  count = 4,
  className,
}: StatCardSkeletonProps) {
  return (
    <div className={cn('grid gap-4 grid-cols-2 lg:grid-cols-4', className)}>
      {Array.from({ length: count }).map((_, index) => (
        <Card key={index}>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div className="space-y-2">
                <Skeleton className="h-4 w-24" />
                <Skeleton className="h-8 w-16" />
              </div>
              <Skeleton className="h-10 w-10 rounded-lg" />
            </div>
            <Skeleton className="h-3 w-20 mt-4" />
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

export default CardSkeleton;
