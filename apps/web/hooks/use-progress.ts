'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { api, Progress, ProgressUpdate, ProgressStats, WeekProgress, ProblemStatus } from '@/lib/api';

interface UseProgressReturn {
  progress: Progress[];
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
  // Local progress functions for component compatibility
  completeProblem: (problemSlug: string) => void;
  isCompleted: (problemSlug: string) => boolean;
  updateStreak: () => void;
}

interface UseProblemProgressReturn {
  progress: Progress | null;
  isLoading: boolean;
  error: Error | null;
  updateProgress: (data: ProgressUpdate) => Promise<Progress | null>;
  recordAttempt: () => Promise<Progress | null>;
  refetch: () => Promise<void>;
}

interface UseUpdateProgressReturn {
  updateProgress: (problemSlug: string, data: ProgressUpdate) => Promise<Progress | null>;
  isLoading: boolean;
  error: Error | null;
}

interface UseWeekProgressReturn {
  weekProgress: WeekProgress | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

interface UseProgressStatsReturn {
  stats: ProgressStats | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

// Local storage key for offline support
const PROGRESS_STORAGE_KEY = 'oop-journey-progress-cache';
const STATS_STORAGE_KEY = 'oop-journey-progress-stats';

/**
 * Hook to get all user progress
 */
export function useProgress(): UseProgressReturn {
  const [progress, setProgress] = useState<Progress[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchProgress = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await api.progress.getAll();
      setProgress(data.items);
      
      // Cache to localStorage
      localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(data.items));
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch progress'));
      
      // Try to load from cache on error
      const cached = localStorage.getItem(PROGRESS_STORAGE_KEY);
      if (cached) {
        try {
          setProgress(JSON.parse(cached));
        } catch {
          // Ignore parse errors
        }
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchProgress();
  }, [fetchProgress]);

  // Local progress functions (backward compatible)
  const localProgress = useLocalProgress();

  return {
    progress,
    isLoading,
    error,
    refetch: fetchProgress,
    completeProblem: localProgress.completeProblem,
    isCompleted: localProgress.isCompleted,
    updateStreak: localProgress.updateStreak,
  };
}

/**
 * Hook to get progress for a specific problem
 */
export function useProblemProgress(problemSlug: string): UseProblemProgressReturn {
  const [progress, setProgress] = useState<Progress | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchProgress = useCallback(async () => {
    if (!problemSlug) return;
    
    try {
      setIsLoading(true);
      setError(null);
      const data = await api.progress.get(problemSlug);
      setProgress(data);
    } catch (err) {
      // If 404, it means no progress yet - that's ok
      if (err instanceof Error && err.message.includes('404')) {
        setProgress(null);
      } else {
        setError(err instanceof Error ? err : new Error('Failed to fetch progress'));
      }
    } finally {
      setIsLoading(false);
    }
  }, [problemSlug]);

  const updateProgress = useCallback(async (data: ProgressUpdate) => {
    try {
      setError(null);
      const updated = await api.progress.update(problemSlug, data);
      setProgress(updated);
      return updated;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to update progress'));
      return null;
    }
  }, [problemSlug]);

  const recordAttempt = useCallback(async () => {
    try {
      setError(null);
      const updated = await api.progress.recordAttempt(problemSlug);
      setProgress(updated);
      return updated;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to record attempt'));
      return null;
    }
  }, [problemSlug]);

  useEffect(() => {
    fetchProgress();
  }, [fetchProgress]);

  return {
    progress,
    isLoading,
    error,
    updateProgress,
    recordAttempt,
    refetch: fetchProgress,
  };
}

/**
 * Hook to update progress (mutation only)
 */
export function useUpdateProgress(): UseUpdateProgressReturn {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const updateProgress = useCallback(async (problemSlug: string, data: ProgressUpdate) => {
    try {
      setIsLoading(true);
      setError(null);
      const updated = await api.progress.update(problemSlug, data);
      return updated;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to update progress'));
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    updateProgress,
    isLoading,
    error,
  };
}

/**
 * Hook to get week progress
 */
export function useWeekProgress(weekSlug: string): UseWeekProgressReturn {
  const [weekProgress, setWeekProgress] = useState<WeekProgress | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchWeekProgress = useCallback(async () => {
    if (!weekSlug) return;
    
    try {
      setIsLoading(true);
      setError(null);
      const data = await api.progress.getWeekProgress(weekSlug);
      setWeekProgress(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch week progress'));
    } finally {
      setIsLoading(false);
    }
  }, [weekSlug]);

  useEffect(() => {
    fetchWeekProgress();
  }, [fetchWeekProgress]);

  return {
    weekProgress,
    isLoading,
    error,
    refetch: fetchWeekProgress,
  };
}

/**
 * Hook to get overall progress stats
 */
export function useProgressStats(): UseProgressStatsReturn {
  const [stats, setStats] = useState<ProgressStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchStats = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await api.progress.getStats();
      setStats(data);
      
      // Cache to localStorage
      localStorage.setItem(STATS_STORAGE_KEY, JSON.stringify(data));
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch stats'));
      
      // Try to load from cache on error
      const cached = localStorage.getItem(STATS_STORAGE_KEY);
      if (cached) {
        try {
          setStats(JSON.parse(cached));
        } catch {
          // Ignore parse errors
        }
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  return {
    stats,
    isLoading,
    error,
    refetch: fetchStats,
  };
}

// Legacy hook for backward compatibility with localStorage
interface LegacyProgressData {
  completedProblems: string[];
  totalProblems: number;
  streakDays: number;
  lastActive: string | null;
}

const LEGACY_STORAGE_KEY = 'oop-journey-progress';

/**
 * Legacy hook for backward compatibility - uses localStorage
 * @deprecated Use useProgress() for server-side progress
 */
export function useLocalProgress() {
  const [progress, setProgress] = useState<LegacyProgressData>({
    completedProblems: [],
    totalProblems: 50,
    streakDays: 0,
    lastActive: null,
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem(LEGACY_STORAGE_KEY);
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setProgress(prev => ({ ...prev, ...parsed }));
      } catch {
        // Ignore parse errors
      }
    }
    setIsLoading(false);
  }, []);

  const completeProblem = useCallback((problemSlug: string) => {
    setProgress((prev) => {
      if (prev.completedProblems.includes(problemSlug)) {
        return prev;
      }
      
      const newProgress = {
        ...prev,
        completedProblems: [...prev.completedProblems, problemSlug],
        lastActive: new Date().toISOString(),
      };
      
      localStorage.setItem(LEGACY_STORAGE_KEY, JSON.stringify(newProgress));
      return newProgress;
    });
  }, []);

  const isCompleted = useCallback((problemSlug: string) => {
    return progress.completedProblems.includes(problemSlug);
  }, [progress.completedProblems]);

  const getCompletionPercentage = useCallback(() => {
    if (progress.totalProblems === 0) return 0;
    return Math.round((progress.completedProblems.length / progress.totalProblems) * 100);
  }, [progress.completedProblems.length, progress.totalProblems]);

  const updateStreak = useCallback(() => {
    setProgress((prev) => {
      const today = new Date().toDateString();
      const lastActiveDate = prev.lastActive ? new Date(prev.lastActive).toDateString() : null;
      
      // Only update streak if last active was not today
      if (lastActiveDate !== today) {
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        
        const isConsecutiveDay = lastActiveDate === yesterday.toDateString();
        const newStreakDays = isConsecutiveDay ? prev.streakDays + 1 : 1;
        
        const newProgress = {
          ...prev,
          streakDays: newStreakDays,
          lastActive: new Date().toISOString(),
        };
        
        localStorage.setItem(LEGACY_STORAGE_KEY, JSON.stringify(newProgress));
        return newProgress;
      }
      
      return prev;
    });
  }, []);

  return {
    progress,
    isLoading,
    completeProblem,
    isCompleted,
    getCompletionPercentage,
    updateStreak,
  };
}
