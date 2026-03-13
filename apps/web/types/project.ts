/**
 * Project types for the Python OOP Journey
 */

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

export type ProjectStatus = 'not_started' | 'in_progress' | 'submitted' | 'completed';

export interface Project {
  slug: string;
  title: string;
  description: string;
  overview?: string;
  entryPoint?: string;
  files?: ProjectFile[];
  tasks?: ProjectTask[];
  requirements?: string[];
  hints?: string[];
  submissionGuidelines?: string;
  starter_path?: string | null;
  solution_path?: string | null;
  test_path?: string | null;
}

export interface ProjectSubmission {
  projectSlug: string;
  userId: string;
  code: Record<string, string>;
  completedTasks: string[];
  submittedAt: string;
  status: 'pending' | 'approved' | 'needs_revision';
  feedback?: string;
}

export interface ProjectProgress {
  projectSlug: string;
  status: ProjectStatus;
  completedTasks: string[];
  lastModified: string;
  files: Record<string, string>;
}

// Types for weekly project listings
export interface WeeklyProject {
  slug: string;
  title: string;
  description: string;
  week: number;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimatedHours: number;
  status: ProjectStatus;
  completedTasks: number;
  totalTasks: number;
}

export interface UserProjectProgress {
  projectSlug: string;
  status: ProjectStatus;
  completedTasks: string[];
  lastAccessed: string;
}
