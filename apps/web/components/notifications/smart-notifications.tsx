'use client';

import { useEffect, useCallback } from 'react';
import { useToast } from '@/components/ui/use-toast';
import { 
  useReviewStats, 
  useWeakAreas, 
  useDifficultySuggestion,
  useStreakInfo,
} from '@/hooks/use-recommendations';
import { 
  RotateCcw, 
  TrendingDown, 
  Zap, 
  Flame,
  Bell,
  X
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

interface SmartNotificationsProps {
  userId?: string;
}

// Track shown notifications to avoid duplicates
const shownNotifications = new Set<string>();

export function SmartNotifications({ userId }: SmartNotificationsProps) {
  const { toast } = useToast();
  const { data: reviewStats } = useReviewStats();
  const { data: weakAreas } = useWeakAreas(1);
  const { data: difficultySuggestion } = useDifficultySuggestion();
  const { data: streakInfo } = useStreakInfo();

  const showNotification = useCallback((id: string, content: React.ReactNode, duration?: number) => {
    if (shownNotifications.has(id)) return;
    
    shownNotifications.add(id);
    
    toast({
      title: content,
      duration: duration || 5000,
    });
  }, [toast]);

  useEffect(() => {
    if (!userId) return;

    // Review due notifications
    if (reviewStats && reviewStats.dueNow > 0) {
      const notificationId = `review-due-${reviewStats.dueNow}`;
      showNotification(
        notificationId,
        <div className="flex items-start gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-yellow-500/10">
            <RotateCcw className="h-4 w-4 text-yellow-600" />
          </div>
          <div className="flex-1">
            <p className="font-medium">You have {reviewStats.dueNow} review{reviewStats.dueNow > 1 ? 's' : ''} due</p>
            <p className="text-sm text-muted-foreground">Spaced repetition helps you retain what you learn</p>
            <Link href="/reviews">
              <Button size="sm" variant="secondary" className="mt-2">
                Start Review
              </Button>
            </Link>
          </div>
        </div>,
        8000
      );
    }

    // Weak area notification (show once per session)
    if (weakAreas && weakAreas.length > 0) {
      const notificationId = `weak-area-${weakAreas[0].topicSlug}`;
      showNotification(
        notificationId,
        <div className="flex items-start gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-orange-500/10">
            <TrendingDown className="h-4 w-4 text-orange-600" />
          </div>
          <div className="flex-1">
            <p className="font-medium">Focus on {weakAreas[0].topicName}</p>
            <p className="text-sm text-muted-foreground">Your mastery score is {Math.round(weakAreas[0].masteryScore)}%</p>
            <Link href={`/weeks/${weakAreas[0].topicSlug}`}>
              <Button size="sm" variant="secondary" className="mt-2">
                Review Topic
              </Button>
            </Link>
          </div>
        </div>,
        8000
      );
    }

    // Difficulty progression notification
    if (difficultySuggestion) {
      const notificationId = `difficulty-${difficultySuggestion.suggestedDifficulty}`;
      showNotification(
        notificationId,
        <div className="flex items-start gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-500/10">
            <Zap className="h-4 w-4 text-green-600" />
          </div>
          <div className="flex-1">
            <p className="font-medium">Ready for {difficultySuggestion.suggestedDifficulty} problems!</p>
            <p className="text-sm text-muted-foreground">{difficultySuggestion.message}</p>
          </div>
        </div>,
        6000
      );
    }

    // Streak milestone notifications
    if (streakInfo) {
      if (streakInfo.currentStreak === 7) {
        showNotification(
          'streak-7',
          <div className="flex items-start gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-orange-500/10">
              <Flame className="h-4 w-4 text-orange-600" />
            </div>
            <div className="flex-1">
              <p className="font-medium">🔥 7-day streak!</p>
              <p className="text-sm text-muted-foreground">You're on fire! Keep up the great work!</p>
            </div>
          </div>,
          6000
        );
      } else if (streakInfo.currentStreak === 30) {
        showNotification(
          'streak-30',
          <div className="flex items-start gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-orange-500/10">
              <Flame className="h-4 w-4 text-orange-600" />
            </div>
            <div className="flex-1">
              <p className="font-medium">🎉 30-day streak!</p>
              <p className="text-sm text-muted-foreground">Incredible dedication! You're building amazing habits!</p>
            </div>
          </div>,
          8000
        );
      }
    }
  }, [userId, reviewStats, weakAreas, difficultySuggestion, streakInfo, showNotification]);

  // This component doesn't render anything visible
  return null;
}

// Hook to manually trigger notification
export function useSmartNotification() {
  const { toast } = useToast();

  const notifyReviewDue = useCallback((count: number) => {
    toast({
      title: (
        <div className="flex items-center gap-2">
          <Bell className="h-4 w-4 text-yellow-600" />
          <span>{count} review{count > 1 ? 's' : ''} due</span>
        </div>
      ),
      description: 'Keep your knowledge fresh with spaced repetition',
    });
  }, [toast]);

  const notifyStreak = useCallback((days: number) => {
    toast({
      title: (
        <div className="flex items-center gap-2">
          <Flame className="h-4 w-4 text-orange-600" />
          <span>{days}-day streak! 🔥</span>
        </div>
      ),
      description: 'Keep it up! Consistent practice leads to mastery.',
    });
  }, [toast]);

  const notifyDifficultyProgression = useCallback((newDifficulty: string) => {
    toast({
      title: (
        <div className="flex items-center gap-2">
          <Zap className="h-4 w-4 text-green-600" />
          <span>Ready for {newDifficulty}!</span>
        </div>
      ),
      description: 'Your performance shows you\'re ready for more challenging problems.',
    });
  }, [toast]);

  return {
    notifyReviewDue,
    notifyStreak,
    notifyDifficultyProgression,
  };
}
