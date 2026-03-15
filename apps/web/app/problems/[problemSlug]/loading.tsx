'use client';

import { ProblemSkeleton } from '@/components/problems/problem-skeleton';

/**
 * Loading UI for the problem page
 * Shows while problem data is loading
 */
export default function ProblemLoading() {
  return <ProblemSkeleton />;
}
