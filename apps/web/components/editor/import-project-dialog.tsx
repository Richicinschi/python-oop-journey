"use client";

import { useState, useCallback, useRef } from "react";
import { Upload, FileArchive, AlertCircle, Check, X } from "lucide-react";
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
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Progress } from "@/components/ui/progress";

export interface ImportProjectDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onImport: (file: File) => Promise<boolean>;
}

type ImportState = "idle" | "reading" | "processing" | "success" | "error";

export function ImportProjectDialog({
  isOpen,
  onClose,
  onImport,
}: ImportProjectDialogProps) {
  const [importState, setImportState] = useState<ImportState>("idle");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const dragCounter = useRef(0);
  const [isDragging, setIsDragging] = useState(false);

  const resetState = useCallback(() => {
    setImportState("idle");
    setSelectedFile(null);
    setProgress(0);
    setError(null);
    setIsDragging(false);
    dragCounter.current = 0;
  }, []);

  const handleClose = useCallback(() => {
    if (importState === "processing" || importState === "reading") return;
    resetState();
    onClose();
  }, [importState, resetState, onClose]);

  const validateFile = (file: File): string | null => {
    // Check file type
    const validTypes = [
      "application/zip",
      "application/x-zip-compressed",
      "application/x-zip",
      "multipart/x-zip",
    ];
    
    if (!validTypes.includes(file.type) && !file.name.endsWith(".zip")) {
      return "Please select a valid ZIP file";
    }
    
    // Check file size (max 50MB)
    const maxSize = 50 * 1024 * 1024;
    if (file.size > maxSize) {
      return "File size must be less than 50MB";
    }
    
    return null;
  };

  const handleFileSelect = useCallback((file: File) => {
    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      setImportState("error");
      return;
    }
    
    setSelectedFile(file);
    setError(null);
    setImportState("idle");
  }, []);

  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  }, [handleFileSelect]);

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter.current++;
    if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
      setIsDragging(true);
    }
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter.current--;
    if (dragCounter.current === 0) {
      setIsDragging(false);
    }
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    dragCounter.current = 0;
    
    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  }, [handleFileSelect]);

  const handleImport = useCallback(async () => {
    if (!selectedFile) return;
    
    setImportState("reading");
    setProgress(25);
    
    // Simulate reading delay for UX
    await new Promise(resolve => setTimeout(resolve, 300));
    
    setImportState("processing");
    setProgress(50);
    
    try {
      const success = await onImport(selectedFile);
      
      if (success) {
        setProgress(100);
        setImportState("success");
        setTimeout(() => {
          handleClose();
        }, 1500);
      } else {
        setError("Failed to import project. The ZIP file may be corrupted or contain unsupported files.");
        setImportState("error");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unexpected error occurred");
      setImportState("error");
    }
  }, [selectedFile, onImport, handleClose]);

  const handleBrowseClick = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  const handleClearFile = useCallback(() => {
    setSelectedFile(null);
    setError(null);
    setImportState("idle");
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  }, []);

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && handleClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <FileArchive className="h-5 w-5" />
            Import Project
          </DialogTitle>
          <DialogDescription>
            Import a project from a ZIP file. This will replace your current project.
          </DialogDescription>
        </DialogHeader>

        <div className="py-4">
          {/* Hidden file input */}
          <input
            ref={fileInputRef}
            type="file"
            accept=".zip,application/zip,application/x-zip-compressed"
            onChange={handleInputChange}
            className="hidden"
          />

          {/* Drop zone */}
          {!selectedFile && importState !== "success" && (
            <div
              onClick={handleBrowseClick}
              onDragEnter={handleDragEnter}
              onDragLeave={handleDragLeave}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              className={cn(
                "relative border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors",
                isDragging
                  ? "border-primary bg-primary/5"
                  : "border-muted-foreground/25 hover:border-muted-foreground/50"
              )}
            >
              <Upload className={cn(
                "mx-auto h-12 w-12 mb-4 transition-colors",
                isDragging ? "text-primary" : "text-muted-foreground"
              )} />
              <p className="text-sm font-medium">
                {isDragging ? "Drop ZIP file here" : "Drag and drop a ZIP file"}
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                or click to browse
              </p>
              <p className="text-xs text-muted-foreground mt-2">
                Maximum file size: 50MB
              </p>
            </div>
          )}

          {/* Selected file */}
          {selectedFile && importState !== "success" && (
            <div className="space-y-4">
              <div className="flex items-center gap-3 p-3 bg-muted rounded-lg">
                <FileArchive className="h-8 w-8 text-blue-500" />
                <div className="flex-1 min-w-0">
                  <p className="font-medium truncate">{selectedFile.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
                {importState === "idle" && (
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={handleClearFile}
                    className="h-8 w-8"
                  >
                    <X className="h-4 w-4" />
                  </Button>
                )}
              </div>

              {/* Progress */}
              {(importState === "reading" || importState === "processing") && (
                <div className="space-y-2">
                  <Progress value={progress} className="h-2" />
                  <p className="text-sm text-center text-muted-foreground">
                    {importState === "reading" ? "Reading file..." : "Processing..."}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Success state */}
          {importState === "success" && (
            <div className="text-center py-8">
              <div className="mx-auto w-12 h-12 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center mb-4">
                <Check className="h-6 w-6 text-green-600 dark:text-green-400" />
              </div>
              <p className="font-medium">Project imported successfully!</p>
              <p className="text-sm text-muted-foreground mt-1">
                Closing dialog...
              </p>
            </div>
          )}

          {/* Error state */}
          {error && (
            <Alert variant="destructive" className="mt-4">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </div>

        <DialogFooter>
          <Button 
            variant="outline" 
            onClick={handleClose}
            disabled={importState === "reading" || importState === "processing"}
          >
            Cancel
          </Button>
          <Button
            onClick={handleImport}
            disabled={!selectedFile || importState !== "idle"}
          >
            Import Project
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default ImportProjectDialog;
