'use client';

import { Skeleton } from '@/components/ui/skeleton';
import { EditorSkeleton } from '@/components/editor/editor-skeleton';
import { cn } from '@/lib/utils';

export interface ProblemSkeletonProps {
  /** Custom class name */
  className?: string;
}

/**
 * Problem page skeleton that mimics the full problem page layout
 * Shows while problem data is loading
 */
export function ProblemSkeleton({ className }: ProblemSkeletonProps) {
  return (
    <div className={cn('h-screen flex flex-col bg-background', className)}>
      {/* Breadcrumb Header Skeleton */}
      <header className="border-b bg-card px-4 py-3 shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {/* Weeks link */}
            <Skeleton className="h-4 w-12" />
            <Skeleton className="h-4 w-4 rotate-180" />
            {/* Week title */}
            <Skeleton className="h-4 w-24" />
            <Skeleton className="h-4 w-4 rotate-180" />
            {/* Day title */}
            <Skeleton className="h-4 w-20" />
            <Skeleton className="h-4 w-4 rotate-180" />
            {/* Problem title */}
            <Skeleton className="h-4 w-32" />
          </div>

          <Skeleton className="h-8 w-24" />
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - Instructions Skeleton */}
        <div className="w-[45%] min-w-[400px] max-w-[600px] border-r flex flex-col overflow-hidden">
          {/* Instructions Panel */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {/* Title and badges */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <Skeleton className="h-6 w-20" />
                <Skeleton className="h-5 w-16" />
              </div>
              <Skeleton className="h-8 w-3/4" />
            </div>

            {/* Topic tags */}
            <div className="flex flex-wrap gap-2">
              <Skeleton className="h-6 w-20" />
              <Skeleton className="h-6 w-24" />
              <Skeleton className="h-6 w-16" />
            </div>

            {/* Instructions content */}
            <div className="space-y-3">
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-5/6" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-4/5" />
            </div>

            {/* Examples section */}
            <div className="space-y-3">
              <Skeleton className="h-6 w-24" />
              <div className="bg-muted/50 rounded-lg p-4 space-y-3">
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-3/4" />
                <Skeleton className="h-4 w-5/6" />
              </div>
              <div className="bg-muted/50 rounded-lg p-4 space-y-3">
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-2/3" />
              </div>
            </div>
          </div>

          {/* Hints Section Skeleton */}
          <div className="border-t p-4 bg-card shrink-0 space-y-3">
            <Skeleton className="h-5 w-16" />
            <div className="space-y-2">
              <Skeleton className="h-10 w-full" />
              <Skeleton className="h-10 w-full" />
              <Skeleton className="h-10 w-3/4" />
            </div>
          </div>

          {/* Navigation Skeleton */}
          <div className="border-t p-4 bg-card shrink-0">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Skeleton className="h-9 w-24" />
                <Skeleton className="h-9 w-28" />
              </div>
              <div className="flex items-center gap-2">
                <Skeleton className="h-9 w-28" />
                <Skeleton className="h-9 w-20" />
              </div>
            </div>
          </div>
        </div>

        {/* Right Panel - Editor Skeleton */}
        <div className="flex-1 flex flex-col min-w-[400px] overflow-hidden">
          {/* Toolbar Skeleton */}
          <div className="flex items-center gap-1 px-2 py-1.5 bg-muted/50 border-b">
            <Skeleton className="h-8 w-8" />
            <Skeleton className="h-8 w-8" />
            <Skeleton className="h-6 w-px mx-1" />
            <Skeleton className="h-8 w-20" />
            <div className="flex-1" />
            <Skeleton className="h-8 w-8" />
            <Skeleton className="h-8 w-8" />
            <Skeleton className="h-8 w-8" />
          </div>

          {/* Editor Area */}
          <div className="flex-1 overflow-hidden">
            <EditorSkeleton height="100%" className="border-0 rounded-none" />
          </div>

          {/* Output Panel Skeleton */}
          <div className="h-48 border-t bg-card shrink-0">
            <div className="flex items-center justify-between px-4 py-2 border-b">
              <div className="flex items-center gap-4">
                <Skeleton className="h-4 w-16" />
                <Skeleton className="h-4 w-20" />
                <Skeleton className="h-4 w-16" />
              </div>
              <Skeleton className="h-7 w-16" />
            </div>
            <div className="p-4 space-y-2">
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-3/4" />
              <Skeleton className="h-4 w-5/6" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

/**
 * Compact problem skeleton for embedded use cases
 */
export function CompactProblemSkeleton({ className }: ProblemSkeletonProps) {
  return (
    <div className={cn('space-y-6', className)}>
      {/* Header */}
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          <Skeleton className="h-6 w-20" />
          <Skeleton className="h-5 w-16" />
        </div>
        <Skeleton className="h-8 w-3/4" />
      </div>

      {/* Instructions */}
      <div className="space-y-3">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-5/6" />
        <Skeleton className="h-4 w-full" />
      </div>

      {/* Editor */}
      <EditorSkeleton height="300px" />
    </div>
  );
}

export default ProblemSkeleton;
