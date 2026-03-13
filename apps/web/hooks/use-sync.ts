'use client';

/**
 * Sync Hook
 * 
 * React hook for accessing sync state and operations
 */

import { useState, useEffect, useCallback } from 'react';
import {
  getSyncState,
  subscribeToSyncEvents,
  syncPendingOperations,
  queueOperation,
  SyncState,
  OperationType,
  OperationAction,
  syncProgress,
  syncDraft,
  syncBookmark,
  resolveConflict,
  ConflictResolution,
  ConflictInfo,
} from '@/lib/sync-engine';

export interface UseSyncReturn {
  state: SyncState;
  isOnline: boolean;
  sync: () => Promise<void>;
  queue: (params: {
    type: OperationType;
    action: OperationAction;
    data: unknown;
  }) => Promise<void>;
  queueProgress: (problemSlug: string, status: 'not_started' | 'in_progress' | 'completed') => Promise<void>;
  queueDraft: (problemSlug: string, code: string) => Promise<void>;
  queueBookmark: (problemSlug: string, bookmarked: boolean, note?: string) => Promise<void>;
  resolve: (resolution: ConflictResolution) => void;
}

export function useSync(
  onConflict?: (conflict: ConflictInfo) => void
): UseSyncReturn {
  const [state, setState] = useState<SyncState>(getSyncState());
  const [isOnline, setIsOnline] = useState<boolean>(true);

  useEffect(() => {
    // Subscribe to sync events
    const unsubscribe = subscribeToSyncEvents((newState) => {
      setState(newState);
    });

    // Listen for online/offline
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    setIsOnline(navigator.onLine);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      unsubscribe();
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Sync pending operations
  const sync = useCallback(async () => {
    await syncPendingOperations();
  }, []);

  // Queue a generic operation
  const queue = useCallback(
    async (params: { type: OperationType; action: OperationAction; data: unknown }) => {
      await queueOperation(params);
    },
    []
  );

  // Queue progress update
  const queueProgress = useCallback(async (problemSlug: string, status: 'not_started' | 'in_progress' | 'completed') => {
    await syncProgress(problemSlug, status);
  }, []);

  // Queue draft save
  const queueDraft = useCallback(async (problemSlug: string, code: string) => {
    await syncDraft(problemSlug, code);
  }, []);

  // Queue bookmark toggle
  const queueBookmark = useCallback(async (problemSlug: string, bookmarked: boolean, note?: string) => {
    await syncBookmark(problemSlug, bookmarked, note);
  }, []);

  // Resolve a conflict
  const resolve = useCallback((resolution: ConflictResolution) => {
    resolveConflict(resolution);
  }, []);

  return {
    state,
    isOnline,
    sync,
    queue,
    queueProgress,
    queueDraft,
    queueBookmark,
    resolve,
  };
}

export default useSync;
