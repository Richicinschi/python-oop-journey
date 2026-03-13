'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  AlertTriangle, 
  ArrowRight, 
  BookOpen, 
  Target,
  TrendingDown,
  Lightbulb,
  ChevronRight
} from 'lucide-react';
import Link from 'next/link';
import { cn } from '@/lib/utils';
import type { WeakArea } from '@/hooks/use-recommendations';

interface WeakAreasCardProps {
  weakAreas?: WeakArea[];
  isLoading?: boolean;
}

const masteryColors = {
  novice: 'text-red-600 bg-red-500/10 border-red-200',
  beginner: 'text-orange-600 bg-orange-500/10 border-orange-200',
  developing: 'text-yellow-600 bg-yellow-500/10 border-yellow-200',
  proficient: 'text-blue-600 bg-blue-500/10 border-blue-200',
  mastered: 'text-green-600 bg-green-500/10 border-green-200',
};

export function WeakAreasCard({ weakAreas, isLoading }: WeakAreasCardProps) {
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

  const hasWeakAreas = weakAreas && weakAreas.length > 0;

  if (!hasWeakAreas) {
    return (
      <Card className="border-dashed">
        <CardContent className="py-8 text-center">
          <Target className="h-10 w-10 mx-auto mb-3 text-muted-foreground opacity-50" />
          <p className="text-sm text-muted-foreground font-medium">No weak areas identified</p>
          <p className="text-xs text-muted-foreground mt-1">
            Keep up the good work! You're doing well across all topics.
          </p>
        </CardContent>
      </Card>
    );
  }

  const topWeakArea = weakAreas[0];
  const otherAreas = weakAreas.slice(1, 3);

  return (
    <Card className="border-l-4 border-l-orange-500">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-orange-500/10">
              <TrendingDown className="h-4 w-4 text-orange-600" />
            </div>
            <div>
              <CardTitle className="text-base">Focus Areas</CardTitle>
              <CardDescription className="text-xs">
                Topics to strengthen
              </CardDescription>
            </div>
          </div>
          {weakAreas.length > 1 && (
            <Badge variant="outline" className="text-xs">
              {weakAreas.length} areas
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="pt-0 space-y-4">
        {/* Top weak area */}
        <div className="p-3 bg-muted/50 rounded-lg">
          <div className="flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-orange-600 shrink-0 mt-0.5" />
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-2">
                <p className="font-medium truncate">{topWeakArea.topicName}</p>
                <Badge 
                  variant="secondary" 
                  className={cn("text-xs", masteryColors[topWeakArea.level as keyof typeof masteryColors])}
                >
                  {topWeakArea.level}
                </Badge>
              </div>
              <div className="mt-2">
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="text-muted-foreground">Mastery</span>
                  <span className="font-medium">{Math.round(topWeakArea.masteryScore)}%</span>
                </div>
                <Progress value={topWeakArea.masteryScore} className="h-2" />
              </div>
              {topWeakArea.problemsStruggled.length > 0 && (
                <p className="text-xs text-muted-foreground mt-2">
                  {topWeakArea.problemsStruggled.length} problem{topWeakArea.problemsStruggled.length !== 1 ? 's' : ''} to review
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Remediation suggestion */}
        {topWeakArea.suggestedRemediation && (
          <div className="flex items-start gap-2 p-3 bg-blue-500/5 rounded-lg border border-blue-500/20">
            <Lightbulb className="h-4 w-4 text-blue-600 shrink-0 mt-0.5" />
            <p className="text-sm text-blue-900">{topWeakArea.suggestedRemediation}</p>
          </div>
        )}

        {/* Other weak areas */}
        {otherAreas.length > 0 && (
          <div className="space-y-2">
            <p className="text-xs font-medium text-muted-foreground">Other areas:</p>
            {otherAreas.map((area) => (
              <div 
                key={area.topicSlug}
                className="flex items-center justify-between p-2 bg-muted rounded text-sm"
              >
                <span className="truncate">{area.topicName}</span>
                <Badge 
                  variant="secondary" 
                  className={cn("text-xs shrink-0", masteryColors[area.level as keyof typeof masteryColors])}
                >
                  {Math.round(area.masteryScore)}%
                </Badge>
              </div>
            ))}
          </div>
        )}

        <Link href={`/weeks/${topWeakArea.topicSlug}`}>
          <Button variant="secondary" className="w-full gap-2 group">
            <BookOpen className="h-4 w-4" />
            Review Topic
            <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
          </Button>
        </Link>
      </CardContent>
    </Card>
  );
}

export function WeakAreaBadge({ weakAreas, isLoading }: { weakAreas?: WeakArea[]; isLoading?: boolean }) {
  if (isLoading || !weakAreas || weakAreas.length === 0) {
    return null;
  }

  const count = weakAreas.length;

  return (
    <Link 
      href="/focus-areas" 
      className="flex items-center gap-2 text-sm hover:opacity-80 transition-opacity"
    >
      <div className="flex h-5 w-5 items-center justify-center rounded-full bg-orange-500/10">
        <TrendingDown className="h-3 w-3 text-orange-600" />
      </div>
      <span className="font-medium text-orange-700">
        {count} focus {count === 1 ? 'area' : 'areas'}
      </span>
      <ChevronRight className="h-4 w-4 text-muted-foreground" />
    </Link>
  );
}
