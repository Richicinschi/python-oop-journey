'use client';

import { Skeleton } from '@/components/ui/skeleton';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { cn } from '@/lib/utils';

export interface WeekSkeletonProps {
  /** Custom class name */
  className?: string;
}

/**
 * Week page skeleton that mimics the week detail page layout
 * Shows while week data is loading
 */
export function WeekSkeleton({ className }: WeekSkeletonProps) {
  return (
    <div className={cn('space-y-8', className)}>
      {/* Breadcrumb Skeleton */}
      <div className="flex items-center gap-2 text-sm">
        <Skeleton className="h-4 w-16" />
        <Skeleton className="h-4 w-4" />
        <Skeleton className="h-4 w-20" />
      </div>

      {/* Header Section */}
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
          <div className="flex items-start gap-4">
            {/* Icon placeholder */}
            <Skeleton className="h-14 w-14 rounded-xl shrink-0" />
            <div className="space-y-2">
              <Skeleton className="h-5 w-24" />
              <Skeleton className="h-8 w-64" />
            </div>
          </div>
          
          {/* Navigation buttons */}
          <div className="flex gap-2">
            <Skeleton className="h-9 w-28" />
            <Skeleton className="h-9 w-20" />
          </div>
        </div>

        {/* Objective Card */}
        <Card className="bg-muted/50 border-dashed">
          <CardContent className="pt-6">
            <div className="flex items-start gap-3">
              <Skeleton className="h-5 w-5 mt-0.5 shrink-0" />
              <div className="space-y-2 flex-1">
                <Skeleton className="h-5 w-32" />
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-4/5" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Progress Card */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Skeleton className="h-5 w-5" />
                <Skeleton className="h-5 w-28" />
              </div>
              <Skeleton className="h-4 w-32" />
            </div>
            <Skeleton className="h-3 w-full" />
          </CardContent>
        </Card>
      </div>

      {/* Separator */}
      <Skeleton className="h-px w-full" />

      {/* Days Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <Skeleton className="h-7 w-36" />
          <Skeleton className="h-4 w-16" />
        </div>
        
        {/* Day Cards */}
        <div className="grid gap-4">
          {Array.from({ length: 5 }).map((_, index) => (
            <DayCardSkeleton key={index} />
          ))}
        </div>
      </div>

      {/* Weekly Project Section */}
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <Skeleton className="h-5 w-5" />
          <Skeleton className="h-7 w-36" />
        </div>
        
        <Card className="border-2">
          <CardHeader>
            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
              <div className="flex items-start gap-4">
                <Skeleton className="h-14 w-14 rounded-xl shrink-0" />
                <div className="space-y-2">
                  <Skeleton className="h-6 w-48" />
                  <div className="flex gap-3">
                    <Skeleton className="h-4 w-28" />
                    <Skeleton className="h-4 w-24" />
                  </div>
                </div>
              </div>
              <Skeleton className="h-9 w-32" />
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-5/6" />
            <div className="bg-muted/50 rounded-lg p-4 space-y-2">
              <Skeleton className="h-4 w-32 mb-2" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-3/4" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Navigation Footer */}
      <div className="flex items-center justify-between pt-4 border-t">
        <Skeleton className="h-10 w-28" />
        <Skeleton className="h-10 w-32" />
      </div>
    </div>
  );
}

/**
 * Individual day card skeleton
 */
function DayCardSkeleton() {
  return (
    <Card className="transition-all">
      <CardContent className="p-6">
        <div className="flex flex-col sm:flex-row sm:items-center gap-4">
          {/* Status & Day Number */}
          <div className="flex items-center gap-3">
            <Skeleton className="h-10 w-10 rounded-full shrink-0" />
            <Skeleton className="h-5 w-16" />
          </div>

          {/* Content */}
          <div className="flex-1 min-w-0 space-y-2">
            <Skeleton className="h-6 w-48" />
            <div className="flex flex-wrap items-center gap-3">
              <Skeleton className="h-4 w-24" />
              <Skeleton className="h-4 w-28" />
            </div>
            <div className="space-y-1 mt-2">
              <Skeleton className="h-3 w-full" />
              <Skeleton className="h-3 w-4/5" />
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2">
            <Skeleton className="h-9 w-24" />
            <Skeleton className="h-9 w-20" />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

/**
 * Week list skeleton for the curriculum page
 */
export function WeekListSkeleton({ className }: WeekSkeletonProps) {
  return (
    <div className={cn('space-y-8', className)}>
      {/* Header */}
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <Skeleton className="h-12 w-12 rounded-lg" />
          <div className="space-y-2">
            <Skeleton className="h-8 w-48" />
            <Skeleton className="h-4 w-64" />
          </div>
        </div>
        <div className="flex gap-4">
          <Skeleton className="h-4 w-20" />
          <Skeleton className="h-4 w-24" />
        </div>
      </div>

      {/* Search */}
      <Skeleton className="h-10 w-full max-w-md" />

      {/* Week Cards Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, index) => (
          <WeekCardSkeleton key={index} />
        ))}
      </div>

      {/* Learning Path */}
      <Card className="mt-8">
        <CardHeader>
          <Skeleton className="h-6 w-32" />
          <Skeleton className="h-4 w-48" />
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, index) => (
              <div key={index} className="flex items-start gap-4">
                <Skeleton className="h-8 w-8 rounded-full shrink-0" />
                <div className="flex-1 pb-4 border-b last:border-0 last:pb-0 space-y-1">
                  <Skeleton className="h-5 w-48" />
                  <Skeleton className="h-4 w-32" />
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

/**
 * Individual week card skeleton
 */
function WeekCardSkeleton() {
  return (
    <Card className="group transition-all">
      <CardHeader>
        <div className="flex items-center justify-between">
          <Skeleton className="h-5 w-16" />
          <Skeleton className="h-4 w-12" />
        </div>
        <Skeleton className="h-6 w-full mt-3" />
        <Skeleton className="h-4 w-full mt-2" />
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Progress */}
        <div className="space-y-2">
          <div className="flex justify-between">
            <Skeleton className="h-4 w-16" />
            <Skeleton className="h-4 w-8" />
          </div>
          <Skeleton className="h-2 w-full" />
        </div>

        {/* Stats */}
        <div className="flex items-center gap-4">
          <Skeleton className="h-4 w-16" />
          <Skeleton className="h-4 w-20" />
        </div>

        {/* CTA */}
        <Skeleton className="h-10 w-full mt-2" />
      </CardContent>
    </Card>
  );
}

export default WeekSkeleton;
