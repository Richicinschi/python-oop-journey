/**
 * Utility functions for UI components
 */

import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Merge Tailwind classes with proper precedence
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/**
 * Format a duration in minutes to a readable string
 */
export function formatDuration(minutes: number): string {
  if (minutes < 60) {
    return `${minutes} min`;
  }
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  if (remainingMinutes === 0) {
    return `${hours} hr`;
  }
  return `${hours} hr ${remainingMinutes} min`;
}

/**
 * Get difficulty color classes
 */
export function getDifficultyColor(difficulty: string): string {
  const colors: Record<string, string> = {
    beginner: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300',
    easy: 'bg-teal-100 text-teal-800 dark:bg-teal-900/30 dark:text-teal-300',
    medium: 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300',
    hard: 'bg-rose-100 text-rose-800 dark:bg-rose-900/30 dark:text-rose-300',
    challenge: 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300',
  };
  return colors[difficulty.toLowerCase()] || colors.easy;
}

/**
 * Get status color classes
 */
export function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    not_started: 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400',
    in_progress: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300',
    completed: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300',
    locked: 'bg-slate-100 text-slate-400 dark:bg-slate-800 dark:text-slate-500',
  };
  return colors[status] || colors.not_started;
}
