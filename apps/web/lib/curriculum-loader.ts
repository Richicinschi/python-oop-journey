/**
 * Curriculum data loader for static generation
 * Loads curriculum.json at build time
 */

import { Curriculum, Week, Day, Problem, Project } from '@/types/curriculum';

// Import curriculum.json at build time for static generation
import curriculumData from '@/data/curriculum.json';

let curriculumCache: Curriculum | null = null;

/**
 * Get the full curriculum data
 */
export function getCurriculum(): Curriculum {
  if (!curriculumCache) {
    curriculumCache = curriculumData as Curriculum;
  }
  return curriculumCache;
}

/**
 * Get all weeks
 */
export function getWeeks(): Week[] {
  return getCurriculum().weeks;
}

/**
 * Get a week by its slug
 */
export function getWeekBySlug(slug: string): Week | undefined {
  return getWeeks().find((week) => week.slug === slug);
}

/**
 * Get a day by week slug and day slug
 */
export function getDayBySlug(weekSlug: string, daySlug: string): Day | undefined {
  const week = getWeekBySlug(weekSlug);
  return week?.days.find((day) => day.slug === daySlug);
}

/**
 * Get a problem by week slug, day slug, and problem slug
 */
export function getProblemBySlug(
  weekSlug: string,
  daySlug: string,
  problemSlug: string
): Problem | undefined {
  const day = getDayBySlug(weekSlug, daySlug);
  return day?.problems.find((problem) => problem.slug === problemSlug);
}

/**
 * Get all problems across all weeks
 */
export function getAllProblems(): Problem[] {
  const weeks = getWeeks();
  const problems: Problem[] = [];
  
  for (const week of weeks) {
    for (const day of week.days) {
      problems.push(...day.problems);
    }
  }
  
  return problems;
}

/**
 * Get problems for a specific day
 */
export function getProblemsForDay(weekSlug: string, daySlug: string): Problem[] {
  const day = getDayBySlug(weekSlug, daySlug);
  return day?.problems || [];
}

/**
 * Find a problem by its slug across all weeks
 * Returns problem with both snake_case and camelCase properties
 */
export function findProblemBySlug(problemSlug: string): (Problem & { 
  weekNumber: number; 
  dayNumber: number;
  weekSlug: string;
  daySlug: string;
  starterCode: string;
  solutionCode: string;
  testCode: string;
}) | undefined {
  const weeks = getWeeks();
  
  for (const week of weeks) {
    for (const day of week.days) {
      const problem = day.problems.find((p) => p.slug === problemSlug);
      if (problem) {
        return { 
          ...problem, 
          weekNumber: week.order, 
          dayNumber: day.order,
          weekSlug: week.slug,
          daySlug: day.slug,
          starterCode: problem.starter_code,
          solutionCode: problem.solution_code,
          testCode: problem.test_code,
        };
      }
    }
  }
  
  return undefined;
}

/**
 * Get static params for week pages
 */
export function generateWeekParams(): { weekSlug: string }[] {
  return getWeeks().map((week) => ({
    weekSlug: week.slug,
  }));
}

/**
 * Get static params for day pages
 */
export function generateDayParams(): { weekSlug: string; daySlug: string }[] {
  const params: { weekSlug: string; daySlug: string }[] = [];
  
  for (const week of getWeeks()) {
    for (const day of week.days) {
      params.push({
        weekSlug: week.slug,
        daySlug: day.slug,
      });
    }
  }
  
  return params;
}

/**
 * Get static params for theory pages
 */
export function generateTheoryParams(): { weekSlug: string; daySlug: string }[] {
  return generateDayParams();
}

/**
 * Get difficulty color class
 */
export function getDifficultyColor(difficulty: string): string {
  switch (difficulty.toLowerCase()) {
    case 'easy':
    case 'beginner':
      return 'bg-green-500/10 text-green-600 border-green-500/20';
    case 'medium':
      return 'bg-yellow-500/10 text-yellow-600 border-yellow-500/20';
    case 'hard':
      return 'bg-red-500/10 text-red-600 border-red-500/20';
    default:
      return 'bg-gray-500/10 text-gray-600 border-gray-500/20';
  }
}

/**
 * Format week number for display
 */
export function formatWeekNumber(order: number): string {
  if (order === 0) return 'Week 0';
  return `Week ${order}`;
}

/**
 * Format day number for display
 */
export function formatDayNumber(order: number): string {
  return `Day ${order}`;
}

/**
 * Get total problem count for a week
 */
export function getWeekProblemCount(week: Week): number {
  return week.days.reduce((total, day) => total + day.problems.length, 0);
}

/**
 * Get completion percentage for a week (placeholder)
 */
export function getWeekProgress(week: Week): number {
  // TODO: Connect to user progress store
  return 0;
}

/**
 * Get completion percentage for a day (placeholder)
 */
export function getDayProgress(day: Day): number {
  // TODO: Connect to user progress store
  return 0;
}

// ============================================================================
// Convenience aliases for cleaner API
// ============================================================================

export const loadCurriculum = getCurriculum;
export const getWeek = getWeekBySlug;
export const getDay = getDayBySlug;
export const getProblem = findProblemBySlug;

/**
 * Search problems by query string (matches title or topic)
 */
export function searchProblems(query: string): Problem[] {
  const all = getAllProblems();
  const q = query.toLowerCase();
  return all.filter(p => 
    p.title.toLowerCase().includes(q) || 
    p.topic.toLowerCase().includes(q)
  );
}
