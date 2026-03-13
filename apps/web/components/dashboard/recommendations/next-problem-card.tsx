'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Clock, Play, ArrowRight, Target, Zap, BookOpen } from 'lucide-react';
import Link from 'next/link';
import { cn } from '@/lib/utils';
import type { Recommendation } from '@/hooks/use-recommendations';

interface NextProblemCardProps {
  recommendation?: Recommendation;
  isLoading?: boolean;
}

const difficultyConfig = {
  easy: {
    label: 'Easy',
    color: 'bg-green-500/10 text-green-600 border-green-200',
    icon: BookOpen,
  },
  medium: {
    label: 'Medium',
    color: 'bg-yellow-500/10 text-yellow-600 border-yellow-200',
    icon: Target,
  },
  hard: {
    label: 'Hard',
    color: 'bg-orange-500/10 text-orange-600 border-orange-200',
    icon: Zap,
  },
  challenge: {
    label: 'Challenge',
    color: 'bg-red-500/10 text-red-600 border-red-200',
    icon: Zap,
  },
};

export function NextProblemCard({ recommendation, isLoading }: NextProblemCardProps) {
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

  if (!recommendation) {
    return (
      <Card className="border-dashed">
        <CardContent className="py-8 text-center">
          <Target className="h-10 w-10 mx-auto mb-3 text-muted-foreground opacity-50" />
          <p className="text-sm text-muted-foreground font-medium">No recommendations yet</p>
          <p className="text-xs text-muted-foreground mt-1">
            Start solving problems to get personalized suggestions
          </p>
        </CardContent>
      </Card>
    );
  }

  const difficulty = recommendation.context?.difficulty || 'medium';
  const config = difficultyConfig[difficulty as keyof typeof difficultyConfig] || difficultyConfig.medium;
  const DifficultyIcon = config.icon;

  return (
    <Card className={cn(
      "overflow-hidden transition-all duration-200 hover:shadow-md",
      "border-l-4",
      recommendation.priority >= 9 ? "border-l-red-500" :
      recommendation.priority >= 7 ? "border-l-yellow-500" :
      "border-l-blue-500"
    )}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-2">
              <Badge variant="secondary" className={cn("text-xs", config.color)}>
                <DifficultyIcon className="h-3 w-3 mr-1" />
                {config.label}
              </Badge>
              <span className="text-xs text-muted-foreground flex items-center">
                <Clock className="h-3 w-3 mr-1" />
                ~{recommendation.estimatedTimeMinutes} min
              </span>
            </div>
            <CardTitle className="text-lg truncate">{recommendation.itemTitle}</CardTitle>
            <CardDescription className="mt-1.5 line-clamp-2">
              {recommendation.reason}
            </CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        <Link href={`/problems/${recommendation.itemSlug}`}>
          <Button className="w-full gap-2 group">
            <Play className="h-4 w-4" />
            Start Problem
            <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
          </Button>
        </Link>
      </CardContent>
    </Card>
  );
}
