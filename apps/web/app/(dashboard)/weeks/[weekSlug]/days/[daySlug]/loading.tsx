'use client';

import { DaySkeleton } from '@/components/weeks/day-skeleton';

/**
 * Loading UI for the day page
 * Shows while day data is loading
 */
export default function DayLoading() {
  return <DaySkeleton />;
}
