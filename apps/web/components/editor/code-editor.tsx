"use client";

import React, { useCallback, useEffect, useRef, useState } from "react";
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

export const CodeEditor = React.memo(function CodeEditor({
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
  const [isLoading, setIsLoading] = useState(true);
  
  // Component refs for editor instance access
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);
  const monacoRef = useRef<Monaco | null>(null);
  const loadTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Determine effective theme
  const effectiveTheme = theme === "system" ? systemTheme : theme;
  const isDark = effectiveTheme === "dark";

  // Handle hydration - only render editor on client
  useEffect(() => {
    setIsMounted(true);
    
    // Set a timeout to detect if Monaco fails to load
    loadTimeoutRef.current = setTimeout(() => {
      if (isLoading) {
        console.warn('[CodeEditor] Monaco load timeout - falling back to textarea');
        setHasError(true);
        setIsLoading(false);
      }
    }, 10000); // 10 second timeout
    
    return () => {
      if (loadTimeoutRef.current) {
        clearTimeout(loadTimeoutRef.current);
      }
    };
  }, [isLoading]);

  // Handle editor mount
  const handleMount: OnMount = useCallback(
    (editorInstance, monacoInstance) => {
      try {
        editorRef.current = editorInstance;
        monacoRef.current = monacoInstance;
        
        // Mark loading as complete
        setIsLoading(false);
        if (loadTimeoutRef.current) {
          clearTimeout(loadTimeoutRef.current);
        }
        
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
        setIsLoading(false);
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

  // Error state - fallback to textarea
  if (hasError) {
    return (
      <div
        className={cn(
          "relative rounded-md border border-border overflow-hidden",
          "bg-background flex flex-col",
          className
        )}
        style={{ height, width }}
      >
        <div className="bg-yellow-500/10 border-b border-yellow-500/20 px-3 py-2 text-xs text-yellow-700 dark:text-yellow-400 flex items-center justify-between">
          <span>⚠️ Editor failed to load - using fallback mode</span>
          <button 
            onClick={() => window.location.reload()} 
            className="underline hover:no-underline"
          >
            Retry
          </button>
        </div>
        <textarea
          value={value ?? DEFAULT_STARTER_CODE}
          onChange={(e) => onChange?.(e.target.value)}
          readOnly={readOnly}
          className={cn(
            "flex-1 w-full p-4 font-mono text-sm resize-none focus:outline-none",
            "bg-background text-foreground",
            "border-0"
          )}
          style={{ 
            fontSize: `${fontSize}px`,
            lineHeight: '1.5',
            tabSize: 4,
          }}
          spellCheck={false}
          onKeyDown={(e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
              e.preventDefault();
              onRun?.();
            }
            // Handle Tab key for indentation
            if (e.key === 'Tab' && !e.shiftKey && !readOnly) {
              e.preventDefault();
              const target = e.target as HTMLTextAreaElement;
              const start = target.selectionStart;
              const end = target.selectionEnd;
              const newValue = value?.substring(0, start) + '    ' + value?.substring(end);
              onChange?.(newValue);
              // Set cursor position after tab
              setTimeout(() => {
                target.selectionStart = target.selectionEnd = start + 4;
              }, 0);
            }
          }}
        />
      </div>
    );
  }

  // Server-side or initial render - show skeleton
  if (!isMounted || isLoading) {
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
});

CodeEditor.displayName = 'CodeEditor';


