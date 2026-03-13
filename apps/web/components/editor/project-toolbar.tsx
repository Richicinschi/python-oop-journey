"use client";

import { useState } from "react";
import { 
  Save, 
  Play, 
  Download, 
  Upload, 
  RotateCcw, 
  Columns, 
  MoreVertical,
  Check,
  Loader2,
  FolderOpen,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import type { ProjectFile } from "@/types/project-files";

export interface ProjectToolbarProps {
  /** Whether there are unsaved changes */
  hasUnsavedChanges?: boolean;
  /** Number of modified files */
  modifiedCount?: number;
  /** Whether currently running/saving */
  isRunning?: boolean;
  /** Whether split view is enabled */
  isSplitEnabled?: boolean;
  /** Callback to save all files */
  onSaveAll?: () => void;
  /** Callback to run the project */
  onRun?: () => void;
  /** Callback to download as ZIP */
  onDownloadZip?: () => void;
  /** Callback to import project */
  onImport?: () => void;
  /** Callback to reset project */
  onReset?: () => void;
  /** Callback to toggle split view */
  onToggleSplit?: () => void;
  /** Additional className */
  className?: string;
}

export function ProjectToolbar({
  hasUnsavedChanges = false,
  modifiedCount = 0,
  isRunning = false,
  isSplitEnabled = false,
  onSaveAll,
  onRun,
  onDownloadZip,
  onImport,
  onReset,
  onToggleSplit,
  className,
}: ProjectToolbarProps) {
  const [showSaveSuccess, setShowSaveSuccess] = useState(false);

  const handleSaveAll = () => {
    onSaveAll?.();
    setShowSaveSuccess(true);
    setTimeout(() => setShowSaveSuccess(false), 2000);
  };

  return (
    <TooltipProvider delayDuration={300}>
      <div className={cn(
        "flex items-center justify-between px-3 py-2 border-b bg-muted/30",
        className
      )}>
        {/* Left: Primary Actions */}
        <div className="flex items-center gap-2">
          {/* Save All */}
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                variant={hasUnsavedChanges ? "default" : "outline"}
                size="sm"
                onClick={handleSaveAll}
                disabled={!hasUnsavedChanges || isRunning}
                className={cn(
                  "gap-2",
                  hasUnsavedChanges && "bg-amber-600 hover:bg-amber-700"
                )}
              >
                {showSaveSuccess ? (
                  <Check className="h-4 w-4" />
                ) : (
                  <Save className="h-4 w-4" />
                )}
                <span className="hidden sm:inline">
                  {showSaveSuccess ? "Saved!" : "Save All"}
                </span>
                {modifiedCount > 0 && (
                  <span className="ml-1 text-xs bg-background/20 px-1.5 py-0.5 rounded-full">
                    {modifiedCount}
                  </span>
                )}
              </Button>
            </TooltipTrigger>
            <TooltipContent>
              <p>Save all files (Ctrl+S)</p>
            </TooltipContent>
          </Tooltip>

          {/* Run */}
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                variant="default"
                size="sm"
                onClick={onRun}
                disabled={isRunning}
                className="gap-2 bg-green-600 hover:bg-green-700"
              >
                {isRunning ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Play className="h-4 w-4" />
                )}
                <span className="hidden sm:inline">
                  {isRunning ? "Running..." : "Run"}
                </span>
              </Button>
            </TooltipTrigger>
            <TooltipContent>
              <p>Run project (Ctrl+Enter)</p>
            </TooltipContent>
          </Tooltip>
        </div>

        {/* Right: Secondary Actions */}
        <div className="flex items-center gap-1">
          {/* Split View Toggle */}
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                variant={isSplitEnabled ? "secondary" : "ghost"}
                size="icon"
                onClick={onToggleSplit}
                className={cn(
                  "h-8 w-8",
                  isSplitEnabled && "bg-primary/20 text-primary"
                )}
              >
                <Columns className="h-4 w-4" />
              </Button>
            </TooltipTrigger>
            <TooltipContent>
              <p>Toggle split view</p>
            </TooltipContent>
          </Tooltip>

          {/* More Actions Dropdown */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <MoreVertical className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={onDownloadZip}>
                <Download className="mr-2 h-4 w-4" />
                Download as ZIP
              </DropdownMenuItem>
              
              <DropdownMenuItem onClick={onImport}>
                <Upload className="mr-2 h-4 w-4" />
                Import Project
              </DropdownMenuItem>

              <DropdownMenuSeparator />

              <DropdownMenuItem onClick={onReset} className="text-destructive">
                <RotateCcw className="mr-2 h-4 w-4" />
                Reset to Template
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </TooltipProvider>
  );
}

export default ProjectToolbar;
