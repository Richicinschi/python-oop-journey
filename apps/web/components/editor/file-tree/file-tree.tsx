"use client";

import { useState, useCallback, useMemo } from "react";
import { FolderTree } from "lucide-react";
import { cn } from "@/lib/utils";
import { ScrollArea } from "@/components/ui/scroll-area";
import type { ProjectFile, ProjectFolder, ProjectItem } from "@/types/project-files";
import { isProjectFile, isProjectFolder } from "@/types/project-files";
import { FileTreeItem } from "./file-tree-item";
import { FileTreeContextMenu } from "./file-tree-context-menu";

export interface FileTreeProps {
  root: ProjectFolder;
  activeFileId?: string | null;
  onSelectFile?: (file: ProjectFile) => void;
  onToggleFolder?: (folder: ProjectFolder) => void;
  onNewFile?: (parentFolderId: string) => void;
  onNewFolder?: (parentFolderId: string) => void;
  onRename?: (item: ProjectItem) => void;
  onDelete?: (item: ProjectItem) => void;
  onMove?: (itemId: string, targetFolderId: string) => void;
  className?: string;
}

export function FileTree({
  root,
  activeFileId,
  onSelectFile,
  onToggleFolder,
  onNewFile,
  onNewFolder,
  onRename,
  onDelete,
  onMove,
  className,
}: FileTreeProps) {
  const [dragState, setDragState] = useState<{
    draggingId: string | null;
    dragOverId: string | null;
  }>({ draggingId: null, dragOverId: null });

  // Build flat list with parent info for context menus
  const flatItems = useMemo(() => {
    const items: Array<{ 
      item: ProjectItem; 
      level: number;
      parentId: string;
    }> = [];
    
    function traverse(folder: ProjectFolder, level: number, parentId: string) {
      // Sort: folders first, then alphabetically
      const sorted = [...folder.children].sort((a, b) => {
        const aIsFolder = isProjectFolder(a);
        const bIsFolder = isProjectFolder(b);
        if (aIsFolder !== bIsFolder) return aIsFolder ? -1 : 1;
        return (a.name ?? '').localeCompare(b.name ?? '');
      });
      
      for (const child of sorted) {
        items.push({ item: child, level, parentId });
        if (isProjectFolder(child) && child.isExpanded) {
          if (child.id) traverse(child, level + 1, child.id);
        }
      }
    }
    
    traverse(root, 0, "root");
    return items;
  }, [root]);

  const handleSelect = useCallback((item: ProjectItem) => {
    if (isProjectFile(item)) {
      onSelectFile?.(item);
    }
  }, [onSelectFile]);

  const handleToggleExpand = useCallback((folder: ProjectFolder) => {
    onToggleFolder?.(folder);
  }, [onToggleFolder]);

  const handleContextMenu = useCallback((e: React.MouseEvent, item: ProjectItem) => {
    e.preventDefault();
  }, []);

  const handleDragStart = useCallback((e: React.DragEvent, item: ProjectItem) => {
    setDragState(prev => ({ ...prev, draggingId: item.id ?? null }));
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent, item: ProjectItem) => {
    if (isProjectFolder(item) && item.id !== dragState.draggingId) {
      setDragState(prev => ({ ...prev, dragOverId: item.id ?? null }));
    }
  }, [dragState.draggingId]);

  const handleDragLeave = useCallback((e: React.DragEvent, item: ProjectItem) => {
    setDragState(prev => ({ ...prev, dragOverId: null }));
  }, []);

  const handleDrop = useCallback((e: React.DragEvent, targetItem: ProjectItem) => {
    e.preventDefault();
    
    try {
      const data = JSON.parse(e.dataTransfer.getData("application/json"));
      const sourceId = data.id;
      
      if (sourceId && isProjectFolder(targetItem) && sourceId !== targetItem.id) {
        onMove?.(sourceId, targetItem.id);
      }
    } catch {
      // Invalid drop data
    }
    
    setDragState({ draggingId: null, dragOverId: null });
  }, [onMove]);

  return (
    <div className={cn("flex flex-col h-full bg-background border-r", className)}>
      {/* Header */}
      <FileTreeContextMenu
        onNewFile={onNewFile}
        onNewFolder={onNewFolder}
        onRefresh={() => {}}
      >
        <div className="flex items-center justify-between px-3 py-2 border-b bg-muted/50 cursor-context-menu">
          <div className="flex items-center gap-2">
            <FolderTree className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm font-medium">Explorer</span>
          </div>
          <span className="text-xs text-muted-foreground truncate max-w-[100px]">
            {root.name ?? 'Project'}
          </span>
        </div>
      </FileTreeContextMenu>

      {/* Tree */}
      <ScrollArea className="flex-1">
        <div className="py-1">
          {flatItems.length === 0 ? (
            <FileTreeContextMenu
              onNewFile={onNewFile}
              onNewFolder={onNewFolder}
              onRefresh={() => {}}
            >
              <div className="px-4 py-8 text-center cursor-context-menu">
                <p className="text-sm text-muted-foreground">
                  No files yet
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  Right-click to create new file
                </p>
              </div>
            </FileTreeContextMenu>
          ) : (
            flatItems.map(({ item, level, parentId }) => (
              <FileTreeContextMenu
                key={item.id}
                item={item}
                parentFolderId={parentId}
                onNewFile={onNewFile}
                onNewFolder={onNewFolder}
                onRename={onRename}
                onDelete={onDelete}
                onRefresh={() => {}}
              >
                <div className="cursor-context-menu">
                  <FileTreeItem
                    item={item}
                    level={level}
                    isActive={item.id === activeFileId}
                    onSelect={handleSelect}
                    onToggleExpand={handleToggleExpand}
                    onContextMenu={handleContextMenu}
                    onDragStart={handleDragStart}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    isDragOver={item.id === dragState.dragOverId}
                  />
                </div>
              </FileTreeContextMenu>
            ))
          )}
        </div>
      </ScrollArea>
    </div>
  );
}

export default FileTree;
