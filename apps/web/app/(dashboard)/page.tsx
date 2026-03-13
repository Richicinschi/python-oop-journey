'use client';

import { useEffect, useState, useMemo } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  Code, 
  Trophy, 
  Zap,
  Target,
  Clock,
  Calendar,
  TrendingUp,
  ArrowRight,
  Sparkles,
  Play,
  RotateCcw,
  ChevronRight,
  FolderGit2
} from 'lucide-react';
import Link from 'next/link';

// Dashboard components
import { HeroSection } from '@/components/dashboard/hero-section';
import { EmptyState } from '@/components/dashboard/empty-state';
import { StatCard } from '@/components/dashboard/stat-card';
import { ProgressCard } from '@/components/dashboard/progress-card';
import { ActivityList } from '@/components/dashboard/activity-item';
import { RecommendationList } from '@/components/dashboard/recommendation-card';
import { CircularProgress } from '@/components/dashboard/circular-progress';
import { QuickActions, ActionButtons } from '@/components/dashboard/quick-actions';
import { ActiveProjectsSection } from '@/components/projects';
import { WeeklyProject } from '@/types/project';

// Hooks
import { useDashboardData } from '@/hooks/use-dashboard-data';

// Utils
function formatDuration(seconds: number): string {
  if (seconds < 60) return `${seconds}s`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m`;
  const hours = Math.floor(seconds / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`;
}

// Mock data for projects - in real app, fetch from API/store
const mockProjects: WeeklyProject[] = [
  {
    slug: 'week-01-project',
    title: 'CLI Calculator',
    description: 'Build a command-line calculator with basic operations',
    difficulty: 'beginner',
    estimatedHours: 2,
    week: 1,
    status: 'in_progress',
    completedTasks: 1,
    totalTasks: 3,
  },
  {
    slug: 'week-04-project',
    title: 'Library Management System',
    description: 'Build a library system with books and patrons',
    difficulty: 'intermediate',
    estimatedHours: 3,
    week: 4,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 4,
  },
];

const mockProjectProgress: Record<string, { status: 'not_started' | 'in_progress' | 'submitted'; files: any[]; totalTimeSpent: number }> = {
  'week-01-project': {
    status: 'in_progress',
    files: [
      { id: '1', name: 'calculator.py', isModified: false },
      { id: '2', name: 'test_calculator.py', isModified: true },
    ],
    totalTimeSpent: 3600,
  },
};

export default function DashboardPage() {
  const { 
    data, 
    isLoading, 
    derivedStats, 
    recommendations,
    loadMockData 
  } = useDashboardData();
  
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // Load mock data for demo (remove in production)
    if (typeof window !== 'undefined' && !localStorage.getItem('oop-journey-dashboard-v2')) {
      loadMockData();
    }
  }, [loadMockData]);

  if (!mounted || isLoading) {
    return <DashboardSkeleton />;
  }

  const isNewUser = !data.currentPosition;
  const currentWeek = data.weeksProgress.find(
    w => w.weekNumber === data.currentPosition?.weekNumber
  );

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <HeroSection data={data} overallProgress={derivedStats.overallProgress} />

      {/* Empty State for New Users */}
      {isNewUser ? (
        <EmptyState />
      ) : (
        <>
          {/* Quick Actions */}
          <section>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Quick Actions</h2>
            </div>
            <ActionButtons />
          </section>

          {/* Stats Overview */}
          <section>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Your Progress</h2>
              <Link href="/stats">
                <Button variant="ghost" size="sm" className="gap-1">
                  View All <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
            </div>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <StatCard
                title="Problems Solved"
                value={`${derivedStats.solvedProblems} / ${data.stats.totalProblems}`}
                description={`${derivedStats.overallProgress}% complete`}
                icon={Code}
                variant="highlight"
                index={0}
              />
              <StatCard
                title="Current Streak"
                value={`${data.stats.currentStreak} days`}
                description={data.stats.currentStreak > 0 ? 'Keep it up!' : 'Start your streak today'}
                icon={Zap}
                variant={data.stats.currentStreak > 0 ? 'warning' : 'default'}
                index={1}
              />
              <StatCard
                title="Time This Week"
                value={formatDuration(data.stats.timeThisWeek)}
                description={`Avg: ${formatDuration(data.stats.averageSessionLength)}/session`}
                icon={Clock}
                variant="default"
                index={2}
              />
              <StatCard
                title="Weeks Completed"
                value={`${derivedStats.completedWeeks} / 8`}
                description={`${derivedStats.inProgressWeeks} in progress`}
                icon={Trophy}
                variant={derivedStats.completedWeeks > 0 ? 'success' : 'default'}
                index={3}
              />
            </div>
          </section>

          {/* Active Projects Section */}
          <ActiveProjectsSection
            projects={mockProjects}
            progressMap={mockProjectProgress}
            currentWeekNumber={currentWeek?.weekNumber}
            variant="full"
          />

          {/* Main Content Grid */}
          <div className="grid gap-6 lg:grid-cols-3">
            {/* Left Column - Weekly Progress & Recommendations */}
            <div className="lg:col-span-2 space-y-6">
              {/* Current Progress Widget */}
              {currentWeek && (
                <Card>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div>
                        <CardTitle className="flex items-center gap-2">
                          <Target className="h-5 w-5 text-primary" />
                          Current Progress
                        </CardTitle>
                        <CardDescription>
                          Week {currentWeek.weekNumber}: {currentWeek.weekTitle}
                        </CardDescription>
                      </div>
                      <CircularProgress 
                        value={Math.round((currentWeek.completedProblems / currentWeek.totalProblems) * 100)} 
                        size={80}
                        strokeWidth={6}
                        showPercentage
                      />
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">Progress</span>
                        <span className="font-medium">
                          {currentWeek.completedProblems} / {currentWeek.totalProblems} problems
                        </span>
                      </div>
                      <Progress 
                        value={(currentWeek.completedProblems / currentWeek.totalProblems) * 100} 
                        className="h-2" 
                      />
                      <div className="flex gap-2 pt-2">
                        <Link href={`/weeks/${currentWeek.weekSlug}`} className="flex-1">
                          <Button className="w-full gap-2">
                            <Play className="h-4 w-4" />
                            Continue
                          </Button>
                        </Link>
                        <Link href="/weeks" className="flex-1">
                          <Button variant="outline" className="w-full gap-2">
                            <RotateCcw className="h-4 w-4" />
                            Review
                          </Button>
                        </Link>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Weekly Overview */}
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="flex items-center gap-2">
                        <Calendar className="h-5 w-5 text-primary" />
                        Weekly Overview
                      </CardTitle>
                      <CardDescription>
                        Track your progress across all 8 weeks
                      </CardDescription>
                    </div>
                    <Link href="/weeks">
                      <Button variant="ghost" size="sm" className="gap-1">
                        View All <ChevronRight className="h-4 w-4" />
                      </Button>
                    </Link>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-4 sm:grid-cols-2">
                    {data.weeksProgress.map((week, index) => (
                      <ProgressCard key={week.weekSlug} week={week} index={index} />
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Right Column - Activity & Recommendations */}
            <div className="space-y-6">
              {/* Recommendations */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="h-5 w-5 text-primary" />
                    Recommended Next
                  </CardTitle>
                  <CardDescription>
                    Personalized suggestions for you
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <RecommendationList recommendations={recommendations} />
                </CardContent>
              </Card>

              {/* Recent Activity */}
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5 text-primary" />
                      Recent Activity
                    </CardTitle>
                  </div>
                  <CardDescription>
                    Your last 5 problem attempts
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ActivityList activities={data.recentActivity} />
                </CardContent>
              </Card>

              {/* Quick Jump */}
              <Card className="bg-muted/50">
                <CardHeader className="pb-3">
                  <CardTitle className="text-base">Quick Navigation</CardTitle>
                </CardHeader>
                <CardContent>
                  <QuickActions />
                </CardContent>
              </Card>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

// Loading Skeleton
function DashboardSkeleton() {
  return (
    <div className="space-y-8 animate-pulse">
      {/* Hero Skeleton */}
      <div className="h-64 rounded-2xl bg-muted" />
      
      {/* Stats Skeleton */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-32 rounded-xl bg-muted" />
        ))}
      </div>
      
      {/* Active Projects Skeleton */}
      <div className="h-48 rounded-xl bg-muted" />
      
      {/* Content Skeleton */}
      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-6">
          <div className="h-48 rounded-xl bg-muted" />
          <div className="h-96 rounded-xl bg-muted" />
        </div>
        <div className="space-y-6">
          <div className="h-64 rounded-xl bg-muted" />
          <div className="h-64 rounded-xl bg-muted" />
        </div>
      </div>
    </div>
  );
}
