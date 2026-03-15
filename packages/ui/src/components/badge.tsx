/**
 * Badge Component
 * Status badges for difficulty, completion, and other states
 */

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '../lib/utils';

const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default:
          'border-transparent bg-primary text-primary-foreground hover:bg-primary/80',
        secondary:
          'border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80',
        muted:
          'border-transparent bg-muted text-muted-foreground hover:bg-muted/80',
        outline:
          'text-foreground',
        // Difficulty variants
        beginner:
          'border-transparent bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300',
        easy:
          'border-transparent bg-teal-100 text-teal-800 dark:bg-teal-900/30 dark:text-teal-300',
        medium:
          'border-transparent bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300',
        hard:
          'border-transparent bg-rose-100 text-rose-800 dark:bg-rose-900/30 dark:text-rose-300',
        challenge:
          'border-transparent bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300',
        // Status variants
        completed:
          'border-transparent bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300',
        in_progress:
          'border-transparent bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300',
        not_started:
          'border-transparent bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400',
        locked:
          'border-transparent bg-slate-100 text-slate-400 dark:bg-slate-800 dark:text-slate-500',
        destructive:
          'border-transparent bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}

export { Badge, badgeVariants };
