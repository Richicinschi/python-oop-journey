'use client';

import React, { useMemo } from 'react';
import { HeroSection } from './hero-section';
import { ProgressCard } from './progress-card';
import { QuickActions } from './quick-actions';
import { ActivityList } from './activity-item';
import { StatCard } from './stat-card';
import type { DashboardData, WeekProgress } from '@/types/dashboard';
import { CheckCircle, Flame, Target } from 'lucide-react';

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

const mockWeek: WeekProgress = {
  weekNumber: 1,
  weekSlug: 'week-01-foundations',
  weekTitle: 'Foundations',
  totalProblems: 63,
  completedProblems: 5,
  isStarted: true,
  isCompleted: false,
};

// Memoized stat cards for better performance
const MemoizedStatCard = React.memo(StatCard);
const MemoizedProgressCard = React.memo(ProgressCard);
const MemoizedHeroSection = React.memo(HeroSection);
const MemoizedQuickActions = React.memo(QuickActions);

MemoizedStatCard.displayName = 'MemoizedStatCard';
MemoizedProgressCard.displayName = 'MemoizedProgressCard';
MemoizedHeroSection.displayName = 'MemoizedHeroSection';
MemoizedQuickActions.displayName = 'MemoizedQuickActions';

export const Dashboard = React.memo(function Dashboard() {
  // Memoize derived data calculations
  const overallProgress = useMemo(() => 
    Math.round((mockData.stats.solvedProblems / mockData.stats.totalProblems) * 100),
    []
  );

  // Memoize stat card data to prevent unnecessary re-renders
  const statCards = useMemo(() => [
    { 
      title: "Problems Solved", 
      value: 42, 
      icon: CheckCircle, 
      trend: { value: 12, label: '+12%', positive: true } 
    },
    { 
      title: "Current Streak", 
      value: 7, 
      icon: Flame, 
      trend: { value: 2, label: '+2 days', positive: true } 
    },
  ], []);

  return (
    <div className="space-y-6">
      <MemoizedHeroSection data={mockData} overallProgress={overallProgress} />
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <MemoizedProgressCard week={mockWeek} />
        {statCards.map((stat, index) => (
          <MemoizedStatCard 
            key={stat.title}
            title={stat.title} 
            value={stat.value} 
            icon={stat.icon} 
            trend={stat.trend}
            index={index}
          />
        ))}
      </div>
      <MemoizedQuickActions />
    </div>
  );
});
