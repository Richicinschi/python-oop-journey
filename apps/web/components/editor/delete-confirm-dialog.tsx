"use client";

import { useState, useCallback } from "react";
import { Trash2, AlertTriangle, FileX, FolderX } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import type { ProjectItem, ProjectFolder } from "@/types/project-files";
import { isProjectFile, isProjectFolder } from "@/types/project-files";

export interface DeleteConfirmDialogProps {
  isOpen: boolean;
  onClose: () => void;
  item: ProjectItem | null;
  onConfirm: () => void;
}

export function DeleteConfirmDialog({
  isOpen,
  onClose,
  item,
  onConfirm,
}: DeleteConfirmDialogProps) {
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleConfirm = useCallback(async () => {
    setIsDeleting(true);
    try {
      await onConfirm();
    } finally {
      setIsDeleting(false);
      setConfirmDelete(false);
      onClose();
    }
  }, [onConfirm, onClose]);

  const handleClose = useCallback(() => {
    if (!isDeleting) {
      setConfirmDelete(false);
      onClose();
    }
  }, [isDeleting, onClose]);

  if (!item) return null;

  const isFile = isProjectFile(item);
  const isFolder = isProjectFolder(item);
  
  // Calculate contents for folders
  let fileCount = 0;
  let folderCount = 0;
  
  if (isFolder) {
    const countItems = (folder: ProjectFolder) => {
      for (const child of folder.children) {
        if (isProjectFile(child)) {
          fileCount++;
        } else {
          folderCount++;
          countItems(child);
        }
      }
    };
    countItems(item);
  }

  const hasContents = isFolder && (fileCount > 0 || folderCount > 0);
  const Icon = isFile ? FileX : FolderX;

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && handleClose()}>
      <DialogContent className="sm:max-w-[450px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-destructive">
            <AlertTriangle className="h-5 w-5" />
            Delete {isFile ? "File" : "Folder"}
          </DialogTitle>
          <DialogDescription>
            This action cannot be undone. This will permanently delete:
          </DialogDescription>
        </DialogHeader>

        <div className="py-4">
          {/* Item to delete */}
          <div className="flex items-center gap-3 p-3 bg-muted rounded-lg">
            <Icon className="h-8 w-8 text-muted-foreground" />
            <div className="flex-1 min-w-0">
              <p className="font-medium truncate">{item.name}</p>
              <p className="text-sm text-muted-foreground truncate">
                {item.path || "Root"}
              </p>
            </div>
          </div>

          {/* Folder contents warning */}
          {hasContents && (
            <div className="mt-4 p-3 bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900 rounded-lg">
              <p className="text-sm font-medium text-amber-800 dark:text-amber-200">
                This folder contains:
              </p>
              <ul className="mt-2 text-sm text-amber-700 dark:text-amber-300 space-y-1">
                {fileCount > 0 && (
                  <li>• {fileCount} file{fileCount !== 1 ? "s" : ""}</li>
                )}
                {folderCount > 0 && (
                  <li>• {folderCount} subfolder{folderCount !== 1 ? "s" : ""}</li>
                )}
              </ul>
              <p className="mt-2 text-sm text-amber-800 dark:text-amber-200">
                All contents will be permanently deleted.
              </p>
            </div>
          )}

          {/* Modified file warning */}
          {isFile && (item as ReturnType<typeof isProjectFile>).isModified && (
            <div className="mt-4 p-3 bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-900 rounded-lg">
              <p className="text-sm font-medium text-red-800 dark:text-red-200 flex items-center gap-2">
                <AlertTriangle className="h-4 w-4" />
                Unsaved Changes
              </p>
              <p className="mt-1 text-sm text-red-700 dark:text-red-300">
                This file has unsaved changes that will be lost.
              </p>
            </div>
          )}

          {/* Confirmation checkbox */}
          <div className="mt-4 flex items-center space-x-2">
            <Checkbox
              id="confirm-delete"
              checked={confirmDelete}
              onCheckedChange={(checked) => setConfirmDelete(checked as boolean)}
            />
            <Label 
              htmlFor="confirm-delete" 
              className="text-sm font-medium cursor-pointer"
            >
              I understand that this action cannot be undone
            </Label>
          </div>
        </div>

        <DialogFooter>
          <Button 
            variant="outline" 
            onClick={handleClose}
            disabled={isDeleting}
          >
            Cancel
          </Button>
          <Button
            variant="destructive"
            onClick={handleConfirm}
            disabled={!confirmDelete || isDeleting}
            className="gap-2"
          >
            {isDeleting ? (
              <>
                <div className="h-4 w-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                Deleting...
              </>
            ) : (
              <>
                <Trash2 className="h-4 w-4" />
                Delete {isFile ? "File" : "Folder"}
              </>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default DeleteConfirmDialog;
