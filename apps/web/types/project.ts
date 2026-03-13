/**
 * Project types for the Python OOP Journey
 */

import { ProjectFile } from './project-files';

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
  // Optional fields for detailed project view
  starterFiles?: ProjectFile[];
  files?: ProjectFile[];
  requirements?: string[];
  hints?: string[];
}

export interface UserProjectProgress {
  projectSlug: string;
  status: ProjectStatus;
  completedTasks: string[];
  lastAccessed: string;
}

export interface ActiveProject {
  project: WeeklyProject;
  progress: UserProjectProgress;
  completionPercentage: number;
}

// Editor tab type for multi-file editor
export interface EditorTab {
  id: string;
  fileId: string;
  fileName: string;
  filePath: string;
  isModified: boolean;
  isActive: boolean;
}

// Analytics event type
export interface AnalyticsEvent {
  id: string;
  type: 'file_open' | 'file_edit' | 'file_save' | 'task_complete' | 'project_submit' | 'test_run' | 'tests_run' | 'run_executed' | 'error';
  timestamp: number;
  metadata?: Record<string, unknown>;
}

// Tour step type for project tour
export interface TourStep {
  id: string;
  title: string;
  content: string;
  targetSelector: string;
  position: 'top' | 'bottom' | 'left' | 'right';
  actionRequired?: string;
}
