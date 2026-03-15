"use client";

import { useState, useEffect, useCallback } from "react";

/**
 * Type guard to check if a value is a valid parsed JSON value
 */
function isValidParsedValue<T>(value: unknown): value is T {
  return value !== null && value !== undefined;
}

/**
 * Safely parse JSON with type validation
 */
function safeJsonParse<T>(json: string, defaultValue: T): T {
  try {
    const parsed: unknown = JSON.parse(json);
    return isValidParsedValue<T>(parsed) ? parsed : defaultValue;
  } catch {
    return defaultValue;
  }
}

/**
 * Type guard for Error objects
 */
function isError(value: unknown): value is Error {
  return value instanceof Error || 
    (typeof value === 'object' && 
     value !== null && 
     'message' in value && 
     typeof (value as Error).message === 'string');
}

/**
 * Get error message from unknown error value
 */
function getErrorMessage(error: unknown): string {
  if (isError(error)) {
    return error.message;
  }
  if (typeof error === 'string') {
    return error;
  }
  return 'An unknown error occurred';
}

export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void, () => void] {
  // State to store our value
  const [storedValue, setStoredValue] = useState<T>(initialValue);
  const [isInitialized, setIsInitialized] = useState<boolean>(false);

  // Initialize from localStorage on mount
  useEffect(() => {
    if (typeof window === "undefined") return;
    
    try {
      const item = window.localStorage.getItem(key);
      if (item) {
        const parsedValue = safeJsonParse<T>(item, initialValue);
        setStoredValue(parsedValue);
      }
    } catch (error: unknown) {
      console.warn(`Error reading localStorage key "${key}":`, getErrorMessage(error));
    }
    setIsInitialized(true);
  }, [key, initialValue]);

  // Return a wrapped version of useState's setter function that
  // persists the new value to localStorage.
  const setValue = useCallback(
    (value: T | ((prev: T) => T)): void => {
      try {
        // Allow value to be a function so we have same API as useState
        const valueToStore = value instanceof Function ? value(storedValue) : value;
        setStoredValue(valueToStore);
        
        if (typeof window !== "undefined") {
          window.localStorage.setItem(key, JSON.stringify(valueToStore));
          // Dispatch custom event for cross-tab synchronization
          window.dispatchEvent(new StorageEvent("storage", { key }));
        }
      } catch (error: unknown) {
        console.warn(`Error setting localStorage key "${key}":`, getErrorMessage(error));
      }
    },
    [key, storedValue]
  );

  // Remove value from localStorage
  const removeValue = useCallback((): void => {
    try {
      setStoredValue(initialValue);
      if (typeof window !== "undefined") {
        window.localStorage.removeItem(key);
        window.dispatchEvent(new StorageEvent("storage", { key }));
      }
    } catch (error: unknown) {
      console.warn(`Error removing localStorage key "${key}":`, getErrorMessage(error));
    }
  }, [key, initialValue]);

  // Listen for changes from other tabs
  useEffect(() => {
    if (typeof window === "undefined") return;

    const handleStorageChange = (event: StorageEvent): void => {
      if (event.key === key && event.newValue !== null) {
        try {
          const parsedValue = safeJsonParse<T>(event.newValue, initialValue);
          setStoredValue(parsedValue);
        } catch (error: unknown) {
          console.warn(`Error parsing localStorage change for key "${key}":`, getErrorMessage(error));
        }
      }
    };

    window.addEventListener("storage", handleStorageChange);
    return () => window.removeEventListener("storage", handleStorageChange);
  }, [key, initialValue]);

  // Return placeholder during SSR
  if (!isInitialized && typeof window === "undefined") {
    return [initialValue, setValue, removeValue];
  }

  return [storedValue, setValue, removeValue];
}
