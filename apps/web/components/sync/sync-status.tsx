'use client';

/**
 * Sync Status Component
 * 
 * Small indicator in header showing:
 * - States: Synced, Syncing, Offline, Conflict
 * - Tooltip with pending operations count
 * - Click to view sync queue
 */

import { useState, useEffect } from 'react';
import { 
  Cloud, 
  CloudOff, 
  RefreshCw, 
  AlertCircle, 
  CheckCircle2,
  WifiOff,
} from 'lucide-react';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { 
  getSyncState, 
  subscribeToSyncEvents, 
  SyncState as SyncEngineState,
  syncPendingOperations,
} from '@/lib/sync-engine';
import { useOnlineStatus } from '@/hooks/use-online-status';
import { SyncQueue } from './sync-queue';

export type SyncStatusType = 'synced' | 'syncing' | 'offline' | 'conflict' | 'error';

interface SyncStatusProps {
  className?: string;
  showLabel?: boolean;
}

export function SyncStatus({ className, showLabel = false }: SyncStatusProps) {
  const [syncState, setSyncState] = useState<SyncEngineState>(getSyncState());
  const [isQueueOpen, setIsQueueOpen] = useState(false);
  const { isOnline } = useOnlineStatus();

  useEffect(() => {
    // Subscribe to sync events
    const unsubscribe = subscribeToSyncEvents((newState) => {
      setSyncState(newState);
    });

    return unsubscribe;
  }, []);

  const getStatusConfig = (): {
    icon: React.ReactNode;
    label: string;
    description: string;
    color: string;
    animate?: boolean;
  } => {
    if (!isOnline) {
      return {
        icon: <WifiOff className="h-4 w-4" />,
        label: 'Offline',
        description: `${syncState.pendingCount} changes queued for sync`,
        color: 'text-amber-500',
      };
    }

    switch (syncState.status) {
      case 'syncing':
        return {
          icon: <RefreshCw className="h-4 w-4" />,
          label: 'Syncing...',
          description: 'Syncing your changes...',
          color: 'text-blue-500',
          animate: true,
        };
      
      case 'error':
        return {
          icon: <AlertCircle className="h-4 w-4" />,
          label: 'Sync Error',
          description: syncState.lastError || 'Sync failed. Click to retry.',
          color: 'text-red-500',
        };
      
      case 'conflict':
        return {
          icon: <CloudOff className="h-4 w-4" />,
          label: 'Conflict',
          description: 'Data conflict detected. Review required.',
          color: 'text-orange-500',
        };
      
      default:
        if (syncState.pendingCount > 0) {
          return {
            icon: <Cloud className="h-4 w-4" />,
            label: 'Pending',
            description: `${syncState.pendingCount} changes pending`,
            color: 'text-yellow-500',
          };
        }
        
        return {
          icon: <CheckCircle2 className="h-4 w-4" />,
          label: 'Synced',
          description: syncState.lastSyncAt 
            ? `Last synced ${formatTime(syncState.lastSyncAt)}`
            : 'All changes saved',
          color: 'text-green-500',
        };
    }
  };

  const handleClick = async () => {
    if (syncState.status === 'error' || syncState.pendingCount > 0) {
      if (isOnline) {
        await syncPendingOperations();
      }
    }
    setIsQueueOpen(true);
  };

  const config = getStatusConfig();

  return (
    <>
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant="ghost"
              size={showLabel ? 'default' : 'icon'}
              className={cn(
                'relative gap-2',
                config.color,
                className
              )}
              onClick={handleClick}
            >
              <span className={cn(config.animate && 'animate-spin')}>  
                {config.icon}
              </span>
              {showLabel && (
                <span className="text-sm font-medium">{config.label}</span>
              )}
              {syncState.pendingCount > 0 && !showLabel && (
                <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-primary text-[10px] font-medium text-primary-foreground">
                  {syncState.pendingCount > 9 ? '9+' : syncState.pendingCount}
                </span>
              )}
            </Button>
          </TooltipTrigger>
          <TooltipContent side="bottom" align="end">
            <div className="flex flex-col gap-1">
              <p className="font-medium">{config.label}</p>
              <p className="text-xs text-muted-foreground">{config.description}</p>
              {syncState.pendingCount > 0 && (
                <p className="text-xs text-muted-foreground">
                  Click to view queue
                </p>
              )}
            </div>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>

      <SyncQueue 
        isOpen={isQueueOpen} 
        onClose={() => setIsQueueOpen(false)} 
      />
    </>
  );
}

function formatTime(timestamp: number): string {
  const date = new Date(timestamp);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString();
}

export default SyncStatus;
