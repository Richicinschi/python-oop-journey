'use client';

import { HeroSection } from './hero-section';
import { ProgressCard } from './progress-card';
import { QuickActions } from './quick-actions';
import { ActivityList } from './activity-item';
import { StatCard } from './stat-card';
import type { DashboardData } from '@/types/dashboard';

const mockData: DashboardData = {
  isLoggedIn: true,
  stats: {
    totalProblems: 453,
    solvedProblems: 42,
    currentStreak: 7,
    longestStreak: 14,
    totalTimeSpent: 3600 * 20,
    averageSessionLength: 3600,
    timeThisWeek: 3600 * 5,
    lastActive: new Date().toISOString(),
  },
  weeksProgress: [],
  recentActivity: [],
  recommendations: [],
  currentPosition: null,
};

export function Dashboard() {
  const overallProgress = Math.round((mockData.stats.solvedProblems / mockData.stats.totalProblems) * 100);

  return (
    <div className="space-y-6">
      <HeroSection data={mockData} overallProgress={overallProgress} />
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <ProgressCard weekNumber={1} weekTitle="Week 1" completedProblems={5} totalProblems={10} />
        <StatCard title="Problems Solved" value={42} trend={{ value: 12, positive: true }} />
        <StatCard title="Current Streak" value={7} trend={{ value: 2, positive: true }} />
      </div>
      <QuickActions />
    </div>
  );
}
