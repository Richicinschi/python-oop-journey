"use client";

import { useCallback, useState } from "react";
import { Terminal, Loader2 } from "lucide-react";

import { cn } from "@/lib/utils";
import { CodeEditor } from "./code-editor";
import { EditorToolbar } from "./editor-toolbar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useEditorStore, useEditorKeyboardShortcuts } from "@/hooks/use-editor-store";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";

export interface PlaygroundProps {
  /** Problem ID for localStorage persistence */
  problemId: string;
  /** Initial/starter code */
  starterCode: string;
  /** Problem title */
  title?: string;
  /** Called when user wants to run code */
  onRun?: (code: string) => Promise<PlaygroundResult> | PlaygroundResult;
  /** Optional custom className */
  className?: string;
  /** Editor height (default: 500px) */
  height?: string;
  /** Whether to show output panel */
  showOutput?: boolean;
  /** Read-only mode */
  readOnly?: boolean;
}

export interface PlaygroundResult {
  /** Execution output */
  output: string;
  /** Whether execution was successful */
  success: boolean;
  /** Error message if failed */
  error?: string;
  /** Execution time in ms */
  executionTime?: number;
}

export function Playground({
  problemId,
  starterCode,
  title,
  onRun,
  className,
  height = "500px",
  showOutput = true,
  readOnly = false,
}: PlaygroundProps) {
  const [result, setResult] = useState<PlaygroundResult | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [output, setOutput] = useState<string>("");

  // Editor store with problem-specific persistence
  const editor = useEditorStore({
    storageKey: `playground-${problemId}`,
    initialCode: starterCode,
    enableAutoSave: true,
  });

  // Handle run code
  const handleRun = useCallback(async () => {
    if (!onRun) return;

    setIsRunning(true);
    setOutput("Running code...\n");
    setResult(null);

    try {
      const startTime = performance.now();
      const runResult = await Promise.resolve(onRun(editor.code));
      const executionTime = Math.round(performance.now() - startTime);

      setResult({
        ...runResult,
        executionTime,
      });
      setOutput(runResult.output);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Unknown error occurred";
      setResult({
        output: "",
        success: false,
        error: errorMessage,
      });
      setOutput(`Error: ${errorMessage}`);
    } finally {
      setIsRunning(false);
    }
  }, [onRun, editor.code]);

  // Keyboard shortcuts
  useEditorKeyboardShortcuts({
    onRun: handleRun,
    onSave: editor.save,
  });

  // Reset to starter code
  const handleReset = useCallback(() => {
    if (window.confirm("Reset to starter code? Your changes will be lost.")) {
      editor.reset();
      setOutput("");
      setResult(null);
    }
  }, [editor]);

  const outputPanel = showOutput && (
    <Card className={cn("flex flex-col", "h-[300px] lg:h-auto")}>
      <CardHeader className="py-3 flex flex-row items-center justify-between">
        <CardTitle className="text-sm flex items-center gap-2">
          <Terminal className="h-4 w-4" />
          Output
        </CardTitle>
        {result?.executionTime && (
          <span className="text-xs text-muted-foreground">
            {result.executionTime}ms
          </span>
        )}
      </CardHeader>
      <CardContent className="flex-1 overflow-auto">
        {result?.error && (
          <Alert variant="destructive" className="mb-4">
            <AlertDescription className="font-mono text-xs">
              {result.error}
            </AlertDescription>
          </Alert>
        )}
        <pre
          className={cn(
            "text-xs font-mono whitespace-pre-wrap",
            result?.success
              ? "text-green-600"
              : result?.error
              ? "text-red-600"
              : "text-muted-foreground"
          )}
        >
          {output || "Click 'Run' to execute your code..."}
        </pre>
      </CardContent>
    </Card>
  );

  return (
    <div className={cn("flex flex-col gap-4", className)}>
      {title && (
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">{title}</h3>
        </div>
      )}

      <EditorToolbar
        hasUnsavedChanges={editor.hasUnsavedChanges}
        fontSize={editor.fontSize}
        wordWrap={editor.wordWrap}
        onReset={handleReset}
        onSave={editor.save}
        onRun={onRun ? handleRun : undefined}
        onFontSizeChange={editor.setFontSize}
        onWordWrapChange={editor.setWordWrap}
      />

      <div
        className={cn(
          "grid gap-4",
          showOutput && "lg:grid-cols-[1fr,350px]"
        )}
      >
        <CodeEditor
          value={editor.code}
          onChange={editor.setCode}
          height={height}
          fontSize={editor.fontSize}
          wordWrap={editor.wordWrap ? "on" : "off"}
          minimap={editor.minimap}
          readOnly={readOnly}
          onRun={onRun ? handleRun : undefined}
        />

        {outputPanel}
      </div>

      {/* Status bar */}
      <div className="flex items-center justify-between text-xs text-muted-foreground">
        <div className="flex items-center gap-4">
          <span>{editor.code.length} chars</span>
          <span>{editor.code.split("\n").length} lines</span>
          {editor.hasUnsavedChanges && (
            <span className="text-yellow-500">• Unsaved changes</span>
          )}
        </div>
        <div className="flex items-center gap-4">
          {editor.lastSavedAt && (
            <span>
              Last saved: {new Date(editor.lastSavedAt).toLocaleTimeString()}
            </span>
          )}
          {isRunning && (
            <span className="flex items-center gap-1 text-blue-500">
              <Loader2 className="h-3 w-3 animate-spin" />
              Running...
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

// Simple output-only variant for read-only mode
export function PlaygroundOutput({
  output,
  error,
  executionTime,
  className,
}: {
  output: string;
  error?: string;
  executionTime?: number;
  className?: string;
}) {
  return (
    <Card className={cn("flex flex-col", className)}>
      <CardHeader className="py-3 flex flex-row items-center justify-between">
        <CardTitle className="text-sm flex items-center gap-2">
          <Terminal className="h-4 w-4" />
          Output
        </CardTitle>
        {executionTime && (
          <span className="text-xs text-muted-foreground">
            {executionTime}ms
          </span>
        )}
      </CardHeader>
      <CardContent className="flex-1 overflow-auto">
        {error && (
          <Alert variant="destructive" className="mb-4">
            <AlertDescription className="font-mono text-xs">{error}</AlertDescription>
          </Alert>
        )}
        <pre
          className={cn(
            "text-xs font-mono whitespace-pre-wrap",
            error ? "text-red-600" : "text-muted-foreground"
          )}
        >
          {output}
        </pre>
      </CardContent>
    </Card>
  );
}
