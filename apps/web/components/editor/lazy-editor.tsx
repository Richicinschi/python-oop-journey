"use client";

import dynamic from "next/dynamic";
import { EditorSkeleton } from "./editor-skeleton";

// Lazy load the code editor to reduce initial bundle size
export const LazyCodeEditor = dynamic(
  () => import("./code-editor").then((mod) => ({ default: mod.CodeEditor })),
  {
    ssr: false,
    loading: ({ error, isLoading, pastDelay }) => {
      if (error) {
        return (
          <div className="p-4 text-red-500">
            Failed to load editor. Please refresh the page.
          </div>
        );
      }
      if (pastDelay || isLoading) {
        return <EditorSkeleton height="500px" />;
      }
      return null;
    },
  }
);

// Lazy load the playground component
export const LazyPlayground = dynamic(
  () => import("./playground").then((mod) => ({ default: mod.Playground })),
  {
    ssr: false,
    loading: () => (
      <div className="space-y-4">
        <div className="h-10 bg-muted rounded animate-pulse" />
        <EditorSkeleton height="500px" />
      </div>
    ),
  }
);

// Lazy load the multi-file editor
export const LazyMultiFileEditor = dynamic(
  () => import("./multi-file-editor").then((mod) => ({ default: mod.MultiFileEditor })),
  {
    ssr: false,
    loading: () => (
      <div className="h-screen flex flex-col space-y-4 p-4">
        <div className="h-12 bg-muted rounded animate-pulse" />
        <div className="flex-1 flex gap-4">
          <div className="w-64 bg-muted rounded animate-pulse" />
          <div className="flex-1 bg-muted rounded animate-pulse" />
        </div>
      </div>
    ),
  }
);

// Re-export types
export type { CodeEditorProps } from "./code-editor";
export type { PlaygroundProps, PlaygroundResult } from "./playground";
export type { MultiFileEditorProps } from "./multi-file-editor";
