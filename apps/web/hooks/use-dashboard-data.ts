'use client';

import { useState, useEffect, useCallback, useMemo } from 'react';
import { 
  DashboardData, 
  UserStats, 
  WeekProgress, 
  ActivityItem, 
  Recommendation,
  WEEKS_DATA,
  TOTAL_PROBLEMS 
} from '@/types/dashboard';

const STORAGE_KEY = 'oop-journey-dashboard-v2';

const defaultStats: UserStats = {
  totalProblems: TOTAL_PROBLEMS,
  solvedProblems: 0,
  currentStreak: 0,
  longestStreak: 0,
  totalTimeSpent: 0,
  averageSessionLength: 0,
  timeThisWeek: 0,
  lastActive: null,
};

const createDefaultWeeksProgress = (): WeekProgress[] => 
  WEEKS_DATA.map(w => ({
    weekNumber: w.number,
    weekSlug: w.slug,
    weekTitle: w.title,
    totalProblems: w.problemCount,
    completedProblems: 0,
    isStarted: false,
    isCompleted: false,
  }));

function generateMockData(): DashboardData {
  // Simulate a user who has completed some problems
  const weeksProgress = createDefaultWeeksProgress();
  weeksProgress[0].isStarted = true;
  weeksProgress[0].completedProblems = 15;
  weeksProgress[0].lastAccessed = new Date().toISOString();
  weeksProgress[1].isStarted = true;
  weeksProgress[1].completedProblems = 5;
  
  const recentActivity: ActivityItem[] = [
    {
      id: '1',
      problemSlug: 'problem-01-hello-world',
      problemTitle: 'Hello World',
      weekNumber: 1,
      dayNumber: 1,
      status: 'completed',
      timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(), // 30 min ago
      timeSpent: 120,
    },
    {
      id: '2',
      problemSlug: 'problem-02-variables',
      problemTitle: 'Variable Assignment',
      weekNumber: 1,
      dayNumber: 2,
      status: 'completed',
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), // 2 hours ago
      timeSpent: 180,
    },
    {
      id: '3',
      problemSlug: 'problem-03-functions',
      problemTitle: 'Simple Function',
      weekNumber: 1,
      dayNumber: 3,
      status: 'attempted',
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(), // 1 day ago
      timeSpent: 300,
    },
  ];

  return {
    userName: 'Learner',
    isLoggedIn: true,
    stats: {
      ...defaultStats,
      solvedProblems: 20,
      currentStreak: 3,
      longestStreak: 5,
      totalTimeSpent: 3600 * 5, // 5 hours
      averageSessionLength: 600, // 10 minutes
      timeThisWeek: 3600 * 2, // 2 hours
      lastActive: new Date().toISOString(),
    },
    weeksProgress,
    recentActivity,
    recommendations: [],
    currentPosition: {
      weekNumber: 1,
      dayNumber: 3,
      problemSlug: 'problem-03-functions',
    },
  };
}

export function useDashboardData() {
  const [data, setData] = useState<DashboardData>({
    userName: undefined,
    isLoggedIn: false,
    stats: defaultStats,
    weeksProgress: createDefaultWeeksProgress(),
    recentActivity: [],
    recommendations: [],
    currentPosition: null,
  });
  const [isLoading, setIsLoading] = useState(true);

  // Load data from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setData(prev => ({ ...prev, ...parsed }));
      } catch {
        // Invalid stored data, use defaults
      }
    }
    setIsLoading(false);
  }, []);

  // Save data to localStorage when it changes
  useEffect(() => {
    if (!isLoading) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    }
  }, [data, isLoading]);

  // Calculate derived stats
  const derivedStats = useMemo(() => {
    const solvedProblems = data.weeksProgress.reduce(
      (sum, w) => sum + w.completedProblems, 
      0
    );
    const completedWeeks = data.weeksProgress.filter(w => w.isCompleted).length;
    const inProgressWeeks = data.weeksProgress.filter(w => w.isStarted && !w.isCompleted).length;
    const overallProgress = Math.round((solvedProblems / TOTAL_PROBLEMS) * 100);
    
    return {
      solvedProblems,
      completedWeeks,
      inProgressWeeks,
      overallProgress,
    };
  }, [data.weeksProgress]);

  // Generate recommendations based on progress
  const recommendations = useMemo((): Recommendation[] => {
    const recs: Recommendation[] = [];
    
    if (!data.currentPosition) {
      recs.push({
        type: 'start',
        title: 'Start Your Journey',
        description: 'Begin with Week 1 and learn Python fundamentals',
        actionLabel: 'Start Week 1',
        priority: 'high',
      });
    } else {
      const currentWeek = data.weeksProgress.find(
        w => w.weekNumber === data.currentPosition?.weekNumber
      );
      
      if (currentWeek && !currentWeek.isCompleted) {
        recs.push({
          type: 'continue',
          title: `Continue Week ${currentWeek.weekNumber}`,
          description: `You're making great progress! Complete ${currentWeek.totalProblems - currentWeek.completedProblems} more problems to finish ${currentWeek.weekTitle}.`,
          weekNumber: currentWeek.weekNumber,
          actionLabel: 'Continue Learning',
          priority: 'high',
        });
      }
      
      // Suggest review if there are failed attempts
      const failedAttempts = data.recentActivity.filter(a => a.status === 'failed').length;
      if (failedAttempts > 0) {
        recs.push({
          type: 'review',
          title: 'Review Difficult Problems',
          description: `You have ${failedAttempts} problems that need attention. Review them to strengthen your understanding.`,
          actionLabel: 'Review Problems',
          priority: 'medium',
        });
      }
      
      // Suggest practice
      recs.push({
        type: 'practice',
        title: 'Practice Random Problem',
        description: 'Sharpen your skills with a random problem from your current level.',
        actionLabel: 'Practice Now',
        priority: 'low',
      });
    }
    
    return recs;
  }, [data.currentPosition, data.weeksProgress, data.recentActivity]);

  // Actions
  const updateProgress = useCallback((weekNumber: number, completedProblems: number) => {
    setData(prev => {
      const weeksProgress = [...prev.weeksProgress];
      const weekIndex = weeksProgress.findIndex(w => w.weekNumber === weekNumber);
      
      if (weekIndex >= 0) {
        const week = weeksProgress[weekIndex];
        weeksProgress[weekIndex] = {
          ...week,
          completedProblems,
          isStarted: completedProblems > 0,
          isCompleted: completedProblems >= week.totalProblems,
          lastAccessed: new Date().toISOString(),
        };
      }
      
      return { ...prev, weeksProgress };
    });
  }, []);

  const addActivity = useCallback((activity: Omit<ActivityItem, 'id' | 'timestamp'>) => {
    setData(prev => {
      const newActivity: ActivityItem = {
        ...activity,
        id: Math.random().toString(36).substr(2, 9),
        timestamp: new Date().toISOString(),
      };
      
      return {
        ...prev,
        recentActivity: [newActivity, ...prev.recentActivity].slice(0, 50),
      };
    });
  }, []);

  const setCurrentPosition = useCallback((position: DashboardData['currentPosition']) => {
    setData(prev => ({ ...prev, currentPosition: position }));
  }, []);

  const setUser = useCallback((userName: string, isLoggedIn: boolean = true) => {
    setData(prev => ({ ...prev, userName, isLoggedIn }));
  }, []);

  const resetProgress = useCallback(() => {
    setData({
      userName: data.userName,
      isLoggedIn: data.isLoggedIn,
      stats: defaultStats,
      weeksProgress: createDefaultWeeksProgress(),
      recentActivity: [],
      recommendations: [],
      currentPosition: null,
    });
  }, [data.userName, data.isLoggedIn]);

  // For demo purposes - load mock data
  const loadMockData = useCallback(() => {
    setData(generateMockData());
  }, []);

  return {
    data,
    isLoading,
    derivedStats,
    recommendations,
    updateProgress,
    addActivity,
    setCurrentPosition,
    setUser,
    resetProgress,
    loadMockData,
  };
}
