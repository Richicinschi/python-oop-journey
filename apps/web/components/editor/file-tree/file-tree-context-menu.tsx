"use client";

import { useCallback } from "react";
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuSeparator,
  ContextMenuTrigger,
} from "@/components/ui/context-menu";
import {
  FilePlus,
  FolderPlus,
  Edit,
  Trash2,
  Copy,
  Scissors,
  ClipboardPaste,
  RefreshCw,
} from "lucide-react";
import type { ProjectItem, ProjectFile, ProjectFolder } from "@/types/project-files";
import { isProjectFile, isProjectFolder } from "@/types/project-files";

export interface FileTreeContextMenuProps {
  children: React.ReactNode;
  item?: ProjectItem;
  parentFolderId?: string;
  onNewFile?: (parentFolderId: string) => void;
  onNewFolder?: (parentFolderId: string) => void;
  onRename?: (item: ProjectItem) => void;
  onDelete?: (item: ProjectItem) => void;
  onCopy?: (item: ProjectItem) => void;
  onCut?: (item: ProjectItem) => void;
  onPaste?: (targetFolderId: string) => void;
  onRefresh?: () => void;
  canPaste?: boolean;
}

export function FileTreeContextMenu({
  children,
  item,
  parentFolderId = "root",
  onNewFile,
  onNewFolder,
  onRename,
  onDelete,
  onCopy,
  onCut,
  onPaste,
  onRefresh,
  canPaste = false,
}: FileTreeContextMenuProps) {
  const isFolder = item ? isProjectFolder(item) : true;
  const folderId = item ? (isFolder ? (item.id ?? parentFolderId ?? "root") : (parentFolderId ?? "root")) : "root";

  const handleNewFile = useCallback(() => {
    onNewFile?.(folderId);
  }, [folderId, onNewFile]);

  const handleNewFolder = useCallback(() => {
    onNewFolder?.(folderId);
  }, [folderId, onNewFolder]);

  const handleRename = useCallback(() => {
    if (item) onRename?.(item);
  }, [item, onRename]);

  const handleDelete = useCallback(() => {
    if (item) onDelete?.(item);
  }, [item, onDelete]);

  const handleCopy = useCallback(() => {
    if (item) onCopy?.(item);
  }, [item, onCopy]);

  const handleCut = useCallback(() => {
    if (item) onCut?.(item);
  }, [item, onCut]);

  const handlePaste = useCallback(() => {
    if (isFolder) {
      onPaste?.(item?.id || "root");
    }
  }, [isFolder, item, onPaste]);

  return (
    <ContextMenu>
      <ContextMenuTrigger asChild>{children}</ContextMenuTrigger>
      <ContextMenuContent className="w-48">
        {/* New File/Folder - Always available */}
        <ContextMenuItem onClick={handleNewFile}>
          <FilePlus className="mr-2 h-4 w-4" />
          New File
        </ContextMenuItem>
        <ContextMenuItem onClick={handleNewFolder}>
          <FolderPlus className="mr-2 h-4 w-4" />
          New Folder
        </ContextMenuItem>

        {item && (
          <>
            <ContextMenuSeparator />

            {/* File/Folder Operations */}
            <ContextMenuItem onClick={handleRename}>
              <Edit className="mr-2 h-4 w-4" />
              Rename
            </ContextMenuItem>

            <ContextMenuItem onClick={handleDelete} className="text-destructive focus:text-destructive">
              <Trash2 className="mr-2 h-4 w-4" />
              Delete
            </ContextMenuItem>

            <ContextMenuSeparator />

            {/* Clipboard Operations */}
            <ContextMenuItem onClick={handleCopy}>
              <Copy className="mr-2 h-4 w-4" />
              Copy
            </ContextMenuItem>

            <ContextMenuItem onClick={handleCut}>
              <Scissors className="mr-2 h-4 w-4" />
              Cut
            </ContextMenuItem>

            {isFolder && (
              <ContextMenuItem onClick={handlePaste} disabled={!canPaste}>
                <ClipboardPaste className="mr-2 h-4 w-4" />
                Paste
              </ContextMenuItem>
            )}
          </>
        )}

        <ContextMenuSeparator />

        {/* Refresh */}
        <ContextMenuItem onClick={onRefresh}>
          <RefreshCw className="mr-2 h-4 w-4" />
          Refresh
        </ContextMenuItem>
      </ContextMenuContent>
    </ContextMenu>
  );
}

export default FileTreeContextMenu;
