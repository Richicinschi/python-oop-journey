'use client';

import { useState, useCallback, useMemo } from 'react';
import { ProjectFile } from '@/types/project';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  ChevronRight, 
  ChevronDown, 
  FileCode, 
  Folder, 
  FolderOpen,
  Plus,
  Trash2,
  FilePlus,
  FolderPlus,
  FileText,
  MoreVertical,
  Save,
  Circle
} from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { cn } from '@/lib/utils';

interface FileTreeProps {
  files: ProjectFile[];
  activeFileId: string | null;
  onFileSelect: (fileId: string) => void;
  onFileCreate?: (name: string) => void;
  onFileDelete?: (fileId: string) => void;
  onFileSave?: (fileId: string) => void;
  className?: string;
  isLoading?: boolean;
}

interface FileNode {
  id: string;
  name: string;
  type: 'file' | 'folder';
  file?: ProjectFile;
  children: FileNode[];
  isExpanded?: boolean;
}

// File icon based on extension
function FileIcon({ name, isModified }: { name: string; isModified?: boolean }) {
  const extension = name.split('.').pop()?.toLowerCase();
  
  let Icon = FileCode;
  if (extension === 'md' || extension === 'txt') Icon = FileText;
  else if (extension === 'py') Icon = FileCode;
  
  return (
    <div className="relative">
      <Icon className="h-4 w-4" />
      {isModified && (
        <Circle className="h-2 w-2 fill-current absolute -top-0.5 -right-0.5" />
      )}
    </div>
  );
}

export function FileTree({
  files,
  activeFileId,
  onFileSelect,
  onFileCreate,
  onFileDelete,
  onFileSave,
  className,
  isLoading,
}: FileTreeProps) {
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set(['root']));
  const [isCreating, setIsCreating] = useState(false);
  const [newFileName, setNewFileName] = useState('');

  // Build tree structure from flat files array
  const fileTree = useMemo(() => {
    const root: FileNode = { id: 'root', name: 'project', type: 'folder', children: [] };
    
    files.forEach(file => {
      const parts = file.path.split('/').filter(Boolean);
      let current = root;
      
      parts.forEach((part, index) => {
        const isFile = index === parts.length - 1;
        const existingNode = current.children.find(child => child.name === part);
        
        if (existingNode) {
          current = existingNode;
        } else {
          const newNode: FileNode = {
            id: isFile ? file.id : `${current.id}/${part}`,
            name: part,
            type: isFile ? 'file' : 'folder',
            file: isFile ? file : undefined,
            children: [],
          };
          current.children.push(newNode);
          current.children.sort((a, b) => {
            // Folders first, then alphabetical
            if (a.type !== b.type) return a.type === 'folder' ? -1 : 1;
            return a.name.localeCompare(b.name);
          });
          current = newNode;
        }
      });
    });
    
    return root;
  }, [files]);

  const toggleFolder = useCallback((nodeId: string) => {
    setExpandedFolders(prev => {
      const next = new Set(prev);
      if (next.has(nodeId)) {
        next.delete(nodeId);
      } else {
        next.add(nodeId);
      }
      return next;
    });
  }, []);

  const handleCreateFile = useCallback(() => {
    if (newFileName.trim() && onFileCreate) {
      onFileCreate(newFileName.trim());
      setNewFileName('');
      setIsCreating(false);
    }
  }, [newFileName, onFileCreate]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleCreateFile();
    } else if (e.key === 'Escape') {
      setIsCreating(false);
      setNewFileName('');
    }
  }, [handleCreateFile]);

  // Recursive file tree item component
  const FileTreeItem = ({ node, depth = 0 }: { node: FileNode; depth?: number }) => {
    const isExpanded = expandedFolders.has(node.id);
    const isActive = node.type === 'file' && node.file?.id === activeFileId;

    if (node.type === 'folder') {
      return (
        <div>
          <button
            onClick={() => toggleFolder(node.id)}
            className={cn(
              'w-full flex items-center gap-2 px-2 py-1.5 text-sm rounded-md transition-colors',
              'hover:bg-accent hover:text-accent-foreground',
              'focus:outline-none focus:ring-1 focus:ring-ring'
            )}
            style={{ paddingLeft: `${depth * 12 + 8}px` }}
            aria-expanded={isExpanded}
          >
            {isExpanded ? (
              <ChevronDown className="h-3.5 w-3.5 shrink-0" />
            ) : (
              <ChevronRight className="h-3.5 w-3.5 shrink-0" />
            )}
            {isExpanded ? (
              <FolderOpen className="h-4 w-4 shrink-0 text-primary" />
            ) : (
              <Folder className="h-4 w-4 shrink-0 text-primary" />
            )}
            <span className="truncate">{node.name}</span>
          </button>
          
          {isExpanded && (
            <div role="group" aria-label={`${node.name} contents`}>
              {node.children.map(child => (
                <FileTreeItem key={child.id} node={child} depth={depth + 1} />
              ))}
            </div>
          )}
        </div>
      );
    }

    return (
      <button
        onClick={() => node.file && onFileSelect(node.file.id)}
        className={cn(
          'w-full flex items-center gap-2 px-2 py-1.5 text-sm rounded-md transition-colors group',
          'hover:bg-accent hover:text-accent-foreground',
          'focus:outline-none focus:ring-1 focus:ring-ring',
          isActive && 'bg-accent text-accent-foreground'
        )}
        style={{ paddingLeft: `${depth * 12 + 24}px` }}
        role="treeitem"
        aria-selected={isActive}
        aria-label={`${node.name}${node.file?.isModified ? ' (modified)' : ''}`}
      >
        <FileIcon 
          name={node.name} 
          isModified={node.file?.isModified} 
        />
        <span className="truncate flex-1 text-left">{node.name}</span>
        
        {/* File actions dropdown */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              size="icon"
              className="h-6 w-6 opacity-0 group-hover:opacity-100 focus:opacity-100"
              onClick={(e) => e.stopPropagation()}
            >
              <MoreVertical className="h-3 w-3" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            {node.file?.isModified && onFileSave && (
              <DropdownMenuItem onClick={() => node.file && onFileSave(node.file.id)}>
                <Save className="h-4 w-4 mr-2" />
                Save
              </DropdownMenuItem>
            )}
            {onFileDelete && (
              <>
                <DropdownMenuSeparator />
                <DropdownMenuItem 
                  onClick={() => node.file && onFileDelete(node.file.id)}
                  className="text-destructive"
                >
                  <Trash2 className="h-4 w-4 mr-2" />
                  Delete
                </DropdownMenuItem>
              </>
            )}
          </DropdownMenuContent>
        </DropdownMenu>
      </button>
    );
  };

  return (
    <div 
      className={cn('flex flex-col h-full bg-card', className)}
      data-tour="file-tree"
      role="tree"
      aria-label="Project files"
    >
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b">
        <span className="text-sm font-medium">Explorer</span>
        <div className="flex items-center gap-1">
          {onFileCreate && (
            <Button
              variant="ghost"
              size="icon"
              className="h-7 w-7"
              onClick={() => setIsCreating(true)}
              title="New File"
            >
              <FilePlus className="h-4 w-4" />
            </Button>
          )}
        </div>
      </div>

      {/* New file input */}
      {isCreating && (
        <div className="px-3 py-2 border-b">
          <div className="flex items-center gap-2">
            <FileCode className="h-4 w-4 shrink-0" />
            <Input
              value={newFileName}
              onChange={(e) => setNewFileName(e.target.value)}
              onKeyDown={handleKeyDown}
              onBlur={handleCreateFile}
              placeholder="filename.py"
              className="h-7 text-sm"
              autoFocus
            />
          </div>
        </div>
      )}

      {/* File tree */}
      <ScrollArea className="flex-1">
        <div className="p-1">
          {fileTree.children.map(node => (
            <FileTreeItem key={node.id} node={node} />
          ))}
          
          {files.length === 0 && !isCreating && (
            <div className="text-center py-8 text-muted-foreground">
              <p className="text-sm mb-2">No files yet</p>
              {onFileCreate && (
                <Button 
                  variant="outline" 
                  size="sm" 
                  onClick={() => setIsCreating(true)}
                >
                  <Plus className="h-4 w-4 mr-1" />
                  Create File
                </Button>
              )}
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}

// Simplified file list for mobile or compact views
export function FileList({
  files,
  activeFileId,
  onFileSelect,
  className,
}: Omit<FileTreeProps, 'onFileCreate' | 'onFileDelete' | 'onFileSave' | 'isLoading'>) {
  return (
    <div className={cn('space-y-1', className)}>
      {files.map(file => (
        <button
          key={file.id}
          onClick={() => onFileSelect(file.id)}
          className={cn(
            'w-full flex items-center gap-2 px-3 py-2 text-sm rounded-md transition-colors',
            'hover:bg-accent hover:text-accent-foreground',
            activeFileId === file.id && 'bg-accent text-accent-foreground'
          )}
        >
          <FileIcon name={file.name} isModified={file.isModified} />
          <span className="truncate flex-1 text-left">{file.name}</span>
          {file.isModified && (
            <Circle className="h-2 w-2 fill-current" />
          )}
        </button>
      ))}
    </div>
  );
}

// File tree skeleton for loading state
export function FileTreeSkeleton() {
  return (
    <div className="p-3 space-y-2">
      <div className="flex items-center gap-2">
        <div className="h-4 w-4 rounded bg-muted animate-pulse" />
        <div className="h-4 w-24 rounded bg-muted animate-pulse" />
      </div>
      <div className="ml-4 space-y-2">
        <div className="flex items-center gap-2">
          <div className="h-4 w-4 rounded bg-muted animate-pulse" />
          <div className="h-4 w-32 rounded bg-muted animate-pulse" />
        </div>
        <div className="flex items-center gap-2">
          <div className="h-4 w-4 rounded bg-muted animate-pulse" />
          <div className="h-4 w-28 rounded bg-muted animate-pulse" />
        </div>
      </div>
    </div>
  );
}
