'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Recommendation } from '@/types/dashboard';
import { 
  Play, 
  RotateCcw, 
  Target, 
  Rocket, 
  ArrowRight,
  Sparkles,
  BookOpen
} from 'lucide-react';
import Link from 'next/link';
import { cn } from '@/lib/utils';

interface RecommendationCardProps {
  recommendation: Recommendation;
  index?: number;
}

const typeConfig = {
  continue: {
    icon: Play,
    color: 'text-blue-500',
    bgColor: 'bg-blue-500/10',
    borderColor: 'border-blue-500/20',
  },
  review: {
    icon: RotateCcw,
    color: 'text-yellow-500',
    bgColor: 'bg-yellow-500/10',
    borderColor: 'border-yellow-500/20',
  },
  practice: {
    icon: Target,
    color: 'text-purple-500',
    bgColor: 'bg-purple-500/10',
    borderColor: 'border-purple-500/20',
  },
  project: {
    icon: Rocket,
    color: 'text-green-500',
    bgColor: 'bg-green-500/10',
    borderColor: 'border-green-500/20',
  },
  start: {
    icon: Sparkles,
    color: 'text-pink-500',
    bgColor: 'bg-pink-500/10',
    borderColor: 'border-pink-500/20',
  },
};

const priorityConfig = {
  high: 'border-l-4 border-l-red-500',
  medium: 'border-l-4 border-l-yellow-500',
  low: 'border-l-4 border-l-blue-500',
};

export function RecommendationCard({ recommendation, index = 0 }: RecommendationCardProps) {
  const config = typeConfig[recommendation.type];
  const Icon = config.icon;

  const getHref = () => {
    if (recommendation.problemSlug) {
      return `/problems/${recommendation.problemSlug}`;
    }
    if (recommendation.weekNumber) {
      const weekSlug = recommendation.weekNumber.toString().padStart(2, '0');
      return `/weeks/week-${weekSlug}-foundations`;
    }
    return '/weeks';
  };

  return (
    <div
      className="animate-slide-in-right"
      style={{ animationDelay: `${index * 100}ms` }}
    >
      <Card className={cn(
        'overflow-hidden transition-all duration-200 hover:shadow-md',
        priorityConfig[recommendation.priority],
        config.borderColor
      )}>
        <CardHeader className="pb-3">
          <div className="flex items-start gap-3">
            <div className={cn('flex h-10 w-10 items-center justify-center rounded-full shrink-0', config.bgColor)}>
              <Icon className={cn('h-5 w-5', config.color)} />
            </div>
            <div className="flex-1">
              <CardTitle className="text-base">{recommendation.title}</CardTitle>
              <CardDescription className="mt-1">
                {recommendation.description}
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="pt-0">
          <Link href={getHref()}>
            <Button className="w-full gap-2 group">
              {recommendation.actionLabel}
              <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
            </Button>
          </Link>
        </CardContent>
      </Card>
    </div>
  );
}

export function RecommendationList({ recommendations }: { recommendations: Recommendation[] }) {
  if (recommendations.length === 0) {
    return (
      <Card className="border-dashed">
        <CardContent className="py-8 text-center">
          <BookOpen className="h-8 w-8 mx-auto mb-2 text-muted-foreground opacity-50" />
          <p className="text-sm text-muted-foreground">No recommendations yet</p>
          <p className="text-xs text-muted-foreground">Keep learning to get personalized suggestions</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-3">
      {recommendations.map((rec, index) => (
        <RecommendationCard key={rec.type} recommendation={rec} index={index} />
      ))}
    </div>
  );
}
