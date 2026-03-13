'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { 
  TrendingUp, 
  Clock, 
  Target, 
  Zap,
  BarChart3,
  ArrowUpRight,
  ArrowDownRight,
  Minus
} from 'lucide-react';
import { cn } from '@/lib/utils';
import type { LearningStats, LearningVelocity, DifficultySuggestion } from '@/hooks/use-recommendations';

interface LearningStatsCardProps {
  stats?: LearningStats;
  velocity?: LearningVelocity;
  difficultySuggestion?: DifficultySuggestion | null;
  isLoading?: boolean;
}

const trendIcons = {
  accelerating: ArrowUpRight,
  steady: Minus,
  decelerating: ArrowDownRight,
};

const trendColors = {
  accelerating: 'text-green-600',
  steady: 'text-blue-600',
  decelerating: 'text-orange-600',
};

export function LearningStatsCard({ 
  stats, 
  velocity, 
  difficultySuggestion, 
  isLoading 
}: LearningStatsCardProps) {
  if (isLoading) {
    return (
      <Card className="border-dashed animate-pulse">
        <CardHeader className="pb-3">
          <div className="h-5 w-1/3 bg-muted rounded" />
          <div className="h-4 w-2/3 bg-muted rounded mt-2" />
        </CardHeader>
        <CardContent>
          <div className="h-32 bg-muted rounded" />
        </CardContent>
      </Card>
    );
  }

  if (!stats) {
    return (
      <Card className="border-dashed">
        <CardContent className="py-8 text-center">
          <BarChart3 className="h-10 w-10 mx-auto mb-3 text-muted-foreground opacity-50" />
          <p className="text-sm text-muted-foreground font-medium">No stats available</p>
          <p className="text-xs text-muted-foreground mt-1">
            Start solving problems to see your analytics
          </p>
        </CardContent>
      </Card>
    );
  }

  const TrendIcon = velocity ? trendIcons[velocity.trend] : Minus;
  const trendColor = velocity ? trendColors[velocity.trend] : 'text-muted-foreground';

  // Calculate success rate
  const successRate = stats.problemsAttempted > 0
    ? Math.round((stats.problemsSolved / stats.problemsAttempted) * 100)
    : 0;

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-500/10">
              <BarChart3 className="h-4 w-4 text-blue-600" />
            </div>
            <div>
              <CardTitle className="text-base">Learning Stats</CardTitle>
              <CardDescription className="text-xs">
                Your progress at a glance
              </CardDescription>
            </div>
          </div>
          {velocity && (
            <div className={cn("flex items-center gap-1 text-xs", trendColor)}>
              <TrendIcon className="h-4 w-4" />
              <span className="capitalize">{velocity.trend}</span>
            </div>
          )}
        </div>
      </CardHeader>
      <CardContent className="pt-0 space-y-4">
        {/* Key metrics grid */}
        <div className="grid grid-cols-2 gap-3">
          <div className="p-3 bg-muted/50 rounded-lg">
            <div className="flex items-center gap-2 text-muted-foreground text-xs mb-1">
              <Target className="h-3.5 w-3.5" />
              Solved
            </div>
            <p className="text-2xl font-bold">{stats.problemsSolved}</p>
            <p className="text-xs text-muted-foreground">
              of {stats.problemsAttempted} attempted
            </p>
          </div>
          
          <div className="p-3 bg-muted/50 rounded-lg">
            <div className="flex items-center gap-2 text-muted-foreground text-xs mb-1">
              <Clock className="h-3.5 w-3.5" />
              Avg Time
            </div>
            <p className="text-2xl font-bold">
              {Math.round(stats.averageTimePerProblem / 60)}m
            </p>
            <p className="text-xs text-muted-foreground">
              per problem
            </p>
          </div>
        </div>

        {/* Success rate */}
        <div>
          <div className="flex items-center justify-between text-sm mb-1.5">
            <span className="text-muted-foreground">Success Rate</span>
            <span className="font-medium">{successRate}%</span>
          </div>
          <Progress value={successRate} className="h-2" />
        </div>

        {/* Velocity */}
        {velocity && (
          <div className="p-3 bg-muted/50 rounded-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-blue-600" />
                <span className="text-sm font-medium">Velocity</span>
              </div>
              <span className="text-sm font-bold">
                {velocity.velocityPerWeek.toFixed(1)} <span className="text-xs font-normal text-muted-foreground">/ week</span>
              </span>
            </div>
          </div>
        )}

        {/* Difficulty suggestion */}
        {difficultySuggestion && (
          <div className={cn(
            "p-3 rounded-lg border",
            difficultySuggestion.suggestedDifficulty === 'challenge' 
              ? "bg-purple-500/5 border-purple-500/20" 
              : "bg-green-500/5 border-green-500/20"
          )}>
            <div className="flex items-start gap-2">
              <Zap className={cn(
                "h-4 w-4 shrink-0 mt-0.5",
                difficultySuggestion.suggestedDifficulty === 'challenge'
                  ? "text-purple-600"
                  : "text-green-600"
              )} />
              <div>
                <p className={cn(
                  "text-sm font-medium",
                  difficultySuggestion.suggestedDifficulty === 'challenge'
                    ? "text-purple-900"
                    : "text-green-900"
                )}>
                  Ready for {difficultySuggestion.suggestedDifficulty}!
                </p>
                <p className={cn(
                  "text-xs",
                  difficultySuggestion.suggestedDifficulty === 'challenge'
                    ? "text-purple-700/80"
                    : "text-green-700/80"
                )}>
                  {difficultySuggestion.successRate.toFixed(0)}% success rate on current difficulty
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Streak */}
        {stats.streakDays > 0 && (
          <div className="flex items-center justify-center gap-2 p-2 bg-orange-500/5 rounded-lg">
            <span className="text-2xl">🔥</span>
            <span className="text-sm">
              <span className="font-bold">{stats.streakDays}</span>
              <span className="text-muted-foreground"> day streak</span>
            </span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// Mini stat component for dashboard header
export function LearningStatsMini({ stats, isLoading }: { stats?: LearningStats; isLoading?: boolean }) {
  if (isLoading || !stats) {
    return (
      <div className="flex items-center gap-4 text-sm">
        <div className="animate-pulse h-4 w-20 bg-muted rounded" />
        <div className="animate-pulse h-4 w-20 bg-muted rounded" />
      </div>
    );
  }

  const successRate = stats.problemsAttempted > 0
    ? Math.round((stats.problemsSolved / stats.problemsAttempted) * 100)
    : 0;

  return (
    <div className="flex items-center gap-4 text-sm">
      <div className="flex items-center gap-1.5">
        <Target className="h-4 w-4 text-muted-foreground" />
        <span className="font-medium">{stats.problemsSolved}</span>
        <span className="text-muted-foreground">solved</span>
      </div>
      <div className="flex items-center gap-1.5">
        <Zap className="h-4 w-4 text-muted-foreground" />
        <span className="font-medium">{successRate}%</span>
        <span className="text-muted-foreground">success</span>
      </div>
      {stats.streakDays > 0 && (
        <div className="flex items-center gap-1.5">
          <span>🔥</span>
          <span className="font-medium">{stats.streakDays}</span>
          <span className="text-muted-foreground">streak</span>
        </div>
      )}
    </div>
  );
}
