"use client";

import dynamic from "next/dynamic";
import { Suspense } from "react";

// Skeleton components for loading states
export function DashboardSkeleton() {
  return (
    <div className="space-y-6 p-6">
      <div className="h-8 w-48 bg-muted rounded animate-pulse" />
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="h-32 bg-muted rounded animate-pulse" />
        ))}
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {Array.from({ length: 2 }).map((_, i) => (
          <div key={i} className="h-64 bg-muted rounded animate-pulse" />
        ))}
      </div>
    </div>
  );
}

export function CurriculumSkeleton() {
  return (
    <div className="space-y-4 p-6">
      <div className="h-8 w-64 bg-muted rounded animate-pulse" />
      <div className="space-y-2">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="h-16 bg-muted rounded animate-pulse" />
        ))}
      </div>
    </div>
  );
}

export function ProblemSkeleton() {
  return (
    <div className="h-screen flex flex-col">
      <div className="h-14 border-b bg-muted animate-pulse" />
      <div className="flex-1 flex">
        <div className="w-1/2 border-r bg-muted animate-pulse" />
        <div className="w-1/2 bg-muted animate-pulse" />
      </div>
    </div>
  );
}

export function ProjectSkeleton() {
  return (
    <div className="h-screen flex flex-col">
      <div className="h-14 border-b bg-muted animate-pulse" />
      <div className="flex-1 flex">
        <div className="w-64 border-r bg-muted animate-pulse" />
        <div className="flex-1 bg-muted animate-pulse" />
      </div>
    </div>
  );
}

export function SearchSkeleton() {
  return (
    <div className="space-y-4 p-4">
      <div className="h-10 bg-muted rounded animate-pulse" />
      <div className="space-y-2">
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={i} className="h-20 bg-muted rounded animate-pulse" />
        ))}
      </div>
    </div>
  );
}

// Lazy loaded dashboard components
export const LazyDashboard = dynamic(
  () => import("@/components/dashboard").then((mod) => ({ default: mod.Dashboard })),
  {
    ssr: false,
    loading: DashboardSkeleton,
  }
);

// Lazy loaded curriculum components
export const LazyCurriculumNav = dynamic(
  () => import("@/components/curriculum").then((mod) => ({ default: mod.CurriculumNav })),
  {
    ssr: true,
    loading: CurriculumSkeleton,
  }
);

// Lazy loaded search component
export const LazySearchDialog = dynamic(
  () => import("@/components/search").then((mod) => ({ default: mod.SearchDialog })),
  {
    ssr: false,
    loading: SearchSkeleton,
  }
);

// Lazy loaded verification panel
export const LazyVerificationPanel = dynamic(
  () => import("@/components/verification").then((mod) => ({ default: mod.VerificationPanel })),
  {
    ssr: false,
    loading: () => (
      <div className="p-4 space-y-4">
        <div className="h-6 w-32 bg-muted rounded animate-pulse" />
        <div className="space-y-2">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="h-12 bg-muted rounded animate-pulse" />
          ))}
        </div>
      </div>
    ),
  }
);

// Wrapper component with suspense
interface LazyWrapperProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function LazyWrapper({ children, fallback }: LazyWrapperProps) {
  return (
    <Suspense fallback={fallback || <div className="p-4">Loading...</div>}>
      {children}
    </Suspense>
  );
}
