'use client';

import { WeekListSkeleton } from '@/components/weeks/week-skeleton';

/**
 * Loading UI for the weeks list page
 * Shows while curriculum data is loading
 */
export default function WeeksLoading() {
  return <WeekListSkeleton />;
}
