/**
 * Curriculum types for Python OOP Journey
 * Matches the structure of curriculum.json
 */

export interface Problem {
  slug: string;
  title: string;
  topic: string;
  difficulty: string;
  order: number;
  week_slug: string;
  day_slug: string;
  instructions: string;
  starter_code: string;
  solution_code: string;
  test_code: string;
  hints: string[];
  // CamelCase aliases for component compatibility
  weekSlug?: string;
  daySlug?: string;
  weekNumber?: number;
  dayNumber?: number;
  starterCode?: string;
  solutionCode?: string;
  testCode?: string;
  nextProblemSlug?: string;
}

export interface Day {
  slug: string;
  title: string;
  order: number;
  week_slug: string;
  theory_path: string | null;
  theory_content: string;
  learning_objectives: string[];
  problems: Problem[];
  // CamelCase aliases for component compatibility
  weekSlug?: string;
  theoryPath?: string | null;
  theoryContent?: string;
  learningObjectives?: string[];
}

export interface ProjectFile {
  path: string;
  content?: string;
  template?: string;
  isEntryPoint?: boolean;
  readOnly?: boolean;
}

export interface ProjectTask {
  id: string;
  description: string;
  hint?: string;
  completed?: boolean;
  autoCheck?: boolean;
  testName?: string;
}

export interface Project {
  slug: string;
  title: string;
  description: string;
  starter_path: string | null;
  solution_path: string | null;
  test_path: string | null;
  // Extended fields for project page
  overview?: string;
  entryPoint?: string;
  files?: ProjectFile[];
  tasks?: ProjectTask[];
  requirements?: string[];
  hints?: string[];
  submissionGuidelines?: string;
  // CamelCase aliases for component compatibility
  starterPath?: string | null;
  solutionPath?: string | null;
  testPath?: string | null;
}

export interface Week {
  slug: string;
  title: string;
  order: number;
  objective: string;
  prerequisites: string[];
  days: Day[];
  project: Project | null;
}

export interface Curriculum {
  version: string;
  weeks: Week[];
}

// Legacy types for compatibility
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

export interface Theory {
  title: string;
  content: string;
  code?: string;
}

export interface Progress {
  completedProblems: string[];
  totalProblems: number;
  streakDays: number;
  lastActive: string;
}

export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
}

// Table of Contents item for theory pages
export interface TocItem {
  id: string;
  text: string;
  level: number;
}
