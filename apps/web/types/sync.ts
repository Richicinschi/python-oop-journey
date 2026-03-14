/**
 * Sync Types
 * 
 * TypeScript type definitions for sync/offline functionality
 */

// Sync operation types
export type OperationType = 'progress' | 'draft' | 'bookmark';
export type OperationAction = 'create' | 'update' | 'delete';

// Sync operation
export interface SyncOperation {
  id: string;
  type: OperationType;
  action: OperationAction;
  data: unknown;
  timestamp: number;
  clientId: string;
  retryCount: number;
  lastError?: string;
}

// Local data types
export interface LocalDraft {
  problemSlug: string;
  code: string;
  savedAt: number;
  syncedAt?: number;
}

export interface LocalProgress {
  problemSlug: string;
  status: 'not_started' | 'in_progress' | 'completed';
  attempts: number;
  completedAt?: number;
  updatedAt: number;
}

export interface LocalBookmark {
  problemSlug: string;
  note?: string;
  createdAt: number;
}

export interface CachedCurriculum {
  version: string;
  data: unknown;
  cachedAt: number;
}

// Sync state
export type SyncStatus = 'idle' | 'syncing' | 'error' | 'offline' | 'conflict';

export interface SyncState {
  status: SyncStatus;
  pendingCount: number;
  lastSyncAt: number | null;
  lastError: string | null;
}

// Conflict resolution
export interface ConflictInfo {
  operationId: string;
  type: OperationType;
  localData: unknown;
  serverData: unknown;
  localTimestamp: number;
  serverTimestamp: string;
}

export interface ConflictResolution {
  operationId: string;
  strategy: 'local' | 'server' | 'merge';
  mergedData?: unknown;
}

// Batch sync
export interface BatchSyncRequest {
  operations: Array<{
    id: string;
    type: OperationType;
    action: OperationAction;
    data: unknown;
    timestamp: string;
    clientId: string;
  }>;
}

export interface BatchSyncResponse {
  applied: string[];
  conflicts: Array<{
    operationId: string;
    localData: unknown;
    serverData: unknown;
  }>;
  serverTimestamp: string;
}

// Migration
export interface LegacyProgressData {
  completedProblems: string[];
  totalProblems: number;
  streakDays: number;
  lastActive: string | null;
}

export interface MigrationProgress {
  total: number;
  processed: number;
  currentItem: string | null;
  errors: string[];
}

export interface MigrationResult {
  success: boolean;
  migrated: number;
  skipped: number;
  errors: string[];
  conflicts: Array<{
    problemSlug: string;
    localStatus: string;
    serverStatus: string;
  }>;
}

// Online status
export type ConnectionStatus = 'online' | 'offline' | 'unknown';

export interface OnlineStatusState {
  isOnline: boolean;
  status: ConnectionStatus;
  wasOffline: boolean;
  lastChangedAt: Date | null;
}

// Optimistic updates
export type OptimisticStatus = 'idle' | 'pending' | 'success' | 'error';

export interface OptimisticState<T> {
  data: T;
  status: OptimisticStatus;
  error: string | null;
  isReverting: boolean;
}

// Export/Import
export interface ExportData {
  operations: SyncOperation[];
  drafts: LocalDraft[];
  progress: LocalProgress[];
  bookmarks: LocalBookmark[];
  curriculum: CachedCurriculum[];
  exportedAt: string;
  version: string;
}
