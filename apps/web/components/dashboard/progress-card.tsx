'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { WeekProgress } from '@/types/dashboard';
import { CheckCircle2, Circle, Play } from 'lucide-react';
import Link from 'next/link';
import { cn } from '@/lib/utils';

interface ProgressCardProps {
  week: WeekProgress;
  index?: number;
}

export function ProgressCard({ week, index = 0 }: ProgressCardProps) {
  const progress = Math.round((week.completedProblems / week.totalProblems) * 100);
  
  const statusConfig = {
    completed: {
      icon: CheckCircle2,
      color: 'text-green-500',
      bgColor: 'bg-green-500/10',
      borderColor: 'border-green-500/20',
      label: 'Completed',
    },
    inProgress: {
      icon: Play,
      color: 'text-blue-500',
      bgColor: 'bg-blue-500/10',
      borderColor: 'border-blue-500/20',
      label: 'In Progress',
    },
    notStarted: {
      icon: Circle,
      color: 'text-muted-foreground',
      bgColor: 'bg-muted',
      borderColor: 'border-transparent',
      label: 'Not Started',
    },
  };

  const status = week.isCompleted 
    ? 'completed' 
    : week.isStarted 
    ? 'inProgress' 
    : 'notStarted';
  
  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <div 
      className="animate-fade-in"
      style={{ animationDelay: `${index * 50}ms` }}
    >
      <Link href={`/weeks/${week.weekSlug}`}>
        <Card className={cn(
          'group cursor-pointer transition-all duration-200 hover:shadow-md hover:border-primary/50',
          config.borderColor
        )}>
          <CardHeader className="pb-3">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className={cn(
                  'flex h-10 w-10 items-center justify-center rounded-full shrink-0',
                  config.bgColor
                )}>
                  <span className={cn('text-sm font-bold', config.color)}>
                    {week.weekNumber}
                  </span>
                </div>
                <div>
                  <CardTitle className="text-base group-hover:text-primary transition-colors">
                    {week.weekTitle}
                  </CardTitle>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    {week.completedProblems} / {week.totalProblems} problems
                  </p>
                </div>
              </div>
              <Icon className={cn('h-5 w-5 shrink-0', config.color)} />
            </div>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className={cn('font-medium', config.color)}>
                  {config.label}
                </span>
                <span className="text-muted-foreground">{progress}%</span>
              </div>
              <Progress value={progress} className="h-2" />
            </div>
          </CardContent>
        </Card>
      </Link>
    </div>
  );
}
