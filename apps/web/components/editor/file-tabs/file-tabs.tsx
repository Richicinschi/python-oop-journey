"use client";

import { useState, useRef, useCallback } from "react";
import { X, GripVertical, ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import type { ProjectFile } from "@/types/project-files";
import { getFileIconType } from "@/types/project-files";
import {
  File,
  FileCode,
  FileJson,
  FileText,
  Image,
  Database,
  Settings,
  Terminal,
  Circle,
} from "lucide-react";

export interface FileTab {
  file: ProjectFile;
  isActive: boolean;
  isModified: boolean;
}

export interface FileTabsProps {
  tabs: FileTab[];
  onSelect: (fileId: string) => void;
  onClose: (fileId: string) => void;
  onCloseAll: () => void;
  onCloseOthers: (fileId: string) => void;
  onReorder?: (newOrder: string[]) => void;
  className?: string;
}

export function FileTabs({
  tabs,
  onSelect,
  onClose,
  onCloseAll,
  onCloseOthers,
  onReorder,
  className,
}: FileTabsProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [draggedTab, setDraggedTab] = useState<string | null>(null);
  const [dragOverTab, setDragOverTab] = useState<string | null>(null);

  const handleMouseWheel = useCallback((e: React.WheelEvent) => {
    if (scrollRef.current) {
      scrollRef.current.scrollLeft += e.deltaY;
    }
  }, []);

  const handleDragStart = useCallback((e: React.DragEvent, fileId: string) => {
    setDraggedTab(fileId);
    e.dataTransfer.effectAllowed = "move";
    e.dataTransfer.setData("text/plain", fileId);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent, fileId: string) => {
    e.preventDefault();
    if (fileId !== draggedTab) {
      setDragOverTab(fileId);
    }
  }, [draggedTab]);

  const handleDragLeave = useCallback(() => {
    setDragOverTab(null);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent, targetFileId: string) => {
    e.preventDefault();
    const sourceFileId = e.dataTransfer.getData("text/plain");
    
    if (sourceFileId && sourceFileId !== targetFileId && onReorder) {
      const newOrder = tabs.map(t => t.file.id).filter((id): id is string => id !== undefined);
      const sourceIndex = newOrder.indexOf(sourceFileId);
      const targetIndex = newOrder.indexOf(targetFileId);
      
      if (sourceIndex !== -1 && targetIndex !== -1) {
        newOrder.splice(sourceIndex, 1);
        newOrder.splice(targetIndex, 0, sourceFileId);
        onReorder(newOrder);
      }
    }
    
    setDraggedTab(null);
    setDragOverTab(null);
  }, [tabs, onReorder]);

  const handleDragEnd = useCallback(() => {
    setDraggedTab(null);
    setDragOverTab(null);
  }, []);

  if (tabs.length === 0) {
    return (
      <div className={cn(
        "flex items-center justify-center h-9 border-b bg-muted/30 text-muted-foreground text-sm",
        className
      )}>
        No files open
      </div>
    );
  }

  return (
    <div className={cn("relative flex items-center border-b bg-muted/30", className)}>
      {/* Scrollable Tab Container */}
      <div
        ref={scrollRef}
        className="flex-1 flex overflow-x-auto scrollbar-hide"
        onWheel={handleMouseWheel}
      >
        {tabs.filter((tab): tab is FileTab & { file: ProjectFile & { id: string } } => !!tab.file.id).map((tab) => (
          <TabItem
            key={tab.file.id}
            tab={tab}
            isDragged={tab.file.id === draggedTab}
            isDragOver={tab.file.id === dragOverTab}
            onSelect={() => onSelect(tab.file.id)}
            onClose={(e) => {
              e.stopPropagation();
              onClose(tab.file.id);
            }}
            onCloseOthers={() => onCloseOthers(tab.file.id)}
            onDragStart={(e) => handleDragStart(e, tab.file.id)}
            onDragOver={(e) => handleDragOver(e, tab.file.id)}
            onDragLeave={handleDragLeave}
            onDrop={(e) => handleDrop(e, tab.file.id)}
            onDragEnd={handleDragEnd}
          />
        ))}
      </div>

      {/* Tab Actions Dropdown */}
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            size="sm"
            className="h-9 px-2 border-l rounded-none"
          >
            <ChevronDown className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuItem onClick={onCloseAll}>
            Close All
          </DropdownMenuItem>
          <DropdownMenuItem onClick={() => tabs.find(t => t.isActive) && onCloseOthers(tabs.find(t => t.isActive)!.file.id)}>
            Close Others
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}

interface TabItemProps {
  tab: FileTab;
  isDragged: boolean;
  isDragOver: boolean;
  onSelect: () => void;
  onClose: (e: React.MouseEvent) => void;
  onCloseOthers: () => void;
  onDragStart: (e: React.DragEvent) => void;
  onDragOver: (e: React.DragEvent) => void;
  onDragLeave: () => void;
  onDrop: (e: React.DragEvent) => void;
  onDragEnd: () => void;
}

function TabItem({
  tab,
  isDragged,
  isDragOver,
  onSelect,
  onClose,
  onCloseOthers,
  onDragStart,
  onDragOver,
  onDragLeave,
  onDrop,
  onDragEnd,
}: TabItemProps) {
  const Icon = getTabIcon(tab.file.name);

  return (
    <TooltipProvider delayDuration={500}>
      <Tooltip>
        <TooltipTrigger asChild>
          <div
            className={cn(
              "group relative flex items-center gap-2 px-3 py-2 min-w-[120px] max-w-[200px] h-9",
              "border-r border-border cursor-pointer select-none",
              "transition-colors duration-100",
              tab.isActive
                ? "bg-background text-foreground border-t-2 border-t-primary"
                : "bg-muted/50 text-muted-foreground hover:bg-muted hover:text-foreground",
              isDragged && "opacity-50",
              isDragOver && "bg-accent"
            )}
            onClick={onSelect}
            draggable
            onDragStart={onDragStart}
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            onDragEnd={onDragEnd}
          >
            {/* Drag Handle */}
            <GripVertical className="h-3 w-3 text-muted-foreground opacity-0 group-hover:opacity-50 cursor-grab" />

            {/* File Icon */}
            <Icon className="h-4 w-4 flex-shrink-0" />

            {/* Filename */}
            <span className={cn(
              "flex-1 truncate text-sm",
              tab.isModified && "italic"
            )}>
              {tab.file.name}
            </span>

            {/* Modified Indicator */}
            {tab.isModified && (
              <Circle className="h-2 w-2 fill-current text-amber-500 flex-shrink-0" />
            )}

            {/* Close Button */}
            <button
              className={cn(
                "flex-shrink-0 p-0.5 rounded-sm",
                "text-muted-foreground hover:text-foreground hover:bg-accent",
                "opacity-0 group-hover:opacity-100 transition-opacity",
                tab.isModified && "opacity-100"
              )}
              onClick={onClose}
              title="Close"
            >
              <X className="h-3 w-3" />
            </button>
          </div>
        </TooltipTrigger>
        <TooltipContent side="bottom">
          <p>{tab.file.path || tab.file.name}</p>
          {tab.isModified && <p className="text-amber-500">Modified</p>}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}

function getTabIcon(filename: string) {
  const iconType = getFileIconType(filename);

  switch (iconType) {
    case "python":
      return (props: any) => <FileCode {...props} className={cn(props.className, "text-yellow-500")} />;
    case "javascript":
      return (props: any) => <FileCode {...props} className={cn(props.className, "text-yellow-400")} />;
    case "typescript":
      return (props: any) => <FileCode {...props} className={cn(props.className, "text-blue-500")} />;
    case "html":
      return (props: any) => <FileCode {...props} className={cn(props.className, "text-orange-500")} />;
    case "css":
      return (props: any) => <FileCode {...props} className={cn(props.className, "text-blue-400")} />;
    case "json":
      return (props: any) => <FileJson {...props} className={cn(props.className, "text-green-500")} />;
    case "markdown":
      return (props: any) => <FileText {...props} className={cn(props.className, "text-gray-500")} />;
    case "image":
      return (props: any) => <Image {...props} className={cn(props.className, "text-purple-500")} />;
    case "database":
      return (props: any) => <Database {...props} className={cn(props.className, "text-cyan-500")} />;
    case "settings":
      return (props: any) => <Settings {...props} className={cn(props.className, "text-gray-400")} />;
    case "terminal":
      return (props: any) => <Terminal {...props} className={cn(props.className, "text-green-400")} />;
    default:
      return (props: any) => <File {...props} className={cn(props.className, "text-gray-400")} />;
  }
}

export default FileTabs;
