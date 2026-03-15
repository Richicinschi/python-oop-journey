'use client';

import { Skeleton } from '@/components/ui/skeleton';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { cn } from '@/lib/utils';

export interface DaySkeletonProps {
  /** Custom class name */
  className?: string;
}

/**
 * Day page skeleton that mimics the day detail page layout
 * Shows while day data is loading
 */
export function DaySkeleton({ className }: DaySkeletonProps) {
  return (
    <div className={cn('space-y-8', className)}>
      {/* Breadcrumb Skeleton */}
      <div className="flex items-center gap-2 text-sm">
        <Skeleton className="h-4 w-16" />
        <Skeleton className="h-4 w-4" />
        <Skeleton className="h-4 w-20" />
        <Skeleton className="h-4 w-4" />
        <Skeleton className="h-4 w-24" />
      </div>

      {/* Header Section */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
          <div className="space-y-2">
            <Skeleton className="h-5 w-24" />
            <Skeleton className="h-8 w-64" />
            <Skeleton className="h-4 w-48" />
          </div>
          
          {/* Navigation buttons */}
          <div className="flex gap-2">
            <Skeleton className="h-9 w-28" />
            <Skeleton className="h-9 w-20" />
          </div>
        </div>
      </div>

      {/* Progress Section */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Skeleton className="h-5 w-5" />
              <Skeleton className="h-5 w-28" />
            </div>
            <Skeleton className="h-4 w-32" />
          </div>
          <Skeleton className="h-3 w-full mb-4" />
          
          {/* Stats row */}
          <div className="flex flex-wrap gap-4 pt-4 border-t">
            <Skeleton className="h-4 w-24" />
            <Skeleton className="h-4 w-20" />
            <Skeleton className="h-4 w-28" />
          </div>
        </CardContent>
      </Card>

      {/* Theory Section (conditional in real page) */}
      <Card className="border-dashed">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Skeleton className="h-5 w-5" />
            <Skeleton className="h-6 w-32" />
          </div>
          <Skeleton className="h-4 w-64" />
        </CardHeader>
        <CardContent className="space-y-2">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />
          <Skeleton className="h-9 w-28 mt-4" />
        </CardContent>
      </Card>

      {/* Problems Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <Skeleton className="h-7 w-32" />
          <Skeleton className="h-4 w-24" />
        </div>

        {/* Problem Cards */}
        <div className="grid gap-4">
          {Array.from({ length: 4 }).map((_, index) => (
            <ProblemRowSkeleton key={index} index={index} />
          ))}
        </div>
      </div>

      {/* Navigation Footer */}
      <div className="flex items-center justify-between pt-4 border-t">
        <Skeleton className="h-10 w-32" />
        <Skeleton className="h-10 w-28" />
      </div>
    </div>
  );
}

/**
 * Individual problem row skeleton
 */
function ProblemRowSkeleton({ index }: { index: number }) {
  return (
    <Card className="transition-all hover:shadow-sm">
      <CardContent className="p-4">
        <div className="flex items-center gap-4">
          {/* Status indicator */}
          <Skeleton className="h-10 w-10 rounded-full shrink-0" />
          
          {/* Problem info */}
          <div className="flex-1 min-w-0 space-y-2">
            <div className="flex items-center gap-2">
              <Skeleton className="h-5 w-48" />
              <Skeleton className="h-5 w-16" />
            </div>
            <div className="flex items-center gap-3">
              <Skeleton className="h-4 w-20" />
              <Skeleton className="h-4 w-16" />
              <Skeleton className="h-4 w-24" />
            </div>
          </div>
          
          {/* Action button */}
          <Skeleton className="h-9 w-24 shrink-0" />
        </div>
      </CardContent>
    </Card>
  );
}

export default DaySkeleton;
