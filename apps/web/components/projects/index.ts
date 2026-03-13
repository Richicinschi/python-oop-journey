// Project components
export { ProjectCard, ProjectMiniCard } from './project-card';
export { ProjectEmptyState, ActiveProjectsEmptyState, FileTreeEmptyState } from './empty-state';
export { 
  FileTree, 
  FileList, 
  FileTreeSkeleton 
} from './file-tree';
export { 
  FileTreeSkeleton as FileTreeLoading,
  EditorSkeleton,
  ProjectCardSkeleton,
  ActiveProjectsSkeleton,
  ProjectPageSkeleton,
  ExecutionLoadingState,
  DashboardProjectsSkeleton,
  BreadcrumbSkeleton,
} from './skeletons';
export { 
  ProjectErrorBoundary, 
  ProjectErrorFallback,
  FileTreeError,
  EditorError,
  GracefulDegradation,
  useErrorTracker,
} from './error-boundary';
export { ProjectTour, useProjectTour, TourButton } from './project-tour';
export { 
  KeyboardShortcutsDialog, 
  ShortcutDisplay, 
  ShortcutHint,
  ShortcutBadge,
} from './keyboard-shortcuts';
export { ActiveProjectsSection } from './active-projects-section';

// Types
export type {
  ProjectFolder,
  WeeklyProject,
  UserProjectProgress,
  ProjectStatus,
  EditorTab,
  ActiveProject,
} from '@/types/project';
export type { ProjectFile } from '@/types/project-files';
