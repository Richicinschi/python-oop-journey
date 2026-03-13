'use client';

import { useEffect, useCallback, useRef, useState } from 'react';
import { api } from '@/lib/api';

interface LocalProgressData {
  completedProblems: string[];
  lastActive: string | null;
  version: number;
}

interface SyncStatus {
  isSyncing: boolean;
  lastSyncedAt: string | null;
  error: Error | null;
}

const LEGACY_PROGRESS_KEY = 'oop-journey-progress';
const SYNC_STATUS_KEY = 'oop-journey-sync-status';
const SYNC_INTERVAL_MS = 5 * 60 * 1000; // 5 minutes

/**
 * Hook to handle progress synchronization between localStorage and server
 * Also handles migration from legacy localStorage format
 */
export function useProgressSync(isAuthenticated: boolean) {
  const [syncStatus, setSyncStatus] = useState<SyncStatus>({
    isSyncing: false,
    lastSyncedAt: null,
    error: null,
  });
  
  const syncIntervalRef = useRef<NodeJS.Timeout | null>(null);

  /**
   * Check if there's legacy localStorage progress to migrate
   */
  const checkLegacyProgress = useCallback((): LocalProgressData | null => {
    const legacy = localStorage.getItem(LEGACY_PROGRESS_KEY);
    if (!legacy) return null;

    try {
      const parsed = JSON.parse(legacy);
      return {
        completedProblems: parsed.completedProblems || [],
        lastActive: parsed.lastActive || null,
        version: 1,
      };
    } catch {
      return null;
    }
  }, []);

  /**
   * Sync local progress to server
   */
  const syncToServer = useCallback(async () => {
    if (!isAuthenticated) return;

    setSyncStatus(prev => ({ ...prev, isSyncing: true, error: null }));

    try {
      // Get current server progress
      const serverProgress = await api.progress.getAll();
      const serverSlugs = new Set(serverProgress.items.map(p => p.problemSlug));

      // Get local progress
      const localProgress = checkLegacyProgress();
      if (!localProgress) {
        setSyncStatus(prev => ({
          ...prev,
          isSyncing: false,
          lastSyncedAt: new Date().toISOString(),
        }));
        return;
      }

      // Find problems that need to be synced (not already on server)
      const problemsToSync = localProgress.completedProblems.filter(
        slug => !serverSlugs.has(slug)
      );

      // Sync each problem
      for (const problemSlug of problemsToSync) {
        try {
          await api.progress.update(problemSlug, {
            status: 'solved',
          });
        } catch (err) {
          console.error(`Failed to sync progress for ${problemSlug}:`, err);
        }
      }

      // Update sync status
      const now = new Date().toISOString();
      setSyncStatus({
        isSyncing: false,
        lastSyncedAt: now,
        error: null,
      });
      localStorage.setItem(SYNC_STATUS_KEY, JSON.stringify({ lastSyncedAt: now }));

      // Clear legacy progress after successful sync
      if (problemsToSync.length === localProgress.completedProblems.length) {
        localStorage.removeItem(LEGACY_PROGRESS_KEY);
      }

    } catch (err) {
      setSyncStatus(prev => ({
        ...prev,
        isSyncing: false,
        error: err instanceof Error ? err : new Error('Sync failed'),
      }));
    }
  }, [isAuthenticated, checkLegacyProgress]);

  /**
   * Import localStorage progress to server (manual action)
   */
  const importLocalProgress = useCallback(async (): Promise<{
    imported: number;
    failed: number;
  }> => {
    if (!isAuthenticated) return { imported: 0, failed: 0 };

    const localProgress = checkLegacyProgress();
    if (!localProgress) return { imported: 0, failed: 0 };

    let imported = 0;
    let failed = 0;

    for (const problemSlug of localProgress.completedProblems) {
      try {
        await api.progress.update(problemSlug, {
          status: 'solved',
        });
        imported++;
      } catch {
        failed++;
      }
    }

    // Clear local storage on success
    if (failed === 0) {
      localStorage.removeItem(LEGACY_PROGRESS_KEY);
    }

    return { imported, failed };
  }, [isAuthenticated, checkLegacyProgress]);

  /**
   * Check if migration is needed
   */
  const needsMigration = useCallback((): boolean => {
    if (!isAuthenticated) return false;
    const legacy = localStorage.getItem(LEGACY_PROGRESS_KEY);
    return !!legacy;
  }, [isAuthenticated]);

  /**
   * Clear all local progress data (on logout)
   */
  const clearLocalProgress = useCallback(() => {
    localStorage.removeItem(LEGACY_PROGRESS_KEY);
    localStorage.removeItem(SYNC_STATUS_KEY);
    localStorage.removeItem('oop-journey-progress-cache');
    localStorage.removeItem('oop-journey-progress-stats');
    
    // Clear draft cache
    const keysToRemove: string[] = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith('oop-journey-draft-')) {
        keysToRemove.push(key);
      }
    }
    keysToRemove.forEach(key => localStorage.removeItem(key));
  }, []);

  // Setup periodic sync when authenticated
  useEffect(() => {
    if (!isAuthenticated) {
      if (syncIntervalRef.current) {
        clearInterval(syncIntervalRef.current);
        syncIntervalRef.current = null;
      }
      return;
    }

    // Initial sync on login
    syncToServer();

    // Setup periodic sync
    syncIntervalRef.current = setInterval(syncToServer, SYNC_INTERVAL_MS);

    return () => {
      if (syncIntervalRef.current) {
        clearInterval(syncIntervalRef.current);
      }
    };
  }, [isAuthenticated, syncToServer]);

  // Load last synced at from storage
  useEffect(() => {
    const stored = localStorage.getItem(SYNC_STATUS_KEY);
    if (stored) {
      try {
        const { lastSyncedAt } = JSON.parse(stored);
        setSyncStatus(prev => ({ ...prev, lastSyncedAt }));
      } catch {
        // Ignore parse errors
      }
    }
  }, []);

  return {
    syncStatus,
    syncToServer,
    importLocalProgress,
    needsMigration,
    checkLegacyProgress,
    clearLocalProgress,
  };
}

/**
 * Hook to use WebSocket for real-time progress updates across tabs
 */
export function useProgressWebSocket(
  userId: string | null,
  onProgressUpdate?: (data: { problemSlug: string; status: string }) => void,
  onDraftUpdate?: (data: { problemSlug: string; codePreview: string }) => void
) {
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (!userId) {
      setIsConnected(false);
      return;
    }

    const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:3001';
    const ws = new WebSocket(`${WS_URL}/ws/progress?user_id=${userId}`);
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      // Subscribe to progress updates
      ws.send(JSON.stringify({ type: 'subscribe_progress' }));
    };

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        
        if (message.type === 'progress_updated' && onProgressUpdate) {
          onProgressUpdate(message.data);
        } else if (message.type === 'draft_updated' && onDraftUpdate) {
          onDraftUpdate(message.data);
        }
      } catch {
        // Ignore parse errors
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      // Attempt to reconnect after 5 seconds
      reconnectTimeoutRef.current = setTimeout(() => {
        // React will re-run the effect with the same userId
      }, 5000);
    };

    ws.onerror = () => {
      setIsConnected(false);
    };

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      ws.close();
    };
  }, [userId, onProgressUpdate, onDraftUpdate]);

  const sendProgressUpdate = useCallback((problemSlug: string, status: string) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'progress_update',
        data: { problem_slug: problemSlug, status }
      }));
    }
  }, []);

  const sendDraftUpdate = useCallback((problemSlug: string, code: string) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'draft_update',
        data: { problem_slug: problemSlug, code }
      }));
    }
  }, []);

  return {
    isConnected,
    sendProgressUpdate,
    sendDraftUpdate,
  };
}
