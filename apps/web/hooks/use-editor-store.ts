"use client";

import { useCallback, useEffect, useRef, useState } from "react";

export interface EditorState {
  /** Current code content */
  code: string;
  /** Whether there are unsaved changes */
  hasUnsavedChanges: boolean;
  /** Last saved code */
  lastSavedCode: string;
  /** Last save timestamp */
  lastSavedAt: number | null;
}

export interface UseEditorStoreOptions {
  /** Unique key for localStorage persistence */
  storageKey?: string;
  /** Initial code value */
  initialCode?: string;
  /** Debounce delay for auto-save (ms) */
  autoSaveDelay?: number;
  /** Enable auto-save to localStorage */
  enableAutoSave?: boolean;
}

export interface UseEditorStoreReturn extends EditorState {
  /** Update code content */
  setCode: (code: string) => void;
  /** Save current code */
  save: () => void;
  /** Reset to initial code */
  reset: () => void;
  /** Restore last saved code from localStorage */
  restore: () => boolean;
  /** Clear localStorage for this key */
  clear: () => void;
  /** Current font size */
  fontSize: number;
  /** Set font size */
  setFontSize: (size: number) => void;
  /** Current word wrap state */
  wordWrap: boolean;
  /** Toggle word wrap */
  setWordWrap: (enabled: boolean) => void;
  /** Minimap visibility */
  minimap: boolean;
  /** Toggle minimap */
  setMinimap: (enabled: boolean) => void;
}

const DEFAULT_OPTIONS: Required<UseEditorStoreOptions> = {
  storageKey: "editor-code",
  initialCode: "",
  autoSaveDelay: 1000,
  enableAutoSave: true,
};

// Font size storage key
const FONT_SIZE_KEY = "editor-font-size";
const WORD_WRAP_KEY = "editor-word-wrap";
const MINIMAP_KEY = "editor-minimap";

export function useEditorStore(
  options: UseEditorStoreOptions = {}
): UseEditorStoreReturn {
  const opts = { ...DEFAULT_OPTIONS, ...options };

  // Initialize state
  const [code, setCodeState] = useState<string>(opts.initialCode);
  const [lastSavedCode, setLastSavedCode] = useState<string>(opts.initialCode);
  const [lastSavedAt, setLastSavedAt] = useState<number | null>(null);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

  // Editor settings
  const [fontSize, setFontSizeState] = useState<number>(() => {
    if (typeof window === "undefined") return 14;
    const saved = localStorage.getItem(FONT_SIZE_KEY);
    return saved ? parseInt(saved, 10) : 14;
  });

  const [wordWrap, setWordWrapState] = useState<boolean>(() => {
    if (typeof window === "undefined") return true;
    const saved = localStorage.getItem(WORD_WRAP_KEY);
    return saved ? saved === "true" : true;
  });

  const [minimap, setMinimapState] = useState<boolean>(() => {
    if (typeof window === "undefined") return true;
    const saved = localStorage.getItem(MINIMAP_KEY);
    return saved ? saved === "true" : true;
  });

  // Refs for debounce
  const autoSaveTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const isInitializedRef = useRef(false);

  // Load saved code on mount
  useEffect(() => {
    if (isInitializedRef.current) return;
    isInitializedRef.current = true;

    if (typeof window === "undefined") return;

    try {
      const saved = localStorage.getItem(opts.storageKey);
      if (saved !== null) {
        setCodeState(saved);
        setLastSavedCode(saved);
        setLastSavedAt(Date.now());
      }
    } catch (error) {
      console.warn("Failed to load saved code:", error);
    }
  }, [opts.storageKey]);

  // Update code with unsaved changes tracking
  const setCode = useCallback(
    (newCode: string) => {
      setCodeState(newCode);
      setHasUnsavedChanges(newCode !== lastSavedCode);
    },
    [lastSavedCode]
  );

  // Auto-save effect
  useEffect(() => {
    if (!opts.enableAutoSave || !hasUnsavedChanges) return;

    // Clear existing timeout
    if (autoSaveTimeoutRef.current) {
      clearTimeout(autoSaveTimeoutRef.current);
    }

    // Set new timeout for auto-save
    autoSaveTimeoutRef.current = setTimeout(() => {
      if (typeof window === "undefined") return;

      try {
        localStorage.setItem(opts.storageKey, code);
        setLastSavedCode(code);
        setLastSavedAt(Date.now());
        setHasUnsavedChanges(false);
      } catch (error) {
        console.warn("Failed to auto-save code:", error);
      }
    }, opts.autoSaveDelay);

    return () => {
      if (autoSaveTimeoutRef.current) {
        clearTimeout(autoSaveTimeoutRef.current);
      }
    };
  }, [code, hasUnsavedChanges, opts.storageKey, opts.autoSaveDelay, opts.enableAutoSave]);

  // Manual save
  const save = useCallback(() => {
    if (typeof window === "undefined") return;

    try {
      localStorage.setItem(opts.storageKey, code);
      setLastSavedCode(code);
      setLastSavedAt(Date.now());
      setHasUnsavedChanges(false);

      // Clear any pending auto-save
      if (autoSaveTimeoutRef.current) {
        clearTimeout(autoSaveTimeoutRef.current);
        autoSaveTimeoutRef.current = null;
      }
    } catch (error) {
      console.warn("Failed to save code:", error);
    }
  }, [code, opts.storageKey]);

  // Reset to initial code
  const reset = useCallback(() => {
    setCodeState(opts.initialCode);
    setHasUnsavedChanges(opts.initialCode !== lastSavedCode);

    // Clear auto-save timeout
    if (autoSaveTimeoutRef.current) {
      clearTimeout(autoSaveTimeoutRef.current);
      autoSaveTimeoutRef.current = null;
    }
  }, [opts.initialCode, lastSavedCode]);

  // Restore from localStorage
  const restore = useCallback((): boolean => {
    if (typeof window === "undefined") return false;

    try {
      const saved = localStorage.getItem(opts.storageKey);
      if (saved !== null) {
        setCodeState(saved);
        setLastSavedCode(saved);
        setLastSavedAt(Date.now());
        setHasUnsavedChanges(false);
        return true;
      }
    } catch (error) {
      console.warn("Failed to restore code:", error);
    }
    return false;
  }, [opts.storageKey]);

  // Clear localStorage
  const clear = useCallback(() => {
    if (typeof window === "undefined") return;

    try {
      localStorage.removeItem(opts.storageKey);
      setLastSavedCode("");
      setLastSavedAt(null);
      setHasUnsavedChanges(code !== "");
    } catch (error) {
      console.warn("Failed to clear saved code:", error);
    }
  }, [code, opts.storageKey]);

  // Font size with persistence
  const setFontSize = useCallback((size: number) => {
    const clampedSize = Math.max(10, Math.min(32, size));
    setFontSizeState(clampedSize);
    if (typeof window !== "undefined") {
      localStorage.setItem(FONT_SIZE_KEY, String(clampedSize));
    }
  }, []);

  // Word wrap with persistence
  const setWordWrap = useCallback((enabled: boolean) => {
    setWordWrapState(enabled);
    if (typeof window !== "undefined") {
      localStorage.setItem(WORD_WRAP_KEY, String(enabled));
    }
  }, []);

  // Minimap with persistence
  const setMinimap = useCallback((enabled: boolean) => {
    setMinimapState(enabled);
    if (typeof window !== "undefined") {
      localStorage.setItem(MINIMAP_KEY, String(enabled));
    }
  }, []);

  return {
    code,
    hasUnsavedChanges,
    lastSavedCode,
    lastSavedAt,
    setCode,
    save,
    reset,
    restore,
    clear,
    fontSize,
    setFontSize,
    wordWrap,
    setWordWrap,
    minimap,
    setMinimap,
  };
}

// Hook for keyboard shortcuts
export function useEditorKeyboardShortcuts({
  onRun,
  onSave,
}: {
  onRun?: () => void;
  onSave?: () => void;
}) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ctrl+Enter to run
      if (e.ctrlKey && e.key === "Enter" && onRun) {
        e.preventDefault();
        onRun();
      }

      // Ctrl+S to save
      if (e.ctrlKey && e.key === "s" && onSave) {
        e.preventDefault();
        onSave();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [onRun, onSave]);
}
