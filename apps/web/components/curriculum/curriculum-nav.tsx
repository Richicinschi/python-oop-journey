'use client';

import { WeekNavigator } from './week-navigator';
import { getWeeks } from '@/lib/curriculum-loader';

export function CurriculumNav() {
  const weeks = getWeeks();
  return <WeekNavigator weeks={weeks} />;
}
