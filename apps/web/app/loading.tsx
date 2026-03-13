"use client";

import { Skeleton } from "@/components/ui/skeleton";

/**
 * Global loading UI for the Next.js app
 * This is shown while page content is loading
 */
export default function Loading() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header skeleton */}
      <header className="h-14 border-b bg-background">
        <div className="container h-full flex items-center justify-between">
          <Skeleton className="h-6 w-32" />
          <div className="flex items-center gap-4">
            <Skeleton className="h-8 w-8 rounded-full" />
            <Skeleton className="h-8 w-20" />
          </div>
        </div>
      </header>

      {/* Main content skeleton */}
      <main className="flex-1 container py-8">
        {/* Page title */}
        <Skeleton className="h-10 w-64 mb-8" />

        {/* Content grid */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="space-y-4">
              <Skeleton className="h-48 w-full" />
              <Skeleton className="h-6 w-3/4" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-2/3" />
            </div>
          ))}
        </div>

        {/* Additional content */}
        <div className="mt-8 space-y-4">
          <Skeleton className="h-8 w-48" />
          <div className="space-y-2">
            {Array.from({ length: 4 }).map((_, i) => (
              <Skeleton key={i} className="h-16 w-full" />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
