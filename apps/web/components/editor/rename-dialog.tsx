"use client";

import { useState, useEffect, useCallback } from "react";
import { FileEdit, FolderEdit } from "lucide-react";
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
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type { ProjectItem } from "@/types/project-files";
import { isProjectFile } from "@/types/project-files";

export interface RenameDialogProps {
  isOpen: boolean;
  onClose: () => void;
  item: ProjectItem | null;
  onRename: (newName: string) => void;
}

export function RenameDialog({
  isOpen,
  onClose,
  item,
  onRename,
}: RenameDialogProps) {
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);
  
  const isFile = item ? isProjectFile(item) : false;
  const originalName = item?.name || "";
  
  // Reset and set initial name when dialog opens
  useEffect(() => {
    if (isOpen && item) {
      setName(item.name ?? '');
      setError(null);
      
      // Select name without extension for files
      setTimeout(() => {
        const input = document.getElementById("rename-input") as HTMLInputElement;
        if (input) {
          input.focus();
          if (isFile) {
            const dotIndex = (item.name ?? '').lastIndexOf(".");
            if (dotIndex > 0) {
              input.setSelectionRange(0, dotIndex);
            } else {
              input.select();
            }
          } else {
            input.select();
          }
        }
      }, 100);
    }
  }, [isOpen, item, isFile]);

  const validateName = useCallback((value: string): string | null => {
    const trimmed = value.trim();
    
    if (!trimmed) {
      return "Name cannot be empty";
    }
    
    if (trimmed === originalName) {
      return "New name must be different from current name";
    }
    
    // Check for invalid characters
    if (/[<>:"|?*]/.test(trimmed)) {
      return "Name contains invalid characters: <>:\"|?*";
    }
    
    // Check for slashes
    if (trimmed.includes("/") || trimmed.includes("\\")) {
      return "Name cannot contain slashes";
    }
    
    // Check for leading/trailing dots or spaces
    if (trimmed !== value || trimmed.startsWith(".") || trimmed.endsWith(".")) {
      return "Name cannot start or end with spaces or dots";
    }
    
    return null;
  }, [originalName]);

  const handleSubmit = useCallback((e?: React.FormEvent) => {
    e?.preventDefault();
    
    const validationError = validateName(name);
    if (validationError) {
      setError(validationError);
      return;
    }
    
    onRename(name.trim());
    onClose();
  }, [name, validateName, onRename, onClose]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSubmit();
    } else if (e.key === "Escape") {
      onClose();
    }
  }, [handleSubmit, onClose]);

  if (!item) return null;

  const Icon = isFile ? FileEdit : FolderEdit;

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-[400px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Icon className="h-5 w-5" />
            Rename {isFile ? "File" : "Folder"}
          </DialogTitle>
          <DialogDescription>
            Enter a new name for "{originalName}"
          </DialogDescription>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="rename-input">New Name</Label>
            <Input
              id="rename-input"
              value={name}
              onChange={(e) => {
                setName(e.target.value);
                setError(null);
              }}
              onKeyDown={handleKeyDown}
              placeholder={originalName}
              className={cn(error && "border-destructive")}
            />
            {error ? (
              <p className="text-sm text-destructive">{error}</p>
            ) : (
              <p className="text-xs text-muted-foreground">
                {isFile 
                  ? "Include the file extension (e.g., .py, .js)" 
                  : "Folder names cannot contain special characters"}
              </p>
            )}
          </div>

          {/* Preview */}
          {name.trim() && name.trim() !== originalName && !error && (
            <div className="text-sm">
              <span className="text-muted-foreground">Will be renamed to: </span>
              <span className="font-medium text-foreground">{name.trim()}</span>
            </div>
          )}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button 
            onClick={() => handleSubmit()}
            disabled={!name.trim() || name.trim() === originalName || !!error}
          >
            Rename
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default RenameDialog;
