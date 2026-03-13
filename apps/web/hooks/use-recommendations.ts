"'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';

// Types
export interface Recommendation {
  type: 'next_problem' | 'review' | 'theory' | 'practice' | 'difficulty_adjustment' | 'remedial' | 'challenge';
  itemType: 'problem' | 'day' | 'week' | 'theory' | 'suggestion';
  itemSlug: string;
  itemTitle: string;
  reason: string;
  priority: number;
  estimatedTimeMinutes: number;
  context: {
    difficulty?: string;
    weekSlug?: string;
    daySlug?: string;
    easeFactor?: number;
    interval?: number;
    repetitions?: number;
    daysOverdue?: number;
    currentDifficulty?: string;
    suggestedDifficulty?: string;
    successRate?: number;
    masteryScore?: number;
    problemsStruggled?: string[];
    isChallenge?: boolean;
  };
}

export interface ReviewItem {
  problemSlug: string;
  problemTitle: string;
  easeFactor: number;
  interval: number;
  repetitions: number;
  nextReview: string | null;
  daysOverdue: number;
  priority: number;
}

export interface ReviewQueue {
  items: ReviewItem[];
  total: number;
  dueToday: number;
  dueThisWeek: number;
}

export interface ReviewStats {
  totalItems: number;
  dueNow: number;
  dueToday: number;
  dueThisWeek: number;
  averageEaseFactor: number;
  completedReviews: number;
}

export interface WeakArea {
  topicSlug: string;
  topicName: string;
  masteryScore: number;
  level: string;
  problemsStruggled: string[];
  suggestedRemediation: string;
  priority: number;
}

export interface LearningPath {
  steps: {
    type: string;
    weekSlug: string;
    weekTitle: string;
    reason: string;
    estimatedDays?: number;
  }[];
  estimatedWeeks: number;
  focusAreas: string[];
  skippedTopics: string[];
  reasoning: string;
}

export interface DifficultySuggestion {
  currentDifficulty: string;
  suggestedDifficulty: string;
  successRate: number;
  message: string;
}

export interface TimeAnalytics {
  [difficulty: string]: {
    totalTimeSeconds: number;
    totalTimeFormatted: string;
    problemCount: number;
    averageTimeSeconds: number;
    averageTimeFormatted: string;
    medianTimeSeconds: number;
    minTimeSeconds: number;
    maxTimeSeconds: number;
  };
}

export interface AttemptPatterns {
  systematic: number;
  trialError: number;
  stuck: number;
  perfect: number;
  dominantPattern: string;
}

export interface TopicMastery {
  [topic: string]: {
    score: number;
    level: string;
    solved: number;
    total: number;
    completionPct: number;
    name: string;
  };
}

export interface LearningVelocity {
  velocityPerWeek: number;
  velocityPerDay: number;
  trend: 'accelerating' | 'steady' | 'decelerating';
  totalSolved: number;
  weeksActive: number;
}

export interface SuccessRate {
  attempted: number;
  solved: number;
  abandoned: number;
  successRate: number;
  abandonRate: number;
}

export interface LearningStats {
  problemsAttempted: number;
  problemsSolved: number;
  averageTimePerProblem: number;
  successRateByDifficulty: {
    [difficulty: string]: SuccessRate;
  };
  topicMastery: TopicMastery;
  streakDays: number;
  velocity: number;
}

export interface StreakInfo {
  currentStreak: number;
  longestStreak: number;
  lastReview: string | null;
}

// API functions
async function fetchNextRecommendation(): Promise<Recommendation> {
  const response = await fetch('/api/v1/recommendations/next', {
    credentials: 'include',
  });
  if (!response.ok) throw new Error('Failed to fetch recommendation');
  return response.json();
}

async function fetchAllRecommendations(limit: number = 10): Promise<Recommendation[]> {
  const response = await fetch(`/api/v1/recommendations/all?limit=${limit}`, {
    credentials: 'include',
  });
  if (!response.ok) throw new Error('Failed to fetch recommendations');
  return response.json();
}

async function fetchReviewQueue(limit: number = 10): Promise<ReviewQueue> {
  const response = await fetch(`/api/v1/recommendations/review?limit=${limit}`, {
    credentials: 'include',
  });
  if (!response.ok) throw new Error('Failed to fetch review queue');
  return response.json();
}

async function fetchReviewStats(): Promise<ReviewStats> {
  const response = await fetch('/api/v1/recommendations/review/stats', {
    credentials: 'include',
  });
  if (!response.ok) throw new Error('Failed to fetch review stats');
  return response.json();
}

async function recordReview(problemSlug: string, quality: number) {
  const response = await fetch(`/api/v1/recommendations/review/${problemSlug}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ quality }),
  });
  if (!response.ok) throw new Error('Failed to record review');
  return response.json();
}

async function fetchWeakAreas(limit: number = 5): Promise<WeakArea[]> {
  const response = await fetch(`/api/v1/recommendations/weak-areas?limit=${limit}`, {
    credentials: 'include',
  });
  if (!response.ok) throw new Error('Failed to fetch weak areas');
  return response.json();
}

async function fetchLearningPath(): Promise<LearningPath> {
  const response = await fetch('/api/v1/recommendations/path', {
    credentials: 'include',
  });
  if (!response.ok) throw new Error('Failed to fetch learning path');
  return response.json();
}

async function fetchDifficultySuggestion(): Promise<DifficultySuggestion | null> {
  const response = await fetch('/api/v1/recommendations/difficulty', {
    credentials: 'include',
  });
  if (!response.ok) throw new Error('Failed to fetch difficulty suggestion');
  return response.json();
}

async function fetchLearningStats(): Promise<LearningStats> {
  const response = await fetch('/api/v1/recommendations/stats', {
    credentials: 'include',
  });
  if (!response.ok) throw new Error('Failed to fetch learning stats');
  return response.json();
}

async function fetchStreakInfo(): Promise<StreakInfo> {
  const response = await fetch('/api/v1/recommendations/streak', {
    credentials: 'include',
  });
  if (!response.ok) throw new Error('Failed to fetch streak info');
  return response.json();
}

// Hooks
export function useNextRecommendation() {
  return useQuery({
    queryKey: ['recommendations', 'next'],
    queryFn: fetchNextRecommendation,
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 1,
  });
}

export function useRecommendations(limit: number = 10) {
  return useQuery({
    queryKey: ['recommendations', 'all', limit],
    queryFn: () => fetchAllRecommendations(limit),
    staleTime: 5 * 60 * 1000,
  });
}

export function useReviewQueue(limit: number = 10) {
  return useQuery({
    queryKey: ['recommendations', 'review-queue', limit],
    queryFn: () => fetchReviewQueue(limit),
    staleTime: 1 * 60 * 1000, // 1 minute - review queue changes frequently
  });
}

export function useReviewStats() {
  return useQuery({
    queryKey: ['recommendations', 'review-stats'],
    queryFn: fetchReviewStats,
    staleTime: 5 * 60 * 1000,
  });
}

export function useRecordReview() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ problemSlug, quality }: { problemSlug: string; quality: number }) =>
      recordReview(problemSlug, quality),
    onSuccess: () => {
      // Invalidate review-related queries
      queryClient.invalidateQueries({ queryKey: ['recommendations', 'review-queue'] });
      queryClient.invalidateQueries({ queryKey: ['recommendations', 'review-stats'] });
      queryClient.invalidateQueries({ queryKey: ['recommendations', 'next'] });
    },
  });
}

export function useWeakAreas(limit: number = 5) {
  return useQuery({
    queryKey: ['recommendations', 'weak-areas', limit],
    queryFn: () => fetchWeakAreas(limit),
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
}

export function useLearningPath() {
  return useQuery({
    queryKey: ['recommendations', 'path'],
    queryFn: fetchLearningPath,
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
}

export function useDifficultySuggestion() {
  return useQuery({
    queryKey: ['recommendations', 'difficulty'],
    queryFn: fetchDifficultySuggestion,
    staleTime: 10 * 60 * 1000,
  });
}

export function useLearningStats() {
  return useQuery({
    queryKey: ['recommendations', 'stats'],
    queryFn: fetchLearningStats,
    staleTime: 5 * 60 * 1000,
  });
}

export function useStreakInfo() {
  return useQuery({
    queryKey: ['recommendations', 'streak'],
    queryFn: fetchStreakInfo,
    staleTime: 5 * 60 * 1000,
  });
}

// Utility hook that combines multiple recommendation queries
export function useSmartDashboard() {
  const nextRec = useNextRecommendation();
  const reviewQueue = useReviewQueue(5);
  const weakAreas = useWeakAreas(3);
  const stats = useLearningStats();
  const difficulty = useDifficultySuggestion();
  const streak = useStreakInfo();

  const isLoading = 
    nextRec.isLoading || 
    reviewQueue.isLoading || 
    weakAreas.isLoading || 
    stats.isLoading;

  const hasReviewDue = (reviewQueue.data?.dueToday || 0) > 0;
  const hasWeakAreas = (weakAreas.data?.length || 0) > 0;
  const shouldAdjustDifficulty = difficulty.data !== null;

  return {
    isLoading,
    nextRecommendation: nextRec.data,
    reviewQueue: reviewQueue.data,
    weakAreas: weakAreas.data,
    stats: stats.data,
    difficultySuggestion: difficulty.data,
    streak: streak.data,
    hasReviewDue,
    hasWeakAreas,
    shouldAdjustDifficulty,
    // Helper to get the most urgent action
    getPriorityAction: () => {
      if (hasReviewDue) return { type: 'review', data: reviewQueue.data?.items[0] };
      if (shouldAdjustDifficulty) return { type: 'difficulty', data: difficulty.data };
      if (hasWeakAreas) return { type: 'weak-area', data: weakAreas.data?.[0] };
      return { type: 'next-problem', data: nextRec.data };
    },
  };
}
