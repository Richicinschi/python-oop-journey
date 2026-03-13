'use client';

import { HeroSection } from './hero-section';
import { ProgressCard } from './progress-card';
import { QuickActions } from './quick-actions';
import { ActivityList } from './activity-item';
import { StatCard } from './stat-card';

export function Dashboard() {
  return (
    <div className="space-y-6">
      <HeroSection />
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <ProgressCard weekNumber={1} weekTitle="Week 1" completedProblems={5} totalProblems={10} />
        <StatCard title="Problems Solved" value={42} trend={{ value: 12, positive: true }} />
        <StatCard title="Current Streak" value={7} trend={{ value: 2, positive: true }} />
      </div>
      <QuickActions />
    </div>
  );
}
