/**
 * Sync Engine - Queue-based sync system with conflict resolution
 * 
 * Features:
 * - Queue-based sync system
 * - Operation types: CREATE, UPDATE, DELETE
 * - Conflict resolution: Last-write-wins (server) with manual merge option
 * - Retry with exponential backoff
 * - Max retry attempts: 5
 */

import {
  getDB,
  addOperation,
  getPendingOperations,
  getOperation,
  updateOperation,
  removeOperation,
  getPendingOperationsCount,
  SyncOperation,
  OperationType,
  OperationAction,
  LocalProgress,
  LocalDraft,
  LocalBookmark,
} from './offline-db';
import { api, ApiError } from './api';

// ==================== Types ====================

export type { OperationType, OperationAction } from './offline-db';

// Background Sync API types
interface SyncManager {
  register(tag: string): Promise<void>;
}

interface ServiceWorkerRegistrationWithSync extends ServiceWorkerRegistration {
  sync?: SyncManager;
}

export type SyncStatus = 'idle' | 'syncing' | 'error' | 'offline' | 'conflict';

export interface SyncState {
  status: SyncStatus;
  pendingCount: number;
  lastSyncAt: number | null;
  lastError: string | null;
}

export interface ConflictResolution {
  operationId: string;
  strategy: 'local' | 'server' | 'merge';
  mergedData?: unknown;
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

export interface SyncOptions {
  maxRetries?: number;
  baseDelay?: number;
  maxDelay?: number;
  onStatusChange?: (status: SyncStatus) => void;
  onConflict?: (conflict: ConflictInfo) => void;
  onProgress?: (completed: number, total: number) => void;
}

export interface ConflictInfo {
  operationId: string;
  type: OperationType;
  localData: unknown;
  serverData: unknown;
  localTimestamp: number;
  serverTimestamp: string;
}

// ==================== Constants ====================

const DEFAULT_MAX_RETRIES = 5;
const DEFAULT_BASE_DELAY = 1000; // 1 second
const DEFAULT_MAX_DELAY = 60000; // 60 seconds
const SYNC_INTERVAL = 5 * 60 * 1000; // 5 minutes

// Generate a unique client ID for this device/session
export const CLIENT_ID = typeof window !== 'undefined'
  ? `${navigator.userAgent.slice(0, 20)}-${Date.now()}`
  : 'server';

// ==================== State ====================

let syncState: SyncState = {
  status: 'idle',
  pendingCount: 0,
  lastSyncAt: null,
  lastError: null,
};

let syncOptions: SyncOptions = {};
let syncIntervalId: ReturnType<typeof setInterval> | null = null;
let isSyncing = false;
const conflictResolvers = new Map<string, (resolution: ConflictResolution) => void>();

// ==================== Event Listeners ====================

type SyncEventListener = (state: SyncState) => void;
const listeners = new Set<SyncEventListener>();

function notifyListeners() {
  listeners.forEach((listener) => listener({ ...syncState }));
}

export function subscribeToSyncEvents(listener: SyncEventListener): () => void {
  listeners.add(listener);
  // Immediately notify with current state
  listener({ ...syncState });
  return () => listeners.delete(listener);
}

function updateStatus(status: SyncStatus) {
  syncState.status = status;
  syncOptions.onStatusChange?.(status);
  notifyListeners();
}

// ==================== Core Sync Functions ====================

/**
 * Initialize the sync engine
 */
export function initSyncEngine(options: SyncOptions = {}): void {
  syncOptions = {
    maxRetries: DEFAULT_MAX_RETRIES,
    baseDelay: DEFAULT_BASE_DELAY,
    maxDelay: DEFAULT_MAX_DELAY,
    ...options,
  };

  // Update initial pending count
  updatePendingCount();

  // Start periodic sync
  startPeriodicSync();

  // Listen for online/offline events
  if (typeof window !== 'undefined') {
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Initial online check
    if (navigator.onLine) {
      // Try to sync any pending operations on init
      syncPendingOperations();
    } else {
      updateStatus('offline');
    }
  }
}

/**
 * Cleanup the sync engine
 */
export function cleanupSyncEngine(): void {
  stopPeriodicSync();
  if (typeof window !== 'undefined') {
    window.removeEventListener('online', handleOnline);
    window.removeEventListener('offline', handleOffline);
  }
  listeners.clear();
}

/**
 * Queue an operation for sync
 */
export async function queueOperation(params: {
  type: OperationType;
  action: OperationAction;
  data: unknown;
}): Promise<SyncOperation> {
  const operation = await addOperation({
    ...params,
    timestamp: Date.now(),
    clientId: CLIENT_ID,
  } as Omit<SyncOperation, 'id' | 'retryCount'>);

  await updatePendingCount();

  // Try to sync immediately if online
  if (navigator.onLine && syncState.status !== 'syncing') {
    syncPendingOperations();
  }

  // Register for background sync if available
  registerBackgroundSync();

  return operation;
}

/**
 * Sync all pending operations
 */
export async function syncPendingOperations(): Promise<{
  success: boolean;
  synced: number;
  conflicts: number;
  errors: number;
}> {
  if (isSyncing || !navigator.onLine) {
    return { success: false, synced: 0, conflicts: 0, errors: 0 };
  }

  isSyncing = true;
  updateStatus('syncing');

  try {
    const operations = await getPendingOperations();

    if (operations.length === 0) {
      updateStatus('idle');
      isSyncing = false;
      return { success: true, synced: 0, conflicts: 0, errors: 0 };
    }

    let synced = 0;
    let conflicts = 0;
    let errors = 0;

    for (let i = 0; i < operations.length; i++) {
      const operation = operations[i];
      syncOptions.onProgress?.(i, operations.length);

      const result = await syncOperation(operation);

      if (result.success) {
        synced++;
      } else if (result.conflict) {
        conflicts++;
      } else {
        errors++;
      }
    }

    await updatePendingCount();

    const hasErrors = errors > 0;
    const hasConflicts = conflicts > 0;

    if (hasErrors) {
      updateStatus('error');
    } else if (hasConflicts) {
      // Conflicts need resolution, keep syncing status until resolved
    } else {
      updateStatus('idle');
      syncState.lastSyncAt = Date.now();
    }

    return { success: !hasErrors, synced, conflicts, errors };
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Sync failed';
    syncState.lastError = errorMessage;
    updateStatus('error');
    return { success: false, synced: 0, conflicts: 0, errors: 1 };
  } finally {
    isSyncing = false;
  }
}

/**
 * Sync a single operation
 */
async function syncOperation(
  operation: SyncOperation
): Promise<{ success: boolean; conflict?: boolean; error?: string }> {
  const maxRetries = syncOptions.maxRetries || DEFAULT_MAX_RETRIES;

  // Check if max retries exceeded
  if (operation.retryCount >= maxRetries) {
    return { success: false, error: 'Max retries exceeded' };
  }

  try {
    // Attempt to sync via API
    const response = await apiClient.sync.batch([operation]);

    // Handle conflicts
    if (response.conflicts.length > 0) {
      const conflict = response.conflicts[0];
      const conflictInfo: ConflictInfo = {
        operationId: operation.id,
        type: operation.type,
        localData: conflict.localData,
        serverData: conflict.serverData,
        localTimestamp: operation.timestamp,
        serverTimestamp: response.serverTimestamp,
      };

      // Notify about conflict
      syncOptions.onConflict?.(conflictInfo);

      // Wait for conflict resolution
      const resolution = await waitForConflictResolution(operation.id, conflictInfo);

      if (resolution.strategy === 'local') {
        // Force local version
        await forceSyncOperation(operation);
      } else if (resolution.strategy === 'server') {
        // Accept server version - just remove the operation
        await removeOperation(operation.id);
      } else if (resolution.strategy === 'merge' && resolution.mergedData) {
        // Update with merged data and retry
        const updatedOperation = await updateOperation(operation.id, {
          data: resolution.mergedData,
        });
        if (updatedOperation) {
          return syncOperation(updatedOperation);
        }
      }

      return { success: false, conflict: true };
    }

    // Success - remove from queue
    await removeOperation(operation.id);
    return { success: true };
  } catch (error) {
    // Handle specific error types
    if (error instanceof ApiError) {
      if (error.status === 401) {
        // Auth error - don't retry, redirect to login
        window.location.href = '/auth/login';
        return { success: false, error: 'Authentication required' };
      }

      if (error.status >= 400 && error.status < 500 && error.status !== 429) {
        // Client error (except rate limit) - don't retry
        await removeOperation(operation.id);
        return { success: false, error: error.message };
      }
    }

    // Network or server error - retry with backoff
    const shouldRetry = await handleRetry(operation, error);
    if (!shouldRetry) {
      return { success: false, error: 'Max retries exceeded' };
    }

    return { success: false, error: error instanceof Error ? error.message : 'Unknown error' };
  }
}

/**
 * Force sync an operation (for conflict resolution choosing local)
 */
async function forceSyncOperation(operation: SyncOperation): Promise<void> {
  try {
    await apiClient.sync.force({
      ...operation,
      force: true,
    });
    await removeOperation(operation.id);
  } catch (error) {
    console.error('Force sync failed:', error);
    throw error;
  }
}

/**
 * Handle retry with exponential backoff
 */
async function handleRetry(
  operation: SyncOperation,
  error: unknown
): Promise<boolean> {
  const maxRetries = syncOptions.maxRetries || DEFAULT_MAX_RETRIES;

  if (operation.retryCount >= maxRetries) {
    return false;
  }

  const newRetryCount = operation.retryCount + 1;
  const baseDelay = syncOptions.baseDelay || DEFAULT_BASE_DELAY;
  const maxDelay = syncOptions.maxDelay || DEFAULT_MAX_DELAY;

  // Exponential backoff with jitter
  const delay = Math.min(
    baseDelay * Math.pow(2, newRetryCount) + Math.random() * 1000,
    maxDelay
  );

  // Update operation with retry info
  await updateOperation(operation.id, {
    retryCount: newRetryCount,
    lastError: error instanceof Error ? error.message : 'Unknown error',
  });

  // Wait before next retry
  await sleep(delay);

  return true;
}

/**
 * Wait for user to resolve a conflict
 */
function waitForConflictResolution(
  operationId: string,
  conflictInfo: ConflictInfo
): Promise<ConflictResolution> {
  return new Promise((resolve) => {
    // Store resolver for later
    conflictResolvers.set(operationId, resolve);

    // Set a timeout to auto-resolve with server preference after 30 seconds
    setTimeout(() => {
      if (conflictResolvers.has(operationId)) {
        resolve({ operationId, strategy: 'server' });
        conflictResolvers.delete(operationId);
      }
    }, 30000);
  });
}

/**
 * Resolve a conflict manually
 */
export function resolveConflict(resolution: ConflictResolution): void {
  const resolver = conflictResolvers.get(resolution.operationId);
  if (resolver) {
    resolver(resolution);
    conflictResolvers.delete(resolution.operationId);
  }
}

/**
 * Get current sync state
 */
export function getSyncState(): SyncState {
  return { ...syncState };
}

// ==================== Background Sync ====================

/**
 * Register for background sync
 */
async function registerBackgroundSync(): Promise<void> {
  if (!('serviceWorker' in navigator) || !('sync' in ServiceWorkerRegistration.prototype)) {
    return;
  }

  try {
    const registration = await navigator.serviceWorker.ready;
    await (registration as ServiceWorkerRegistrationWithSync).sync?.register('sync-pending-operations');
  } catch (error) {
    console.error('Background sync registration failed:', error);
  }
}

/**
 * Start periodic sync
 */
function startPeriodicSync(): void {
  if (syncIntervalId) return;

  syncIntervalId = setInterval(() => {
    if (navigator.onLine && syncState.status !== 'syncing') {
      syncPendingOperations();
    }
  }, SYNC_INTERVAL);
}

/**
 * Stop periodic sync
 */
function stopPeriodicSync(): void {
  if (syncIntervalId) {
    clearInterval(syncIntervalId);
    syncIntervalId = null;
  }
}

// ==================== Event Handlers ====================

function handleOnline(): void {
  updateStatus('idle');
  syncPendingOperations();
}

function handleOffline(): void {
  updateStatus('offline');
}

async function updatePendingCount(): Promise<void> {
  syncState.pendingCount = await getPendingOperationsCount();
  notifyListeners();
}

// ==================== API Client for Sync ====================

const apiClient = {
  sync: {
    batch: async (operations: SyncOperation[]): Promise<BatchSyncResponse> => {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/sync/batch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ operations }),
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ message: 'Sync failed' }));
        throw new ApiError(response.status, error.message || 'Sync failed');
      }

      return response.json();
    },

    force: async (operation: SyncOperation & { force: boolean }): Promise<void> => {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/sync/force`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ operation }),
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ message: 'Force sync failed' }));
        throw new ApiError(response.status, error.message || 'Force sync failed');
      }
    },
  },
};

// ==================== Utility Functions ====================

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// ==================== Convenience Methods ====================

/**
 * Queue a progress update
 */
export async function syncProgress(problemSlug: string, status: LocalProgress['status']): Promise<SyncOperation> {
  return queueOperation({
    type: 'progress',
    action: status === 'not_started' ? 'delete' : 'update',
    data: { problemSlug, status },
  });
}

/**
 * Queue a draft save
 */
export async function syncDraft(problemSlug: string, code: string): Promise<SyncOperation> {
  return queueOperation({
    type: 'draft',
    action: 'update',
    data: { problemSlug, code, savedAt: Date.now() },
  });
}

/**
 * Queue a bookmark toggle
 */
export async function syncBookmark(
  problemSlug: string,
  bookmarked: boolean,
  note?: string
): Promise<SyncOperation> {
  return queueOperation({
    type: 'bookmark',
    action: bookmarked ? 'create' : 'delete',
    data: { problemSlug, note, createdAt: Date.now() },
  });
}

// ==================== Export ====================

export default {
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
};
