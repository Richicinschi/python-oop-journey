"use client";

import { useState, useRef, useCallback } from "react";
import { 
  ChevronRight, 
  ChevronDown, 
  File, 
  Folder, 
  FolderOpen,
  FileCode,
  FileJson,
  FileText,
  Image,
  Database,
  Settings,
  Terminal,
  FileType,
  Circle,
} from "lucide-react";
import { cn } from "@/lib/utils";
import type { ProjectFile, ProjectFolder, ProjectItem } from "@/types/project-files";
import { isProjectFile, isProjectFolder, getFileIconType } from "@/types/project-files";

export interface FileTreeItemProps {
  item: ProjectItem;
  level?: number;
  isActive?: boolean;
  onSelect?: (item: ProjectItem) => void;
  onToggleExpand?: (folder: ProjectFolder) => void;
  onContextMenu?: (e: React.MouseEvent, item: ProjectItem) => void;
  onDragStart?: (e: React.DragEvent, item: ProjectItem) => void;
  onDragOver?: (e: React.DragEvent, item: ProjectItem) => void;
  onDragLeave?: (e: React.DragEvent, item: ProjectItem) => void;
  onDrop?: (e: React.DragEvent, targetItem: ProjectItem) => void;
  isDragOver?: boolean;
}

export function FileTreeItem({
  item,
  level = 0,
  isActive = false,
  onSelect,
  onToggleExpand,
  onContextMenu,
  onDragStart,
  onDragOver,
  onDragLeave,
  onDrop,
  isDragOver = false,
}: FileTreeItemProps) {
  const isFile = isProjectFile(item);
  const isFolder = isProjectFolder(item);
  const [isDragging, setIsDragging] = useState(false);
  const dragCounter = useRef(0);

  const handleClick = useCallback(() => {
    if (isFolder) {
      onToggleExpand?.(item);
    } else {
      onSelect?.(item);
    }
  }, [isFolder, item, onSelect, onToggleExpand]);

  const handleContextMenu = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    onContextMenu?.(e, item);
  }, [item, onContextMenu]);

  const handleDragStart = useCallback((e: React.DragEvent) => {
    setIsDragging(true);
    e.dataTransfer.effectAllowed = "move";
    e.dataTransfer.setData("application/json", JSON.stringify({ id: item.id ?? '', type: isFile ? "file" : "folder" }));
    onDragStart?.(e, item);
  }, [item, isFile, onDragStart]);

  const handleDragEnd = useCallback(() => {
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
    
    // Only folders can be drop targets
    if (!isFolder) return;
    
    dragCounter.current++;
    onDragOver?.(e, item);
  }, [isFolder, item, onDragOver]);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    dragCounter.current--;
    if (dragCounter.current === 0) {
      onDragLeave?.(e, item);
    }
  }, [item, onDragLeave]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter.current = 0;
    
    if (!isFolder) return;
    
    onDrop?.(e, item);
  }, [isFolder, item, onDrop]);

  const icon = isFolder ? (
    item.isExpanded ? (
      <FolderOpen className="h-4 w-4 text-blue-500" />
    ) : (
      <Folder className="h-4 w-4 text-blue-500" />
    )
  ) : (
    getFileIcon(item.name ?? 'unnamed')
  );

  return (
    <div
      className={cn(
        "group flex items-center gap-1 px-2 py-1 text-sm cursor-pointer select-none",
        "hover:bg-accent hover:text-accent-foreground",
        "transition-colors duration-100",
        isActive && "bg-accent text-accent-foreground",
        isDragging && "opacity-50",
        isDragOver && isFolder && "bg-blue-100 dark:bg-blue-900/30 border-2 border-dashed border-blue-400",
        level > 0 && "ml-4"
      )}
      style={{ paddingLeft: `${level * 12 + 8}px` }}
      onClick={handleClick}
      onContextMenu={handleContextMenu}
      draggable
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      data-item-id={item.id}
      data-item-type={isFile ? "file" : "folder"}
    >
      {/* Expand/Collapse Indicator */}
      <span className="w-4 h-4 flex items-center justify-center flex-shrink-0">
        {isFolder && item.children.length > 0 && (
          item.isExpanded ? (
            <ChevronDown className="h-3 w-3 text-muted-foreground" />
          ) : (
            <ChevronRight className="h-3 w-3 text-muted-foreground" />
          )
        )}
      </span>

      {/* Icon */}
      <span className="flex-shrink-0">{icon}</span>

      {/* Name */}
      <span className={cn(
        "flex-1 truncate min-w-0",
        isFile && (item as ProjectFile).isModified && "italic"
      )}>
        {item.name ?? 'unnamed'}
      </span>

      {/* Modified Indicator */}
      {isFile && (item as ProjectFile).isModified && (
        <Circle className="h-2 w-2 fill-current text-amber-500 flex-shrink-0" />
      )}
    </div>
  );
}

function getFileIcon(filename: string) {
  const iconType = getFileIconType(filename);
  const className = "h-4 w-4";

  switch (iconType) {
    case "python":
      return <FileCode className={cn(className, "text-yellow-500")} />;
    case "javascript":
      return <FileCode className={cn(className, "text-yellow-400")} />;
    case "typescript":
      return <FileCode className={cn(className, "text-blue-500")} />;
    case "html":
      return <FileCode className={cn(className, "text-orange-500")} />;
    case "css":
      return <FileCode className={cn(className, "text-blue-400")} />;
    case "json":
      return <FileJson className={cn(className, "text-green-500")} />;
    case "markdown":
      return <FileText className={cn(className, "text-gray-500")} />;
    case "yaml":
      return <FileText className={cn(className, "text-red-400")} />;
    case "image":
      return <Image className={cn(className, "text-purple-500")} />;
    case "database":
      return <Database className={cn(className, "text-cyan-500")} />;
    case "settings":
      return <Settings className={cn(className, "text-gray-400")} />;
    case "terminal":
      return <Terminal className={cn(className, "text-green-400")} />;
    default:
      return <File className={cn(className, "text-gray-400")} />;
  }
}

export default FileTreeItem;
