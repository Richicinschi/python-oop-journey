/**
 * Skeleton Component
 * Loading state placeholders
 */

import { cn } from '../lib/utils';

interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Width of the skeleton
   */
  width?: string | number;
  /**
   * Height of the skeleton
   */
  height?: string | number;
  /**
   * Whether to show rounded corners
   */
  rounded?: boolean | 'sm' | 'md' | 'lg' | 'full';
  /**
   * Whether to show animation
   */
  animate?: boolean;
}

function Skeleton({
  className,
  width,
  height,
  rounded = true,
  animate = true,
  style,
  ...props
}: SkeletonProps) {
  const roundedClass =
    rounded === true
      ? 'rounded-md'
      : rounded === 'sm'
      ? 'rounded-sm'
      : rounded === 'md'
      ? 'rounded-md'
      : rounded === 'lg'
      ? 'rounded-lg'
      : rounded === 'full'
      ? 'rounded-full'
      : '';

  const widthStyle = width
    ? typeof width === 'number'
      ? `${width}px`
      : width
    : undefined;

  const heightStyle = height
    ? typeof height === 'number'
      ? `${height}px`
      : height
    : undefined;

  return (
    <div
      className={cn(
        'bg-muted',
        roundedClass,
        animate && 'animate-pulse',
        className
      )}
      style={{
        width: widthStyle,
        height: heightStyle,
        ...style,
      }}
      {...props}
    />
  );
}

/**
 * Skeleton text for loading text content
 */
function SkeletonText({
  lines = 3,
  className,
  lastLineWidth = '60%',
}: {
  lines?: number;
  className?: string;
  lastLineWidth?: string;
}) {
  return (
    <div className={cn('space-y-2', className)}>
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton
          key={i}
          height={16}
          width={i === lines - 1 ? lastLineWidth : '100%'}
          className="last:opacity-70"
        />
      ))}
    </div>
  );
}

/**
 * Skeleton card for loading card content
 */
function SkeletonCard({ className }: { className?: string }) {
  return (
    <div className={cn('rounded-lg border p-6 space-y-4', className)}>
      <Skeleton height={24} width="60%" />
      <SkeletonText lines={2} />
      <div className="flex gap-2">
        <Skeleton height={32} width={80} rounded="sm" />
        <Skeleton height={32} width={80} rounded="sm" />
      </div>
    </div>
  );
}

export { Skeleton, SkeletonText, SkeletonCard };
