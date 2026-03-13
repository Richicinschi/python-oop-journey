/**
 * Offline Database - IndexedDB wrapper using idb
 * 
 * Database: oop-journey-offline
 * Stores:
 *   - operations: Pending sync operations
 *   - drafts: Local code drafts
 *   - progress: Local progress cache
 *   - bookmarks: Local bookmarks cache
 *   - curriculum: Cached curriculum data
 */

import { openDB, DBSchema, IDBPDatabase, deleteDB } from 'idb';

const DB_NAME = 'oop-journey-offline';
const DB_VERSION = 1;

// Operation types for sync
export type OperationType = 'progress' | 'draft' | 'bookmark';
export type OperationAction = 'create' | 'update' | 'delete';

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

// Database schema definition
interface OOPJourneyDB extends DBSchema {
  operations: {
    key: string;
    value: SyncOperation;
    indexes: { 'by-timestamp': number; 'by-type': string };
  };
  drafts: {
    key: string;
    value: LocalDraft;
  };
  progress: {
    key: string;
    value: LocalProgress;
  };
  bookmarks: {
    key: string;
    value: LocalBookmark;
  };
  curriculum: {
    key: string;
    value: CachedCurriculum;
  };
}

let dbPromise: Promise<IDBPDatabase<OOPJourneyDB>> | null = null;

/**
 * Get or create the IndexedDB database instance
 */
export function getDB(): Promise<IDBPDatabase<OOPJourneyDB>> {
  if (!dbPromise) {
    dbPromise = openDB<OOPJourneyDB>(DB_NAME, DB_VERSION, {
      upgrade(db) {
        // Operations store for pending sync
        if (!db.objectStoreNames.contains('operations')) {
          const operationStore = db.createObjectStore('operations', {
            keyPath: 'id',
          });
          operationStore.createIndex('by-timestamp', 'timestamp');
          operationStore.createIndex('by-type', 'type');
        }

        // Drafts store
        if (!db.objectStoreNames.contains('drafts')) {
          db.createObjectStore('drafts', { keyPath: 'problemSlug' });
        }

        // Progress store
        if (!db.objectStoreNames.contains('progress')) {
          db.createObjectStore('progress', { keyPath: 'problemSlug' });
        }

        // Bookmarks store
        if (!db.objectStoreNames.contains('bookmarks')) {
          db.createObjectStore('bookmarks', { keyPath: 'problemSlug' });
        }

        // Curriculum cache store
        if (!db.objectStoreNames.contains('curriculum')) {
          db.createObjectStore('curriculum', { keyPath: 'version' });
        }
      },
    });
  }
  return dbPromise;
}

/**
 * Close the database connection
 */
export async function closeDB(): Promise<void> {
  if (dbPromise) {
    const db = await dbPromise;
    db.close();
    dbPromise = null;
  }
}

/**
 * Delete the entire database (useful for logout/reset)
 */
export async function deleteDatabase(): Promise<void> {
  await closeDB();
  await deleteDB(DB_NAME);
}

// ==================== Operations (Sync Queue) ====================

/**
 * Add a sync operation to the queue
 */
export async function addOperation(
  operation: Omit<SyncOperation, 'id' | 'retryCount'>
): Promise<SyncOperation> {
  const db = await getDB();
  const fullOperation: SyncOperation = {
    ...operation,
    id: generateOperationId(),
    retryCount: 0,
  };
  await db.put('operations', fullOperation);
  return fullOperation;
}

/**
 * Alias for addOperation - used by migration
 */
export const queueOperation = addOperation;

/**
 * Get all pending operations, sorted by timestamp
 */
export async function getPendingOperations(): Promise<SyncOperation[]> {
  const db = await getDB();
  return db.getAllFromIndex('operations', 'by-timestamp');
}

/**
 * Get operations by type
 */
export async function getOperationsByType(
  type: OperationType
): Promise<SyncOperation[]> {
  const db = await getDB();
  return db.getAllFromIndex('operations', 'by-type', type);
}

/**
 * Get a single operation by ID
 */
export async function getOperation(id: string): Promise<SyncOperation | undefined> {
  const db = await getDB();
  return db.get('operations', id);
}

/**
 * Update an operation (e.g., increment retry count)
 */
export async function updateOperation(
  id: string,
  updates: Partial<SyncOperation>
): Promise<SyncOperation | undefined> {
  const db = await getDB();
  const existing = await db.get('operations', id);
  if (!existing) return undefined;

  const updated = { ...existing, ...updates };
  await db.put('operations', updated);
  return updated;
}

/**
 * Remove an operation from the queue (after successful sync)
 */
export async function removeOperation(id: string): Promise<void> {
  const db = await getDB();
  await db.delete('operations', id);
}

/**
 * Clear all operations
 */
export async function clearAllOperations(): Promise<void> {
  const db = await getDB();
  await db.clear('operations');
}

/**
 * Get count of pending operations
 */
export async function getPendingOperationsCount(): Promise<number> {
  const db = await getDB();
  return db.count('operations');
}

// ==================== Drafts ====================

/**
 * Save a code draft locally
 */
export async function saveDraft(draft: LocalDraft): Promise<void> {
  const db = await getDB();
  await db.put('drafts', draft);
}

/**
 * Get a draft for a specific problem
 */
export async function getDraft(problemSlug: string): Promise<LocalDraft | undefined> {
  const db = await getDB();
  return db.get('drafts', problemSlug);
}

/**
 * Get all drafts
 */
export async function getAllDrafts(): Promise<LocalDraft[]> {
  const db = await getDB();
  return db.getAll('drafts');
}

/**
 * Delete a draft
 */
export async function deleteDraft(problemSlug: string): Promise<void> {
  const db = await getDB();
  await db.delete('drafts', problemSlug);
}

// ==================== Progress ====================

/**
 * Save progress locally
 */
export async function saveProgress(progress: LocalProgress): Promise<void> {
  const db = await getDB();
  await db.put('progress', progress);
}

/**
 * Get progress for a specific problem
 */
export async function getProgress(problemSlug: string): Promise<LocalProgress | undefined> {
  const db = await getDB();
  return db.get('progress', problemSlug);
}

/**
 * Get all progress entries
 */
export async function getAllProgress(): Promise<LocalProgress[]> {
  const db = await getDB();
  return db.getAll('progress');
}

/**
 * Update problem status
 */
export async function updateProblemStatus(
  problemSlug: string,
  status: LocalProgress['status']
): Promise<LocalProgress> {
  const db = await getDB();
  const existing = await db.get('progress', problemSlug);

  const updated: LocalProgress = {
    problemSlug,
    status,
    attempts: (existing?.attempts || 0) + (status === 'completed' ? 1 : 0),
    completedAt: status === 'completed' ? Date.now() : existing?.completedAt,
    updatedAt: Date.now(),
  };

  await db.put('progress', updated);
  return updated;
}

// ==================== Bookmarks ====================

/**
 * Save a bookmark locally
 */
export async function saveBookmark(bookmark: LocalBookmark): Promise<void> {
  const db = await getDB();
  await db.put('bookmarks', bookmark);
}

/**
 * Get a bookmark for a specific problem
 */
export async function getBookmark(problemSlug: string): Promise<LocalBookmark | undefined> {
  const db = await getDB();
  return db.get('bookmarks', problemSlug);
}

/**
 * Get all bookmarks
 */
export async function getAllBookmarks(): Promise<LocalBookmark[]> {
  const db = await getDB();
  return db.getAll('bookmarks');
}

/**
 * Delete a bookmark
 */
export async function deleteBookmark(problemSlug: string): Promise<void> {
  const db = await getDB();
  await db.delete('bookmarks', problemSlug);
}

// ==================== Curriculum Cache ====================

/**
 * Cache curriculum data
 */
export async function cacheCurriculum(curriculum: CachedCurriculum): Promise<void> {
  const db = await getDB();
  await db.put('curriculum', curriculum);
}

/**
 * Get cached curriculum
 */
export async function getCachedCurriculum(version: string): Promise<CachedCurriculum | undefined> {
  const db = await getDB();
  return db.get('curriculum', version);
}

/**
 * Get all cached curriculum versions
 */
export async function getAllCachedCurriculum(): Promise<CachedCurriculum[]> {
  const db = await getDB();
  return db.getAll('curriculum');
}

/**
 * Clear curriculum cache
 */
export async function clearCurriculumCache(): Promise<void> {
  const db = await getDB();
  await db.clear('curriculum');
}

// ==================== Utility ====================

/**
 * Generate a unique operation ID
 */
function generateOperationId(): string {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Export all local data (for backup/export)
 */
export async function exportAllData(): Promise<{
  operations: SyncOperation[];
  drafts: LocalDraft[];
  progress: LocalProgress[];
  bookmarks: LocalBookmark[];
  curriculum: CachedCurriculum[];
  exportedAt: string;
}> {
  const [operations, drafts, progress, bookmarks, curriculum] = await Promise.all([
    getPendingOperations(),
    getAllDrafts(),
    getAllProgress(),
    getAllBookmarks(),
    getAllCachedCurriculum(),
  ]);

  return {
    operations,
    drafts,
    progress,
    bookmarks,
    curriculum,
    exportedAt: new Date().toISOString(),
  };
}

/**
 * Import data (for restore/import)
 * Note: This should be used carefully to avoid conflicts
 */
export async function importData(data: {
  operations?: SyncOperation[];
  drafts?: LocalDraft[];
  progress?: LocalProgress[];
  bookmarks?: LocalBookmark[];
  curriculum?: CachedCurriculum[];
}): Promise<void> {
  const db = await getDB();

  await db.transaction(
    ['operations', 'drafts', 'progress', 'bookmarks', 'curriculum'],
    'readwrite',
    async (tx) => {
      if (data.operations) {
        for (const op of data.operations) {
          await tx.objectStore('operations').put(op);
        }
      }
      if (data.drafts) {
        for (const draft of data.drafts) {
          await tx.objectStore('drafts').put(draft);
        }
      }
      if (data.progress) {
        for (const prog of data.progress) {
          await tx.objectStore('progress').put(prog);
        }
      }
      if (data.bookmarks) {
        for (const bookmark of data.bookmarks) {
          await tx.objectStore('bookmarks').put(bookmark);
        }
      }
      if (data.curriculum) {
        for (const curr of data.curriculum) {
          await tx.objectStore('curriculum').put(curr);
        }
      }
    }
  );
}

export default {
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
  // Curriculum
  cacheCurriculum,
  getCachedCurriculum,
  getAllCachedCurriculum,
  clearCurriculumCache,
  // Import/Export
  exportAllData,
  importData,
};
