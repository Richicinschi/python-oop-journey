'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface StatCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon: LucideIcon;
  trend?: {
    value: number;
    label: string;
    positive?: boolean;
  };
  className?: string;
  index?: number;
  variant?: 'default' | 'highlight' | 'success' | 'warning';
}

const variantStyles = {
  default: {
    card: '',
    iconBg: 'bg-muted',
    iconColor: 'text-muted-foreground',
  },
  highlight: {
    card: 'border-primary/50 bg-primary/5',
    iconBg: 'bg-primary/10',
    iconColor: 'text-primary',
  },
  success: {
    card: 'border-green-500/20 bg-green-500/5',
    iconBg: 'bg-green-500/10',
    iconColor: 'text-green-500',
  },
  warning: {
    card: 'border-yellow-500/20 bg-yellow-500/5',
    iconBg: 'bg-yellow-500/10',
    iconColor: 'text-yellow-500',
  },
};

export function StatCard({
  title,
  value,
  description,
  icon: Icon,
  trend,
  className,
  index = 0,
  variant = 'default',
}: StatCardProps) {
  const styles = variantStyles[variant];

  return (
    <div 
      className={cn("animate-scale-in", className)}
      style={{ animationDelay: `${index * 100}ms` }}
    >
      <Card className={styles.card}>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            {title}
          </CardTitle>
          <div className={cn('flex h-8 w-8 items-center justify-center rounded-md', styles.iconBg)}>
            <Icon className={cn('h-4 w-4', styles.iconColor)} />
          </div>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{value}</div>
          {description && (
            <p className="text-xs text-muted-foreground mt-1">{description}</p>
          )}
          {trend && (
            <div className="flex items-center gap-1 mt-2">
              <span
                className={cn(
                  'text-xs font-medium',
                  trend.positive ? 'text-green-500' : 'text-red-500'
                )}
              >
                {trend.positive ? '+' : ''}{trend.value}%
              </span>
              <span className="text-xs text-muted-foreground">{trend.label}</span>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
