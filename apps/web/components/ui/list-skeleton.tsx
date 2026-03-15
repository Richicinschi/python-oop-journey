'use client';

import { Skeleton } from './skeleton';
import { cn } from '@/lib/utils';

export interface ListSkeletonProps {
  /** Number of items to show */
  count?: number;
  /** Whether to show avatars/icons */
  showAvatar?: boolean;
  /** Whether to show actions/buttons */
  showAction?: boolean;
  /** Number of text lines per item */
  lines?: 1 | 2 | 3;
  /** Custom class name */
  className?: string;
}

/**
 * List skeleton component for loading states
 * Shows a list of placeholder items with configurable elements
 * 
 * @example
 * ```tsx
 * // Simple list
 * <ListSkeleton count={5} />
 * 
 * // With avatars and actions
 * <ListSkeleton count={5} showAvatar showAction lines={2} />
 * ```
 */
export function ListSkeleton({
  count = 5,
  showAvatar = false,
  showAction = false,
  lines = 2,
  className,
}: ListSkeletonProps) {
  return (
    <div className={cn('space-y-3', className)}>
      {Array.from({ length: count }).map((_, index) => (
        <div
          key={index}
          className="flex items-center gap-4 p-3 rounded-lg border bg-card"
        >
          {/* Avatar/Icon placeholder */}
          {showAvatar && (
            <Skeleton className="h-10 w-10 rounded-full shrink-0" />
          )}

          {/* Content lines */}
          <div className="flex-1 min-w-0 space-y-2">
            {lines >= 1 && (
              <Skeleton 
                className="h-4" 
                style={{ width: `${60 + Math.random() * 30}%` }}
              />
            )}
            {lines >= 2 && (
              <Skeleton 
                className="h-3" 
                style={{ width: `${40 + Math.random() * 40}%` }}
              />
            )}
            {lines >= 3 && (
              <Skeleton 
                className="h-3" 
                style={{ width: `${50 + Math.random() * 30}%` }}
              />
            )}
          </div>

          {/* Action placeholder */}
          {showAction && (
            <Skeleton className="h-8 w-20 shrink-0" />
          )}
        </div>
      ))}
    </div>
  );
}

export interface TableRowSkeletonProps {
  /** Number of rows */
  rows?: number;
  /** Number of columns */
  columns?: number;
  /** Whether to show header */
  showHeader?: boolean;
  /** Custom class name */
  className?: string;
}

/**
 * Table row skeleton for table loading states
 */
export function TableRowSkeleton({
  rows = 5,
  columns = 4,
  showHeader = true,
  className,
}: TableRowSkeletonProps) {
  return (
    <div className={cn('w-full', className)}>
      {/* Header */}
      {showHeader && (
        <div className="flex gap-4 p-3 border-b bg-muted/50">
          {Array.from({ length: columns }).map((_, index) => (
            <Skeleton
              key={index}
              className="h-4"
              style={{ 
                width: index === 0 ? '40%' : `${20 + Math.random() * 20}%`,
                flex: index === 0 ? 2 : 1 
              }}
            />
          ))}
        </div>
      )}

      {/* Rows */}
      <div className="divide-y">
        {Array.from({ length: rows }).map((_, rowIndex) => (
          <div key={rowIndex} className="flex gap-4 p-3 items-center">
            {Array.from({ length: columns }).map((_, colIndex) => (
              <div
                key={colIndex}
                style={{ flex: colIndex === 0 ? 2 : 1 }}
              >
                {colIndex === 0 ? (
                  <div className="flex items-center gap-3">
                    <Skeleton className="h-8 w-8 rounded" />
                    <Skeleton 
                      className="h-4" 
                      style={{ width: `${60 + Math.random() * 30}%` }}
                    />
                  </div>
                ) : colIndex === columns - 1 ? (
                  <div className="flex gap-2">
                    <Skeleton className="h-7 w-16" />
                    <Skeleton className="h-7 w-7" />
                  </div>
                ) : (
                  <Skeleton 
                    className="h-4" 
                    style={{ width: `${50 + Math.random() * 30}%` }}
                  />
                )}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export interface TimelineSkeletonProps {
  /** Number of timeline items */
  count?: number;
  /** Custom class name */
  className?: string;
}

/**
 * Timeline skeleton for activity feeds and history
 */
export function TimelineSkeleton({
  count = 4,
  className,
}: TimelineSkeletonProps) {
  return (
    <div className={cn('space-y-0', className)}>
      {Array.from({ length: count }).map((_, index) => (
        <div key={index} className="flex gap-4 pb-6 last:pb-0">
          {/* Timeline line and dot */}
          <div className="flex flex-col items-center">
            <Skeleton className="h-3 w-3 rounded-full" />
            {index < count - 1 && (
              <Skeleton className="w-px flex-1 mt-2" />
            )}
          </div>

          {/* Content */}
          <div className="flex-1 pb-6 last:pb-0 space-y-2">
            <div className="flex items-center gap-2">
              <Skeleton className="h-4 w-32" />
              <Skeleton className="h-3 w-16" />
            </div>
            <Skeleton className="h-3 w-full" />
            <Skeleton className="h-3 w-2/3" />
          </div>
        </div>
      ))}
    </div>
  );
}

export interface FormSkeletonProps {
  /** Number of form fields */
  fields?: number;
  /** Whether to show submit button */
  showSubmit?: boolean;
  /** Custom class name */
  className?: string;
}

/**
 * Form skeleton for form loading states
 */
export function FormSkeleton({
  fields = 4,
  showSubmit = true,
  className,
}: FormSkeletonProps) {
  return (
    <div className={cn('space-y-6', className)}>
      {Array.from({ length: fields }).map((_, index) => (
        <div key={index} className="space-y-2">
          <Skeleton className="h-4 w-24" />
          <Skeleton className="h-10 w-full" />
          {index % 2 === 0 && (
            <Skeleton className="h-3 w-48" />
          )}
        </div>
      ))}
      
      {showSubmit && (
        <div className="flex gap-3 pt-2">
          <Skeleton className="h-10 w-24" />
          <Skeleton className="h-10 w-24" />
        </div>
      )}
    </div>
  );
}

export default ListSkeleton;
