/**
 * Curriculum types for Python OOP Journey
 * Matches the structure of curriculum.json
 */

import { ProjectFile } from './project-files';

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

// ============================================================================
// TRANSFORMED TYPES (camelCase for components)
// ============================================================================

/** Transformed Project File ready for component consumption */
export interface TransformedProjectFile {
  id: string;
  name: string;
  path: string;
  content: string;
  language: string;
  isModified: boolean;
  lastModified: number;
  isEntryPoint?: boolean;
  template?: string;
}

/** Transformed Problem ready for component consumption */
export interface TransformedProblem {
  slug: string;
  title: string;
  topic: string;
  difficulty: string;
  order: number;
  instructions: string;
  hints: string[];
  weekSlug: string;
  daySlug: string;
  weekNumber: number;
  dayNumber: number;
  starterCode: string;
  solutionCode: string;
  testCode: string;
  nextProblemSlug: string | null;
  prevProblemSlug: string | null;
}

/** Transformed Day ready for component consumption */
export interface TransformedDay {
  slug: string;
  title: string;
  order: number;
  problems: TransformedProblem[];
  weekSlug: string;
  theoryPath: string | null;
  theoryContent: string;
  learningObjectives: string[];
}

/** Transformed Project ready for component consumption */
export interface TransformedProject {
  slug: string;
  title: string;
  description: string;
  overview: string;
  entryPoint: string;
  starterPath: string | null;
  solutionPath: string | null;
  testPath: string | null;
  requirements: string[];
  hints: string[];
  files: TransformedProjectFile[];
  tasks: ProjectTask[];
}

/** Transformed Week ready for component consumption */
export interface TransformedWeek {
  slug: string;
  title: string;
  order: number;
  objective: string;
  prerequisites: string[];
  days: TransformedDay[];
  project: TransformedProject | null;
}

/** Transformed Curriculum */
export interface TransformedCurriculum {
  version: string;
  weeks: TransformedWeek[];
}
