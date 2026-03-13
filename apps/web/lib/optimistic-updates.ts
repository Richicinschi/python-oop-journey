/**
 * Optimistic Updates System
 * 
 * Features:
 * - Update UI immediately
 * - Queue operation for sync
 * - Rollback on failure (with retry)
 * - Show sync status indicator
 */

import { useState, useCallback } from 'react';
import {
  queueOperation,
  updateProblemStatus,
  saveDraft,
  saveBookmark,
  deleteBookmark,
  LocalProgress,
} from './offline-db';
import { syncPendingOperations } from './sync-engine';

// ==================== Types ====================

export type OptimisticStatus = 'idle' | 'pending' | 'success' | 'error';

export interface OptimisticState<T> {
  data: T;
  status: OptimisticStatus;
  error: string | null;
  isReverting: boolean;
}

export interface OptimisticOptions<T> {
  onSuccess?: (data: T) => void;
  onError?: (error: Error, originalData: T) => void;
  onRevert?: (originalData: T) => void;
}

// ==================== Progress Optimistic Updates ====================

/**
 * Optimistically update problem progress
 */
export async function optimisticProgressUpdate(
  problemSlug: string,
  status: LocalProgress['status'],
  options: {
    onSuccess?: () => void;
    onError?: (error: Error) => void;
    onRevert?: () => void;
  } = {}
): Promise<{ success: boolean; revert: () => Promise<void> }> {
  const previousStatus = await getCurrentProgressStatus(problemSlug);

  try {
    // 1. Update local state immediately (optimistic)
    await updateProblemStatus(problemSlug, status);

    // 2. Queue for sync
    await queueOperation({
      type: 'progress',
      action: status === 'not_started' ? 'delete' : 'update',
      data: { problemSlug, status, updatedAt: Date.now() },
    });

    // 3. Try immediate sync if online
    if (navigator.onLine) {
      syncPendingOperations().then((result) => {
        if (result.success) {
          options.onSuccess?.();
        }
      });
    }

    // Return revert function
    return {
      success: true,
      revert: async () => {
        options.onRevert?.();
        if (previousStatus) {
          await updateProblemStatus(problemSlug, previousStatus);
        }
      },
    };
  } catch (error) {
    const err = error instanceof Error ? error : new Error('Unknown error');
    options.onError?.(err);

    // Revert on error
    if (previousStatus) {
      await updateProblemStatus(problemSlug, previousStatus);
      options.onRevert?.();
    }

    return {
      success: false,
      revert: async () => {
        // Already reverted
      },
    };
  }
}

// ==================== Draft Optimistic Updates ====================

/**
 * Optimistically save a draft
 */
export async function optimisticDraftSave(
  problemSlug: string,
  code: string,
  options: {
    onSuccess?: () => void;
    onError?: (error: Error) => void;
  } = {}
): Promise<{ success: boolean; revert: () => Promise<void> }> {
  const previousDraft = await getCurrentDraft(problemSlug);

  try {
    // 1. Save locally immediately
    await saveDraft({
      problemSlug,
      code,
      savedAt: Date.now(),
    });

    // 2. Queue for sync
    await queueOperation({
      type: 'draft',
      action: 'update',
      data: { problemSlug, code, savedAt: Date.now() },
    });

    // 3. Try immediate sync if online
    if (navigator.onLine) {
      syncPendingOperations().then((result) => {
        if (result.success) {
          options.onSuccess?.();
        }
      });
    }

    return {
      success: true,
      revert: async () => {
        if (previousDraft) {
          await saveDraft(previousDraft);
        }
      },
    };
  } catch (error) {
    const err = error instanceof Error ? error : new Error('Unknown error');
    options.onError?.(err);

    // Revert
    if (previousDraft) {
      await saveDraft(previousDraft);
    }

    return {
      success: false,
      revert: async () => {},
    };
  }
}

// ==================== Bookmark Optimistic Updates ====================

/**
 * Optimistically toggle a bookmark
 */
export async function optimisticBookmarkToggle(
  problemSlug: string,
  bookmarked: boolean,
  note?: string,
  options: {
    onSuccess?: () => void;
    onError?: (error: Error) => void;
  } = {}
): Promise<{ success: boolean; revert: () => Promise<void> }> {
  const previousBookmark = await getCurrentBookmark(problemSlug);

  try {
    // 1. Update locally immediately
    if (bookmarked) {
      await saveBookmark({
        problemSlug,
        note,
        createdAt: Date.now(),
      });
    } else {
      await deleteBookmark(problemSlug);
    }

    // 2. Queue for sync
    await queueOperation({
      type: 'bookmark',
      action: bookmarked ? 'create' : 'delete',
      data: { problemSlug, note, createdAt: Date.now() },
    });

    // 3. Try immediate sync if online
    if (navigator.onLine) {
      syncPendingOperations().then((result) => {
        if (result.success) {
          options.onSuccess?.();
        }
      });
    }

    return {
      success: true,
      revert: async () => {
        if (previousBookmark) {
          await saveBookmark(previousBookmark);
        } else if (bookmarked) {
          await deleteBookmark(problemSlug);
        }
      },
    };
  } catch (error) {
    const err = error instanceof Error ? error : new Error('Unknown error');
    options.onError?.(err);

    // Revert
    if (previousBookmark) {
      await saveBookmark(previousBookmark);
    } else if (bookmarked) {
      await deleteBookmark(problemSlug);
    }

    return {
      success: false,
      revert: async () => {},
    };
  }
}

// ==================== React Hook for Optimistic Updates ====================

/**
 * Hook for managing optimistic state in React components
 */
export function useOptimistic<T>(
  initialData: T,
  options: OptimisticOptions<T> = {}
): {
  state: OptimisticState<T>;
  execute: (optimisticData: T, operation: () => Promise<void>) => Promise<void>;
  revert: () => void;
  reset: () => void;
} {
  const [state, setState] = useState<OptimisticState<T>>({
    data: initialData,
    status: 'idle',
    error: null,
    isReverting: false,
  });

  const [originalData, setOriginalData] = useState<T>(initialData);

  const execute = useCallback(
    async (optimisticData: T, operation: () => Promise<void>) => {
      // Store original data for potential revert
      setOriginalData(state.data);

      // Apply optimistic update
      setState((prev) => ({
        ...prev,
        data: optimisticData,
        status: 'pending',
        error: null,
      }));

      try {
        await operation();

        setState((prev) => ({
          ...prev,
          status: 'success',
        }));

        options.onSuccess?.(optimisticData);
      } catch (error) {
        const err = error instanceof Error ? error : new Error('Operation failed');

        setState((prev) => ({
          ...prev,
          status: 'error',
          error: err.message,
        }));

        options.onError?.(err, originalData);
      }
    },
    [state.data, originalData, options]
  );

  const revert = useCallback(() => {
    setState((prev) => ({
      ...prev,
      data: originalData,
      status: 'idle',
      error: null,
      isReverting: true,
    }));

    options.onRevert?.(originalData);

    // Clear revert flag after a moment
    setTimeout(() => {
      setState((prev) => ({
        ...prev,
        isReverting: false,
      }));
    }, 100);
  }, [originalData, options]);

  const reset = useCallback(() => {
    setState({
      data: initialData,
      status: 'idle',
      error: null,
      isReverting: false,
    });
  }, [initialData]);

  return { state, execute, revert, reset };
}

// ==================== Utility Functions ====================

async function getCurrentProgressStatus(
  problemSlug: string
): Promise<LocalProgress['status'] | null> {
  try {
    const { getProgress } = await import('./offline-db');
    const progress = await getProgress(problemSlug);
    return progress?.status || null;
  } catch {
    return null;
  }
}

async function getCurrentDraft(problemSlug: string) {
  try {
    const { getDraft } = await import('./offline-db');
    return await getDraft(problemSlug);
  } catch {
    return undefined;
  }
}

async function getCurrentBookmark(problemSlug: string) {
  try {
    const { getBookmark } = await import('./offline-db');
    return await getBookmark(problemSlug);
  } catch {
    return undefined;
  }
}

// ==================== Export ====================

export default {
  optimisticProgressUpdate,
  optimisticDraftSave,
  optimisticBookmarkToggle,
  useOptimistic,
};
