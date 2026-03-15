"use client";

import { cn } from "@/lib/utils";
import { Skeleton } from "@/components/ui/skeleton";

export interface EditorSkeletonProps {
  /** Skeleton height (default: "400px") */
  height?: string;
  /** Custom class name */
  className?: string;
}

// Pre-computed width variations for consistent SSR/CSR rendering
const LINE_WIDTHS = [45, 72, 58, 83, 37, 91, 64, 52, 78, 41];
const LINE_OPACITIES = [0.5, 0.7, 0.6, 0.8, 0.5, 0.7, 0.6, 0.5, 0.7, 0.6];

export function EditorSkeleton({
  height = "400px",
  className,
}: EditorSkeletonProps) {
  return (
    <div
      className={cn(
        "relative flex flex-col rounded-md border border-border overflow-hidden",
        "bg-muted/50",
        className
      )}
      style={{ height }}
    >
      {/* Fake editor toolbar/line numbers area */}
      <div className="flex flex-1">
        {/* Line numbers column */}
        <div className="w-12 flex-shrink-0 bg-muted border-r border-border py-2">
          <div className="space-y-1 px-2">
            {Array.from({ length: 12 }).map((_, i) => (
              <Skeleton
                key={i}
                className="h-4 w-6"
                style={{ opacity: 0.3 + (i % 3) * 0.2 }}
              />
            ))}
          </div>
        </div>

        {/* Code area */}
        <div className="flex-1 p-3 space-y-2">
          {Array.from({ length: 10 }).map((_, i) => (
            <div key={i} className="flex items-center gap-2">
              {/* Indentation */}
              {i > 2 && i < 7 && (
                <Skeleton className="h-4 w-8 flex-shrink-0" />
              )}
              {/* Code line - use pre-computed values to avoid hydration mismatch */}
              <Skeleton
                className="h-4"
                style={{
                  width: `${LINE_WIDTHS[i]}%`,
                  opacity: LINE_OPACITIES[i],
                }}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Fake status bar */}
      <div className="h-6 bg-muted border-t border-border flex items-center px-3 gap-4">
        <Skeleton className="h-3 w-16" />
        <Skeleton className="h-3 w-20" />
        <Skeleton className="h-3 w-12" />
        <div className="flex-1" />
        <Skeleton className="h-3 w-24" />
      </div>
    </div>
  );
}
