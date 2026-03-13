'use client';

import { ActivityItem as ActivityItemType } from '@/types/dashboard';
import { CheckCircle2, XCircle, Clock, ArrowRight } from 'lucide-react';
import { cn } from '@/lib/utils';
import Link from 'next/link';

interface ActivityItemProps {
  activity: ActivityItemType;
  index?: number;
}

const statusConfig = {
  completed: {
    icon: CheckCircle2,
    color: 'text-green-500',
    bgColor: 'bg-green-500/10',
    label: 'Completed',
  },
  attempted: {
    icon: Clock,
    color: 'text-yellow-500',
    bgColor: 'bg-yellow-500/10',
    label: 'In Progress',
  },
  failed: {
    icon: XCircle,
    color: 'text-red-500',
    bgColor: 'bg-red-500/10',
    label: 'Failed',
  },
};

function formatDuration(seconds?: number): string {
  if (!seconds) return '';
  if (seconds < 60) return `${seconds}s`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m`;
  return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`;
}

function formatDistanceToNow(timestamp: string): string {
  const date = new Date(timestamp);
  const now = new Date();
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);
  
  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}

export function ActivityItemRow({ activity, index = 0 }: ActivityItemProps) {
  const config = statusConfig[activity.status];
  const Icon = config.icon;

  return (
    <div
      className="animate-slide-in"
      style={{ animationDelay: `${index * 50}ms` }}
    >
      <Link 
        href={`/problems/${activity.problemSlug}`}
        className="flex items-center gap-3 p-3 rounded-lg hover:bg-accent transition-colors group"
      >
        <div className={cn('flex h-9 w-9 items-center justify-center rounded-full shrink-0', config.bgColor)}>
          <Icon className={cn('h-4 w-4', config.color)} />
        </div>
        
        <div className="flex-1 min-w-0">
          <p className="font-medium text-sm truncate group-hover:text-primary transition-colors">
            {activity.problemTitle}
          </p>
          <p className="text-xs text-muted-foreground">
            Week {activity.weekNumber} • Day {activity.dayNumber}
          </p>
        </div>

        <div className="text-right shrink-0">
          <p className="text-xs font-medium text-muted-foreground">
            {formatDistanceToNow(activity.timestamp)}
          </p>
          {activity.timeSpent && (
            <p className="text-xs text-muted-foreground">
              {formatDuration(activity.timeSpent)}
            </p>
          )}
        </div>

        <ArrowRight className="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
      </Link>
    </div>
  );
}

export function ActivityList({ activities }: { activities: ActivityItemType[] }) {
  if (activities.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        <Clock className="h-8 w-8 mx-auto mb-2 opacity-50" />
        <p className="text-sm">No activity yet</p>
        <p className="text-xs">Start solving problems to see your activity here</p>
      </div>
    );
  }

  return (
    <div className="space-y-1">
      {activities.slice(0, 5).map((activity, index) => (
        <ActivityItemRow key={activity.id} activity={activity} index={index} />
      ))}
    </div>
  );
}
