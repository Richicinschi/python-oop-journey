'use client';

/**
 * Online/Offline Status Hook
 * 
 * Detects navigator.onLine and listens to online/offline events
 * Shows toast notification when going offline/online
 */

import { useState, useEffect, useCallback } from 'react';

export type ConnectionStatus = 'online' | 'offline' | 'unknown';

export interface OnlineStatusState {
  isOnline: boolean;
  status: ConnectionStatus;
  wasOffline: boolean;
  lastChangedAt: Date | null;
}

interface UseOnlineStatusOptions {
  onStatusChange?: (status: ConnectionStatus) => void;
  onGoOffline?: () => void;
  onGoOnline?: () => void;
}

export function useOnlineStatus(options: UseOnlineStatusOptions = {}): OnlineStatusState {
  const [state, setState] = useState<OnlineStatusState>({
    isOnline: true,
    status: 'unknown',
    wasOffline: false,
    lastChangedAt: null,
  });

  const handleOnline = useCallback(() => {
    setState((prev) => {
      const wasOffline = prev.status === 'offline';
      
      // Notify callbacks
      options.onStatusChange?.('online');
      if (wasOffline) {
        options.onGoOnline?.();
      }
      
      return {
        isOnline: true,
        status: 'online',
        wasOffline,
        lastChangedAt: new Date(),
      };
    });
  }, [options]);

  const handleOffline = useCallback(() => {
    setState((prev) => {
      // Notify callbacks
      options.onStatusChange?.('offline');
      options.onGoOffline?.();
      
      return {
        isOnline: false,
        status: 'offline',
        wasOffline: false,
        lastChangedAt: new Date(),
      };
    });
  }, [options]);

  useEffect(() => {
    // Check initial status
    const isOnline = typeof navigator !== 'undefined' ? navigator.onLine : true;
    setState({
      isOnline,
      status: isOnline ? 'online' : 'offline',
      wasOffline: false,
      lastChangedAt: new Date(),
    });

    // Add event listeners
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [handleOnline, handleOffline]);

  return state;
}

/**
 * Hook that returns just the online status boolean
 */
export function useIsOnline(): boolean {
  const [isOnline, setIsOnline] = useState<boolean>(true);

  useEffect(() => {
    setIsOnline(navigator.onLine);

    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return isOnline;
}

/**
 * Hook for showing toast notifications on connection changes
 */
export function useConnectionToast(): OnlineStatusState {
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'warning' } | null>(null);

  const handleGoOffline = useCallback(() => {
    setToast({ message: 'You are offline. Changes will sync when you reconnect.', type: 'warning' });
  }, []);

  const handleGoOnline = useCallback(() => {
    setToast({ message: 'Back online! Syncing your changes...', type: 'success' });
  }, []);

  const status = useOnlineStatus({
    onGoOffline: handleGoOffline,
    onGoOnline: handleGoOnline,
  });

  // Expose toast via a global or context if needed
  // For now, we just return the status
  return status;
}

export default useOnlineStatus;
