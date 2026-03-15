"use client";

import { useState, useEffect, useCallback } from "react";

export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void, () => void] {
  // State to store our value
  const [storedValue, setStoredValue] = useState<T>(initialValue);
  const [isInitialized, setIsInitialized] = useState(false);

  // Initialize from localStorage on mount
  useEffect(() => {
    if (typeof window === "undefined") return;
    
    try {
      const item = window.localStorage.getItem(key);
      if (item) {
        setStoredValue(JSON.parse(item));
      }
    } catch (error: unknown) {
      console.warn(`Error reading localStorage key "${key}":`, error as Error);
    }
    setIsInitialized(true);
  }, [key]);

  // Return a wrapped version of useState's setter function that
  // persists the new value to localStorage.
  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
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
        console.warn(`Error setting localStorage key "${key}":`, error as Error);
      }
    },
    [key, storedValue]
  );

  // Remove value from localStorage
  const removeValue = useCallback(() => {
    try {
      setStoredValue(initialValue);
      if (typeof window !== "undefined") {
        window.localStorage.removeItem(key);
        window.dispatchEvent(new StorageEvent("storage", { key }));
      }
    } catch (error: unknown) {
      console.warn(`Error removing localStorage key "${key}":`, error as Error);
    }
  }, [key, initialValue]);

  // Listen for changes from other tabs
  useEffect(() => {
    if (typeof window === "undefined") return;

    const handleStorageChange = (event: StorageEvent) => {
      if (event.key === key && event.newValue !== null) {
        try {
          setStoredValue(JSON.parse(event.newValue));
        } catch (error: unknown) {
          console.warn(`Error parsing localStorage change for key "${key}":`, error as Error);
        }
      }
    };

    window.addEventListener("storage", handleStorageChange);
    return () => window.removeEventListener("storage", handleStorageChange);
  }, [key]);

  // Return placeholder during SSR
  if (!isInitialized && typeof window === "undefined") {
    return [initialValue, setValue, removeValue];
  }

  return [storedValue, setValue, removeValue];
}
