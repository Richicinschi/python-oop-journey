/**
 * Data Migration on Login
 * 
 * Features:
 * - Scan localStorage for legacy progress data
 * - Convert to new format
 * - Queue for sync to server
 * - Show migration progress modal
 * - Handle conflicts during import
 */

import { useState, useCallback } from 'react';
import {
  getAllProgress,
  saveProgress,
  queueOperation,
  LocalProgress,
  SyncOperation,
  addOperation,
} from './offline-db';
import { syncPendingOperations } from './sync-engine';

// ==================== Types ====================

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

export interface MigrationOptions {
  onProgress?: (progress: MigrationProgress) => void;
  onComplete?: (result: MigrationResult) => void;
  onConflict?: (conflict: {
    problemSlug: string;
    local: LocalProgress | null;
    legacy: LegacyProgressData;
    server: unknown;
  }) => 'local' | 'server' | 'merge';
  dryRun?: boolean;
}

// ==================== Constants ====================

const LEGACY_STORAGE_KEY = 'oop-journey-progress';
const LEGACY_DRAFTS_KEY_PREFIX = 'oop-journey-draft-';
const LEGACY_BOOKMARKS_KEY = 'oop-journey-bookmarks';

// ==================== Migration Functions ====================

/**
 * Check if there's legacy data to migrate
 */
export function hasLegacyData(): boolean {
  if (typeof window === 'undefined') return false;

  const legacyProgress = localStorage.getItem(LEGACY_STORAGE_KEY);
  const legacyBookmarks = localStorage.getItem(LEGACY_BOOKMARKS_KEY);

  // Check for legacy draft keys
  const hasDrafts = Object.keys(localStorage).some(key => 
    key.startsWith(LEGACY_DRAFTS_KEY_PREFIX)
  );

  return !!(legacyProgress || legacyBookmarks || hasDrafts);
}

/**
 * Scan localStorage for all legacy data
 */
export function scanLegacyData(): {
  progress: LegacyProgressData | null;
  drafts: Array<{ problemSlug: string; code: string; savedAt: number }>;
  bookmarks: string[];
} {
  if (typeof window === 'undefined') {
    return { progress: null, drafts: [], bookmarks: [] };
  }

  // Scan progress
  let progress: LegacyProgressData | null = null;
  try {
    const progressData = localStorage.getItem(LEGACY_STORAGE_KEY);
    if (progressData) {
      progress = JSON.parse(progressData);
    }
  } catch (error) {
    console.error('Failed to parse legacy progress:', error);
  }

  // Scan drafts
  const drafts: Array<{ problemSlug: string; code: string; savedAt: number }> = [];
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key?.startsWith(LEGACY_DRAFTS_KEY_PREFIX)) {
      try {
        const problemSlug = key.replace(LEGACY_DRAFTS_KEY_PREFIX, '');
        const code = localStorage.getItem(key);
        if (code) {
          drafts.push({
            problemSlug,
            code,
            savedAt: Date.now(), // Legacy drafts don't have timestamps
          });
        }
      } catch (error) {
        console.error('Failed to parse legacy draft:', error);
      }
    }
  }

  // Scan bookmarks
  let bookmarks: string[] = [];
  try {
    const bookmarksData = localStorage.getItem(LEGACY_BOOKMARKS_KEY);
    if (bookmarksData) {
      bookmarks = JSON.parse(bookmarksData);
    }
  } catch (error) {
    console.error('Failed to parse legacy bookmarks:', error);
  }

  return { progress, drafts, bookmarks };
}

/**
 * Migrate legacy data to new IndexedDB format
 */
export async function migrateLegacyData(
  options: MigrationOptions = {}
): Promise<MigrationResult> {
  const { onProgress, onComplete, dryRun = false } = options;

  const result: MigrationResult = {
    success: false,
    migrated: 0,
    skipped: 0,
    errors: [],
    conflicts: [],
  };

  const legacyData = scanLegacyData();
  const itemsToMigrate: Array<{
    type: 'progress' | 'draft' | 'bookmark';
    data: unknown;
    identifier: string;
  }> = [];

  // Build list of items to migrate
  if (legacyData.progress?.completedProblems) {
    for (const problemSlug of legacyData.progress.completedProblems) {
      itemsToMigrate.push({
        type: 'progress',
        data: { problemSlug, status: 'completed' },
        identifier: problemSlug,
      });
    }
  }

  for (const draft of legacyData.drafts) {
    itemsToMigrate.push({
      type: 'draft',
      data: draft,
      identifier: draft.problemSlug,
    });
  }

  for (const problemSlug of legacyData.bookmarks) {
    itemsToMigrate.push({
      type: 'bookmark',
      data: { problemSlug, createdAt: Date.now() },
      identifier: problemSlug,
    });
  }

  const progress: MigrationProgress = {
    total: itemsToMigrate.length,
    processed: 0,
    currentItem: null,
    errors: [],
  };

  // Migrate each item
  for (const item of itemsToMigrate) {
    progress.currentItem = item.identifier;
    onProgress?.({ ...progress });

    try {
      if (!dryRun) {
        await migrateItem(item);
      }
      result.migrated++;
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : 'Unknown error';
      result.errors.push(`Failed to migrate ${item.type} ${item.identifier}: ${errorMsg}`);
      progress.errors.push(errorMsg);
    }

    progress.processed++;
  }

  progress.currentItem = null;
  onProgress?.({ ...progress });

  result.success = result.errors.length === 0;
  onComplete?.(result);

  // Trigger sync if not dry run
  if (!dryRun && result.migrated > 0 && navigator.onLine) {
    syncPendingOperations();
  }

  return result;
}

/**
 * Migrate a single item
 */
async function migrateItem(item: {
  type: 'progress' | 'draft' | 'bookmark';
  data: unknown;
  identifier: string;
}): Promise<void> {
  switch (item.type) {
    case 'progress': {
      const { problemSlug, status } = item.data as { problemSlug: string; status: string };
      
      // Check if already exists in IndexedDB
      const existingProgress = await getAllProgress();
      const exists = existingProgress.some(p => p.problemSlug === problemSlug);
      
      if (!exists) {
        const progress: LocalProgress = {
          problemSlug,
          status: status as 'completed' | 'in_progress' | 'not_started',
          attempts: 1,
          completedAt: status === 'completed' ? Date.now() : undefined,
          updatedAt: Date.now(),
        };
        
        await saveProgress(progress);
        
        // Queue for sync
        await queueOperation({
          type: 'progress',
          action: 'create',
          data: progress,
        });
      }
      break;
    }

    case 'draft': {
      const draft = item.data as { problemSlug: string; code: string; savedAt: number };
      
      const { saveDraft } = await import('./offline-db');
      await saveDraft({
        problemSlug: draft.problemSlug,
        code: draft.code,
        savedAt: draft.savedAt,
      });
      
      // Queue for sync
      await queueOperation({
        type: 'draft',
        action: 'create',
        data: draft,
      });
      break;
    }

    case 'bookmark': {
      const bookmark = item.data as { problemSlug: string; createdAt: number };
      
      const { saveBookmark } = await import('./offline-db');
      await saveBookmark({
        problemSlug: bookmark.problemSlug,
        createdAt: bookmark.createdAt,
      });
      
      // Queue for sync
      await queueOperation({
        type: 'bookmark',
        action: 'create',
        data: bookmark,
      });
      break;
    }
  }
}

/**
 * Clear legacy data from localStorage after successful migration
 */
export function clearLegacyData(): void {
  if (typeof window === 'undefined') return;

  // Remove progress
  localStorage.removeItem(LEGACY_STORAGE_KEY);

  // Remove bookmarks
  localStorage.removeItem(LEGACY_BOOKMARKS_KEY);

  // Remove drafts
  const keysToRemove: string[] = [];
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key?.startsWith(LEGACY_DRAFTS_KEY_PREFIX)) {
      keysToRemove.push(key);
    }
  }
  
  for (const key of keysToRemove) {
    localStorage.removeItem(key);
  }

  console.log('[Migration] Cleared legacy data from localStorage');
}

/**
 * Estimate the amount of data to migrate
 */
export function estimateMigrationSize(): {
  progressItems: number;
  draftItems: number;
  bookmarkItems: number;
  totalSize: number;
} {
  const legacyData = scanLegacyData();

  const progressItems = legacyData.progress?.completedProblems.length || 0;
  const draftItems = legacyData.drafts.length;
  const bookmarkItems = legacyData.bookmarks.length;

  // Rough size estimation
  let totalSize = 0;
  if (legacyData.progress) {
    totalSize += JSON.stringify(legacyData.progress).length;
  }
  for (const draft of legacyData.drafts) {
    totalSize += draft.code.length;
  }
  totalSize += JSON.stringify(legacyData.bookmarks).length;

  return {
    progressItems,
    draftItems,
    bookmarkItems,
    totalSize,
  };
}

// ==================== React Hook ====================

/**
 * Hook for managing data migration
 */
export function useDataMigration() {
  const [isMigrating, setIsMigrating] = useState(false);
  const [progress, setProgress] = useState<MigrationProgress | null>(null);
  const [result, setResult] = useState<MigrationResult | null>(null);
  const [showMigrationModal, setShowMigrationModal] = useState(false);

  const checkAndMigrate = useCallback(async (autoMigrate = false) => {
    if (!hasLegacyData()) {
      return;
    }

    if (autoMigrate) {
      setIsMigrating(true);
      const migrationResult = await migrateLegacyData({
        onProgress: setProgress,
        onComplete: (res) => {
          setResult(res);
          if (res.success) {
            clearLegacyData();
          }
        },
      });
      setIsMigrating(false);
      return migrationResult;
    } else {
      setShowMigrationModal(true);
      return null;
    }
  }, []);

  const startMigration = useCallback(async () => {
    setIsMigrating(true);
    setShowMigrationModal(false);
    
    const migrationResult = await migrateLegacyData({
      onProgress: setProgress,
      onComplete: (res) => {
        setResult(res);
        if (res.success) {
          clearLegacyData();
        }
      },
    });
    
    setIsMigrating(false);
    return migrationResult;
  }, []);

  const skipMigration = useCallback(() => {
    setShowMigrationModal(false);
  }, []);

  return {
    hasLegacyData: hasLegacyData(),
    isMigrating,
    progress,
    result,
    showMigrationModal,
    checkAndMigrate,
    startMigration,
    skipMigration,
    estimateSize: estimateMigrationSize,
  };
}

export default {
  hasLegacyData,
  scanLegacyData,
  migrateLegacyData,
  clearLegacyData,
  estimateMigrationSize,
  useDataMigration,
};
