"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Editor, { OnMount, BeforeMount, type Monaco } from "@monaco-editor/react";
import type { editor } from "monaco-editor";
import { useTheme } from "@/components/theme-provider";

import { cn } from "@/lib/utils";
import {
  configureMonacoLoader,
  initializeMonaco,
  getDefaultEditorOptions,
  DEFAULT_STARTER_CODE,
} from "@/lib/monaco";
import { EditorSkeleton } from "./editor-skeleton";

// Configure loader once on module load
configureMonacoLoader();

export interface CodeEditorProps {
  /** Current code value */
  value?: string;
  /** Called when code changes */
  onChange?: (value: string | undefined) => void;
  /** Called when editor is mounted */
  onMount?: (editor: editor.IStandaloneCodeEditor, monaco: Monaco) => void;
  /** Called before editor mounts */
  beforeMount?: BeforeMount;
  /** Editor height (default: "400px") */
  height?: string;
  /** Editor width (default: "100%") */
  width?: string;
  /** Read-only mode */
  readOnly?: boolean;
  /** Custom class name */
  className?: string;
  /** Show minimap */
  minimap?: boolean;
  /** Word wrap mode */
  wordWrap?: "on" | "off" | "wordWrapColumn" | "bounded";
  /** Font size */
  fontSize?: number;
  /** Line numbers visibility */
  lineNumbers?: "on" | "off" | "relative" | "interval";
  /** Language mode (default: "python") */
  language?: string;
  /** Additional editor options */
  options?: editor.IStandaloneEditorConstructionOptions;
  /** Callback for Ctrl+Enter to run code */
  onRun?: () => void;
}

export function CodeEditor({
  value,
  onChange,
  onMount,
  beforeMount,
  height = "400px",
  width = "100%",
  readOnly = false,
  className,
  minimap = true,
  wordWrap = "on",
  fontSize = 14,
  lineNumbers = "on",
  language = "python",
  options = {},
  onRun,
}: CodeEditorProps) {
  const { theme, systemTheme } = useTheme();
  const [isMounted, setIsMounted] = useState(false);
  const [hasError, setHasError] = useState(false);
  
  // Component refs for editor instance access
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);
  const monacoRef = useRef<Monaco | null>(null);

  // Determine effective theme
  const effectiveTheme = theme === "system" ? systemTheme : theme;
  const isDark = effectiveTheme === "dark";

  // Handle hydration - only render editor on client
  useEffect(() => {
    setIsMounted(true);
  }, []);

  // Handle editor mount
  const handleMount: OnMount = useCallback(
    (editorInstance, monacoInstance) => {
      try {
        editorRef.current = editorInstance;
        monacoRef.current = monacoInstance;
        
        // Initialize Python language support
        initializeMonaco(monacoInstance);

        // Add Ctrl+Enter keyboard shortcut
        if (onRun) {
          editorInstance.addCommand(
            monacoInstance.KeyMod.CtrlCmd | monacoInstance.KeyCode.Enter,
            () => {
              onRun();
            }
          );
        }

        // Call user's onMount callback
        onMount?.(editorInstance, monacoInstance);
      } catch (error) {
        console.error("Monaco editor mount error:", error);
        setHasError(true);
      }
    },
    [onMount, onRun]
  );

  // Handle before mount
  const handleBeforeMount: BeforeMount = useCallback(
    (monaco) => {
      try {
        initializeMonaco(monaco);
        beforeMount?.(monaco);
      } catch (error) {
        console.error("Monaco beforeMount error:", error);
      }
    },
    [beforeMount]
  );

  // Update editor options when props change
  useEffect(() => {
    if (editorRef.current) {
      editorRef.current.updateOptions({
        readOnly,
        minimap: { enabled: minimap },
        wordWrap,
        fontSize,
        lineNumbers,
      });
    }
  }, [readOnly, minimap, wordWrap, fontSize, lineNumbers]);

  // Update theme when it changes
  useEffect(() => {
    if (monacoRef.current && editorRef.current) {
      const newTheme = isDark ? "vs-code-dark" : "vs-code-light";
      monacoRef.current.editor.setTheme(newTheme);
    }
  }, [isDark]);

  // Get merged options
  const mergedOptions: editor.IStandaloneEditorConstructionOptions = {
    ...getDefaultEditorOptions(isDark, readOnly),
    minimap: { enabled: minimap },
    wordWrap,
    fontSize,
    lineNumbers,
    ...options,
  };

  // Error state
  if (hasError) {
    return (
      <div
        className={cn(
          "relative rounded-md border border-border overflow-hidden",
          "bg-muted flex items-center justify-center",
          className
        )}
        style={{ height, width }}
      >
        <div className="text-center p-4">
          <p className="text-destructive font-medium">Failed to load code editor</p>
          <p className="text-muted-foreground text-sm mt-1">
            Please refresh the page to try again
          </p>
        </div>
      </div>
    );
  }

  // Server-side or initial render - show skeleton
  if (!isMounted) {
    return (
      <div
        className={cn(
          "relative rounded-md border border-border overflow-hidden",
          className
        )}
        style={{ height, width }}
      >
        <EditorSkeleton height={height} />
      </div>
    );
  }

  return (
    <div
      className={cn(
        "relative rounded-md border border-border overflow-hidden",
        "bg-background",
        className
      )}
      style={{ height, width }}
    >
      <Editor
        height="100%"
        width="100%"
        defaultLanguage={language}
        language={language}
        value={value ?? DEFAULT_STARTER_CODE}
        theme={isDark ? "vs-code-dark" : "vs-code-light"}
        options={mergedOptions}
        onChange={onChange}
        onMount={handleMount}
        beforeMount={handleBeforeMount}
        loading={<EditorSkeleton height="100%" />}
        className="min-h-0"
      />
    </div>
  );
}


