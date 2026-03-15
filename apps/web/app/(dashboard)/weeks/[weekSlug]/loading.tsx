'use client';

import { WeekSkeleton } from '@/components/weeks/week-skeleton';

/**
 * Loading UI for the individual week page
 * Shows while week data is loading
 */
export default function WeekLoading() {
  return <WeekSkeleton />;
}
