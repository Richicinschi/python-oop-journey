// Legacy curriculum data file
// Re-exports from curriculum-loader for backwards compatibility
// New code should import directly from '@/lib/curriculum-loader'

export {
  getCurriculum,
  getWeeks,
  getWeekBySlug,
  getDayBySlug,
  getProblemBySlug,
  getAllProblems,
  getProblemsForDay,
  generateWeekParams,
  generateDayParams,
  generateTheoryParams,
  getDifficultyColor,
  formatWeekNumber,
  formatDayNumber,
  getWeekProblemCount,
  getWeekProgress,
  getDayProgress,
} from './curriculum-loader';

// Legacy type definitions for backwards compatibility
import { Week, Day, Problem } from '@/types/curriculum';

// Legacy mock data - kept for backwards compatibility
// Use the loader functions above for real data
export function getLegacyWeeks(): LegacyWeek[] {
  return [
    {
      slug: 'week-01-foundations',
      number: 1,
      title: 'Foundations',
      description: 'Python basics and introduction to OOP concepts',
      days: [
        { slug: 'day-01-intro', number: 1, title: 'Introduction' },
        { slug: 'day-02-variables', number: 2, title: 'Variables & Types' },
        { slug: 'day-03-functions', number: 3, title: 'Functions' },
        { slug: 'day-04-control-flow', number: 4, title: 'Control Flow' },
        { slug: 'day-05-data-structures', number: 5, title: 'Data Structures' },
      ],
    },
    {
      slug: 'week-02-classes-objects',
      number: 2,
      title: 'Classes & Objects',
      description: 'Understanding classes, objects, and methods',
      days: [
        { slug: 'day-01-what-is-oop', number: 1, title: 'What is OOP?' },
        { slug: 'day-02-creating-classes', number: 2, title: 'Creating Classes' },
        { slug: 'day-03-constructors', number: 3, title: 'Constructors' },
        { slug: 'day-04-instance-methods', number: 4, title: 'Instance Methods' },
        { slug: 'day-05-class-attributes', number: 5, title: 'Class Attributes' },
      ],
    },
  ];
}

export function getLegacyProblems(): LegacyProblem[] {
  return [
    {
      slug: 'problem-01-calculate-sum',
      title: 'Calculate Sum',
      description: 'Write a function to calculate the sum of two numbers',
      difficulty: 'easy',
      weekNumber: 1,
      dayNumber: 1,
    },
  ];
}

// Legacy types
export interface LegacyDay {
  slug: string;
  number: number;
  title: string;
}

export interface LegacyWeek {
  slug: string;
  number: number;
  title: string;
  description: string;
  days: LegacyDay[];
}

export interface LegacyProblem {
  slug: string;
  title: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard';
  weekNumber: number;
  dayNumber: number;
}
