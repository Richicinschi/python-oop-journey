/**
 * Library exports
 * 
 * Core utilities and services for the web application.
 */

// Core utilities
export { cn } from './utils';
export { api, ApiError } from './api';

// Curriculum loading
export {
  loadCurriculum,
  getWeeks,
  getWeek,
  getDay,
  getProblem,
  searchProblems,
} from './curriculum-loader';

// Search
export { buildSearchIndex, searchCurriculum, type SearchResult } from './search';

// Verification
export { verifySolution, submitSolution } from './verification-api';

// Offline & Sync
export {
  // Database operations
  getDB,
  closeDB,
  deleteDatabase,
  // Operations
  addOperation,
  getPendingOperations,
  getOperationsByType,
  getOperation,
  updateOperation,
  removeOperation,
  clearAllOperations,
  getPendingOperationsCount,
  // Drafts
  saveDraft,
  getDraft,
  getAllDrafts,
  deleteDraft,
  // Progress
  saveProgress,
  getProgress,
  getAllProgress,
  updateProblemStatus,
  // Bookmarks
  saveBookmark,
  getBookmark,
  getAllBookmarks,
  deleteBookmark,
  // Curriculum cache
  cacheCurriculum,
  getCachedCurriculum,
  getAllCachedCurriculum,
  clearCurriculumCache,
  // Import/Export
  exportAllData,
  importData,
  // Types
  type SyncOperation,
  type OperationType,
  type OperationAction,
  type LocalDraft,
  type LocalProgress,
  type LocalBookmark,
  type CachedCurriculum,
} from './offline-db';

// Multi-file Project Database (Agent 16)
export {
  // Database
  getProjectDB,
  closeProjectDB,
  deleteProjectDatabase,
  // Projects
  saveProject,
  getProject,
  getAllProjects,
  deleteProject,
  projectExists,
  // Files
  saveFile,
  saveFiles,
  getFile,
  getFiles,
  deleteFile,
  deleteFiles,
  // Import/Export
  exportProject,
  importProject,
  // Utility
  getProjectDBStats,
  clearAllProjects,
} from './project-db';

// Sync Engine
export {
  initSyncEngine,
  cleanupSyncEngine,
  queueOperation,
  syncPendingOperations,
  resolveConflict,
  getSyncState,
  subscribeToSyncEvents,
  syncProgress,
  syncDraft,
  syncBookmark,
  CLIENT_ID,
  type SyncStatus,
  type SyncState,
  type ConflictResolution,
  type BatchSyncResponse,
  type SyncOptions,
  type ConflictInfo,
} from './sync-engine';

// Optimistic Updates
export {
  optimisticProgressUpdate,
  optimisticDraftSave,
  optimisticBookmarkToggle,
  useOptimistic,
  type OptimisticStatus,
  type OptimisticState,
} from './optimistic-updates';

// Data Migration
export {
  hasLegacyData,
  scanLegacyData,
  migrateLegacyData,
  clearLegacyData,
  estimateMigrationSize,
  useDataMigration,
  type LegacyProgressData,
  type MigrationProgress,
  type MigrationResult,
  type MigrationOptions,
} from './migrate-local-data';
