'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  ArrowRight, 
  CheckCircle2, 
  RotateCcw, 
  Sparkles,
  Target,
  TrendingDown,
  Lightbulb,
  ChevronRight,
  Clock
} from 'lucide-react';
import Link from 'next/link';
import { cn } from '@/lib/utils';
import { 
  useNextRecommendation, 
  useReviewQueue, 
  useWeakAreas,
  useRecordReview,
} from '@/hooks/use-recommendations';
import { useToast } from '@/components/ui/use-toast';

interface PostSolveRecommendationsProps {
  problemSlug: string;
  attempts: number;
  timeSpent: number;
  onClose?: () => void;
}

export function PostSolveRecommendations({ 
  problemSlug, 
  attempts, 
  timeSpent,
  onClose 
}: PostSolveRecommendationsProps) {
  const { toast } = useToast();
  const { data: nextRec } = useNextRecommendation();
  const { data: reviewQueue } = useReviewQueue(3);
  const { data: weakAreas } = useWeakAreas(2);
  const recordReview = useRecordReview();
  
  const [showReviewPrompt, setShowReviewPrompt] = useState(false);

  // Determine what to show based on solve context
  const isFirstTry = attempts === 1;
  const tookManyAttempts = attempts > 5;
  const hasReviewDue = reviewQueue && reviewQueue.dueToday > 0;
  const hasWeakAreas = weakAreas && weakAreas.length > 0;

  const handleRecordReview = async (quality: number) => {
    try {
      await recordReview.mutateAsync({ problemSlug, quality });
      toast({
        title: 'Review recorded',
        description: 'Your spaced repetition schedule has been updated.',
      });
      setShowReviewPrompt(false);
    } catch {
      toast({
        title: 'Failed to record review',
        description: 'Please try again later.',
        variant: 'error',
      });
    }
  };

  // Show quality rating after a successful solve
  useEffect(() => {
    const timer = setTimeout(() => {
      setShowReviewPrompt(true);
    }, 500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="space-y-4">
      {/* Success celebration */}
      <div className="flex items-center gap-3 p-4 bg-green-500/10 rounded-lg border border-green-500/20">
        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-green-500/20">
          <CheckCircle2 className="h-5 w-5 text-green-600" />
        </div>
        <div>
          <p className="font-medium text-green-900">Problem Solved!</p>
          <p className="text-sm text-green-700/80">
            {isFirstTry 
              ? 'Perfect solve on the first try! 🎉' 
              : `Solved in ${attempts} attempts. Keep practicing!`}
          </p>
        </div>
      </div>

      {/* Spaced repetition quality rating */}
      {showReviewPrompt && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm flex items-center gap-2">
              <Clock className="h-4 w-4" />
              How difficult was this problem?
            </CardTitle>
            <CardDescription className="text-xs">
              This helps schedule your next review
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex gap-2">
              {[1, 2, 3, 4, 5].map((quality) => (
                <Button
                  key={quality}
                  variant="outline"
                  size="sm"
                  className={cn(
                    "flex-1 text-xs",
                    quality <= 2 ? "hover:bg-red-500/10 hover:text-red-600" :
                    quality === 3 ? "hover:bg-yellow-500/10 hover:text-yellow-600" :
                    "hover:bg-green-500/10 hover:text-green-600"
                  )}
                  onClick={() => handleRecordReview(quality)}
                  disabled={recordReview.isPending}
                >
                  {quality === 1 ? 'Again' :
                   quality === 2 ? 'Hard' :
                   quality === 3 ? 'Good' :
                   quality === 4 ? 'Easy' :
                   'Perfect'}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Next recommended problem */}
      {nextRec && (
        <Card className="border-l-4 border-l-blue-500">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-blue-600" />
              <CardTitle className="text-sm">Next Recommended Problem</CardTitle>
            </div>
            <CardDescription className="text-xs">
              {nextRec.reason}
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">{nextRec.itemTitle}</p>
                <div className="flex items-center gap-2 text-xs text-muted-foreground mt-1">
                  <Badge variant="secondary" className="text-xs">
                    {nextRec.context?.difficulty || 'medium'}
                  </Badge>
                  <span>~{nextRec.estimatedTimeMinutes} min</span>
                </div>
              </div>
              <Link href={`/problems/${nextRec.itemSlug}`}>
                <Button size="sm" className="gap-1">
                  Continue
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      )}

      {/* If struggled, suggest review */}
      {tookManyAttempts && (
        <Card className="border-l-4 border-l-orange-500">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <TrendingDown className="h-4 w-4 text-orange-600" />
              <CardTitle className="text-sm">This one was challenging</CardTitle>
            </div>
            <CardDescription className="text-xs">
              Consider reviewing the concepts before moving on
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-0 space-y-2">
            <Link href={`/theory?ref=${problemSlug}`}>
              <Button variant="outline" size="sm" className="w-full justify-start gap-2">
                <Lightbulb className="h-4 w-4" />
                Review related theory
                <ChevronRight className="h-4 w-4 ml-auto" />
              </Button>
            </Link>
            <Button 
              variant="ghost" 
              size="sm" 
              className="w-full justify-start gap-2"
              onClick={() => window.location.reload()}
            >
              <RotateCcw className="h-4 w-4" />
              Practice this problem again
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Review queue notification */}
      {hasReviewDue && (
        <Card className="border-l-4 border-l-yellow-500">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <RotateCcw className="h-4 w-4 text-yellow-600" />
              <CardTitle className="text-sm">Reviews Due</CardTitle>
            </div>
            <CardDescription className="text-xs">
              {reviewQueue.dueToday} {reviewQueue.dueToday === 1 ? 'problem' : 'problems'} waiting for review
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-0">
            <Link href="/reviews">
              <Button variant="secondary" size="sm" className="w-full gap-2">
                View Review Queue
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </CardContent>
        </Card>
      )}

      {/* Weak areas suggestion */}
      {hasWeakAreas && (
        <Card className="border-l-4 border-l-purple-500">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <Target className="h-4 w-4 text-purple-600" />
              <CardTitle className="text-sm">Focus Area</CardTitle>
            </div>
            <CardDescription className="text-xs">
              {weakAreas[0].topicName} needs attention
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-0">
            <Link href={`/weeks/${weakAreas[0].topicSlug}`}>
              <Button variant="outline" size="sm" className="w-full gap-2">
                Review Topic
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </CardContent>
        </Card>
      )}

      {/* Close button */}
      {onClose && (
        <Button variant="ghost" className="w-full" onClick={onClose}>
          Close
        </Button>
      )}
    </div>
  );
}

// Compact version for inline use
export function PostSolveCompact({ 
  problemSlug, 
  onNext 
}: { 
  problemSlug: string; 
  onNext?: () => void;
}) {
  const { data: nextRec } = useNextRecommendation();
  
  if (!nextRec) return null;

  return (
    <div className="flex items-center gap-4 p-3 bg-muted rounded-lg">
      <div className="flex-1 min-w-0">
        <p className="text-xs text-muted-foreground">Next up:</p>
        <p className="font-medium truncate">{nextRec.itemTitle}</p>
      </div>
      <Link href={`/problems/${nextRec.itemSlug}`}>
        <Button size="sm" onClick={onNext}>
          Continue
          <ArrowRight className="h-4 w-4 ml-1" />
        </Button>
      </Link>
    </div>
  );
}
