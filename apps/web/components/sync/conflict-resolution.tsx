'use client';

/**
 * Conflict Resolution Component
 * 
 * Shows:
 * - Modal when conflicts detected
 * - Local version vs Server version
 * - Options: Keep Local, Keep Server, Merge Manually
 * - Preview diff between versions
 */

import { useState, useEffect } from 'react';
import { 
  AlertTriangle, 
  ChevronDown, 
  ChevronUp,
  Monitor,
  Server,
  GitMerge,
  Check,
} from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import { resolveConflict, ConflictInfo } from '@/lib/sync-engine';
import { CodeEditor } from '@/components/editor/code-editor';

interface ConflictResolutionProps {
  conflict: ConflictInfo | null;
  isOpen: boolean;
  onClose: () => void;
}

type ResolutionStrategy = 'local' | 'server' | 'merge';

export function ConflictResolution({ 
  conflict, 
  isOpen, 
  onClose 
}: ConflictResolutionProps) {
  const [selectedStrategy, setSelectedStrategy] = useState<ResolutionStrategy>('server');
  const [mergedData, setMergedData] = useState<unknown>(null);
  const [isResolving, setIsResolving] = useState(false);

  useEffect(() => {
    if (conflict && isOpen) {
      setSelectedStrategy('server');
      setMergedData(null);
    }
  }, [conflict, isOpen]);

  const handleResolve = async () => {
    if (!conflict) return;

    setIsResolving(true);
    try {
      resolveConflict({
        operationId: conflict.operationId,
        strategy: selectedStrategy,
        mergedData: selectedStrategy === 'merge' ? mergedData : undefined,
      });
      onClose();
    } finally {
      setIsResolving(false);
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'progress':
        return 'Progress';
      case 'draft':
        return 'Code Draft';
      case 'bookmark':
        return 'Bookmark';
      default:
        return type;
    }
  };

  if (!conflict) return null;

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="max-w-4xl max-h-[90vh] flex flex-col">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-amber-500" />
            Sync Conflict Detected
          </DialogTitle>
          <DialogDescription>
            A conflict was detected for {getTypeLabel(conflict.type)}. 
            Please choose which version to keep.
          </DialogDescription>
        </DialogHeader>

        <div className="flex items-center gap-4 py-2">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>Local time:</span>
            <Badge variant="outline">
              {new Date(conflict.localTimestamp).toLocaleString()}
            </Badge>
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>Server time:</span>
            <Badge variant="outline">
              {new Date(conflict.serverTimestamp).toLocaleString()}
            </Badge>
          </div>
        </div>

        <Tabs defaultValue="diff" className="flex-1 flex flex-col">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="diff">Compare (Diff)</TabsTrigger>
            <TabsTrigger value="local">Local Version</TabsTrigger>
            <TabsTrigger value="server">Server Version</TabsTrigger>
          </TabsList>

          <TabsContent value="diff" className="flex-1 border rounded-md">
            <ScrollArea className="h-[300px]">
              <DiffView 
                local={conflict.localData} 
                server={conflict.serverData} 
              />
            </ScrollArea>
          </TabsContent>

          <TabsContent value="local" className="flex-1 border rounded-md">
            <ScrollArea className="h-[300px]">
              <div className="p-4">
                <div className="flex items-center gap-2 mb-2 text-sm font-medium text-blue-600">
                  <Monitor className="h-4 w-4" />
                  Your Local Version
                </div>
                <DataView data={conflict.localData} />
              </div>
            </ScrollArea>
          </TabsContent>

          <TabsContent value="server" className="flex-1 border rounded-md">
            <ScrollArea className="h-[300px]">
              <div className="p-4">
                <div className="flex items-center gap-2 mb-2 text-sm font-medium text-green-600">
                  <Server className="h-4 w-4" />
                  Server Version
                </div>
                <DataView data={conflict.serverData} />
              </div>
            </ScrollArea>
          </TabsContent>
        </Tabs>

        <div className="grid grid-cols-3 gap-4 py-4">
          <ResolutionOption
            title="Keep Local"
            description="Use your local version and overwrite server"
            icon={<Monitor className="h-5 w-5" />}
            selected={selectedStrategy === 'local'}
            onClick={() => setSelectedStrategy('local')}
            color="blue"
          />
          <ResolutionOption
            title="Keep Server"
            description="Use server version and discard local changes"
            icon={<Server className="h-5 w-5" />}
            selected={selectedStrategy === 'server'}
            onClick={() => setSelectedStrategy('server')}
            color="green"
          />
          <ResolutionOption
            title="Merge Manually"
            description="Combine both versions (for code only)"
            icon={<GitMerge className="h-5 w-5" />}
            selected={selectedStrategy === 'merge'}
            onClick={() => setSelectedStrategy('merge')}
            color="amber"
            disabled={conflict.type !== 'draft'}
          />
        </div>

        {selectedStrategy === 'merge' && conflict.type === 'draft' && (
          <div className="border rounded-md p-4">
            <label className="text-sm font-medium mb-2 block">
              Edit Merged Code:
            </label>
            <div className="h-[200px] border rounded-md">
              <CodeEditor
                value={String(mergedData ?? (conflict.localData as { code?: string })?.code ?? '')}
                onChange={(value) => value !== undefined && setMergedData({ code: value })}
                language="python"
              />
            </div>
          </div>
        )}

        <DialogFooter className="gap-2">
          <Button variant="outline" onClick={onClose} disabled={isResolving}>
            Decide Later
          </Button>
          <Button 
            onClick={handleResolve} 
            disabled={isResolving || (selectedStrategy === 'merge' && !mergedData)}
          >
            {isResolving ? 'Resolving...' : 'Resolve Conflict'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

interface ResolutionOptionProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  selected: boolean;
  onClick: () => void;
  color: 'blue' | 'green' | 'amber' | 'red';
  disabled?: boolean;
}

function ResolutionOption({
  title,
  description,
  icon,
  selected,
  onClick,
  color,
  disabled,
}: ResolutionOptionProps) {
  const colorClasses = {
    blue: 'border-blue-200 hover:border-blue-300 bg-blue-50/50 data-[selected=true]:border-blue-500 data-[selected=true]:bg-blue-50',
    green: 'border-green-200 hover:border-green-300 bg-green-50/50 data-[selected=true]:border-green-500 data-[selected=true]:bg-green-50',
    amber: 'border-amber-200 hover:border-amber-300 bg-amber-50/50 data-[selected=true]:border-amber-500 data-[selected=true]:bg-amber-50',
    red: 'border-red-200 hover:border-red-300 bg-red-50/50 data-[selected=true]:border-red-500 data-[selected=true]:bg-red-50',
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      data-selected={selected}
      className={cn(
        'relative flex flex-col items-center gap-2 p-4 rounded-lg border-2 transition-all text-left',
        colorClasses[color],
        disabled && 'opacity-50 cursor-not-allowed',
        selected && 'ring-2 ring-offset-2',
        color === 'blue' && selected && 'ring-blue-500',
        color === 'green' && selected && 'ring-green-500',
        color === 'amber' && selected && 'ring-amber-500',
      )}
    >
      {selected && (
        <div className="absolute top-2 right-2">
          <Check className="h-4 w-4" />
        </div>
      )}
      <div className={cn(
        'p-2 rounded-full',
        color === 'blue' && 'bg-blue-100 text-blue-600',
        color === 'green' && 'bg-green-100 text-green-600',
        color === 'amber' && 'bg-amber-100 text-amber-600',
      )}>
        {icon}
      </div>
      <div className="text-center">
        <div className="font-medium text-sm">{title}</div>
        <div className="text-xs text-muted-foreground mt-1">{description}</div>
      </div>
    </button>
  );
}

function DataView({ data }: { data: unknown }) {
  if (data === null || data === undefined) {
    return <span className="text-muted-foreground italic">No data</span>;
  }

  if (typeof data === 'string') {
    return (
      <pre className="text-sm bg-muted p-2 rounded overflow-auto">
        <code>{data}</code>
      </pre>
    );
  }

  if (typeof data === 'object') {
    return (
      <pre className="text-sm bg-muted p-2 rounded overflow-auto">
        <code>{JSON.stringify(data, null, 2)}</code>
      </pre>
    );
  }

  return <span>{String(data)}</span>;
}

function DiffView({ local, server }: { local: unknown; server: unknown }) {
  // Simple diff visualization
  const localStr = JSON.stringify(local, null, 2);
  const serverStr = JSON.stringify(server, null, 2);

  const localLines = localStr.split('\n');
  const serverLines = serverStr.split('\n');

  const maxLines = Math.max(localLines.length, serverLines.length);
  const diffLines: Array<{ type: 'same' | 'local' | 'server' | 'both'; content: string }> = [];

  for (let i = 0; i < maxLines; i++) {
    const localLine = localLines[i] || '';
    const serverLine = serverLines[i] || '';

    if (localLine === serverLine) {
      diffLines.push({ type: 'same', content: localLine });
    } else if (localLine && !serverLine) {
      diffLines.push({ type: 'local', content: localLine });
    } else if (!localLine && serverLine) {
      diffLines.push({ type: 'server', content: serverLine });
    } else {
      // Both different
      diffLines.push({ type: 'local', content: localLine });
      diffLines.push({ type: 'server', content: serverLine });
    }
  }

  return (
    <div className="grid grid-cols-2 gap-0 text-sm">
      <div className="border-r">
        <div className="sticky top-0 bg-blue-50 px-4 py-2 text-xs font-medium text-blue-700 border-b flex items-center gap-2">
          <Monitor className="h-3 w-3" />
          Your Version
        </div>
        <div className="p-4 space-y-0">
          {diffLines.map((line, i) => (
            <div
              key={i}
              className={cn(
                'font-mono text-xs py-0.5 px-1 -mx-1',
                line.type === 'local' && 'bg-blue-100 text-blue-900',
                line.type === 'same' && 'text-foreground',
                line.type === 'server' && 'text-muted-foreground'
              )}
            >
              {line.type === 'local' || line.type === 'same' ? line.content : ''}
            </div>
          ))}
        </div>
      </div>
      <div>
        <div className="sticky top-0 bg-green-50 px-4 py-2 text-xs font-medium text-green-700 border-b flex items-center gap-2">
          <Server className="h-3 w-3" />
          Server Version
        </div>
        <div className="p-4 space-y-0">
          {diffLines.map((line, i) => (
            <div
              key={i}
              className={cn(
                'font-mono text-xs py-0.5 px-1 -mx-1',
                line.type === 'server' && 'bg-green-100 text-green-900',
                line.type === 'same' && 'text-foreground',
                line.type === 'local' && 'text-muted-foreground'
              )}
            >
              {line.type === 'server' || line.type === 'same' ? line.content : ''}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ConflictResolution;
