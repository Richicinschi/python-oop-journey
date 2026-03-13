"use client";

import { Suspense } from "react";

/**
 * Root template with progressive loading
 * Wraps all pages with common UI elements
 */
export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen flex items-center justify-center">
          <div className="flex flex-col items-center gap-4">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
            <p className="text-sm text-muted-foreground">Loading...</p>
          </div>
        </div>
      }
    >
      {children}
    </Suspense>
  );
}
