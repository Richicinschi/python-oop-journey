'use client';

/**
 * Sync Queue Component
 * 
 * Shows:
 * - List pending operations
 * - Show retry count
 * - Manual retry button
 * - Cancel operation button
 */

import { useState, useEffect, useCallback } from 'react';
import { 
  X, 
  RotateCcw, 
  Trash2, 
  Code, 
  BookOpen, 
  Bookmark,
  AlertCircle,
  CheckCircle2,
  Clock,
  WifiOff,
} from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import {
  getPendingOperations,
  removeOperation,
  updateOperation,
  SyncOperation,
  OperationType,
  clearAllOperations,
} from '@/lib/offline-db';
import {
  syncPendingOperations,
  getSyncState,
  subscribeToSyncEvents,
} from '@/lib/sync-engine';
import { useOnlineStatus } from '@/hooks/use-online-status';

interface SyncQueueProps {
  isOpen: boolean;
  onClose: () => void;
}

export function SyncQueue({ isOpen, onClose }: SyncQueueProps) {
  const [operations, setOperations] = useState<SyncOperation[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const { isOnline } = useOnlineStatus();

  const loadOperations = useCallback(async () => {
    const ops = await getPendingOperations();
    setOperations(ops);
  }, []);

  useEffect(() => {
    if (isOpen) {
      loadOperations();
    }
  }, [isOpen, loadOperations]);

  useEffect(() => {
    const unsubscribe = subscribeToSyncEvents((state) => {
      setIsSyncing(state.status === 'syncing');
      if (state.status === 'idle' || state.status === 'error') {
        loadOperations();
      }
    });

    return unsubscribe;
  }, [loadOperations]);

  const handleRetry = async (operationId: string) => {
    setIsLoading(true);
    try {
      await updateOperation(operationId, { retryCount: 0, lastError: undefined });
      if (isOnline) {
        await syncPendingOperations();
      }
      await loadOperations();
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetryAll = async () => {
    setIsLoading(true);
    try {
      if (isOnline) {
        await syncPendingOperations();
      }
      await loadOperations();
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = async (operationId: string) => {
    setIsLoading(true);
    try {
      await removeOperation(operationId);
      await loadOperations();
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearAll = async () => {
    setIsLoading(true);
    try {
      await clearAllOperations();
      await loadOperations();
    } finally {
      setIsLoading(false);
    }
  };

  const getOperationIcon = (type: OperationType) => {
    switch (type) {
      case 'progress':
        return <BookOpen className="h-4 w-4" />;
      case 'draft':
        return <Code className="h-4 w-4" />;
      case 'bookmark':
        return <Bookmark className="h-4 w-4" />;
      default:
        return <Clock className="h-4 w-4" />;
    }
  };

  const getOperationLabel = (type: OperationType, action: string) => {
    const typeLabel = {
      progress: 'Progress',
      draft: 'Draft',
      bookmark: 'Bookmark',
    }[type];

    const actionLabel = {
      create: 'Create',
      update: 'Update',
      delete: 'Delete',
    }[action] || action;

    return `${actionLabel} ${typeLabel}`;
  };

  const getOperationDetails = (operation: SyncOperation): string => {
    const data = operation.data as Record<string, unknown>;
    
    if (data.problemSlug) {
      return `Problem: ${data.problemSlug}`;
    }
    if (data.weekSlug) {
      return `Week: ${data.weekSlug}`;
    }
    
    return JSON.stringify(data).slice(0, 50) + '...';
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[80vh] flex flex-col">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            Sync Queue
            {operations.length > 0 && (
              <Badge variant="secondary">{operations.length} pending</Badge>
            )}
          </DialogTitle>
          <DialogDescription>
            {isOnline 
              ? 'Pending operations will sync automatically when possible.'
              : 'You are offline. Changes will sync when you reconnect.'}
          </DialogDescription>
        </DialogHeader>

        {!isOnline && (
          <div className="flex items-center gap-2 p-3 rounded-md bg-amber-50 text-amber-700 text-sm">
            <WifiOff className="h-4 w-4" />
            <span>You are currently offline</span>
          </div>
        )}

        <div className="flex items-center justify-between py-2">
          <div className="flex items-center gap-2">
            <Button
              size="sm"
              onClick={handleRetryAll}
              disabled={isLoading || isSyncing || !isOnline || operations.length === 0}
            >
              <RotateCcw className={cn('h-4 w-4 mr-2', isSyncing && 'animate-spin')} />
              Sync Now
            </Button>
          </div>
          {operations.length > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={handleClearAll}
              disabled={isLoading}
            >
              <Trash2 className="h-4 w-4 mr-2" />
              Clear All
            </Button>
          )}
        </div>

        <ScrollArea className="flex-1 -mx-6 px-6">
          {operations.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <CheckCircle2 className="h-12 w-12 text-green-500 mb-4" />
              <h3 className="text-lg font-medium">All caught up!</h3>
              <p className="text-sm text-muted-foreground">
                No pending operations in the queue.
              </p>
            </div>
          ) : (
            <div className="space-y-2">
              {operations.map((operation) => (
                <div
                  key={operation.id}
                  className={cn(
                    'flex items-start gap-3 p-3 rounded-lg border',
                    operation.retryCount > 0 && 'border-amber-200 bg-amber-50/50',
                    operation.lastError && 'border-red-200 bg-red-50/50'
                  )}
                >
                  <div className="flex-shrink-0 mt-0.5">
                    {getOperationIcon(operation.type)}
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-sm">
                        {getOperationLabel(operation.type, operation.action)}
                      </span>
                      {operation.retryCount > 0 && (
                        <Badge variant="outline" className="text-xs">
                          Retry {operation.retryCount}
                        </Badge>
                      )}
                    </div>
                    
                    <p className="text-xs text-muted-foreground truncate">
                      {getOperationDetails(operation)}
                    </p>
                    
                    {operation.lastError && (
                      <div className="flex items-center gap-1 mt-1 text-xs text-red-600">
                        <AlertCircle className="h-3 w-3" />
                        <span className="truncate">{operation.lastError}</span>
                      </div>
                    )}
                    
                    <p className="text-xs text-muted-foreground mt-1">
                      {new Date(operation.timestamp).toLocaleString()}
                    </p>
                  </div>

                  <div className="flex items-center gap-1">
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8"
                      onClick={() => handleRetry(operation.id)}
                      disabled={isLoading || !isOnline}
                      title="Retry"
                    >
                      <RotateCcw className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8 text-destructive hover:text-destructive"
                      onClick={() => handleCancel(operation.id)}
                      disabled={isLoading}
                      title="Cancel"
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}

export default SyncQueue;
