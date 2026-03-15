"use client";

import { useCallback, useEffect, useRef } from "react";
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
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);
  const monacoRef = useRef<Monaco | null>(null);

  // Determine effective theme
  const effectiveTheme = theme === "system" ? systemTheme : theme;
  const isDark = effectiveTheme === "dark";

  // Handle editor mount
  const handleMount: OnMount = useCallback(
    (editorInstance, monacoInstance) => {
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
    },
    [onMount, onRun]
  );

  // Handle before mount
  const handleBeforeMount: BeforeMount = useCallback(
    (monaco) => {
      initializeMonaco(monaco);
      beforeMount?.(monaco);
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

  return (
    <div
      className={cn(
        "relative rounded-md border border-border overflow-hidden",
        "bg-background",
        className
      )}
    >
      <Editor
        height={height}
        width={width}
        defaultLanguage={language}
        language={language}
        value={value ?? DEFAULT_STARTER_CODE}
        theme={isDark ? "vs-code-dark" : "vs-code-light"}
        options={mergedOptions}
        onChange={onChange}
        onMount={handleMount}
        beforeMount={handleBeforeMount}
        loading={<EditorSkeleton height={height} />}
        className="[&_.monaco-editor]:outline-none"
      />
    </div>
  );
}

// Export hook to access editor instance
export function useCodeEditor() {
  return {
    getEditor: () => editorRef.current,
    getMonaco: () => monacoRef.current,
  };
}

// Keep the refs accessible
let editorRef = { current: null as editor.IStandaloneCodeEditor | null };
let monacoRef = { current: null as Monaco | null };
