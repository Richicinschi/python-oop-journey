"use client";

import { useRef, useCallback, useState, useEffect } from "react";
import { ChevronLeft, ChevronRight, ArrowLeftRight, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { CodeEditor } from "./code-editor";
import type { ProjectFile } from "@/types/project-files";
import type { editor } from "monaco-editor";

export interface SplitEditorProps {
  /** Primary file (left/top pane) */
  primaryFile: ProjectFile | null;
  /** Secondary file (right/bottom pane) */
  secondaryFile?: ProjectFile | null;
  /** Whether split view is enabled */
  isSplitEnabled?: boolean;
  /** Split direction */
  splitDirection?: "horizontal" | "vertical";
  /** Initial split ratio (0.2 - 0.8) */
  splitRatio?: number;
  /** Callback when primary file content changes */
  onPrimaryChange?: (content: string) => void;
  /** Callback when secondary file content changes */
  onSecondaryChange?: (content: string) => void;
  /** Callback when split is toggled */
  onToggleSplit?: () => void;
  /** Callback when split ratio changes */
  onSplitRatioChange?: (ratio: number) => void;
  /** Callback to swap panes */
  onSwapPanes?: () => void;
  /** Callback to close secondary pane */
  onCloseSecondary?: () => void;
  /** Callback when editor mounts */
  onEditorMount?: (editor: editor.IStandaloneCodeEditor, isPrimary: boolean) => void;
  /** Editor height */
  height?: string;
  /** Additional className */
  className?: string;
  /** Read-only mode */
  readOnly?: boolean;
}

export function SplitEditor({
  primaryFile,
  secondaryFile,
  isSplitEnabled = false,
  splitDirection = "vertical",
  splitRatio = 0.5,
  onPrimaryChange,
  onSecondaryChange,
  onToggleSplit,
  onSplitRatioChange,
  onSwapPanes,
  onCloseSecondary,
  onEditorMount,
  height = "100%",
  className,
  readOnly = false,
}: SplitEditorProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isResizing, setIsResizing] = useState(false);
  const [localRatio, setLocalRatio] = useState(splitRatio);

  // Update local ratio when prop changes
  useEffect(() => {
    setLocalRatio(splitRatio);
  }, [splitRatio]);

  // Handle resize start
  const handleResizeStart = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    setIsResizing(true);
  }, []);

  // Handle resize
  useEffect(() => {
    if (!isResizing) return;

    const handleMouseMove = (e: MouseEvent) => {
      if (!containerRef.current) return;
      
      const rect = containerRef.current.getBoundingClientRect();
      let newRatio: number;
      
      if (splitDirection === "vertical") {
        newRatio = (e.clientX - rect.left) / rect.width;
      } else {
        newRatio = (e.clientY - rect.top) / rect.height;
      }
      
      // Clamp ratio between 0.2 and 0.8
      newRatio = Math.max(0.2, Math.min(0.8, newRatio));
      setLocalRatio(newRatio);
    };

    const handleMouseUp = () => {
      setIsResizing(false);
      onSplitRatioChange?.(localRatio);
    };

    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);
    document.body.style.cursor = splitDirection === "vertical" ? "col-resize" : "row-resize";
    document.body.style.userSelect = "none";

    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
      document.body.style.cursor = "";
      document.body.style.userSelect = "";
    };
  }, [isResizing, splitDirection, localRatio, onSplitRatioChange]);

  // Handle primary editor mount
  const handlePrimaryMount = useCallback((editor: editor.IStandaloneCodeEditor) => {
    onEditorMount?.(editor, true);
  }, [onEditorMount]);

  // Handle secondary editor mount
  const handleSecondaryMount = useCallback((editor: editor.IStandaloneCodeEditor) => {
    onEditorMount?.(editor, false);
  }, [onEditorMount]);

  // Calculate sizes based on split state
  const getPrimarySize = () => {
    if (!isSplitEnabled || !secondaryFile) return "100%";
    return `${localRatio * 100}%`;
  };

  const getSecondarySize = () => {
    if (!isSplitEnabled || !secondaryFile) return "0%";
    return `${(1 - localRatio) * 100}%`;
  };

  return (
    <div
      ref={containerRef}
      className={cn(
        "relative flex overflow-hidden bg-background",
        splitDirection === "vertical" ? "flex-row" : "flex-col",
        className
      )}
      style={{ height }}
    >
      {/* Primary Pane */}
      <div
        className="relative overflow-hidden"
        style={{ 
          width: splitDirection === "vertical" ? getPrimarySize() : "100%",
          height: splitDirection === "horizontal" ? getPrimarySize() : "100%",
        }}
      >
        {primaryFile ? (
          <div className="h-full flex flex-col">
            {/* Pane Header */}
            <div className="flex items-center justify-between px-3 py-1.5 bg-muted/50 border-b text-xs">
              <span className="font-medium truncate">{primaryFile.name}</span>
              <div className="flex items-center gap-1">
                {onToggleSplit && (
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-5 w-5"
                    onClick={onToggleSplit}
                    title={isSplitEnabled ? "Disable split view" : "Enable split view"}
                  >
                    <ArrowLeftRight className="h-3 w-3" />
                  </Button>
                )}
              </div>
            </div>
            
            {/* Editor */}
            <div className="flex-1 overflow-hidden">
              <CodeEditor
                value={primaryFile.content}
                onChange={(value) => value !== undefined && onPrimaryChange?.(value)}
                onMount={handlePrimaryMount}
                language={primaryFile.language}
                readOnly={readOnly || primaryFile.isReadOnly}
                height="100%"
                className="border-0 rounded-none"
              />
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            <p>Select a file to edit</p>
          </div>
        )}
      </div>

      {/* Resize Handle */}
      {isSplitEnabled && secondaryFile && (
        <div
          className={cn(
            "relative flex items-center justify-center bg-border hover:bg-primary/20 transition-colors z-10",
            splitDirection === "vertical" 
              ? "w-1 cursor-col-resize" 
              : "h-1 cursor-row-resize"
          )}
          onMouseDown={handleResizeStart}
        >
          <div className={cn(
            "bg-muted-foreground/50 rounded-full",
            splitDirection === "vertical" ? "w-0.5 h-8" : "h-0.5 w-8"
          )} />
        </div>
      )}

      {/* Secondary Pane */}
      {isSplitEnabled && secondaryFile && (
        <div
          className="relative overflow-hidden"
          style={{ 
            width: splitDirection === "vertical" ? getSecondarySize() : "100%",
            height: splitDirection === "horizontal" ? getSecondarySize() : "100%",
          }}
        >
          <div className="h-full flex flex-col">
            {/* Pane Header */}
            <div className="flex items-center justify-between px-3 py-1.5 bg-muted/50 border-b text-xs">
              <span className="font-medium truncate">{secondaryFile.name}</span>
              <div className="flex items-center gap-1">
                {onSwapPanes && (
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-5 w-5"
                    onClick={onSwapPanes}
                    title="Swap panes"
                  >
                    <ArrowLeftRight className="h-3 w-3" />
                  </Button>
                )}
                {onCloseSecondary && (
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-5 w-5"
                    onClick={onCloseSecondary}
                    title="Close"
                  >
                    <X className="h-3 w-3" />
                  </Button>
                )}
              </div>
            </div>
            
            {/* Editor */}
            <div className="flex-1 overflow-hidden">
              <CodeEditor
                value={secondaryFile.content}
                onChange={(value) => value !== undefined && onSecondaryChange?.(value)}
                onMount={handleSecondaryMount}
                language={secondaryFile.language}
                readOnly={readOnly || secondaryFile.isReadOnly}
                height="100%"
                className="border-0 rounded-none"
              />
            </div>
          </div>
        </div>
      )}

      {/* Empty Secondary State */}
      {isSplitEnabled && !secondaryFile && (
        <div
          className="flex items-center justify-center bg-muted/20 border-l"
          style={{ 
            width: splitDirection === "vertical" ? getSecondarySize() : "100%",
            height: splitDirection === "horizontal" ? getSecondarySize() : "100%",
          }}
        >
          <div className="text-center text-muted-foreground">
            <p className="text-sm">Select another file for split view</p>
            <p className="text-xs mt-1">Right-click a file in the explorer</p>
          </div>
        </div>
      )}

      {/* Resizing Overlay */}
      {isResizing && (
        <div className="fixed inset-0 z-50" />
      )}
    </div>
  );
}

export default SplitEditor;
