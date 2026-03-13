'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  RotateCcw, 
  Clock, 
  ArrowRight, 
  AlertCircle,
  CheckCircle2,
  Calendar,
  TrendingUp,
  Brain
} from 'lucide-react';
import Link from 'next/link';
import { cn } from '@/lib/utils';
import type { ReviewQueue, ReviewStats } from '@/hooks/use-recommendations';

interface ReviewQueueCardProps {
  reviewQueue?: ReviewQueue;
  stats?: ReviewStats;
  isLoading?: boolean;
}

export function ReviewQueueCard({ reviewQueue, stats, isLoading }: ReviewQueueCardProps) {
  if (isLoading) {
    return (
      <Card className="border-dashed animate-pulse">
        <CardHeader className="pb-3">
          <div className="h-5 w-1/3 bg-muted rounded" />
          <div className="h-4 w-2/3 bg-muted rounded mt-2" />
        </CardHeader>
        <CardContent>
          <div className="h-10 bg-muted rounded" />
        </CardContent>
      </Card>
    );
  }

  const dueCount = reviewQueue?.dueToday || 0;
  const hasDueItems = dueCount > 0;
  const upcomingCount = (reviewQueue?.dueThisWeek || 0) - dueCount;

  return (
    <Card className={cn(
      "overflow-hidden transition-all duration-200",
      hasDueItems ? "border-l-4 border-l-yellow-500" : ""
    )}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-yellow-500/10">
              <Brain className="h-4 w-4 text-yellow-600" />
            </div>
            <div>
              <CardTitle className="text-base">Spaced Repetition</CardTitle>
              <CardDescription className="text-xs">
                Retain what you learn
              </CardDescription>
            </div>
          </div>
          {hasDueItems && (
            <Badge variant="destructive" className="animate-pulse">
              {dueCount} due
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        {hasDueItems ? (
          <div className="space-y-3">
            <div className="flex items-start gap-3 p-3 bg-muted/50 rounded-lg">
              <AlertCircle className="h-5 w-5 text-yellow-600 shrink-0 mt-0.5" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium">{reviewQueue?.items[0]?.problemTitle}</p>
                <p className="text-xs text-muted-foreground mt-0.5">
                  {(reviewQueue?.items[0]?.daysOverdue ?? 0) > 0 
                    ? `${reviewQueue?.items[0]?.daysOverdue} days overdue`
                    : 'Due today'}
                </p>
              </div>
            </div>
            <Link href={`/problems/${reviewQueue?.items[0]?.problemSlug}`}>
              <Button variant="secondary" className="w-full gap-2 group">
                <RotateCcw className="h-4 w-4" />
                Review Now
                <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Button>
            </Link>
            {reviewQueue && reviewQueue.items.length > 1 && (
              <p className="text-xs text-center text-muted-foreground">
                +{reviewQueue.items.length - 1} more items in queue
              </p>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center gap-3 p-3 bg-green-500/5 rounded-lg border border-green-500/20">
              <CheckCircle2 className="h-5 w-5 text-green-600 shrink-0" />
              <div>
                <p className="text-sm font-medium text-green-800">All caught up!</p>
                <p className="text-xs text-green-700/80">
                  No items due for review
                </p>
              </div>
            </div>
            
            {upcomingCount > 0 && (
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <Calendar className="h-4 w-4" />
                <span>{upcomingCount} items coming up this week</span>
              </div>
            )}

            {stats && (
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="p-2 bg-muted rounded">
                  <p className="text-muted-foreground">Total Items</p>
                  <p className="font-semibold">{stats.totalItems}</p>
                </div>
                <div className="p-2 bg-muted rounded">
                  <p className="text-muted-foreground">Avg Ease</p>
                  <p className="font-semibold">{stats.averageEaseFactor.toFixed(2)}</p>
                </div>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export function ReviewQueueMini({ reviewQueue, isLoading }: { reviewQueue?: ReviewQueue; isLoading?: boolean }) {
  if (isLoading) {
    return (
      <div className="animate-pulse flex items-center gap-2">
        <div className="h-4 w-4 bg-muted rounded-full" />
        <div className="h-4 w-24 bg-muted rounded" />
      </div>
    );
  }

  const dueCount = reviewQueue?.dueToday || 0;

  if (dueCount === 0) {
    return (
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <CheckCircle2 className="h-4 w-4 text-green-500" />
        <span>No reviews due</span>
      </div>
    );
  }

  return (
    <Link href="/reviews" className="flex items-center gap-2 text-sm hover:opacity-80 transition-opacity">
      <div className="flex h-5 w-5 items-center justify-center rounded-full bg-yellow-500/10">
        <RotateCcw className="h-3 w-3 text-yellow-600" />
      </div>
      <span className="font-medium text-yellow-700">
        {dueCount} {dueCount === 1 ? 'review' : 'reviews'} due
      </span>
    </Link>
  );
}
