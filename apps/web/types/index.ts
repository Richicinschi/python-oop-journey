/**
 * Global Types
 * 
 * Shared type definitions used across the application.
 */

// Multi-file project types
export type {
  ProjectFile,
  ProjectFolder,
  ProjectItem,
  OpenTab,
  ProjectState,
  FileOperationResult,
} from './project-files';

export {
  isProjectFile,
  isProjectFolder,
  LANGUAGE_MAP,
  getLanguageFromExtension,
  getFileIconType,
  DEFAULT_STARTER_CODE,
  getStarterCode,
} from './project-files';
